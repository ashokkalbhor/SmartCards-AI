#!/usr/bin/env python3
"""
Check the actual content of the database
"""

import sqlite3
from pathlib import Path

def check_database_content():
    """Check what's actually in the database"""
    db_path = Path("backend/smartcards_ai.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return
    
    print(f"🔍 Analyzing database: {db_path}")
    print(f"📊 Size: {db_path.stat().st_size / 1024:.1f} KB")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check card_master_data table
        cursor.execute("SELECT COUNT(*) FROM card_master_data")
        total_cards = cursor.fetchone()[0]
        print(f"💳 Total cards: {total_cards}")
        
        # Check a few sample cards
        cursor.execute("SELECT id, bank_name, card_name, card_type FROM card_master_data LIMIT 5")
        sample_cards = cursor.fetchall()
        print(f"\n📋 Sample cards:")
        for card in sample_cards:
            print(f"  - {card[1]} {card[2]} ({card[3]})")
        
        # Check if cards have detailed information
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE annual_fee IS NOT NULL")
        cards_with_fees = cursor.fetchone()[0]
        print(f"\n💰 Cards with annual fees: {cards_with_fees}")
        
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE reward_rate IS NOT NULL")
        cards_with_rewards = cursor.fetchone()[0]
        print(f"🎁 Cards with reward rates: {cards_with_rewards}")
        
        # Check card_merchant_rewards table
        cursor.execute("SELECT COUNT(*) FROM card_merchant_rewards")
        merchant_rewards = cursor.fetchone()[0]
        print(f"🏪 Merchant rewards entries: {merchant_rewards}")
        
        # Check card_spending_categories table
        cursor.execute("SELECT COUNT(*) FROM card_spending_categories")
        spending_categories = cursor.fetchone()[0]
        print(f"📊 Spending categories entries: {spending_categories}")
        
        # Check if there's any detailed data
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE description IS NOT NULL AND description != ''")
        cards_with_description = cursor.fetchone()[0]
        print(f"📝 Cards with descriptions: {cards_with_description}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_database_content() 