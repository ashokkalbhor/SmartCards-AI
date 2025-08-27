from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# JWT Authentication Models
class TokenData(BaseModel):
    user_id: Optional[str] = None
    client_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

# Chat History Models
class ChatMessage(BaseModel):
    id: Optional[int] = None
    user_id: str
    conversation_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence: Optional[float] = None
    sql_query: Optional[str] = None
    execution_time: Optional[float] = None
    error_message: Optional[str] = None

class Conversation(BaseModel):
    id: Optional[int] = None
    user_id: str
    conversation_id: str
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message_count: int = 0

class UserSession(BaseModel):
    id: Optional[int] = None
    user_id: str
    session_id: str
    session_start: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

# Chat API Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    confidence: Optional[float] = None
    sql_query: Optional[str] = None
    execution_time: Optional[float] = None

class ConversationListResponse(BaseModel):
    conversations: List[Conversation]
    total_count: int

class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage]
    conversation: Conversation
