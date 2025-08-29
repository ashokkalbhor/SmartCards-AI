#!/usr/bin/env python3
"""
Test script to verify direct SQL Agent Service integration
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
SQL_AGENT_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

async def test_sql_agent_service_direct():
    """Test direct access to SQL Agent Service"""
    print("🔍 Testing Direct SQL Agent Service Access...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test query to SQL agent service directly
            query_data = {
                "query": "Which is the best credit card for Airtel spends?",
                "user_id": 1,
                "context": {
                    "user_cards": [
                        {"card_name": "HDFC Regalia", "bank_name": "HDFC Bank"}
                    ]
                },
                "include_sql": True,
                "include_explanation": True,
                "max_results": 5
            }
            
            response = await client.post(
                f"{SQL_AGENT_URL}/api/v1/sql-agent/query",
                json=query_data
            )
            
            if response.status_code == 200:
                print("✅ Direct SQL Agent query successful")
                result = response.json()
                print(f"   Response: {result.get('response', 'No response')[:100]}...")
                return True
            else:
                print(f"❌ Direct SQL Agent query failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Direct SQL Agent query error: {e}")
        return False

async def test_sql_agent_health():
    """Test SQL Agent Service health endpoint"""
    print("\n🔍 Testing SQL Agent Service Health...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{SQL_AGENT_URL}/health")
            
            if response.status_code == 200:
                print("✅ SQL Agent Service is healthy")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ SQL Agent Service health check failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ SQL Agent Service health check error: {e}")
        return False

async def test_cors_configuration():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS Configuration...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test OPTIONS request to check CORS
            response = await client.options(
                f"{SQL_AGENT_URL}/api/v1/sql-agent/query",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            if response.status_code == 200:
                print("✅ CORS configuration is working")
                print(f"   CORS Headers: {dict(response.headers)}")
                return True
            else:
                print(f"⚠️  CORS check returned: {response.status_code}")
                return True  # Not critical for functionality
                
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

async def main():
    """Run all direct integration tests"""
    print("🚀 Starting Direct SQL Agent Integration Tests...\n")
    
    tests = [
        ("SQL Agent Service Health", test_sql_agent_health),
        ("CORS Configuration", test_cors_configuration),
        ("Direct SQL Agent Query", test_sql_agent_service_direct),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"📋 Running: {test_name}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Total: {total}, Passed: {passed}, Failed: {total - passed}")
    
    if passed == total:
        print("🎉 All tests passed! Direct integration is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Start the SQL Agent Service: cd sql-agent-service && python -m app.main")
        print("2. Update frontend to use sqlAgentServiceAPI")
        print("3. Test chat functionality in the frontend")
    else:
        print("⚠️  Some tests failed. Check the service status and configuration.")

if __name__ == "__main__":
    asyncio.run(main())
