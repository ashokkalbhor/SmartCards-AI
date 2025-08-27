from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, get_async_db
from app.core.security import get_current_user_async
from app.core.database import ChatUser
from app.services.chat_service import ChatService
from app.models.chat_models import (
    ChatRequest, ChatResponse, ConversationListResponse, 
    ChatHistoryResponse, Conversation
)
from app.core.sql_agent import SQLAgentService

router = APIRouter()
chat_service = ChatService()

@router.post("/conversations", response_model=Conversation)
async def create_conversation(
    title: Optional[str] = None,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Create a new conversation"""
    conversation = await chat_service.create_conversation_async(
        db, current_user.user_id, title
    )
    return conversation

@router.get("/conversations", response_model=ConversationListResponse)
async def get_conversations(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Get user's conversations"""
    return await chat_service.get_conversations_async(
        db, current_user.user_id, limit, offset
    )

@router.get("/conversations/{conversation_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    conversation_id: str,
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Get chat history for a conversation"""
    try:
        return await chat_service.get_chat_history_async(
            db, current_user.user_id, conversation_id, limit, offset
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Delete a conversation and all its messages"""
    success = await chat_service.delete_conversation_async(
        db, current_user.user_id, conversation_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return {"message": "Conversation deleted successfully"}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Chat with the SQL agent"""
    # Get or create conversation
    conversation_id = request.conversation_id
    if not conversation_id:
        # Create new conversation
        conversation = await chat_service.create_conversation_async(
            db, current_user.user_id
        )
        conversation_id = conversation.conversation_id
    
    # Process the query with SQL agent
    try:
        # Initialize SQL agent service
        sql_agent = SQLAgentService()
        
        # Prepare user context
        user_context = {
            "user_id": current_user.user_id,
            "client_id": current_user.client_id,
            "conversation_id": conversation_id
        }
        
        if request.context:
            user_context.update(request.context)
        
        # Process query
        start_time = time.time()
        result = await sql_agent.process_query(
            query=request.message,
            user_context=user_context
        )
        execution_time = time.time() - start_time
        
        # Save the message and response
        await chat_service.save_message_async(
            db=db,
            user_id=current_user.user_id,
            conversation_id=conversation_id,
            message=request.message,
            response=result["response"],
            confidence=result.get("confidence"),
            sql_query=result.get("sql_query"),
            execution_time=execution_time,
            error_message=result.get("error")
        )
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            confidence=result.get("confidence"),
            sql_query=result.get("sql_query"),
            execution_time=execution_time
        )
        
    except Exception as e:
        # Save error message
        await chat_service.save_message_async(
            db=db,
            user_id=current_user.user_id,
            conversation_id=conversation_id,
            message=request.message,
            response=f"Sorry, I encountered an error: {str(e)}",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/stats")
async def get_chat_stats(
    current_user: ChatUser = Depends(get_current_user_async),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Get chat statistics for the user"""
    # Get conversation count
    conversations = await chat_service.get_conversations_async(
        db, current_user.user_id, limit=1000, offset=0
    )
    
    # Get total message count
    from sqlalchemy import select, func
    from ...core.database import ChatMessage
    
    result = await db.execute(
        select(func.count(ChatMessage.id)).where(ChatMessage.user_id == current_user.user_id)
    )
    total_messages = result.scalar() or 0
    
    # Get recent activity
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    result = await db.execute(
        select(func.count(ChatMessage.id)).where(
            and_(ChatMessage.user_id == current_user.user_id,
                 ChatMessage.timestamp >= week_ago)
        )
    )
    messages_this_week = result.scalar() or 0
    
    return {
        "total_conversations": conversations.total_count,
        "total_messages": total_messages,
        "messages_this_week": messages_this_week,
        "user_id": current_user.user_id,
        "username": current_user.username
    }

# Import time and and_ for the chat endpoint
import time
from sqlalchemy import and_
