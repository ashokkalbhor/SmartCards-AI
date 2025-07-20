#!/usr/bin/env python3
"""
Standard Chartered Bank Credit Cards Population Script
Populates 11 Standard Chartered Bank credit cards into the database
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
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'Standard Chartered Bank'")
        total_cards = cursor.fetchone()[0]
        
        print(f"✅ Successfully populated {total_cards} Standard Chartered Bank cards")
        
        # Get card breakdown
        cursor.execute("""
            SELECT card_tier, COUNT(*) 
            FROM card_master_data 
            WHERE bank_name = 'Standard Chartered Bank' 
            GROUP BY card_tier
        """)
        tier_breakdown = cursor.fetchall()
        
        print("\n📊 Card Tier Breakdown:")
        for tier, count in tier_breakdown:
            print(f"   • {tier}: {count} cards")
        
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
        
        # Check Standard Chartered Bank cards
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'Standard Chartered Bank'")
        sc_cards = cursor.fetchone()[0]
        
        if sc_cards > 0:
            print(f"\n✅ Verification: Found {sc_cards} Standard Chartered Bank cards in database")
            
            # Show sample cards
            cursor.execute("""
                SELECT card_name, card_tier, annual_fee, domestic_lounge_visits 
                FROM card_master_data 
                WHERE bank_name = 'Standard Chartered Bank' 
                ORDER BY annual_fee
                LIMIT 5
            """)
            sample_cards = cursor.fetchall()
            
            print("\n🎯 Sample Standard Chartered Cards:")
            for card_name, tier, annual_fee, lounge in sample_cards:
                print(f"   • {card_name} ({tier}) - Fee: ₹{annual_fee} - Lounge: {lounge}")
            
            # Show network distribution
            cursor.execute("""
                SELECT card_network, COUNT(*) 
                FROM card_master_data 
                WHERE bank_name = 'Standard Chartered Bank' 
                GROUP BY card_network
            """)
            networks = cursor.fetchall()
            
            print("\n🏦 Card Network Distribution:")
            for network, count in networks:
                print(f"   • {network}: {count} cards")
            
        else:
            print("❌ Verification failed: No Standard Chartered Bank cards found")
            
        conn.close()
        return sc_cards > 0
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        return False

def main():
    print("🚀 Standard Chartered Bank Credit Cards Population")
    print("=" * 55)
    
    # Get file paths
    current_dir = os.path.dirname(__file__)
    sql_file = os.path.join(current_dir, 'populate_standard_chartered_cards.sql')
    db_path = get_database_path()
    
    print(f"📁 SQL File: {sql_file}")
    print(f"🗄️ Database: {db_path}")
    
    # Check if SQL file exists
    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        return
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"\n⏰ Starting population at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Execute population script
    if execute_sql_script(db_path, sql_file):
        # Verify population
        if verify_population(db_path):
            print("\n🎉 Standard Chartered Bank population completed successfully!")
            print("📋 Summary: 11 credit cards covering all major categories")
            print("🌟 Range: Entry-level to Super-Premium cards")
            print("💳 Networks: Visa and Mastercard")
            print("🏆 Special Features: International banking expertise")
        else:
            print("\n⚠️ Population completed but verification failed")
    else:
        print("\n❌ Population failed")
    
    print(f"\n⏰ Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 