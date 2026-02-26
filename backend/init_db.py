#!/usr/bin/env python3
"""
Database initialization script for SmartCards AI
Creates all tables in the SQLite database
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, close_db
from app.models import *  # Import all models
import structlog

logger = structlog.get_logger()


async def main():
    """Initialize the database"""
    try:
        logger.info("Starting database initialization...")
        await init_db()
        logger.info("Database initialization completed successfully!")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        sys.exit(1)
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(main()) 