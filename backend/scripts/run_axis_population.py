#!/usr/bin/env python3
"""
Axis Bank Credit Cards Population Script Runner
Executes the SQL script to populate Axis Bank credit cards data
"""

import sqlite3
import os
import sys
from pathlib import Path

def get_database_path():
    """Get the path to the SQLite database"""
    # Go up from scripts directory to backend, then to database
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    db_path = backend_dir / "smartcards_ai.db"
    return str(db_path)

def read_sql_script():
    """Read the Axis Bank cards population SQL script"""
    script_path = Path(__file__).parent / "populate_axis_cards.sql"
    
    if not script_path.exists():
        raise FileNotFoundError(f"SQL script not found: {script_path}")
    
    with open(script_path, 'r', encoding='utf-8') as file:
        return file.read()

def execute_sql_script(db_path, sql_content):
    """Execute the SQL script against the database"""
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Connected to database successfully")
        
        # Execute the SQL script
        print("Executing Axis Bank cards population script...")
        cursor.executescript(sql_content)
        
        # Commit the changes
        conn.commit()
        print("Axis Bank cards data populated successfully!")
        
        # Get count of Axis Bank cards inserted
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'Axis Bank'")
        count = cursor.fetchone()[0]
        print(f"Total Axis Bank cards in database: {count}")
        
        # Get count of spending categories for Axis Bank cards
        cursor.execute("""
            SELECT COUNT(*) FROM card_spending_categories csc
            JOIN card_master_data cmd ON csc.card_master_id = cmd.id
            WHERE cmd.bank_name = 'Axis Bank'
        """)
        categories_count = cursor.fetchone()[0]
        print(f"Total Axis Bank card spending categories: {categories_count}")
        
        # Get count of merchant rewards for Axis Bank cards
        cursor.execute("""
            SELECT COUNT(*) FROM card_merchant_rewards cmr
            JOIN card_master_data cmd ON cmr.card_master_id = cmd.id
            WHERE cmd.bank_name = 'Axis Bank'
        """)
        merchants_count = cursor.fetchone()[0]
        print(f"Total Axis Bank card merchant rewards: {merchants_count}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("Database connection closed")
    
    return True

def main():
    """Main execution function"""
    print("Axis Bank Credit Cards Population Script")
    print("=" * 50)
    
    try:
        # Get database path
        db_path = get_database_path()
        print(f"Database path: {db_path}")
        
        if not os.path.exists(db_path):
            print(f"Error: Database file not found at {db_path}")
            print("Please ensure the database is created and accessible")
            sys.exit(1)
        
        # Read SQL script
        print("Reading Axis Bank cards SQL script...")
        sql_content = read_sql_script()
        print(f"SQL script loaded successfully ({len(sql_content)} characters)")
        
        # Execute script
        success = execute_sql_script(db_path, sql_content)
        
        if success:
            print("\n✅ Axis Bank cards population completed successfully!")
            print("\nYou can now:")
            print("1. Check the database for Axis Bank entries")
            print("2. Test the SmartCards AI application with Axis Bank cards")
            print("3. Run comparison queries between different banks")
        else:
            print("\n❌ Axis Bank cards population failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Script execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 