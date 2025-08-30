from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import structlog
import time

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine
from app.core.logging import setup_logging
# Temporarily disable SQL Agent for debugging
# from app.core.sql_agent import SQLAgentService

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Global SQL Agent Service instance
sql_agent_service = None

# Create FastAPI app
app = FastAPI(
    title="SmartCards AI API",
    description="Intelligent credit card recommendation system with SQL Agent",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security middleware - Temporarily disabled for deployment
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=settings.ALLOWED_HOSTS
# )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time,
    )
    
    return response

# Temporarily disabled SQL Agent startup for debugging
# @app.on_event("startup")
# async def startup_event():
#     """Initialize services on startup"""
#     global sql_agent_service
#     
#     try:
#         # Initialize SQL Agent Service
#         sql_agent_service = SQLAgentService()
#         await sql_agent_service.initialize()
#         logger.info("✅ SQL Agent Service initialized successfully")
#     except Exception as e:
#         logger.error(f"❌ Failed to initialize SQL Agent Service: {e}")
#         # Continue running - service will be in degraded mode

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        error=str(exc),
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting SmartCards AI API")
    
    try:
        # Run startup script for database initialization
        import subprocess
        import sys
        from pathlib import Path
        
        backend_dir = Path(__file__).parent.parent
        startup_script = backend_dir / "startup.py"
        
        if startup_script.exists():
            logger.info("Running startup script for database initialization...")
            result = subprocess.run(
                [sys.executable, str(startup_script)],
                capture_output=True,
                text=True,
                cwd=backend_dir
            )
            
            if result.returncode != 0:
                logger.warning(f"Startup script had issues: {result.stderr}")
            else:
                logger.info("Startup script completed successfully")
        
        # Initialize database (fallback)
        from app.core.database import init_db
        await init_db()
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        # Don't fail the startup, just log the error
    
    logger.info("SmartCards AI API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down SmartCards AI API")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SmartCards AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "SmartCards AI API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 