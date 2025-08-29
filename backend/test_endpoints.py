#!/usr/bin/env python3
"""
Quick test script to verify main API endpoints work after removing old chatbot code
"""

import requests
import json

def test_endpoints():
    """Test main API endpoints"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing Main API Endpoints")
    print("=" * 40)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: PASS")
        else:
            print(f"❌ Health check: FAIL (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health check: FAIL (Error: {e})")
    
    # Test 2: Card master data endpoint
    try:
        response = requests.get(f"{base_url}/card-master-data/")
        if response.status_code == 200:
            print("✅ Card master data: PASS")
        else:
            print(f"❌ Card master data: FAIL (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Card master data: FAIL (Error: {e})")
    
    # Test 3: Merchants endpoint
    try:
        response = requests.get(f"{base_url}/merchants/")
        if response.status_code == 200:
            print("✅ Merchants endpoint: PASS")
        else:
            print(f"❌ Merchants endpoint: FAIL (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Merchants endpoint: FAIL (Error: {e})")
    
    print("=" * 40)
    print("✅ Endpoint testing complete!")

if __name__ == "__main__":
    test_endpoints()
