#!/usr/bin/env python3
"""
Test script for the admin system
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8001/api/v1"

def test_admin_system():
    """Test the admin system functionality"""
    
    print("🧪 Testing Admin System...")
    
    # Test 1: Check if admin info endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/admin/admin-info")
        print(f"✅ Admin info endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Admin emails: {data.get('admin_emails', [])}")
    except Exception as e:
        print(f"❌ Admin info endpoint failed: {e}")
    
    # Test 2: Check if moderator info endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/moderator/moderator-info")
        print(f"✅ Moderator info endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Moderator info endpoint failed: {e}")
    
    # Test 3: Check if user roles endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/user-roles/my-role")
        print(f"✅ User role endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ User role endpoint failed: {e}")
    
    print("\n🎯 Admin System Test Complete!")
    print("\n📋 Available Endpoints:")
    print("   GET  /api/v1/admin/admin-info")
    print("   GET  /api/v1/admin/users")
    print("   GET  /api/v1/admin/moderator-requests")
    print("   PUT  /api/v1/admin/moderator-requests/{request_id}")
    print("   GET  /api/v1/admin/edit-suggestions")
    print("   PUT  /api/v1/admin/edit-suggestions/{suggestion_id}")
    print("   GET  /api/v1/admin/stats")
    print("   GET  /api/v1/moderator/moderator-info")
    print("   GET  /api/v1/moderator/edit-suggestions")
    print("   PUT  /api/v1/moderator/edit-suggestions/{suggestion_id}")
    print("   GET  /api/v1/moderator/stats")
    print("   POST /api/v1/user-roles/request-moderator")
    print("   GET  /api/v1/user-roles/my-moderator-request")
    print("   GET  /api/v1/user-roles/my-role")
    print("   POST /api/v1/user-roles/edit-suggestions")
    print("   GET  /api/v1/user-roles/my-suggestions")
    print("   GET  /api/v1/user-roles/my-suggestions/stats")

if __name__ == "__main__":
    test_admin_system() 