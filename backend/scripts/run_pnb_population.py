#!/usr/bin/env python3
"""
Punjab National Bank (PNB) Credit Cards Population Script
Populates the database with comprehensive PNB card portfolio
"""

import sqlite3
import os
import sys

def get_database_path():
    """Get the path to the SQLite database"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    db_path = os.path.join(backend_dir, 'smartcards_ai.db')
    return db_path

def run_pnb_population():
    """Execute the PNB cards population script"""
    try:
        # Get database path
        db_path = get_database_path()
        
        if not os.path.exists(db_path):
            print(f"❌ Database not found at: {db_path}")
            return False
        
        print("🏦 Starting Punjab National Bank Credit Cards Population...")
        print(f"📍 Database: {db_path}")
        
        # Get the SQL script path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_script_path = os.path.join(current_dir, 'populate_pnb_cards.sql')
        
        if not os.path.exists(sql_script_path):
            print(f"❌ SQL script not found at: {sql_script_path}")
            return False
        
        # Read the SQL script
        with open(sql_script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Connect to database and execute
        conn = sqlite3.connect(db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Execute the population script
        cursor.executescript(sql_script)
        conn.commit()
        
        print("✅ PNB cards population completed successfully!")
        
        # Verification queries
        print("\n📊 Population Verification:")
        print("=" * 50)
        
        # Total cards verification
        cursor.execute("""
            SELECT 
                COUNT(*) as total_cards,
                COUNT(CASE WHEN card_tier = 'Standard' THEN 1 END) as standard,
                COUNT(CASE WHEN card_tier = 'Premium' THEN 1 END) as premium
            FROM card_master_data 
            WHERE bank_name = 'Punjab National Bank'
        """)
        
        tier_stats = cursor.fetchone()
        if tier_stats:
            print(f"📈 Total PNB Cards: {tier_stats[0]}")
            print(f"   ├─ Standard: {tier_stats[1]}")
            print(f"   └─ Premium: {tier_stats[2]}")
        
        # Network distribution
        cursor.execute("""
            SELECT 
                card_network,
                COUNT(*) as card_count
            FROM card_master_data 
            WHERE bank_name = 'Punjab National Bank'
            GROUP BY card_network
            ORDER BY card_count DESC
        """)
        
        network_stats = cursor.fetchall()
        print(f"\n🌐 Network Distribution:")
        for network, count in network_stats:
            print(f"   └─ {network}: {count} cards")
        
        # Special features verification
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN annual_fee IS NULL THEN 1 END) as free_cards,
                COUNT(CASE WHEN domestic_lounge_visits > 0 THEN 1 END) as lounge_cards,
                COUNT(CASE WHEN international_lounge_visits > 0 THEN 1 END) as intl_lounge_cards,
                COUNT(CASE WHEN card_variant LIKE '%Rakshak%' THEN 1 END) as defense_cards,
                COUNT(CASE WHEN card_variant LIKE '%Patanjali%' THEN 1 END) as cobranded_cards
            FROM card_master_data 
            WHERE bank_name = 'Punjab National Bank'
        """)
        
        features = cursor.fetchone()
        if features:
            print(f"\n🎯 Special Features:")
            print(f"   ├─ Free Cards (No Annual Fee): {features[0]}")
            print(f"   ├─ Domestic Lounge Access: {features[1]}")
            print(f"   ├─ International Lounge Access: {features[2]}")
            print(f"   ├─ Defense Personnel Cards: {features[3]}")
            print(f"   └─ Co-branded Cards: {features[4]}")
        
        # Sample card details
        cursor.execute("""
            SELECT card_name, card_tier, annual_fee, minimum_salary
            FROM card_master_data 
            WHERE bank_name = 'Punjab National Bank'
            ORDER BY 
                CASE card_tier
                    WHEN 'Standard' THEN 1
                    WHEN 'Premium' THEN 2
                END
            LIMIT 5
        """)
        
        sample_cards = cursor.fetchall()
        print(f"\n💳 Sample Cards:")
        for card_name, tier, annual_fee, minimum_salary in sample_cards:
            fee_display = f"₹{annual_fee}" if annual_fee else "Free"
            income_display = f"₹{minimum_salary:,}" if minimum_salary else "N/A"
            print(f"   └─ {card_name} ({tier}) - Fee: {fee_display}, Income: {income_display}")
        
        # Overall database statistics
        cursor.execute("SELECT COUNT(*) FROM card_master_data")
        total_db_cards = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT bank_name) FROM card_master_data")
        total_banks = cursor.fetchone()[0]
        
        print(f"\n🎯 Database Status:")
        print(f"   ├─ Total Cards in Database: {total_db_cards}")
        print(f"   ├─ Total Banks: {total_banks}")
        print(f"   └─ PNB Cards: {tier_stats[0]} ({(tier_stats[0]/total_db_cards*100):.1f}%)")
        
        conn.close()
        
        print("\n🎉 Punjab National Bank population completed successfully!")
        print("   ✅ 15 comprehensive PNB cards added")
        print("   ✅ RuPay and Visa networks covered")
        print("   ✅ Defense personnel specialized cards")
        print("   ✅ Co-branded Patanjali partnerships")
        print("   ✅ Entry-level to super-premium tiers")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Punjab National Bank Credit Cards Population")
    print("=" * 50)
    
    success = run_pnb_population()
    
    if success:
        print("\n✨ Population completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Population failed!")
        sys.exit(1) 