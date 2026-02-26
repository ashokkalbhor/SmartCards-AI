import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
import logging

from ..core.database import ChatMessage, Conversation, UserSession
from ..models.chat_models import ChatRequest, ChatResponse, ConversationListResponse, ChatHistoryResponse
from ..core.config import settings

logger = logging.getLogger(__name__)

class ChatService:
    """Service for managing chat history and conversations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_conversation(self, db: Session, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    async def create_conversation_async(self, db: AsyncSession, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation (async)"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation
    
    def save_message(self, db: Session, user_id: str, conversation_id: str, message: str, 
                    response: str, confidence: Optional[float] = None, 
                    sql_query: Optional[str] = None, execution_time: Optional[float] = None,
                    error_message: Optional[str] = None) -> ChatMessage:
        """Save a chat message"""
        chat_message = ChatMessage(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            response=response,
            confidence=confidence,
            sql_query=sql_query,
            execution_time=execution_time,
            error_message=error_message
        )
        db.add(chat_message)
        
        # Update conversation message count and timestamp
        conversation = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        if conversation:
            conversation.message_count += 1
            conversation.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(chat_message)
        return chat_message
    
    async def save_message_async(self, db: AsyncSession, user_id: str, conversation_id: str, message: str, 
                               response: str, confidence: Optional[float] = None, 
                               sql_query: Optional[str] = None, execution_time: Optional[float] = None,
                               error_message: Optional[str] = None) -> ChatMessage:
        """Save a chat message (async)"""
        chat_message = ChatMessage(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            response=response,
            confidence=confidence,
            sql_query=sql_query,
            execution_time=execution_time,
            error_message=error_message
        )
        db.add(chat_message)
        
        # Update conversation message count and timestamp
        result = await db.execute(select(Conversation).where(Conversation.conversation_id == conversation_id))
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.message_count += 1
            conversation.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(chat_message)
        return chat_message
    
    def get_conversations(self, db: Session, user_id: str, limit: int = 50, offset: int = 0) -> ConversationListResponse:
        """Get user's conversations"""
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(desc(Conversation.updated_at)).offset(offset).limit(limit).all()
        
        total_count = db.query(Conversation).filter(Conversation.user_id == user_id).count()
        
        return ConversationListResponse(
            conversations=conversations,
            total_count=total_count
        )
    
    async def get_conversations_async(self, db: AsyncSession, user_id: str, limit: int = 50, offset: int = 0) -> ConversationListResponse:
        """Get user's conversations (async)"""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
        )
        conversations = result.scalars().all()
        
        result = await db.execute(
            select(Conversation).where(Conversation.user_id == user_id)
        )
        total_count = len(result.scalars().all())
        
        return ConversationListResponse(
            conversations=conversations,
            total_count=total_count
        )
    
    def get_chat_history(self, db: Session, user_id: str, conversation_id: str, 
                        limit: int = 100, offset: int = 0) -> ChatHistoryResponse:
        """Get chat history for a conversation"""
        # Get conversation
        conversation = db.query(Conversation).filter(
            and_(Conversation.conversation_id == conversation_id, 
                 Conversation.user_id == user_id)
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Get messages
        messages = db.query(ChatMessage).filter(
            ChatMessage.conversation_id == conversation_id
        ).order_by(ChatMessage.timestamp).offset(offset).limit(limit).all()
        
        return ChatHistoryResponse(
            messages=messages,
            conversation=conversation
        )
    
    async def get_chat_history_async(self, db: AsyncSession, user_id: str, conversation_id: str, 
                                   limit: int = 100, offset: int = 0) -> ChatHistoryResponse:
        """Get chat history for a conversation (async)"""
        # Get conversation
        result = await db.execute(
            select(Conversation).where(
                and_(Conversation.conversation_id == conversation_id, 
                     Conversation.user_id == user_id)
            )
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Get messages
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.timestamp)
            .offset(offset)
            .limit(limit)
        )
        messages = result.scalars().all()
        
        return ChatHistoryResponse(
            messages=messages,
            conversation=conversation
        )
    
    def delete_conversation(self, db: Session, user_id: str, conversation_id: str) -> bool:
        """Delete a conversation and all its messages"""
        # Delete messages first
        db.query(ChatMessage).filter(
            and_(ChatMessage.conversation_id == conversation_id,
                 ChatMessage.user_id == user_id)
        ).delete()
        
        # Delete conversation
        result = db.query(Conversation).filter(
            and_(Conversation.conversation_id == conversation_id,
                 Conversation.user_id == user_id)
        ).delete()
        
        db.commit()
        return result > 0
    
    async def delete_conversation_async(self, db: AsyncSession, user_id: str, conversation_id: str) -> bool:
        """Delete a conversation and all its messages (async)"""
        # Delete messages first
        await db.execute(
            select(ChatMessage).where(
                and_(ChatMessage.conversation_id == conversation_id,
                     ChatMessage.user_id == user_id)
            )
        )
        
        # Delete conversation
        result = await db.execute(
            select(Conversation).where(
                and_(Conversation.conversation_id == conversation_id,
                     Conversation.user_id == user_id)
            )
        )
        
        await db.commit()
        return result.rowcount > 0
    
    def create_user_session(self, db: Session, user_id: str) -> UserSession:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        user_session = UserSession(
            user_id=user_id,
            session_id=session_id
        )
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        return user_session
    
    async def create_user_session_async(self, db: AsyncSession, user_id: str) -> UserSession:
        """Create a new user session (async)"""
        session_id = str(uuid.uuid4())
        user_session = UserSession(
            user_id=user_id,
            session_id=session_id
        )
        db.add(user_session)
        await db.commit()
        await db.refresh(user_session)
        return user_session
    
    def update_session_activity(self, db: Session, session_id: str) -> bool:
        """Update session last activity"""
        session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
        if session:
            session.last_activity = datetime.utcnow()
            db.commit()
            return True
        return False
    
    async def update_session_activity_async(self, db: AsyncSession, session_id: str) -> bool:
        """Update session last activity (async)"""
        result = await db.execute(select(UserSession).where(UserSession.session_id == session_id))
        session = result.scalar_one_or_none()
        if session:
            session.last_activity = datetime.utcnow()
            await db.commit()
            return True
        return False
    
    def cleanup_old_sessions(self, db: Session, days: int = 7) -> int:
        """Clean up old inactive sessions"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = db.query(UserSession).filter(
            and_(UserSession.last_activity < cutoff_date,
                 UserSession.is_active == True)
        ).update({"is_active": False})
        db.commit()
        return result
    
    async def cleanup_old_sessions_async(self, db: AsyncSession, days: int = 7) -> int:
        """Clean up old inactive sessions (async)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await db.execute(
            select(UserSession).where(
                and_(UserSession.last_activity < cutoff_date,
                     UserSession.is_active == True)
            )
        )
        # Update sessions to inactive
        sessions = result.scalars().all()
        for session in sessions:
            session.is_active = False
        await db.commit()
        return len(sessions)
    
    def cleanup_old_chat_history(self, db: Session, days: int = None) -> int:
        """Clean up old chat history"""
        if days is None:
            days = settings.CHAT_HISTORY_RETENTION_DAYS
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete old messages
        deleted_messages = db.query(ChatMessage).filter(
            ChatMessage.timestamp < cutoff_date
        ).delete()
        
        # Delete conversations with no messages
        db.commit()
        return deleted_messages
    
    async def cleanup_old_chat_history_async(self, db: AsyncSession, days: int = None) -> int:
        """Clean up old chat history (async)"""
        if days is None:
            days = settings.CHAT_HISTORY_RETENTION_DAYS
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete old messages
        result = await db.execute(
            select(ChatMessage).where(ChatMessage.timestamp < cutoff_date)
        )
        old_messages = result.scalars().all()
        
        for message in old_messages:
            await db.delete(message)
        
        await db.commit()
        return len(old_messages)
