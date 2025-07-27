#!/usr/bin/env python3
"""
Script to check if AU IXIGO Credit Card exists in the database
"""

import requests

def check_au_ixigo_card():
    """Check if AU IXIGO Credit Card exists in the database"""
    
    try:
        # Get all AU Small Finance Bank cards
        response = requests.get('http://localhost:8000/api/v1/card-master-data/cards?bank_name=AU%20Small%20Finance%20Bank')
        
        if response.status_code == 200:
            cards = response.json()
            
            # Look for IXIGO cards
            ixigo_cards = [card for card in cards if 'IXIGO' in card['card_name']]
            
            print(f"Found {len(ixigo_cards)} IXIGO cards:")
            for card in ixigo_cards:
                print(f"- {card['card_name']}")
                print(f"  Variant: {card['card_variant']}")
                print(f"  Network: {card['card_network']}")
                print(f"  Annual Fee: ₹{card['annual_fee']}")
                print(f"  Description: {card['description']}")
                print()
            
            if not ixigo_cards:
                print("❌ No AU IXIGO cards found in the database.")
                print("Total AU Small Finance Bank cards found:", len(cards))
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error checking for AU IXIGO card: {e}")

if __name__ == "__main__":
    check_au_ixigo_card() 