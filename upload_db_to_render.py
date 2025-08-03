#!/usr/bin/env python3
"""
Script to upload local database to Render production
"""

import requests
import json
import os
import sqlite3
from pathlib import Path

def check_local_db():
    """Check what's in the local database"""
    db_path = Path("backend/smartcards_ai.db")
    if not db_path.exists():
        print("❌ Local database not found!")
        return False
    
    print(f"✅ Found local database: {db_path}")
    print(f"📊 Size: {db_path.stat().st_size / 1024:.1f} KB")
    
    # Check what tables exist
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[table[0] for table in tables]}")
        
        # Check card_master_data table
        if ('card_master_data',) in tables:
            cursor.execute("SELECT COUNT(*) FROM card_master_data")
            count = cursor.fetchone()[0]
            print(f"💳 Cards in database: {count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return False

def upload_to_render():
    """Upload database to Render via API"""
    print("\n🚀 Uploading database to Render...")
    
    # Your Render backend URL
    render_url = "https://smartcards-ai-2.onrender.com"
    
    # Check if backend is accessible
    try:
        response = requests.get(f"{render_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is accessible")
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False
    
    # For now, we'll need to manually upload the database
    # Render doesn't allow direct file uploads via API
    print("\n📋 Manual Upload Instructions:")
    print("1. Go to Render Dashboard")
    print("2. Select your backend service")
    print("3. Go to 'Environment' tab")
    print("4. Add environment variable: DATABASE_FILE=smartcards_ai.db")
    print("5. Upload the database file manually")
    
    return True

def main():
    print("🔍 Checking local database...")
    if not check_local_db():
        return
    
    print("\n📤 Preparing to upload to Render...")
    upload_to_render()

if __name__ == "__main__":
    main() 