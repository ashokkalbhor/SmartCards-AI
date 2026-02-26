"""
Script to seed the database with sample card master data for comparison.
This populates the card_master_data, card_spending_categories, and card_merchant_rewards tables.
"""

import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward, CardTierEnum


def create_sample_card_data():
    """Create sample card master data"""
    
    db: Session = SessionLocal()
    
    try:
        # Sample card data based on your comparison image
        sample_cards = [
            {
                "bank_name": "SBI",
                "card_name": "Cashback Card",
                "card_network": "Visa",
                "card_tier": CardTierEnum.BASIC,
                "joining_fee": 999,
                "annual_fee": 999,
                "annual_fee_waiver_spend": 200000,
                "is_active": True,
                "reward_program_name": "SBI Reward Points",
                "categories": [
                    {"category_name": "offline_spends", "category_display_name": "Offline Spends", "reward_rate": 1.0},
                    {"category_name": "online_spends", "category_display_name": "Online Spends", "reward_rate": 5.0},
                ],
                "merchants": [
                    {"merchant_name": "amazon", "merchant_display_name": "Amazon", "reward_rate": 5.0},
                    {"merchant_name": "bigbasket", "merchant_display_name": "BigBasket", "reward_rate": 5.0},
                    {"merchant_name": "flipkart", "merchant_display_name": "Flipkart", "reward_rate": 5.0},
                    {"merchant_name": "myntra", "merchant_display_name": "Myntra", "reward_rate": 5.0},
                    {"merchant_name": "ola", "merchant_display_name": "Ola", "reward_rate": 5.0},
                    {"merchant_name": "swiggy", "merchant_display_name": "Swiggy", "reward_rate": 5.0},
                    {"merchant_name": "rapido", "merchant_display_name": "Rapido", "reward_rate": 5.0},
                    {"merchant_name": "uber", "merchant_display_name": "Uber", "reward_rate": 5.0},
                    {"merchant_name": "zomato", "merchant_display_name": "Zomato", "reward_rate": 5.0},
                    {"merchant_name": "nps", "merchant_display_name": "NPS", "reward_rate": 5.0},
                ]
            },
            {
                "bank_name": "HDFC",
                "card_name": "Swiggy Card",
                "card_network": "Visa",
                "card_tier": CardTierEnum.PREMIUM,
                "joining_fee": 500,
                "is_lifetime_free": True,
                "annual_fee_waiver_spend": 200000,
                "is_active": True,
                "reward_program_name": "HDFC Reward Points",
                "categories": [
                    {"category_name": "education", "category_display_name": "Education", "reward_rate": 1.0},
                    {"category_name": "offline_spends", "category_display_name": "Offline Spends", "reward_rate": 1.0},
                    {"category_name": "online_spends", "category_display_name": "Online Spends", "reward_rate": 5.0},
                    {"category_name": "utilities", "category_display_name": "Utilities", "reward_rate": 1.0},
                ],
                "merchants": [
                    {"merchant_name": "amazon", "merchant_display_name": "Amazon", "reward_rate": 1.0},
                    {"merchant_name": "bigbasket", "merchant_display_name": "BigBasket", "reward_rate": 1.0},
                    {"merchant_name": "flipkart", "merchant_display_name": "Flipkart", "reward_rate": 5.0},
                    {"merchant_name": "myntra", "merchant_display_name": "Myntra", "reward_rate": 5.0},
                    {"merchant_name": "ola", "merchant_display_name": "Ola", "reward_rate": 5.0},
                    {"merchant_name": "swiggy", "merchant_display_name": "Swiggy", "reward_rate": 10.0},
                    {"merchant_name": "rapido", "merchant_display_name": "Rapido", "reward_rate": 1.0},
                    {"merchant_name": "uber", "merchant_display_name": "Uber", "reward_rate": 5.0},
                    {"merchant_name": "zomato", "merchant_display_name": "Zomato", "reward_rate": 1.0},
                    {"merchant_name": "nps", "merchant_display_name": "NPS", "reward_rate": 1.0},
                ]
            },
            {
                "bank_name": "Axis",
                "card_name": "Ace Card",
                "card_network": "Visa",
                "card_tier": CardTierEnum.PREMIUM,
                "joining_fee": 499,
                "annual_fee": 499,
                "annual_fee_waiver_spend": 200000,
                "domestic_lounge_visits": 4,
                "lounge_spend_requirement": 50000,
                "lounge_spend_period": "quarterly",
                "is_active": True,
                "reward_program_name": "EDGE Reward Points",
                "categories": [
                    {"category_name": "insurance", "category_display_name": "Insurance", "reward_rate": 1.0},
                    {"category_name": "offline_spends", "category_display_name": "Offline Spends", "reward_rate": 1.5},
                    {"category_name": "online_spends", "category_display_name": "Online Spends", "reward_rate": 1.5},
                    {"category_name": "utilities", "category_display_name": "Utilities", "reward_rate": 4.0},
                ],
                "merchants": [
                    {"merchant_name": "amazon", "merchant_display_name": "Amazon", "reward_rate": 1.5},
                    {"merchant_name": "bigbasket", "merchant_display_name": "BigBasket", "reward_rate": 1.5},
                    {"merchant_name": "flipkart", "merchant_display_name": "Flipkart", "reward_rate": 1.5},
                    {"merchant_name": "myntra", "merchant_display_name": "Myntra", "reward_rate": 1.5},
                    {"merchant_name": "ola", "merchant_display_name": "Ola", "reward_rate": 4.0},
                    {"merchant_name": "swiggy", "merchant_display_name": "Swiggy", "reward_rate": 4.0},
                    {"merchant_name": "rapido", "merchant_display_name": "Rapido", "reward_rate": 1.5},
                    {"merchant_name": "uber", "merchant_display_name": "Uber", "reward_rate": 1.5},
                    {"merchant_name": "zomato", "merchant_display_name": "Zomato", "reward_rate": 4.0},
                    {"merchant_name": "nps", "merchant_display_name": "NPS", "reward_rate": 1.5},
                ]
            },
            {
                "bank_name": "HDFC",
                "card_name": "Millennia Card",
                "card_network": "Visa",
                "card_tier": CardTierEnum.PREMIUM,
                "joining_fee": 1000,
                "is_lifetime_free": True,
                "annual_fee_waiver_spend": 100000,
                "domestic_lounge_visits": 4,
                "lounge_spend_requirement": 25000,
                "lounge_spend_period": "quarterly",
                "is_active": True,
                "reward_program_name": "HDFC Reward Points",
                "categories": [
                    {"category_name": "education", "category_display_name": "Education", "reward_rate": 1.0},
                    {"category_name": "jewelry", "category_display_name": "Jewelry", "reward_rate": 1.0},
                    {"category_name": "insurance", "category_display_name": "Insurance", "reward_rate": 1.0},
                    {"category_name": "offline_spends", "category_display_name": "Offline Spends", "reward_rate": 1.0},
                    {"category_name": "online_spends", "category_display_name": "Online Spends", "reward_rate": 1.0},
                    {"category_name": "utilities", "category_display_name": "Utilities", "reward_rate": 1.0},
                ],
                "merchants": [
                    {"merchant_name": "amazon", "merchant_display_name": "Amazon", "reward_rate": 5.0},
                    {"merchant_name": "bigbasket", "merchant_display_name": "BigBasket", "reward_rate": 5.0},
                    {"merchant_name": "flipkart", "merchant_display_name": "Flipkart", "reward_rate": 5.0},
                    {"merchant_name": "myntra", "merchant_display_name": "Myntra", "reward_rate": 5.0},
                    {"merchant_name": "ola", "merchant_display_name": "Ola", "reward_rate": 1.0},
                    {"merchant_name": "swiggy", "merchant_display_name": "Swiggy", "reward_rate": 5.0},
                    {"merchant_name": "rapido", "merchant_display_name": "Rapido", "reward_rate": 1.0},
                    {"merchant_name": "uber", "merchant_display_name": "Uber", "reward_rate": 5.0},
                    {"merchant_name": "zomato", "merchant_display_name": "Zomato", "reward_rate": 5.0},
                    {"merchant_name": "nps", "merchant_display_name": "NPS", "reward_rate": 1.0},
                ]
            },
            {
                "bank_name": "ICICI",
                "card_name": "Amazon Pay Card",
                "card_network": "Visa",
                "card_tier": CardTierEnum.BASIC,
                "is_lifetime_free": True,
                "is_active": True,
                "reward_program_name": "Amazon Pay Rewards",
                "categories": [
                    {"category_name": "education", "category_display_name": "Education", "reward_rate": 1.0},
                    {"category_name": "jewelry", "category_display_name": "Jewelry", "reward_rate": 1.0},
                    {"category_name": "insurance", "category_display_name": "Insurance", "reward_rate": 2.0},
                    {"category_name": "offline_spends", "category_display_name": "Offline Spends", "reward_rate": 1.0},
                    {"category_name": "online_spends", "category_display_name": "Online Spends", "reward_rate": 1.0},
                    {"category_name": "utilities", "category_display_name": "Utilities", "reward_rate": 2.0},
                    {"category_name": "wallets", "category_display_name": "Wallets", "reward_rate": 1.0},
                ],
                "merchants": [
                    {"merchant_name": "amazon", "merchant_display_name": "Amazon", "reward_rate": 5.0},
                    {"merchant_name": "bigbasket", "merchant_display_name": "BigBasket", "reward_rate": 2.0},
                    {"merchant_name": "flipkart", "merchant_display_name": "Flipkart", "reward_rate": 1.0},
                    {"merchant_name": "myntra", "merchant_display_name": "Myntra", "reward_rate": 1.0},
                    {"merchant_name": "ola", "merchant_display_name": "Ola", "reward_rate": 1.0},
                    {"merchant_name": "swiggy", "merchant_display_name": "Swiggy", "reward_rate": 1.0},
                    {"merchant_name": "rapido", "merchant_display_name": "Rapido", "reward_rate": 1.0},
                    {"merchant_name": "uber", "merchant_display_name": "Uber", "reward_rate": 1.0},
                    {"merchant_name": "zomato", "merchant_display_name": "Zomato", "reward_rate": 1.0},
                    {"merchant_name": "nps", "merchant_display_name": "NPS", "reward_rate": 1.0},
                ]
            }
        ]
        
        print("🚀 Starting card master data seeding...")
        
        for card_info in sample_cards:
            # Check if card already exists
            existing_card = db.query(CardMasterData).filter_by(
                bank_name=card_info["bank_name"],
                card_name=card_info["card_name"]
            ).first()
            
            if existing_card:
                print(f"⏭️  Card {card_info['bank_name']} {card_info['card_name']} already exists, skipping...")
                continue
            
            # Create card master data
            categories_data = card_info.pop("categories", [])
            merchants_data = card_info.pop("merchants", [])
            
            card = CardMasterData(**card_info)
            db.add(card)
            db.flush()  # Get the ID
            
            print(f"✅ Created card: {card.bank_name} {card.card_name}")
            
            # Add spending categories
            for category_info in categories_data:
                category = CardSpendingCategory(
                    card_master_id=card.id,
                    **category_info
                )
                db.add(category)
            
            # Add merchant rewards
            for merchant_info in merchants_data:
                merchant = CardMerchantReward(
                    card_master_id=card.id,
                    **merchant_info
                )
                db.add(merchant)
            
            print(f"   📂 Added {len(categories_data)} categories and {len(merchants_data)} merchants")
        
        db.commit()
        print("\n🎉 Card master data seeding completed successfully!")
        print(f"📊 Total cards created: {len(sample_cards)}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_card_data() 