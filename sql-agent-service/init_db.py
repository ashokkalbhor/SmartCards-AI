#!/usr/bin/env python3
"""
Database initialization script for SQL Agent Service
This script will be run during container startup to ensure databases are properly set up
"""

import os
import shutil
import sqlite3
from pathlib import Path

def init_databases():
    """Initialize databases for SQL Agent Service"""
    
    # Use environment-based directory
    if os.getenv("ENVIRONMENT") == "production":
        data_dir = Path("/app/data")
        data_dir.mkdir(exist_ok=True)
    else:
        data_dir = Path(".")
    
    # Paths for databases
    sql_agent_db = data_dir / "sql_agent_service.db"
    target_db = data_dir / "smartcards_ai.db"
    
    # Initialize SQL Agent Service database if it doesn't exist
    if not sql_agent_db.exists():
        print("Creating SQL Agent Service database...")
        conn = sqlite3.connect(sql_agent_db)
        conn.close()
        print(f"Created: {sql_agent_db}")
    
    # Copy target database if it doesn't exist
    if not target_db.exists():
        print("Target database not found. Will be created when main backend starts.")
        # Create empty database for now
        conn = sqlite3.connect(target_db)
        conn.close()
        print(f"Created placeholder: {target_db}")
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_databases()
