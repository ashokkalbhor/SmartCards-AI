#!/usr/bin/env python3
"""
Check the database structure
"""

import sqlite3
from pathlib import Path

def check_database_structure():
    """Check the database structure"""
    db_path = Path("backend/smartcards_ai.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return
    
    print(f"🔍 Analyzing database structure: {db_path}")
    print(f"📊 Size: {db_path.stat().st_size / 1024:.1f} KB")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n📋 Tables found: {[table[0] for table in tables]}")
        
        # Check card_master_data structure
        if ('card_master_data',) in tables:
            cursor.execute("PRAGMA table_info(card_master_data);")
            columns = cursor.fetchall()
            print(f"\n🏗️ card_master_data columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Check sample data
            cursor.execute("SELECT * FROM card_master_data LIMIT 3")
            sample_data = cursor.fetchall()
            print(f"\n📋 Sample card data:")
            for row in sample_data:
                print(f"  - {row}")
        
        # Check other important tables
        for table in ['card_merchant_rewards', 'card_spending_categories', 'merchants']:
            if (table,) in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"\n📊 {table}: {count} entries")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_database_structure() 