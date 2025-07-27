#!/usr/bin/env python3
"""
Debug script to test merchant service responses
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.enhanced_chatbot_service import enhanced_chatbot_service
from app.core.database import get_async_db

async def debug_merchant_responses():
    """Test merchant service responses"""
    
    # Test queries
    test_queries = [
        "Which card is best for Amazon?",
        "Should I use my HDFC card for Swiggy?",
        "Best card for Netflix",
        "Which card for Uber?",
        "Show my credit cards"
    ]
    
    # Use test user ID (assuming test user exists)
    test_user_id = 1
    
    print("🔍 Debugging Merchant Service Responses")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 30)
        
        try:
            async for db in get_async_db():
                response = await enhanced_chatbot_service.process_query(
                    user_id=test_user_id,
                    query=query,
                    db=db
                )
                
                print(f"✅ Response: {response['response'][:200]}...")
                print(f"📊 Source: {response['source']}")
                print(f"🎯 Confidence: {response['confidence']}")
                print(f"⚡ API Calls Saved: {response.get('api_calls_saved', 0)}")
                
                if 'merchant' in response:
                    print(f"🏪 Merchant: {response['merchant']}")
                if 'recommendation' in response:
                    print(f"💳 Recommendation: {response['recommendation']}")
                
                break
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Debug complete!")

if __name__ == "__main__":
    asyncio.run(debug_merchant_responses()) 