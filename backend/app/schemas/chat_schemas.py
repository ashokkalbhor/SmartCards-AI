from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

class ConversationCreate(BaseModel):
    title: str
    conversation_type: Optional[str] = "card_recommendation"

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    conversation_type: str
    status: str
    user_preferences: Optional[Dict[str, Any]] = None
    conversation_context: Optional[Dict[str, Any]] = None
    message_count: int
    total_tokens_used: int
    ai_response_time_avg: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConversationMessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    message_type: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    response_time: Optional[float] = None
    message_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]
    total_count: int

class ChatHistoryResponse(BaseModel):
    messages: List[ConversationMessageResponse]
    conversation: ConversationResponse

class ChatAccessRequestCreate(BaseModel):
    pass  # No additional fields needed for now

class ChatAccessRequestResponse(BaseModel):
    id: int
    user_id: int
    status: str
    requested_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None

    class Config:
        from_attributes = True

class ChatAccessRequestListResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    status: str
    requested_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    review_notes: Optional[str] = None

    class Config:
        from_attributes = True
