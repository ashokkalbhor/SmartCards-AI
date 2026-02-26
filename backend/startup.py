#!/usr/bin/env python3
"""
Startup script for SmartCards AI Backend
Handles database migrations and initialization
"""

import asyncio
import os
import sys
import subprocess
import structlog
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.database import init_db, engine, Base

logger = structlog.get_logger()

def run_alembic_migrations():
    """Run Alembic migrations"""
    try:
        logger.info("Running Alembic migrations...")
        
        # Change to backend directory
        os.chdir(backend_dir)
        
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=backend_dir
        )
        
        if result.returncode == 0:
            logger.info("Alembic migrations completed successfully")
            if result.stdout:
                logger.info(f"Migration output: {result.stdout}")
        else:
            logger.error(f"Alembic migration failed: {result.stderr}")
            # Don't fail the startup, just log the error
            return False
            
    except Exception as e:
        logger.error(f"Error running Alembic migrations: {e}")
        return False
    
    return True

def create_tables_if_not_exist():
    """Create tables if they don't exist (fallback)"""
    try:
        logger.info("Creating tables if they don't exist...")
        
        # Import all models to ensure they are registered
        from app.models import (
            user, credit_card, transaction, merchant, 
            reward, conversation, card_master_data
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

async def initialize_database():
    """Initialize database with proper error handling"""
    try:
        logger.info("Initializing database...")
        
        # First try Alembic migrations
        migration_success = run_alembic_migrations()
        
        if not migration_success:
            logger.warning("Alembic migrations failed, trying fallback table creation")
            create_tables_if_not_exist()
        
        # Initialize database
        await init_db()
        
        logger.info("Database initialization completed")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def check_database_file():
    """Check if database file exists and is accessible"""
    db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
    
    if not db_path.exists():
        logger.warning(f"Database file not found at {db_path}")
        return False
    
    logger.info(f"Database file found: {db_path} ({db_path.stat().st_size / 1024:.1f} KB)")
    return True

def main():
    """Main startup function"""
    logger.info("Starting SmartCards AI Backend...")
    
    # Check database file
    check_database_file()
    
    # Initialize database
    success = asyncio.run(initialize_database())
    
    if success:
        logger.info("Backend startup completed successfully")
    else:
        logger.error("Backend startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 