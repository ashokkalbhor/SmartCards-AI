from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.core.ai_service import ai_service
from app.core.vector_db import vector_db_service
from app.models.user import User
from app.models.conversation import Conversation, ConversationMessage
from app.models.credit_card import CreditCard

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic models for request/response
class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    conversation_id: Optional[int] = None
    include_card_context: bool = Field(default=True, description="Include user's credit cards in context")
    max_history: int = Field(default=5, description="Maximum conversation history to include")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI assistant's response")
    conversation_id: int = Field(..., description="Conversation ID")
    message_id: int = Field(..., description="Response message ID")
    source: str = Field(..., description="Response source: vector_db, llm, or hybrid")
    confidence: float = Field(..., description="Confidence score (0-1)")
    metadata: Optional[Dict[str, Any]] = None
    related_cards: Optional[List[Dict]] = None
    suggested_actions: Optional[List[str]] = None


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    last_message_at: Optional[datetime]
    message_count: int
    status: str


class ConversationHistoryResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[ChatMessage]


class VectorSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    collection: Optional[str] = Field(None, description="Specific collection to search")
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(default=5, ge=1, le=20)


class VectorSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_results: int
    query: str
    collection_searched: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Chat with the AI assistant about credit cards
    """
    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(
            request.conversation_id, current_user.id, db
        )
        
        # Save user message
        user_message = ConversationMessage(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            message_type="text"
        )
        db.add(user_message)
        await db.commit()
        await db.refresh(user_message)
        
        # Process the query with AI service
        ai_response = await ai_service.process_user_query(
            user_id=current_user.id,
            query=request.message,
            conversation_id=conversation.id,
            db=db
        )
        
        # Save assistant message
        assistant_message = ConversationMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response["response"],
            message_type="text",
            model_used="gpt-4-turbo-preview",
            response_time=0.5,  # TODO: Track actual response time
            message_metadata={
                "source": ai_response["source"],
                "confidence": ai_response["confidence"],
                "user_cards_used": ai_response.get("user_cards_used", False)
            }
        )
        db.add(assistant_message)
        
        # Update conversation
        conversation.message_count += 2
        conversation.last_message_at = datetime.now()
        
        # Generate title if this is the first exchange
        if conversation.message_count == 2 and not conversation.title:
            conversation.title = generate_conversation_title(request.message)
        
        await db.commit()
        await db.refresh(assistant_message)
        
        # Extract related cards and suggestions
        related_cards = None
        if ai_response.get("user_cards_used"):
            related_cards = await get_user_cards_summary(current_user.id, db)
        
        suggested_actions = generate_suggested_actions(request.message, ai_response)
        
        return ChatResponse(
            response=ai_response["response"],
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            source=ai_response["source"],
            confidence=ai_response["confidence"],
            metadata=ai_response.get("metadata", {}),
            related_cards=related_cards,
            suggested_actions=suggested_actions
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing chat request"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_user_conversations(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user's conversation history
    """
    try:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == current_user.id)
            .order_by(Conversation.last_message_at.desc())
            .limit(limit)
            .offset(offset)
        )
        conversations = result.scalars().all()
        
        return [
            ConversationResponse(
                id=conv.id,
                title=conv.title or "New Conversation",
                created_at=conv.created_at,
                last_message_at=conv.last_message_at,
                message_count=conv.message_count,
                status=conv.status
            )
            for conv in conversations
        ]
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversations"
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get detailed conversation history
    """
    try:
        # Get conversation
        conversation_result = await db.execute(
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        conversation = conversation_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        messages_result = await db.execute(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == conversation_id)
            .order_by(ConversationMessage.created_at)
        )
        messages = messages_result.scalars().all()
        
        return ConversationHistoryResponse(
            conversation=ConversationResponse(
                id=conversation.id,
                title=conversation.title or "New Conversation",
                created_at=conversation.created_at,
                last_message_at=conversation.last_message_at,
                message_count=conversation.message_count,
                status=conversation.status
            ),
            messages=[
                ChatMessage(
                    role=msg.role,
                    content=msg.content,
                    timestamp=msg.created_at,
                    metadata=msg.message_metadata
                )
                for msg in messages
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation history"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Delete a conversation
    """
    try:
        # Get conversation
        conversation_result = await db.execute(
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        conversation = conversation_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete conversation (messages will be deleted via cascade)
        await db.delete(conversation)
        await db.commit()
        
        return {"message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting conversation"
        )


@router.post("/search", response_model=VectorSearchResponse)
async def search_knowledge_base(
    request: VectorSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search the credit card knowledge base directly
    """
    try:
        if request.collection:
            # Search specific collection
            results = await vector_db_service.search_specific_collection(
                collection_name=request.collection,
                query=request.query,
                filters=request.filters,
                n_results=request.limit
            )
            collection_searched = request.collection
        else:
            # Search all collections
            all_results = await vector_db_service.search_all_collections(
                query=request.query,
                filters=request.filters,
                n_results=request.limit
            )
            
            # Combine and sort results
            results = []
            for collection, collection_results in all_results.items():
                results.extend(collection_results)
            
            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)
            results = results[:request.limit]
            collection_searched = None
        
        return VectorSearchResponse(
            results=results,
            total_results=len(results),
            query=request.query,
            collection_searched=collection_searched
        )
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error searching knowledge base"
        )


@router.get("/health")
async def chatbot_health_check():
    """
    Check chatbot system health
    """
    try:
        # Check vector database
        db_info = vector_db_service.get_database_info()
        
        # Check AI service
        ai_status = "healthy"
        try:
            await ai_service._search_vector_db("test query")
        except Exception as e:
            ai_status = f"error: {str(e)}"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "vector_database": {
                    "status": db_info["status"],
                    "total_documents": db_info["total_documents"],
                    "collections": db_info["collections"]
                },
                "ai_service": {
                    "status": ai_status
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


# Helper functions
async def get_or_create_conversation(
    conversation_id: Optional[int],
    user_id: int,
    db: AsyncSession
) -> Conversation:
    """Get existing conversation or create new one"""
    if conversation_id:
        result = await db.execute(
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        conversation = result.scalar_one_or_none()
        
        if conversation:
            return conversation
    
    # Create new conversation
    conversation = Conversation(
        user_id=user_id,
        conversation_type="card_recommendation",
        status="active"
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


def generate_conversation_title(first_message: str) -> str:
    """Generate a title for the conversation based on the first message"""
    # Simple title generation - could be enhanced with LLM
    message_lower = first_message.lower()
    
    if "myntra" in message_lower or "shopping" in message_lower:
        return "Shopping Credit Card Query"
    elif "travel" in message_lower:
        return "Travel Credit Card Query"
    elif "dining" in message_lower or "restaurant" in message_lower:
        return "Dining Credit Card Query"
    elif "reward" in message_lower or "cashback" in message_lower:
        return "Rewards Credit Card Query"
    elif "best card" in message_lower or "recommend" in message_lower:
        return "Credit Card Recommendation"
    else:
        return "Credit Card Query"


async def get_user_cards_summary(user_id: int, db: AsyncSession) -> List[Dict]:
    """Get summary of user's credit cards"""
    try:
        result = await db.execute(
            select(CreditCard)
            .where(
                CreditCard.user_id == user_id,
                CreditCard.is_active == True
            )
        )
        cards = result.scalars().all()
        
        return [
            {
                "id": card.id,
                "name": card.card_name,
                "type": card.card_type,
                "network": card.card_network,
                "reward_rate_general": card.reward_rate_general
            }
            for card in cards
        ]
    except Exception as e:
        logger.error(f"Error getting user cards summary: {e}")
        return []


def generate_suggested_actions(user_message: str, ai_response: Dict) -> List[str]:
    """Generate suggested follow-up actions"""
    suggestions = []
    
    message_lower = user_message.lower()
    
    if "best card" in message_lower or "recommend" in message_lower:
        suggestions.extend([
            "Compare reward rates for different categories",
            "Check eligibility requirements",
            "View annual fees and benefits"
        ])
    
    if "myntra" in message_lower or "shopping" in message_lower:
        suggestions.extend([
            "Find cards with online shopping bonuses",
            "Compare cashback vs reward points",
            "Check for merchant-specific offers"
        ])
    
    if ai_response.get("source") == "vector_db":
        suggestions.append("Ask for more detailed explanation")
    
    # Generic suggestions
    if not suggestions:
        suggestions.extend([
            "Ask about specific credit cards",
            "Compare multiple cards",
            "Get spending optimization tips"
        ])
    
    return suggestions[:3]  # Return max 3 suggestions 