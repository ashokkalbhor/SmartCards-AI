import sys
import logging
import structlog
from typing import Any, Dict

from app.core.config import settings


def setup_logging():
    """Setup structured logging configuration"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Set log levels for external libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.DEBUG else logging.WARNING
    )
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("redis").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


def log_request(request_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log incoming request data"""
    if logger is None:
        logger = get_logger()
    
    logger.info(
        "Incoming request",
        method=request_data.get("method"),
        url=request_data.get("url"),
        headers=request_data.get("headers"),
        client_ip=request_data.get("client_ip"),
    )


def log_response(response_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log outgoing response data"""
    if logger is None:
        logger = get_logger()
    
    logger.info(
        "Outgoing response",
        status_code=response_data.get("status_code"),
        response_time=response_data.get("response_time"),
        content_length=response_data.get("content_length"),
    )


def log_error(error: Exception, context: Dict[str, Any] = None, logger: structlog.BoundLogger = None):
    """Log error with context"""
    if logger is None:
        logger = get_logger()
    
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    
    if context:
        log_data.update(context)
    
    logger.error("Application error", **log_data, exc_info=True) 