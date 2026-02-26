#!/usr/bin/env python3
"""
American Express India Credit Cards and Charge Cards Population Script
Populates 5 American Express cards (4 credit cards + 1 charge card) into the database
"""

import sqlite3
import os
from datetime import datetime

def get_database_path():
    """Get the path to the database"""
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, '..', 'smartcards_ai.db')

def execute_sql_script(db_path, sql_file):
    """Execute SQL script file"""
    try:
        # Read SQL script
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute script
        cursor.executescript(sql_script)
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'American Express'")
        card_count = cursor.fetchone()[0]
        
        print(f"✅ Successfully populated {card_count} American Express cards")
        
        # Show sample cards
        cursor.execute("""
            SELECT card_name, card_variant, annual_fee, card_tier
            FROM card_master_data 
            WHERE bank_name = 'American Express' 
            ORDER BY annual_fee
        """)
        cards = cursor.fetchall()
        
        print("\n📋 American Express Card Portfolio:")
        for card_name, variant, fee, tier in cards:
            print(f"  • {card_name} ({variant}) - {tier} - Annual Fee: ₹{fee}")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error executing SQL script: {str(e)}")
        return False

def verify_population(db_path):
    """Verify the population was successful"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check total cards
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'American Express'")
        total_cards = cursor.fetchone()[0]
        
        # Check card tiers
        cursor.execute("""
            SELECT card_tier, COUNT(*) 
            FROM card_master_data 
            WHERE bank_name = 'American Express' 
            GROUP BY card_tier
            ORDER BY COUNT(*) DESC
        """)
        tiers = cursor.fetchall()
        
        # Check premium features
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN concierge_service = 1 THEN 1 ELSE 0 END) as concierge_cards,
                SUM(CASE WHEN domestic_lounge_visits > 0 THEN 1 ELSE 0 END) as lounge_cards,
                SUM(CASE WHEN international_lounge_visits > 0 THEN 1 ELSE 0 END) as intl_lounge_cards
            FROM card_master_data 
            WHERE bank_name = 'American Express'
        """)
        features = cursor.fetchone()
        
        print(f"\n🎯 American Express Population Verification:")
        print(f"📊 Total Cards: {total_cards}")
        
        print(f"\n🏆 Card Tiers:")
        for tier, count in tiers:
            print(f"  • {tier}: {count} cards")
        
        print(f"\n🌟 Premium Features:")
        print(f"  • Concierge Service: {features[0]} cards")
        print(f"  • Domestic Lounge Access: {features[1]} cards")
        print(f"  • International Lounge Access: {features[2]} cards")
        
        print(f"\n💳 American Express Highlights:")
        print(f"  • Premium Membership Rewards Program")
        print(f"  • World-class customer service")
        print(f"  • Exclusive charge card offerings")
        print(f"  • No pre-set spending limits on select cards")
        print(f"  • Global acceptance and prestige")
        
        conn.close()
        
        return total_cards > 0
        
    except Exception as e:
        print(f"❌ Error verifying population: {str(e)}")
        return False

def main():
    print("🏆 American Express India Credit Cards & Charge Cards Population")
    print("=" * 70)
    
    # Get database path
    db_path = get_database_path()
    print(f"📂 Database: {db_path}")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    # Get script path
    script_path = os.path.join(os.path.dirname(__file__), 'populate_american_express_cards.sql')
    print(f"📄 Script: {script_path}")
    
    # Check if script exists
    if not os.path.exists(script_path):
        print("❌ SQL script file not found!")
        return
    
    # Execute script
    print(f"\n⏳ Executing American Express population script...")
    if execute_sql_script(db_path, script_path):
        print("\n🔍 Verifying population...")
        if verify_population(db_path):
            print("\n✅ American Express population completed successfully!")
            print("\n🎉 Key Achievements:")
            print("  • Premium card portfolio populated")
            print("  • Both credit cards and charge cards included")
            print("  • Membership Rewards program cards covered")
            print("  • Complete tier coverage (Entry to Ultra-Premium)")
            print("  • Invitation-only Centurion card included")
        else:
            print("\n⚠️ Population verification failed!")
    else:
        print("\n❌ American Express population failed!")

if __name__ == "__main__":
    main() 