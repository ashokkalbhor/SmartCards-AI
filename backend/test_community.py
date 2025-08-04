#!/usr/bin/env python3
"""
Test script for the community discussion module
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8001/api/v1"

def test_community_functionality():
    """Test the community discussion functionality"""
    
    print("Testing Community Discussion Module...")
    print("=" * 50)
    
    # Test data
    test_card_id = 1  # Assuming card ID 1 exists
    test_post_data = {
        "title": "Test Post - Community Discussion",
        "body": "This is a test post to verify the community discussion functionality is working correctly."
    }
    
    test_comment_data = {
        "body": "This is a test comment on the post."
    }
    
    # Test 1: Get posts for a card
    print("\n1. Testing GET posts for card...")
    try:
        response = requests.get(f"{BASE_URL}/community/cards/{test_card_id}/posts")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total_count']} posts")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Create a post (requires authentication)
    print("\n2. Testing POST creation (requires auth)...")
    print("Note: This requires a valid authentication token")
    
    # Test 3: Get post detail
    print("\n3. Testing GET post detail...")
    try:
        response = requests.get(f"{BASE_URL}/community/posts/1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Post title: {data.get('title', 'N/A')}")
            print(f"Comments: {len(data.get('comments', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("Community module test completed!")
    print("\nTo test with authentication:")
    print("1. Login to get an access token")
    print("2. Use the token in Authorization header")
    print("3. Test creating posts and comments")

if __name__ == "__main__":
    test_community_functionality() 