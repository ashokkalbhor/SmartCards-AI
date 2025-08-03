#!/usr/bin/env python3
"""
Fix database issues and ensure proper initialization
"""

import asyncio
import sqlite3
from pathlib import Path
import structlog

logger = structlog.get_logger()

def fix_database():
    """Fix common database issues"""
    try:
        db_path = Path("smartcards_ai.db")
        
        if not db_path.exists():
            logger.error("Database file not found!")
            return False
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check database integrity
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()
        
        if integrity_result[0] != "ok":
            logger.error(f"Database integrity check failed: {integrity_result[0]}")
            return False
        
        logger.info("Database integrity check passed")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        logger.info(f"Found tables: {tables}")
        
        # Check card_master_data table
        if 'card_master_data' in tables:
            cursor.execute("SELECT COUNT(*) FROM card_master_data")
            card_count = cursor.fetchone()[0]
            logger.info(f"Card count: {card_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error fixing database: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    try:
        from app.core.database import async_engine
        
        async with async_engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            logger.info("Database connection test passed")
            return True
            
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("Fixing database issues...")
    
    # Fix database
    if fix_database():
        logger.info("Database fix completed")
    else:
        logger.error("Database fix failed")
    
    # Test connection
    asyncio.run(test_database_connection())

if __name__ == "__main__":
    main() 