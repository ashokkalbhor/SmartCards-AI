#!/usr/bin/env python3
"""
IndusInd Bank Credit Cards Population Script
Populates 11 IndusInd Bank credit cards into the database
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
        cursor.execute("SELECT COUNT(*) FROM card_master_data WHERE bank_name = 'IndusInd Bank'")
        total_cards = cursor.fetchone()[0]
        
        conn.close()
        return True, total_cards
        
    except Exception as e:
        print(f"❌ Error executing SQL script: {str(e)}")
        return False, 0

def verify_population(db_path):
    """Verify the populated data"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get IndusInd Bank cards
        cursor.execute("""
            SELECT card_name, card_variant, card_tier, annual_fee 
            FROM card_master_data 
            WHERE bank_name = 'IndusInd Bank'
            ORDER BY annual_fee, joining_fee
        """)
        cards = cursor.fetchall()
        
        print("🎯 IndusInd Bank Cards Successfully Populated:")
        print("=" * 55)
        
        # Group by tier
        tiers = {'Standard': [], 'Premium': [], 'Super-Premium': []}
        for card in cards:
            card_name, variant, tier, annual_fee = card
            tier_key = 'Super-Premium' if tier == 'Super-Premium' else ('Premium' if tier == 'Premium' else 'Standard')
            tiers[tier_key].append((card_name, variant, annual_fee))
        
        for tier, card_list in tiers.items():
            if card_list:
                print(f"\n📊 {tier} Cards:")
                for card_name, variant, annual_fee in card_list:
                    fee_str = "Lifetime Free" if annual_fee == 0 else f"₹{annual_fee}/year"
                    print(f"  • {card_name} ({variant}) - {fee_str}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {str(e)}")
        return False

def main():
    print("🏦 IndusInd Bank Credit Cards Population")
    print("=" * 45)
    print(f"📅 Starting population: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get file paths
    current_dir = os.path.dirname(__file__)
    db_path = get_database_path()
    sql_file = os.path.join(current_dir, 'populate_indusind_cards.sql')
    
    # Check if files exist
    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        return
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"📁 Database: {db_path}")
    print(f"📄 SQL Script: {sql_file}")
    
    # Execute population
    print("\n🔄 Executing IndusInd Bank population script...")
    success, total_cards = execute_sql_script(db_path, sql_file)
    
    if success:
        print(f"✅ Successfully populated {total_cards} IndusInd Bank cards!")
        
        # Verify the data
        print("\n🔍 Verifying populated data...")
        if verify_population(db_path):
            print(f"\n🎉 IndusInd Bank Population Complete!")
            print("📈 Key Features:")
            print("  • 11 comprehensive credit cards")
            print("  • Complete tier coverage (Entry to Super-Premium)")
            print("  • 5 Lifetime-free cards")
            print("  • Premium travel and dining benefits")
            print("  • Innovative products (Interactive Nexxt Card, UPI RuPay)")
        else:
            print("⚠️  Data verification failed")
    else:
        print("❌ Population failed!")
    
    print(f"\n📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 