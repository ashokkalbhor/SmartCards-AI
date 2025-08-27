from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentType(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    TEXT = "text"
    UNKNOWN = "unknown"

class DocumentUploadRequest(BaseModel):
    filename: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    user_id: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    document_type: DocumentType
    status: DocumentStatus
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    user_id: str
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    text_content: Optional[str] = None
    vector_id: Optional[str] = None
    error_message: Optional[str] = None

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total_count: int
    page: int
    page_size: int

class DocumentUpdateRequest(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class DocumentProcessingStatus(BaseModel):
    document_id: str
    status: DocumentStatus
    progress: Optional[float] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
