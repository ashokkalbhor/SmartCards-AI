#!/usr/bin/env python3
"""
Test script for Enhanced Chatbot
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.enhanced_chatbot_service import enhanced_chatbot_service
from app.core.database import get_async_db
from app.models.user import User
from app.models.credit_card import CreditCard

# Test queries
TEST_QUERIES = [
    "Which card is best for Amazon?",
    "Show my credit cards",
    "Should I use my HDFC card for Swiggy?",
    "What's the best card for Netflix?",
    "Help me choose a card for Uber",
    "Compare my cards",
    "How many reward points do I have?",
    "Which card should I use for online shopping?",
    "Best card for dining",
    "Recommend a card for travel"
]

async def create_test_user_and_cards():
    """Create a test user with some credit cards"""
    async for db in get_async_db():
        try:
            # Create test user
            test_user = User(
                email="test@smartcards.ai",
                first_name="Test",
                last_name="User",
                is_active=True
            )
            db.add(test_user)
            await db.commit()
            await db.refresh(test_user)
            
            # Create test credit cards
            test_cards = [
                CreditCard(
                    user_id=test_user.id,
                    card_name="HDFC Regalia Gold",
                    card_type="Credit",
                    card_network="Visa",
                    card_number_last4="1234",
                    card_holder_name="Test User",
                    expiry_month=12,
                    expiry_year=2025,
                    reward_rate_general=1.0,
                    reward_rate_online_shopping=4.0,
                    reward_rate_dining=3.0,
                    reward_rate_travel=2.0,
                    is_active=True
                ),
                CreditCard(
                    user_id=test_user.id,
                    card_name="SBI Elite",
                    card_type="Credit",
                    card_network="Mastercard",
                    card_number_last4="5678",
                    card_holder_name="Test User",
                    expiry_month=12,
                    expiry_year=2025,
                    reward_rate_general=1.5,
                    reward_rate_online_shopping=2.0,
                    reward_rate_dining=4.0,
                    reward_rate_travel=3.0,
                    is_active=True
                ),
                CreditCard(
                    user_id=test_user.id,
                    card_name="ICICI Amazon Pay",
                    card_type="Credit",
                    card_network="Visa",
                    card_number_last4="9012",
                    card_holder_name="Test User",
                    expiry_month=12,
                    expiry_year=2025,
                    reward_rate_general=2.0,
                    reward_rate_online_shopping=5.0,
                    reward_rate_dining=2.0,
                    reward_rate_travel=1.0,
                    is_active=True
                )
            ]
            
            for card in test_cards:
                db.add(card)
            
            await db.commit()
            print(f"✅ Created test user (ID: {test_user.id}) with {len(test_cards)} cards")
            return test_user.id
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            await db.rollback()
            return None

async def test_queries(user_id: int):
    """Test the enhanced chatbot with various queries"""
    print(f"\n🧪 Testing Enhanced Chatbot with user ID: {user_id}")
    print("=" * 60)
    
    total_queries = len(TEST_QUERIES)
    successful_queries = 0
    api_calls_saved = 0
    total_processing_time = 0
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n{i}/{total_queries}: {query}")
        print("-" * 40)
        
        try:
            async for db in get_async_db():
                response = await enhanced_chatbot_service.process_query(
                    user_id=user_id,
                    query=query,
                    db=db
                )
                
                print(f"Response: {response['response'][:100]}...")
                print(f"Source: {response['source']}")
                print(f"Confidence: {response['confidence']:.2f}")
                print(f"API Calls Saved: {response.get('api_calls_saved', 0)}")
                print(f"Processing Time: {response.get('processing_time', 0):.3f}s")
                
                if response['source'] != 'error':
                    successful_queries += 1
                    api_calls_saved += response.get('api_calls_saved', 0)
                    total_processing_time += response.get('processing_time', 0)
                
                break
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Queries: {total_queries}")
    print(f"Successful Queries: {successful_queries}")
    print(f"Success Rate: {(successful_queries/total_queries)*100:.1f}%")
    print(f"Total API Calls Saved: {api_calls_saved}")
    print(f"Total Processing Time: {total_processing_time:.3f}s")
    print(f"Average Processing Time: {total_processing_time/total_queries:.3f}s")
    
    if successful_queries == total_queries:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total_queries - successful_queries} tests failed")

async def main():
    """Main test function"""
    print("🧪 Testing Enhanced Chatbot...")
    
    try:
        # Create test user and cards
        user_id = await create_test_user_and_cards()
        
        if user_id:
            # Test queries
            await test_queries(user_id)
        else:
            print("❌ Failed to create test user")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 