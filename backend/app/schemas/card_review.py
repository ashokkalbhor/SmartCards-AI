from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CardReviewBase(BaseModel):
    overall_rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    review_title: Optional[str] = Field(None, max_length=200)
    review_content: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    experience: Optional[str] = None

class CardReviewCreate(CardReviewBase):
    card_master_id: int

class CardReviewUpdate(CardReviewBase):
    pass

class CardReviewResponse(CardReviewBase):
    id: int
    user_id: int
    card_master_id: int
    user_name: str
    is_verified_cardholder: bool
    helpful_votes: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CardReviewList(BaseModel):
    reviews: List[CardReviewResponse]
    total_count: int
    average_rating: float

class ReviewVoteCreate(BaseModel):
    vote_type: str = Field(..., pattern="^(helpful|not_helpful)$")

class ReviewVoteResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    vote_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True 