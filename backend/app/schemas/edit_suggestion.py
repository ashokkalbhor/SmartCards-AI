from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class EditSuggestionBase(BaseModel):
    field_type: str  # spending_category, merchant_reward
    field_name: str  # category name or merchant name
    old_value: Optional[str] = None
    new_value: str
    suggestion_reason: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class EditSuggestionCreate(EditSuggestionBase):
    user_id: int
    card_master_id: int


class EditSuggestionUpdate(BaseModel):
    status: str  # pending, approved, rejected
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None


class EditSuggestionResponse(EditSuggestionBase):
    id: int
    user_id: int
    moderator_id: Optional[int] = None
    card_master_id: int
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


class EditSuggestionSummary(BaseModel):
    id: int
    field_type: str
    field_name: str
    old_value: Optional[str] = None
    new_value: str
    status: str
    created_at: datetime
    user_name: str
    card_name: str
    
    class Config:
        from_attributes = True


class EditSuggestionStats(BaseModel):
    total_pending: int
    total_approved: int
    total_rejected: int
    pending_by_type: Dict[str, int]  # spending_category: 5, merchant_reward: 3


class CardEditSuggestionRequest(BaseModel):
    field_type: str
    field_name: str
    old_value: Optional[str] = None
    new_value: str
    suggestion_reason: Optional[str] = None 