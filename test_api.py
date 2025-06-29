#!/usr/bin/env python3
"""
Simple test script to verify the API is working
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    try:
        # Test if server is running
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Backend server is running!")
            print(f"📖 API Documentation: {base_url}/docs")
        else:
            print(f"❌ Backend server returned status: {response.status_code}")
            return False
            
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print(f"⚠️  Health check failed: {response.status_code}")
            
        # Test registration endpoint
        test_user = {
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(f"{base_url}/api/v1/auth/register", json=test_user)
        if response.status_code == 200:
            print("✅ Registration endpoint working!")
            user_data = response.json()
            print(f"   User created with ID: {user_data.get('id')}")
        else:
            print(f"⚠️  Registration endpoint returned: {response.status_code}")
            print(f"   Response: {response.text}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing UNGI SmartCards AI API...")
    print("=" * 50)
    
    success = test_api()
    
    print("=" * 50)
    if success:
        print("🎉 API test completed successfully!")
        print("\n🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
        print("📖 API Docs: http://localhost:8000/docs")
    else:
        print("�� API test failed!") 