#!/usr/bin/env python3
"""
Quick Database Refresh Script
============================

A faster version that only clears and re-seeds data without dropping tables.
Use this for quick testing iterations.

Usage:
    python quick_refresh.py
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def clear_all_data():
    """Clear all data from tables without dropping them"""
    print("🧹 Clearing existing data...")
    
    db: Session = SessionLocal()
    try:
        # Import models
        from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
        from app.models.credit_card import CreditCard
        from app.models.transaction import Transaction
        from app.models.reward import Reward
        from app.models.user import User
        from app.models.conversation import Conversation, ConversationMessage, CardRecommendation
        from app.models.merchant import Merchant
        
        # Delete in order to avoid foreign key constraints
        print("  • Clearing conversation messages...")
        db.query(ConversationMessage).delete()
        
        print("  • Clearing card recommendations...")
        db.query(CardRecommendation).delete()
        
        print("  • Clearing conversations...")
        db.query(Conversation).delete()
        
        print("  • Clearing rewards...")
        db.query(Reward).delete()
        
        print("  • Clearing transactions...")
        db.query(Transaction).delete()
        
        print("  • Clearing credit cards...")
        db.query(CreditCard).delete()
        
        print("  • Clearing card spending categories...")
        db.query(CardSpendingCategory).delete()
        
        print("  • Clearing card merchant rewards...")
        db.query(CardMerchantReward).delete()
        
        print("  • Clearing card master data...")
        db.query(CardMasterData).delete()
        
        print("  • Clearing merchants...")
        db.query(Merchant).delete()
        
        print("  • Clearing users...")
        db.query(User).delete()
        
        db.commit()
        print("✅ All data cleared successfully")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def seed_data():
    """Seed with fresh sample data"""
    print("🌱 Seeding fresh data...")
    
    try:
        from app.scripts.seed_card_master_data import create_sample_card_data
        create_sample_card_data()
        print("✅ Data seeding completed")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        raise


def main():
    """Quick refresh without dropping tables"""
    print("⚡ Quick Database Refresh")
    print("This will clear and re-seed data without dropping tables.\n")
    
    try:
        # Clear existing data
        clear_all_data()
        
        # Seed fresh data
        seed_data()
        
        print("\n🎉 Quick refresh completed!")
        print("Your database now has fresh sample data.")
        
    except Exception as e:
        print(f"\n❌ Quick refresh failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 