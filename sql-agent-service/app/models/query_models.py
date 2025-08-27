from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for SQL agent queries"""
    query: str = Field(..., description="Natural language query")
    user_id: Optional[int] = Field(None, description="User ID for personalized responses")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    include_sql: bool = Field(False, description="Include generated SQL in response")
    include_explanation: bool = Field(True, description="Include explanation of results")
    max_results: int = Field(10, description="Maximum number of results to return")


class QueryResponse(BaseModel):
    """Response model for SQL agent queries"""
    response: str = Field(..., description="Natural language response")
    sql_query: Optional[str] = Field(None, description="Generated SQL query")
    results: Optional[List[Dict[str, Any]]] = Field(None, description="Query results")
    explanation: Optional[str] = Field(None, description="Explanation of results")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    source: str = Field(..., description="Source of response (sql_agent, cache, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DocumentProcessRequest(BaseModel):
    """Request model for document processing"""
    document_id: int = Field(..., description="Document ID")
    card_id: int = Field(..., description="Card ID")
    file_path: str = Field(..., description="Path to document file")
    document_type: str = Field(..., description="Type of document")
    user_id: int = Field(..., description="User ID")


class DocumentProcessResponse(BaseModel):
    """Response model for document processing"""
    success: bool = Field(..., description="Processing success status")
    document_id: int = Field(..., description="Document ID")
    vectors_created: int = Field(0, description="Number of vectors created")
    processing_time: float = Field(..., description="Processing time in seconds")
    message: str = Field(..., description="Processing message")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Current timestamp")
    database_connected: bool = Field(..., description="Database connection status")
    vector_db_connected: bool = Field(..., description="Vector database connection status")
    openai_connected: bool = Field(..., description="OpenAI connection status")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
