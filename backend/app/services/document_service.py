import os
import uuid
import json
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from pathlib import Path

import PyPDF2
from PIL import Image
import pytesseract
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import Document
from ..models.document_models import DocumentStatus, DocumentType, DocumentResponse
from ..services.vector_service import VectorService
from ..core.config import settings

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for handling document uploads, processing, and storage"""
    
    def __init__(self):
        self.upload_dir = Path("uploads/documents")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.vector_service = VectorService()
        
    def _get_document_type(self, filename: str) -> DocumentType:
        """Determine document type from filename"""
        ext = Path(filename).suffix.lower()
        if ext == '.pdf':
            return DocumentType.PDF
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            return DocumentType.IMAGE
        elif ext in ['.txt', '.md', '.csv']:
            return DocumentType.TEXT
        else:
            return DocumentType.UNKNOWN
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_text_from_image(self, file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image {file_path}: {e}")
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    def _extract_text_from_text_file(self, file_path: str) -> str:
        """Extract text from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise Exception(f"Failed to read text file: {str(e)}")
    
    def _extract_text(self, file_path: str, document_type: DocumentType) -> str:
        """Extract text from document based on type"""
        if document_type == DocumentType.PDF:
            return self._extract_text_from_pdf(file_path)
        elif document_type == DocumentType.IMAGE:
            return self._extract_text_from_image(file_path)
        elif document_type == DocumentType.TEXT:
            return self._extract_text_from_text_file(file_path)
        else:
            raise Exception(f"Unsupported document type: {document_type}")
    
    async def save_uploaded_file(self, file: UploadFile, user_id: str) -> Document:
        """Save uploaded file and create document record"""
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        filename = f"{file_id}{file_extension}"
        file_path = self.upload_dir / filename
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                file_size = len(content)
        except Exception as e:
            logger.error(f"Error saving file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Create document record
        document = Document(
            id=file_id,
            filename=filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            document_type=self._get_document_type(file.filename).value,
            status=DocumentStatus.PENDING.value,
            user_id=user_id
        )
        
        return document
    
    async def process_document_async(self, document: Document, db: AsyncSession) -> None:
        """Process document asynchronously (extract text and store in vector DB)"""
        try:
            # Update status to processing
            document.status = DocumentStatus.PROCESSING.value
            await db.commit()
            
            # Extract text
            text_content = self._extract_text(document.file_path, DocumentType(document.document_type))
            
            # Store in vector database
            vector_id = await self.vector_service.add_document(
                document_id=document.id,
                content=text_content,
                metadata={
                    "filename": document.original_filename,
                    "document_type": document.document_type,
                    "user_id": document.user_id,
                    "uploaded_at": document.uploaded_at.isoformat()
                }
            )
            
            # Update document record
            document.text_content = text_content
            document.vector_id = vector_id
            document.status = DocumentStatus.COMPLETED.value
            document.processed_at = datetime.utcnow()
            
            await db.commit()
            logger.info(f"Document {document.id} processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing document {document.id}: {e}")
            document.status = DocumentStatus.FAILED.value
            document.error_message = str(e)
            await db.commit()
    
    async def get_document(self, document_id: str, user_id: str, db: AsyncSession) -> Optional[Document]:
        """Get document by ID for specific user"""
        result = await db.execute(
            select(Document).where(
                Document.id == document_id,
                Document.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_documents(
        self, 
        user_id: str, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Document]:
        """Get documents for a user with pagination"""
        result = await db.execute(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.uploaded_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def delete_document(self, document_id: str, user_id: str, db: AsyncSession) -> bool:
        """Delete document and its file"""
        document = await self.get_document(document_id, user_id, db)
        if not document:
            return False
        
        try:
            # Delete file
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
            
            # Remove from vector database
            if document.vector_id:
                await self.vector_service.delete_document(document.vector_id)
            
            # Delete database record
            await db.delete(document)
            await db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False
    
    async def update_document(
        self, 
        document_id: str, 
        user_id: str, 
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        db: AsyncSession = None
    ) -> Optional[Document]:
        """Update document metadata"""
        document = await self.get_document(document_id, user_id, db)
        if not document:
            return None
        
        if description is not None:
            document.description = description
        if tags is not None:
            document.tags = json.dumps(tags)
        
        await db.commit()
        return document
