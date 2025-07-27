"""
Enhanced chatbot API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time

from app.core.database import get_async_db
from app.core.security import get_current_user
from app.core.enhanced_chatbot_service import enhanced_chatbot_service
from app.models.user import User

router = APIRouter()

class EnhancedChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    conversation_id: Optional[int] = None
    use_cache: bool = Field(default=True, description="Use response caching")

class EnhancedChatResponse(BaseModel):
    response: str = Field(..., description="AI assistant's response")
    conversation_id: Optional[int] = Field(None, description="Conversation ID")
    source: str = Field(..., description="Response source: cache, pattern_matching, llm, or error")
    confidence: float = Field(..., description="Confidence score (0-1)")
    api_calls_saved: int = Field(..., description="Number of API calls saved")
    processing_time: float = Field(..., description="Processing time in seconds")
    query_type: Optional[str] = Field(None, description="Type of query detected")
    complexity: Optional[str] = Field(None, description="Query complexity: simple or complex")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

@router.post("/enhanced-chat", response_model=EnhancedChatResponse)
async def enhanced_chat(
    request: EnhancedChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Enhanced chatbot endpoint with pattern matching and caching
    """
    try:
        response = await enhanced_chatbot_service.process_query(
            user_id=current_user.id,
            query=request.message,
            conversation_id=request.conversation_id,
            db=db
        )
        
        return EnhancedChatResponse(
            response=response["response"],
            conversation_id=request.conversation_id,
            source=response["source"],
            confidence=response["confidence"],
            api_calls_saved=response.get("api_calls_saved", 0),
            processing_time=response.get("processing_time", 0),
            query_type=response.get("query_type"),
            complexity=response.get("complexity"),
            metadata=response.get("metadata", {})
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing enhanced chat request: {str(e)}"
        )

@router.get("/health")
async def enhanced_chatbot_health_check():
    """
    Check enhanced chatbot system health
    """
    try:
        # Get cache stats
        cache_stats = enhanced_chatbot_service.cache.get_stats()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "components": {
                "enhanced_chatbot": {
                    "status": "healthy",
                    "cache_stats": cache_stats
                },
                "merchant_service": {
                    "status": "healthy"
                },
                "query_matcher": {
                    "status": "healthy"
                }
            }
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e)
        }

@router.get("/stats")
async def get_chatbot_stats():
    """
    Get chatbot usage statistics
    """
    try:
        cache_stats = enhanced_chatbot_service.cache.get_stats()
        
        return {
            "cache": cache_stats,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting stats: {str(e)}"
        ) 