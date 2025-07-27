#!/usr/bin/env python3
"""
Setup script for Enhanced Chatbot
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.models.merchant import Merchant

async def setup_database():
    """Run database migrations"""
    print("Running database migrations...")
    
    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    print("✅ Database migrations completed")

async def seed_merchants():
    """Seed merchants table"""
    print("Seeding merchants table...")
    
    # Import and run the seed script
    from scripts.seed_merchants import seed_merchants as seed_merchants_func
    await seed_merchants_func()
    
    print("✅ Merchants seeded successfully")

async def verify_setup():
    """Verify that setup was successful"""
    print("Verifying setup...")
    
    async for db in get_async_db():
        try:
            # Check if merchants table exists and has data
            result = await db.execute("SELECT COUNT(*) FROM merchants")
            count = result.scalar()
            
            if count > 0:
                print(f"✅ Found {count} merchants in database")
            else:
                print("⚠️  No merchants found in database")
            
            # Check if other required tables exist
            required_tables = ["users", "credit_cards", "card_master_data"]
            for table in required_tables:
                result = await db.execute(f"SELECT COUNT(*) FROM {table}")
                count = result.scalar()
                print(f"✅ {table} table: {count} records")
            
            break
            
        except Exception as e:
            print(f"❌ Error verifying setup: {e}")
            return False
    
    return True

async def main():
    """Main setup function"""
    print("🚀 Setting up Enhanced Chatbot...")
    
    try:
        # Step 1: Run database migrations
        await setup_database()
        
        # Step 2: Seed merchants
        await seed_merchants()
        
        # Step 3: Verify setup
        success = await verify_setup()
        
        if success:
            print("\n🎉 Enhanced Chatbot setup completed successfully!")
            print("\nNext steps:")
            print("1. Start the backend server: python -m uvicorn app.main:app --reload")
            print("2. Start the frontend: npm start")
            print("3. Test the chatbot at: http://localhost:3000")
            print("\nTest queries:")
            print("- 'Which card is best for Amazon?'")
            print("- 'Show my credit cards'")
            print("- 'Should I use my HDFC card for Swiggy?'")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 