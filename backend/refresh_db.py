#!/usr/bin/env python3
"""
Database Refresh Script for SmartCards AI
==========================================

This script completely refreshes the database by:
1. Dropping all existing tables
2. Creating fresh tables
3. Seeding with sample data

Usage:
    python refresh_db.py

WARNING: This will DELETE ALL existing data!
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import *  # Import all models to ensure they're registered
from app.core.database import Base


def print_step(step_number, description):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step_number}: {description}")
    print(f"{'='*60}")


def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")


def print_info(message):
    """Print an info message"""
    print(f"ℹ️  {message}")


def drop_all_tables():
    """Drop all existing tables"""
    print_step(1, "Dropping all existing tables")
    
    try:
        # Get all table names
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
        
        if tables:
            print_info(f"Found {len(tables)} tables to drop: {', '.join(tables)}")
            
            # Drop all tables
            Base.metadata.drop_all(bind=engine)
            print_success("All tables dropped successfully")
        else:
            print_info("No tables found to drop")
            
    except Exception as e:
        print_error(f"Error dropping tables: {e}")
        raise


def create_all_tables():
    """Create all tables from models"""
    print_step(2, "Creating fresh database tables")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print_success("All tables created successfully")
        
        # List created tables
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
            print_info(f"Created {len(tables)} tables: {', '.join(tables)}")
            
    except Exception as e:
        print_error(f"Error creating tables: {e}")
        raise


def seed_sample_data():
    """Seed the database with sample data"""
    print_step(3, "Seeding database with sample data")
    
    try:
        # Import and run the card seeding function
        from app.scripts.seed_card_master_data import create_sample_card_data
        
        print_info("Seeding card master data...")
        create_sample_card_data()
        print_success("Card master data seeded successfully")
        
        # Add other seeding functions here as needed
        # Example: seed_sample_users(), seed_sample_transactions(), etc.
        
    except Exception as e:
        print_error(f"Error seeding data: {e}")
        raise


def verify_database():
    """Verify the database is properly set up"""
    print_step(4, "Verifying database setup")
    
    try:
        db: Session = SessionLocal()
        
        # Check if tables exist and have data
        tables_status = {}
        
        # Check card master data
        from app.models.card_master_data import CardMasterData
        card_count = db.query(CardMasterData).count()
        tables_status['CardMasterData'] = card_count
        
        # Check other tables as needed
        # Add more checks here for other models
        
        db.close()
        
        print_info("Database verification results:")
        for table, count in tables_status.items():
            print(f"  • {table}: {count} records")
        
        if all(count > 0 for count in tables_status.values()):
            print_success("Database verification completed successfully")
        else:
            print_error("Some tables are empty - check seeding process")
            
    except Exception as e:
        print_error(f"Error verifying database: {e}")
        raise
    finally:
        if 'db' in locals():
            db.close()


def main():
    """Main function to refresh the entire database"""
    print("🚀 SmartCards AI Database Refresh Tool")
    print("⚠️  WARNING: This will DELETE ALL existing data!")
    
    # Ask for confirmation
    confirmation = input("\nDo you want to proceed? (yes/no): ").lower().strip()
    if confirmation not in ['yes', 'y']:
        print("❌ Database refresh cancelled.")
        return
    
    try:
        # Step 1: Drop all tables
        drop_all_tables()
        
        # Step 2: Create fresh tables
        create_all_tables()
        
        # Step 3: Seed with sample data
        seed_sample_data()
        
        # Step 4: Verify everything is working
        verify_database()
        
        print("\n" + "="*60)
        print("🎉 DATABASE REFRESH COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("Your database is now fresh and ready for testing.")
        print("\nNext steps:")
        print("1. Start the backend server: python main.py")
        print("2. Start the frontend: npm start")
        print("3. Begin testing with fresh data")
        
    except Exception as e:
        print(f"\n❌ Database refresh failed: {e}")
        print("Please check the error messages above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main() 