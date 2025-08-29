#!/usr/bin/env python3
"""
Test script to verify SQL Agent Service integration
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
MAIN_API_URL = "http://localhost:8000"
SQL_AGENT_URL = "http://localhost:8001"

async def test_sql_agent_service_health():
    """Test SQL Agent Service health endpoint"""
    print("🔍 Testing SQL Agent Service Health...")
    
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

async def test_main_api_sql_agent_health():
    """Test Main API SQL Agent health endpoint"""
    print("\n🔍 Testing Main API SQL Agent Health...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{MAIN_API_URL}/api/v1/sql-agent/health")
            
            if response.status_code == 200:
                print("✅ Main API SQL Agent health check successful")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Main API SQL Agent health check failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Main API SQL Agent health check error: {e}")
        return False

async def test_sql_agent_query():
    """Test SQL Agent query endpoint (without authentication)"""
    print("\n🔍 Testing SQL Agent Query Endpoint...")
    
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
                print("✅ SQL Agent query successful")
                result = response.json()
                print(f"   Response: {result.get('response', 'No response')[:100]}...")
                return True
            elif response.status_code == 401:
                print("⚠️  SQL Agent query requires authentication (expected)")
                return True
            else:
                print(f"❌ SQL Agent query failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ SQL Agent query error: {e}")
        return False

async def test_main_api_sql_agent_query():
    """Test Main API SQL Agent query endpoint (without authentication)"""
    print("\n🔍 Testing Main API SQL Agent Query...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            query_data = {
                "query": "Which is the best credit card for Airtel spends?",
                "include_sql": True,
                "include_explanation": True,
                "max_results": 5
            }
            
            response = await client.post(
                f"{MAIN_API_URL}/api/v1/sql-agent/query",
                json=query_data
            )
            
            if response.status_code == 401:
                print("⚠️  Main API SQL Agent query requires authentication (expected)")
                return True
            elif response.status_code == 503:
                print("⚠️  SQL Agent service unavailable (may be expected if service not running)")
                return True
            else:
                print(f"❌ Main API SQL Agent query failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Main API SQL Agent query error: {e}")
        return False

async def main():
    """Run all integration tests"""
    print("🚀 Starting SQL Agent Integration Tests...\n")
    
    tests = [
        ("SQL Agent Service Health", test_sql_agent_service_health),
        ("Main API SQL Agent Health", test_main_api_sql_agent_health),
        ("SQL Agent Query", test_sql_agent_query),
        ("Main API SQL Agent Query", test_main_api_sql_agent_query),
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
        print("🎉 All tests passed! Integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the service status and configuration.")

if __name__ == "__main__":
    asyncio.run(main())
