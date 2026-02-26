#!/usr/bin/env python3
"""
Bank of Baroda (BOBCARD) Credit Cards Population Script
======================================================

This script populates the card_master_data table with Bank of Baroda's 
comprehensive credit card portfolio of 23+ cards covering all segments.

Features:
- Complete BOBCARD portfolio including premium, professional, defense, and co-branded cards
- Error handling and rollback capability
- Comprehensive verification and reporting
- Detailed success/failure logging

Usage:
    python run_bob_population.py
"""

import sqlite3
import os
import sys
from datetime import datetime

def get_database_path():
    """Get the path to the database"""
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, '..', 'smartcards_ai.db')

def get_db_connection():
    """Establish database connection with error handling."""
    try:
        db_path = get_database_path()
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def verify_existing_bob_cards(cursor):
    """Check for existing Bank of Baroda cards."""
    cursor.execute("""
        SELECT card_name, card_variant, card_tier
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda'
        ORDER BY card_name
    """)
    
    existing_cards = cursor.fetchall()
    if existing_cards:
        print("⚠️  Existing Bank of Baroda cards found:")
        for card in existing_cards:
            print(f"   • {card[0]} ({card[1]}) - {card[2]}")
        return True
    return False

def run_population_script(cursor, script_path):
    """Execute the SQL population script."""
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        cursor.executescript(sql_script)
        return True
        
    except FileNotFoundError:
        print(f"❌ SQL script not found: {script_path}")
        return False
    except Exception as e:
        print(f"❌ SQL execution error: {e}")
        return False

def verify_population_results(cursor):
    """Verify the population was successful and display results."""
    
    # Get total Bank of Baroda cards
    cursor.execute("""
        SELECT COUNT(*) FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda'
    """)
    total_cards = cursor.fetchone()[0]
    
    # Get cards by tier
    cursor.execute("""
        SELECT card_tier, COUNT(*) 
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda'
        GROUP BY card_tier 
        ORDER BY COUNT(*) DESC
    """)
    tier_breakdown = cursor.fetchall()
    
    # Get cards by category/variant
    cursor.execute("""
        SELECT card_variant, COUNT(*) 
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda'
        GROUP BY card_variant 
        ORDER BY COUNT(*) DESC
    """)
    variant_breakdown = cursor.fetchall()
    
    # Get lifetime free cards
    cursor.execute("""
        SELECT card_name, card_variant 
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda' 
        AND annual_fee = 0
        ORDER BY card_name
    """)
    free_cards = cursor.fetchall()
    
    # Get premium cards
    cursor.execute("""
        SELECT card_name, card_variant, annual_fee 
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda' 
        AND annual_fee >= 1000
        ORDER BY annual_fee DESC
    """)
    premium_cards = cursor.fetchall()
    
    # Display results
    print(f"\n✅ Bank of Baroda Cards Population Successful!")
    print(f"📊 Total Bank of Baroda Cards: {total_cards}")
    
    print(f"\n🎯 Cards by Tier:")
    for tier, count in tier_breakdown:
        print(f"   • {tier}: {count} cards")
    
    print(f"\n📋 Cards by Category:")
    for variant, count in variant_breakdown:
        print(f"   • {variant}: {count} card{'s' if count > 1 else ''}")
    
    print(f"\n🆓 Lifetime Free Cards ({len(free_cards)}):")
    for card_name, variant in free_cards:
        print(f"   • {card_name} ({variant})")
    
    print(f"\n💎 Premium Cards (₹1000+ annual fee) ({len(premium_cards)}):")
    for card_name, variant, fee in premium_cards:
        print(f"   • {card_name} ({variant}) - ₹{fee}")
    
    # Show special categories
    cursor.execute("""
        SELECT card_name, card_variant 
        FROM card_master_data 
        WHERE bank_name = 'Bank of Baroda' 
        AND (card_variant LIKE '%Defense%' OR card_variant LIKE '%Professional%')
        ORDER BY card_variant, card_name
    """)
    special_cards = cursor.fetchall()
    
    if special_cards:
        print(f"\n🎖️ Special Category Cards ({len(special_cards)}):")
        current_category = None
        for card_name, variant in special_cards:
            if variant != current_category:
                current_category = variant
                print(f"   {variant}:")
            print(f"     • {card_name}")
    
    return total_cards

def get_overall_database_stats(cursor):
    """Get overall database statistics."""
    cursor.execute("SELECT COUNT(*) FROM card_master_data")
    total_cards = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT bank_name, COUNT(*) 
        FROM card_master_data 
        GROUP BY bank_name 
        ORDER BY COUNT(*) DESC
    """)
    bank_breakdown = cursor.fetchall()
    
    print(f"\n📈 Overall Database Status:")
    print(f"   Total Cards in Database: {total_cards}")
    print(f"   Banks Covered: {len(bank_breakdown)}")
    print(f"\n🏦 All Banks:")
    for bank, count in bank_breakdown:
        print(f"   • {bank}: {count} cards")

def main():
    """Main execution function."""
    print("🚀 Starting Bank of Baroda Credit Cards Population...")
    print("=" * 60)
    
    # Get database connection
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check for existing cards
        print("🔍 Checking for existing Bank of Baroda cards...")
        has_existing = verify_existing_bob_cards(cursor)
        
        if has_existing:
            response = input("\nDo you want to continue and add more cards? (yes/no): ").lower()
            if response not in ['yes', 'y']:
                print("❌ Operation cancelled by user.")
                return False
            print("➡️  Proceeding with population...")
        
        # Execute population script
        script_path = os.path.join(os.path.dirname(__file__), 'populate_bob_cards.sql')
        print(f"\n📥 Executing population script: {script_path}")
        
        if not run_population_script(cursor, script_path):
            conn.rollback()
            return False
        
        # Verify results
        print("\n🔍 Verifying population results...")
        total_cards = verify_population_results(cursor)
        
        # Get overall stats
        get_overall_database_stats(cursor)
        
        # Commit transaction
        conn.commit()
        print(f"\n✅ Transaction committed successfully!")
        print(f"🎉 Bank of Baroda credit cards population completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 