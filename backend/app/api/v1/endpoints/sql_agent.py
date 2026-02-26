from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel
import logging

from app.core.sql_agent import SQLAgentService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()

# Global SQL Agent Service instance
sql_agent_service = None

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[int] = None
    context: Optional[Dict[str, Any]] = None
    include_sql: bool = False
    include_explanation: bool = True
    max_results: int = 10

class QueryResponse(BaseModel):
    query: str
    response: str
    sql_query: Optional[str] = None
    explanation: Optional[str] = None
    results: Optional[Any] = None
    error: Optional[str] = None

async def get_sql_agent_service():
    """Get or initialize SQL Agent Service"""
    global sql_agent_service
    if sql_agent_service is None:
        sql_agent_service = SQLAgentService()
        try:
            await sql_agent_service.initialize()
            logger.info("SQL Agent Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SQL Agent Service: {e}")
            raise HTTPException(status_code=500, detail="SQL Agent Service initialization failed")
    return sql_agent_service

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db),
    agent_service: SQLAgentService = Depends(get_sql_agent_service)
):
    """Process a natural language query using the SQL agent"""
    try:
        result = await agent_service.process_query(
            query=request.query,
            user_id=request.user_id,
            context=request.context,
            include_sql=request.include_sql,
            include_explanation=request.include_explanation,
            max_results=request.max_results
        )
        
        return QueryResponse(
            query=request.query,
            response=result.get("response", ""),
            sql_query=result.get("sql_query"),
            explanation=result.get("explanation"),
            results=result.get("results")
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return QueryResponse(
            query=request.query,
            response="I'm sorry, I'm having trouble processing your request right now. Please try again.",
            error=str(e)
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for SQL Agent Service"""
    global sql_agent_service
    try:
        if sql_agent_service is None:
            return {
                "status": "not_initialized",
                "service": "sql-agent",
                "agent_initialized": False,
                "database_connected": False
            }
        
        # Check if agent is properly initialized
        agent_ready = sql_agent_service.agent is not None
        db_connected = sql_agent_service.target_db is not None
        
        status = "healthy" if agent_ready and db_connected else "degraded"
        
        return {
            "status": status,
            "service": "sql-agent",
            "agent_initialized": agent_ready,
            "database_connected": db_connected
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "sql-agent",
            "agent_initialized": False,
            "database_connected": False,
            "error": str(e)
        }
