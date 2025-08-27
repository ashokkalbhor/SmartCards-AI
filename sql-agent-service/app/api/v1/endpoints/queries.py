import asyncio
import logging
import time
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.models.query_models import QueryRequest, QueryResponse, ErrorResponse
from app.core.sql_agent import sql_agent_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> Any:
    """Process a natural language query using the SQL agent"""
    
    # Check if SQL agent is initialized
    if not sql_agent_service.agent:
        logger.error("SQL Agent Service not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SQL Agent Service is not available. Please try again later."
        )
    
    try:
        # Process the query
        result = await sql_agent_service.process_query(
            query=request.query,
            user_id=request.user_id,
            context=request.context,
            include_sql=request.include_sql,
            include_explanation=request.include_explanation,
            max_results=request.max_results
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


async def _process_query_with_retry(request: QueryRequest) -> Dict[str, Any]:
    """Process query with retry logic"""
    
    last_error = None
    
    for attempt in range(settings.MAX_RETRIES):
        try:
            # Process the query
            result = await sql_agent_service.process_query(
                query=request.query,
                user_id=request.user_id,
                context=request.context,
                include_sql=request.include_sql,
                include_explanation=request.include_explanation,
                max_results=request.max_results
            )
            
            return result
            
        except Exception as e:
            last_error = e
            logger.warning(f"Query attempt {attempt + 1} failed: {e}")
            
            # If this is not the last attempt, wait before retrying
            if attempt < settings.MAX_RETRIES - 1:
                wait_time = settings.RETRY_DELAY * (settings.RETRY_BACKOFF ** attempt)
                await asyncio.sleep(wait_time)
    
    # All retries failed
    logger.error(f"All {settings.MAX_RETRIES} query attempts failed")
    raise last_error


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check for the SQL agent service"""
    return {
        "status": "healthy" if sql_agent_service.agent else "degraded",
        "service": "sql-agent",
        "agent_initialized": sql_agent_service.agent is not None,
        "database_connected": sql_agent_service.db is not None
    }


@router.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """Get service statistics"""
    return {
        "service": "sql-agent",
        "agent_initialized": sql_agent_service.agent is not None,
        "cache_stats": sql_agent_service.cache_service.get_stats() if sql_agent_service.cache_service else {},
        "vector_db_stats": sql_agent_service.vector_service.get_collection_stats() if sql_agent_service.vector_service else {}
    }
