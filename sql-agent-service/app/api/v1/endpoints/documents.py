import asyncio
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.core.security import get_current_user_async
from app.core.database import ChatUser
from app.services.document_service import DocumentService
from app.models.document_models import (
    DocumentResponse, DocumentListResponse, DocumentUpdateRequest, 
    DocumentProcessingStatus, DocumentStatus
)

router = APIRouter()
document_service = DocumentService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),  # Comma-separated tags
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Upload a document for processing"""
    
    # Validate file type
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.txt', '.md', '.csv']
    file_extension = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
    
    if f'.{file_extension}' not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Parse tags
    tag_list = None
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    try:
        # Save uploaded file
        document = await document_service.save_uploaded_file(file, current_user.user_id)
        
        # Add description and tags if provided
        if description:
            document.description = description
        if tag_list:
            import json
            document.tags = json.dumps(tag_list)
        
        # Save to database
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        # Start background processing
        asyncio.create_task(
            document_service.process_document_async(document, db)
        )
        
        return DocumentResponse(
            id=document.id,
            filename=document.filename,
            original_filename=document.original_filename,
            file_path=document.file_path,
            file_size=document.file_size,
            document_type=document.document_type,
            status=document.status,
            description=document.description,
            tags=tag_list,
            user_id=document.user_id,
            uploaded_at=document.uploaded_at,
            processed_at=document.processed_at,
            text_content=document.text_content,
            vector_id=document.vector_id,
            error_message=document.error_message
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """List user's documents with pagination"""
    
    skip = (page - 1) * page_size
    
    try:
        documents = await document_service.get_user_documents(
            current_user.user_id, db, skip, page_size
        )
        
        # Convert to response models
        document_responses = []
        for doc in documents:
            tag_list = None
            if doc.tags:
                import json
                tag_list = json.loads(doc.tags)
            
            document_responses.append(DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                original_filename=doc.original_filename,
                file_path=doc.file_path,
                file_size=doc.file_size,
                document_type=doc.document_type,
                status=doc.status,
                description=doc.description,
                tags=tag_list,
                user_id=doc.user_id,
                uploaded_at=doc.uploaded_at,
                processed_at=doc.processed_at,
                text_content=doc.text_content,
                vector_id=doc.vector_id,
                error_message=doc.error_message
            ))
        
        # Get total count
        from sqlalchemy import select, func
        from app.core.database import Document
        
        result = await db.execute(
            select(func.count(Document.id)).where(Document.user_id == current_user.user_id)
        )
        total_count = result.scalar() or 0
        
        return DocumentListResponse(
            documents=document_responses,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}"
        )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Get a specific document"""
    
    document = await document_service.get_document(document_id, current_user.user_id, db)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    tag_list = None
    if document.tags:
        import json
        tag_list = json.loads(document.tags)
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_path=document.file_path,
        file_size=document.file_size,
        document_type=document.document_type,
        status=document.status,
        description=document.description,
        tags=tag_list,
        user_id=document.user_id,
        uploaded_at=document.uploaded_at,
        processed_at=document.processed_at,
        text_content=document.text_content,
        vector_id=document.vector_id,
        error_message=document.error_message
    )

@router.get("/{document_id}/status", response_model=DocumentProcessingStatus)
async def get_document_status(
    document_id: str,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Get document processing status"""
    
    document = await document_service.get_document(document_id, current_user.user_id, db)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentProcessingStatus(
        document_id=document.id,
        status=document.status,
        message=f"Document is {document.status}",
        error_message=document.error_message
    )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    update_request: DocumentUpdateRequest,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Update document metadata"""
    
    document = await document_service.update_document(
        document_id, 
        current_user.user_id, 
        update_request.description,
        update_request.tags,
        db
    )
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    tag_list = None
    if document.tags:
        import json
        tag_list = json.loads(document.tags)
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_path=document.file_path,
        file_size=document.file_size,
        document_type=document.document_type,
        status=document.status,
        description=document.description,
        tags=tag_list,
        user_id=document.user_id,
        uploaded_at=document.uploaded_at,
        processed_at=document.processed_at,
        text_content=document.text_content,
        vector_id=document.vector_id,
        error_message=document.error_message
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Delete a document"""
    
    success = await document_service.delete_document(document_id, current_user.user_id, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document deleted successfully"}
