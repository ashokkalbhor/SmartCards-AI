#!/usr/bin/env python3
"""
Script to add AU IXIGO Credit Card to the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models.card_master_data import CardMasterData
from sqlalchemy.orm import sessionmaker

def add_au_ixigo_card():
    """Add AU IXIGO Credit Card to the database"""
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if the card already exists
        existing_card = session.query(CardMasterData).filter(
            CardMasterData.bank_name == 'AU Small Finance Bank',
            CardMasterData.card_name == 'AU Bank IXIGO Credit Card'
        ).first()
        
        if existing_card:
            print("AU Bank IXIGO Credit Card already exists in the database.")
            return
        
        # Create the AU IXIGO card
        au_ixigo_card = CardMasterData(
            bank_name='AU Small Finance Bank',
            card_name='AU Bank IXIGO Credit Card',
            card_variant='Co-branded Travel',
            card_network='Visa',
            card_tier='Standard',
            joining_fee=999,
            annual_fee=999,
            minimum_salary=400000,
            minimum_age=21,
            maximum_age=70,
            domestic_lounge_visits=2,
            international_lounge_visits=2,
            contactless_enabled=True,
            minimum_credit_limit=40000,
            maximum_credit_limit=800000,
            foreign_transaction_fee=3.5,
            description='Travel-focused co-branded card with IXIGO booking benefits, travel insurance, and reward points on travel spends',
            is_active=True
        )
        
        session.add(au_ixigo_card)
        session.commit()
        
        print("✅ AU Bank IXIGO Credit Card successfully added to the database!")
        
    except Exception as e:
        print(f"❌ Error adding AU IXIGO card: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    add_au_ixigo_card() 