#!/usr/bin/env python3
"""
Create a test user with sample credit cards for testing the chatbot
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.models.user import User
from app.models.credit_card import CreditCard
from app.core.security import get_password_hash

async def create_test_user_with_cards():
    """Create a test user with sample credit cards"""
    async for db in get_async_db():
        try:
            # Check if test user already exists
            from sqlalchemy import select, text
            result = await db.execute(
                select(User).where(User.email == "test@smartcards.ai")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"Test user already exists with ID: {existing_user.id}")
                user_id = existing_user.id
            else:
                # Create test user
                test_user = User(
                    email="test@smartcards.ai",
                    hashed_password=get_password_hash("testpassword123"),
                    first_name="Test",
                    last_name="User",
                    is_active=True,
                    is_verified=True
                )
                db.add(test_user)
                await db.commit()
                await db.refresh(test_user)
                user_id = test_user.id
                print(f"✅ Created test user with ID: {user_id}")
                print(f"   Email: test@smartcards.ai")
                print(f"   Password: testpassword123")
            
            # Check if user already has cards
            result = await db.execute(
                select(CreditCard).where(CreditCard.user_id == user_id)
            )
            existing_cards = result.scalars().all()
            
            if existing_cards:
                print(f"User already has {len(existing_cards)} cards:")
                for card in existing_cards:
                    print(f"  - {card.card_name}")
                return user_id
            
            # Create sample credit cards with realistic reward rates
            sample_cards = [
                {
                    "card_name": "HDFC Regalia Gold",
                    "card_type": "Credit",
                    "card_network": "Visa",
                    "card_number_last4": "1234",
                    "card_holder_name": "Test User",
                    "expiry_month": 12,
                    "expiry_year": 2027,
                    "credit_limit": 500000.0,
                    "current_balance": 0.0,
                    "annual_fee": 2500.0,
                    "reward_rate_general": 1.0,
                    "reward_rate_online_shopping": 4.0,
                    "reward_rate_dining": 4.0,
                    "reward_rate_travel": 4.0,
                    "reward_rate_fuel": 1.0,
                    "reward_rate_entertainment": 4.0,
                    "reward_rate_groceries": 2.0,
                    "is_active": True,
                    "is_primary": True
                },
                {
                    "card_name": "SBI Elite",
                    "card_type": "Credit", 
                    "card_network": "Mastercard",
                    "card_number_last4": "5678",
                    "card_holder_name": "Test User",
                    "expiry_month": 8,
                    "expiry_year": 2028,
                    "credit_limit": 300000.0,
                    "current_balance": 0.0,
                    "annual_fee": 4999.0,
                    "reward_rate_general": 1.5,
                    "reward_rate_online_shopping": 2.0,
                    "reward_rate_dining": 5.0,
                    "reward_rate_travel": 3.0,
                    "reward_rate_fuel": 2.5,
                    "reward_rate_entertainment": 3.0,
                    "reward_rate_groceries": 2.5,
                    "is_active": True,
                    "is_primary": False
                },
                {
                    "card_name": "ICICI Amazon Pay",
                    "card_type": "Credit",
                    "card_network": "Visa",
                    "card_number_last4": "9012",
                    "card_holder_name": "Test User",
                    "expiry_month": 6,
                    "expiry_year": 2029,
                    "credit_limit": 200000.0,
                    "current_balance": 0.0,
                    "annual_fee": 0.0,
                    "reward_rate_general": 1.0,
                    "reward_rate_online_shopping": 5.0,
                    "reward_rate_dining": 2.0,
                    "reward_rate_travel": 1.0,
                    "reward_rate_fuel": 1.0,
                    "reward_rate_entertainment": 2.0,
                    "reward_rate_groceries": 1.0,
                    "is_active": True,
                    "is_primary": False
                },
                {
                    "card_name": "Axis Magnus",
                    "card_type": "Credit",
                    "card_network": "Mastercard", 
                    "card_number_last4": "3456",
                    "card_holder_name": "Test User",
                    "expiry_month": 10,
                    "expiry_year": 2026,
                    "credit_limit": 1000000.0,
                    "current_balance": 0.0,
                    "annual_fee": 12500.0,
                    "reward_rate_general": 1.2,
                    "reward_rate_online_shopping": 2.0,
                    "reward_rate_dining": 5.0,
                    "reward_rate_travel": 5.0,
                    "reward_rate_fuel": 2.0,
                    "reward_rate_entertainment": 4.0,
                    "reward_rate_groceries": 1.5,
                    "is_active": True,
                    "is_primary": False
                }
            ]
            
            # Add the cards
            created_cards = []
            for card_data in sample_cards:
                card = CreditCard(
                    user_id=user_id,
                    **card_data
                )
                db.add(card)
                created_cards.append(card_data["card_name"])
            
            await db.commit()
            
            print(f"✅ Created {len(sample_cards)} test credit cards:")
            for card_name in created_cards:
                print(f"  - {card_name}")
            
            print(f"\n🎯 Test Setup Complete!")
            print(f"   User ID: {user_id}")
            print(f"   Login: test@smartcards.ai / testpassword123")
            print(f"   Cards: {len(sample_cards)} cards with realistic reward rates")
            
            print(f"\n🧪 Test Queries to Try:")
            print(f"   - 'Which card is best for Amazon?'")
            print(f"   - 'Show my credit cards'")
            print(f"   - 'Should I use my HDFC card for Swiggy?'")
            print(f"   - 'Best card for dining'")
            print(f"   - 'Which card for travel?'")
            
            return user_id
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(create_test_user_with_cards()) 