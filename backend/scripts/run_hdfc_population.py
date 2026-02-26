#!/usr/bin/env python3
"""
Script to populate HDFC Bank credit cards data into the master database.
This script will execute the populate_hdfc_cards.sql file.
"""

import os
import sys
import sqlite3
from pathlib import Path

def get_database_path():
    """Get the path to the SQLite database"""
    # Go up from scripts directory to backend, then to database
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    db_path = backend_dir / "smartcards_ai.db"
    return str(db_path)

def get_db_connection():
    """Get database connection using SQLite."""
    try:
        db_path = get_database_path()
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_sql_file(conn, sql_file_path):
    """Execute SQL file and handle any errors."""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = conn.cursor()
        cursor.executescript(sql_content)
        conn.commit()
        
        print(f"✅ Successfully executed {sql_file_path}")
        
        # Get count of HDFC Bank cards inserted
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'HDFC Bank'")
        count = cursor.fetchone()[0]
        print(f"✅ Total HDFC Bank cards in database: {count}")
        
        # Get count of spending categories for HDFC Bank cards
        cursor.execute("""
            SELECT COUNT(*) FROM card_spending_categories csc
            JOIN card_master_data cmd ON csc.card_master_id = cmd.id
            WHERE cmd.bank_name = 'HDFC Bank'
        """)
        categories_count = cursor.fetchone()[0]
        print(f"✅ Total HDFC Bank card spending categories: {categories_count}")
        
        # Get count of merchant rewards for HDFC Bank cards
        cursor.execute("""
            SELECT COUNT(*) FROM card_merchant_rewards cmr
            JOIN card_master_data cmd ON cmr.card_master_id = cmd.id
            WHERE cmd.bank_name = 'HDFC Bank'
        """)
        merchants_count = cursor.fetchone()[0]
        print(f"✅ Total HDFC Bank card merchant rewards: {merchants_count}")
        
        cursor.close()
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: SQL file not found: {sql_file_path}")
        return False
    except Exception as e:
        print(f"❌ Error executing SQL: {e}")
        conn.rollback()
        return False

def main():
    """Main function to populate HDFC Bank credit cards."""
    print("🏦 HDFC Bank Credit Cards Population Script")
    print("=" * 50)
    
    # Get database path
    db_path = get_database_path()
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file not found at {db_path}")
        print("Please ensure the database is created and accessible")
        sys.exit(1)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(script_dir, 'populate_hdfc_cards.sql')
    
    # Check if SQL file exists
    if not os.path.exists(sql_file_path):
        print(f"❌ SQL file not found: {sql_file_path}")
        sys.exit(1)
    
    # Connect to database
    conn = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database")
        sys.exit(1)
    
    try:
        # Execute the SQL file
        success = execute_sql_file(conn, sql_file_path)
        
        if success:
            print("\n🎉 HDFC Bank credit cards populated successfully!")
            print("\n📋 Cards Added:")
            print("   • 23 HDFC Bank credit cards (including new PIXEL and Tata Neu cards)")
            print("   • Complete financial details")
            print("   • Reward rates and categories")
            print("   • Merchant-specific benefits")
            print("   • Insurance and benefits")
            print("\n✨ Your master database is now ready with enhanced HDFC Bank cards!")
        else:
            print("❌ Failed to populate HDFC Bank credit cards")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main() 