from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.core.database import get_db, get_async_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, ConversationMessage
from app.models.chat_access_request import ChatAccessRequest
from app.schemas.chat_schemas import (
    ConversationCreate, ConversationResponse, 
    ChatHistoryResponse, ConversationListResponse,
    ChatAccessRequestResponse, ChatAccessRequestCreate
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new conversation"""
    try:
        conversation = Conversation(
            user_id=current_user.id,
            title=conversation_data.title,
            conversation_type=conversation_data.conversation_type or "card_recommendation"
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return ConversationResponse.from_orm(conversation)
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to create conversation")

@router.get("/conversations", response_model=ConversationListResponse)
async def get_conversations(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's conversations"""
    try:
        # Verify user can access their own conversations
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        from sqlalchemy import select, desc
        
        # Get conversations
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
        )
        conversations = result.scalars().all()
        
        # Get total count
        count_result = await db.execute(
            select(Conversation).where(Conversation.user_id == user_id)
        )
        total_count = len(count_result.scalars().all())
        
        return ConversationListResponse(
            conversations=conversations,
            total_count=total_count
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversations")

@router.get("/conversations/{conversation_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    conversation_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get chat history for a conversation"""
    try:
        from sqlalchemy import select, and_
        
        # Verify conversation belongs to user
        conversation_result = await db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == conversation_id,
                    Conversation.user_id == current_user.id
                )
            )
        )
        conversation = conversation_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages
        messages_result = await db.execute(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == conversation_id)
            .order_by(ConversationMessage.created_at)
            .offset(offset)
            .limit(limit)
        )
        messages = messages_result.scalars().all()
        
        return ChatHistoryResponse(
            messages=messages,
            conversation=conversation
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get chat history")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a conversation"""
    try:
        from sqlalchemy import select, and_
        
        # Verify conversation belongs to user
        conversation_result = await db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == conversation_id,
                    Conversation.user_id == current_user.id
                )
            )
        )
        conversation = conversation_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        await db.delete(conversation)
        await db.commit()
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete conversation")

@router.post("/conversations/{conversation_id}/messages")
async def save_message(
    conversation_id: int,
    message_data: dict,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Save a message to a conversation"""
    try:
        from sqlalchemy import select, and_
        from datetime import datetime
        
        # Verify conversation belongs to user
        conversation_result = await db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == conversation_id,
                    Conversation.user_id == current_user.id
                )
            )
        )
        conversation = conversation_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Create message
        message = ConversationMessage(
            conversation_id=conversation_id,
            role=message_data.get("role", "user"),
            content=message_data.get("content", ""),
            message_type=message_data.get("message_type", "text"),
            tokens_used=message_data.get("tokens_used"),
            model_used=message_data.get("model_used"),
            response_time=message_data.get("response_time"),
            message_metadata=message_data.get("message_metadata")
        )
        
        db.add(message)
        
        # Update conversation
        conversation.message_count += 1
        conversation.updated_at = datetime.utcnow()
        conversation.last_message_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(message)
        
        return {"message": "Message saved successfully", "message_id": message.id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise HTTPException(status_code=500, detail="Failed to save message")


@router.post("/request-access", response_model=ChatAccessRequestResponse)
async def request_chat_access(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Request chat access"""
    try:
        # Check if user already has access
        if current_user.chat_access_granted:
            raise HTTPException(status_code=400, detail="User already has chat access")
        
        # Check if user already has a pending request
        from sqlalchemy import select
        existing_request = await db.execute(
            select(ChatAccessRequest).where(
                ChatAccessRequest.user_id == current_user.id,
                ChatAccessRequest.status == "pending"
            )
        )
        if existing_request.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User already has a pending request")
        
        # Create new request
        request = ChatAccessRequest(
            user_id=current_user.id,
            status="pending"
        )
        db.add(request)
        await db.commit()
        await db.refresh(request)
        
        return ChatAccessRequestResponse(
            id=request.id,
            user_id=request.user_id,
            status=request.status,
            requested_at=request.requested_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error requesting chat access: {e}")
        raise HTTPException(status_code=500, detail="Failed to request chat access")


@router.get("/access-status")
async def get_chat_access_status(
    current_user: User = Depends(get_current_user)
):
    """Get user's chat access status"""
    return {
        "has_access": current_user.chat_access_granted,
        "user_id": current_user.id
    }
