#!/usr/bin/env python3
"""
Upload database to Render via file system
"""

import requests
import base64
import json

def upload_database_to_render():
    """Upload database to Render"""
    
    # Read the database file
    try:
        with open("backend/smartcards_ai.db", "rb") as f:
            db_content = f.read()
        
        print(f"✅ Read database file: {len(db_content)} bytes")
        
        # Encode as base64 for transmission
        db_b64 = base64.b64encode(db_content).decode('utf-8')
        
        # Your Render backend URL
        render_url = "https://smartcards-ai-2.onrender.com"
        
        # Try to upload via API endpoint (if available)
        upload_data = {
            "database": db_b64,
            "filename": "smartcards_ai.db"
        }
        
        print("🚀 Attempting to upload database...")
        response = requests.post(
            f"{render_url}/api/v1/admin/upload-database",
            json=upload_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Database uploaded successfully!")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except FileNotFoundError:
        print("❌ Database file not found!")
        return False
    except Exception as e:
        print(f"❌ Error uploading: {e}")
        return False

def main():
    print("📤 Uploading database to Render...")
    upload_database_to_render()

if __name__ == "__main__":
    main() 