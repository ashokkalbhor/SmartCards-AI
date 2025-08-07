from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class CardDocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    document_type: str  # link, file, policy_update, terms_change
    content: str  # URL for links, file path for uploads, or text content
    submission_reason: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class CardDocumentCreate(CardDocumentBase):
    user_id: int
    card_master_id: int
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None


class CardDocumentUpdate(BaseModel):
    status: str  # pending, approved, rejected
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None


class CardDocumentResponse(CardDocumentBase):
    id: int
    user_id: int
    card_master_id: int
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    status: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Additional fields for display
    user_name: Optional[str] = None
    card_name: Optional[str] = None
    bank_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class CardDocumentSummary(BaseModel):
    id: int
    title: str
    document_type: str
    status: str
    created_at: datetime
    user_name: str
    card_name: str
    
    class Config:
        from_attributes = True


class CardDocumentStats(BaseModel):
    total_pending: int
    total_approved: int
    total_rejected: int
    pending_by_type: Dict[str, int]  # link: 5, file: 3, policy_update: 2


class CardDocumentSubmissionRequest(BaseModel):
    title: str
    description: Optional[str] = None
    document_type: str  # link, file, policy_update, terms_change
    content: str  # URL for links, file path for uploads, or text content
    submission_reason: Optional[str] = None 