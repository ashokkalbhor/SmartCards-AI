import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import create_async_tables
from app.core.sql_agent import initialize_sql_agent_service
from app.api.v1.endpoints import queries, auth, chat, documents

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting SQL Agent Service...")
    
    # Initialize databases (for Render deployment)
    try:
        import subprocess
        subprocess.run(["python", "init_db.py"], check=True)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
    
    # Create database tables
    try:
        await create_async_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    
    # Initialize SQL Agent Service
    try:
        sql_agent_ready = await initialize_sql_agent_service()
        if sql_agent_ready:
            logger.info("SQL Agent Service initialized successfully")
        else:
            logger.warning("SQL Agent Service initialization failed - running in degraded mode")
    except Exception as e:
        logger.error(f"Error initializing SQL Agent Service: {e}")
        # Continue running - service will be in degraded mode
    
    logger.info("SQL Agent Service started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SQL Agent Service...")

# Create FastAPI app
app = FastAPI(
    title="SQL Agent Service",
    description="LLM-based SQL agent for natural language database queries",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://smartcards-ai-frontend.onrender.com"  # Production frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(queries.router, prefix="/api/v1/sql-agent", tags=["sql-agent"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SQL Agent Service",
        "version": settings.VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
