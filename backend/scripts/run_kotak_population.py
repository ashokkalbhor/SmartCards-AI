#!/usr/bin/env python3
"""
Kotak Mahindra Bank Credit Cards Population Runner
Executes the SQL script to populate Kotak Mahindra Bank credit cards data
"""

import sqlite3
import os
import sys
from datetime import datetime

def connect_database():
    """Connect to the SmartCards AI database"""
    try:
        # Database path relative to the script location
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'smartcards_ai.db')
        conn = sqlite3.connect(db_path)
        print(f"✅ Successfully connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def execute_sql_script(conn, script_path):
    """Execute the SQL script file"""
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        print(f"✅ Successfully executed SQL script: {script_path}")
        return True
    except Exception as e:
        print(f"❌ Error executing SQL script: {e}")
        return False

def verify_population(conn):
    """Verify that Kotak Mahindra Bank cards were populated successfully"""
    try:
        cursor = conn.cursor()
        
        # Count Kotak Mahindra Bank cards
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'Kotak Mahindra Bank'")
        card_count = cursor.fetchone()[0]
        
        # Count Kotak Mahindra Bank spending categories
        cursor.execute("SELECT COUNT(*) FROM spending_categories WHERE bank_name = 'Kotak Mahindra Bank'")
        category_count = cursor.fetchone()[0]
        
        # Count Kotak Mahindra Bank merchant rewards
        cursor.execute("SELECT COUNT(*) FROM merchant_rewards WHERE bank_name = 'Kotak Mahindra Bank'")
        merchant_count = cursor.fetchone()[0]
        
        # Get list of Kotak Mahindra Bank cards
        cursor.execute("SELECT card_name FROM card_master_data WHERE bank_name = 'Kotak Mahindra Bank' ORDER BY card_name")
        cards = cursor.fetchall()
        
        print("\n" + "="*70)
        print("KOTAK MAHINDRA BANK POPULATION VERIFICATION REPORT")
        print("="*70)
        print(f"📊 Total Cards Populated: {card_count}")
        print(f"📊 Total Spending Categories: {category_count}")
        print(f"📊 Total Merchant Rewards: {merchant_count}")
        print("\n📋 Kotak Mahindra Bank Cards List:")
        for i, (card_name,) in enumerate(cards, 1):
            print(f"   {i:2d}. {card_name}")
        
        print("\n✅ Kotak Mahindra Bank credit cards population completed successfully!")
        print(f"🕒 Population completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def main():
    """Main execution function"""
    print("🏦 Kotak Mahindra Bank Credit Cards Population Script")
    print("="*60)
    
    # Connect to database
    conn = connect_database()
    if not conn:
        sys.exit(1)
    
    try:
        # Get script path
        script_dir = os.path.dirname(__file__)
        sql_script_path = os.path.join(script_dir, 'populate_kotak_cards.sql')
        
        if not os.path.exists(sql_script_path):
            print(f"❌ SQL script not found: {sql_script_path}")
            sys.exit(1)
        
        print(f"📁 Using SQL script: {sql_script_path}")
        
        # Execute the population script
        if execute_sql_script(conn, sql_script_path):
            # Verify the population
            verify_population(conn)
        else:
            print("❌ Failed to execute Kotak Mahindra Bank population script")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    finally:
        if conn:
            conn.close()
            print("\n🔒 Database connection closed")

if __name__ == "__main__":
    main() 