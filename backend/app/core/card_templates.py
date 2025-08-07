#!/usr/bin/env python3
"""
Card Templates for User-Generated Content
Provides default templates for spending categories and merchant rewards
that users can edit and customize.
"""

from typing import List, Dict, Any
from app.models.card_master_data import CardSpendingCategory, CardMerchantReward

def get_default_spending_categories(card_tier: str, bank_name: str) -> List[Dict[str, Any]]:
    """
    Generate default spending categories based on card tier and bank.
    These serve as editable templates for users.
    """
    base_categories = {
        "basic": [
            {
                "category_name": "general",
                "category_display_name": "General Spends",
                "reward_rate": 1.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "fuel",
                "category_display_name": "Fuel",
                "reward_rate": 1.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ],
        "premium": [
            {
                "category_name": "general",
                "category_display_name": "General Spends",
                "reward_rate": 2.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "dining",
                "category_display_name": "Dining",
                "reward_rate": 3.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "fuel",
                "category_display_name": "Fuel",
                "reward_rate": 2.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "groceries",
                "category_display_name": "Groceries",
                "reward_rate": 2.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ],
        "super_premium": [
            {
                "category_name": "general",
                "category_display_name": "General Spends",
                "reward_rate": 3.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "dining",
                "category_display_name": "Dining",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "entertainment",
                "category_display_name": "Entertainment",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "fuel",
                "category_display_name": "Fuel",
                "reward_rate": 3.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "category_name": "groceries",
                "category_display_name": "Groceries",
                "reward_rate": 3.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ]
    }
    
    return base_categories.get(card_tier.lower(), base_categories["basic"])

def get_default_merchant_rewards(card_tier: str, bank_name: str) -> List[Dict[str, Any]]:
    """
    Generate default merchant rewards based on card tier and bank.
    These serve as editable templates for users.
    """
    base_merchants = {
        "basic": [
            {
                "merchant_name": "amazon",
                "merchant_display_name": "Amazon",
                "merchant_category": "e-commerce",
                "reward_rate": 2.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "flipkart",
                "merchant_display_name": "Flipkart",
                "merchant_category": "e-commerce",
                "reward_rate": 2.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ],
        "premium": [
            {
                "merchant_name": "amazon",
                "merchant_display_name": "Amazon",
                "merchant_category": "e-commerce",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "flipkart",
                "merchant_display_name": "Flipkart",
                "merchant_category": "e-commerce",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "bookmyshow",
                "merchant_display_name": "BookMyShow",
                "merchant_category": "entertainment",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "zomato",
                "merchant_display_name": "Zomato",
                "merchant_category": "food_delivery",
                "reward_rate": 3.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ],
        "super_premium": [
            {
                "merchant_name": "amazon",
                "merchant_display_name": "Amazon",
                "merchant_category": "e-commerce",
                "reward_rate": 10.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "flipkart",
                "merchant_display_name": "Flipkart",
                "merchant_category": "e-commerce",
                "reward_rate": 10.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "bookmyshow",
                "merchant_display_name": "BookMyShow",
                "merchant_category": "entertainment",
                "reward_rate": 10.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "pvr_cinemas",
                "merchant_display_name": "PVR Cinemas",
                "merchant_category": "entertainment",
                "reward_rate": 10.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            },
            {
                "merchant_name": "zomato",
                "merchant_display_name": "Zomato",
                "merchant_category": "food_delivery",
                "reward_rate": 5.0,
                "reward_type": "points",
                "reward_cap": None,
                "reward_cap_period": None,
                "is_active": True
            }
        ]
    }
    
    return base_merchants.get(card_tier.lower(), base_merchants["basic"])

def create_default_spending_categories_for_card(card_master_id: int, card_tier: str, bank_name: str, db) -> List[CardSpendingCategory]:
    """
    Create default spending categories for a card that users can edit.
    """
    default_categories = get_default_spending_categories(card_tier, bank_name)
    categories = []
    
    for cat_data in default_categories:
        category = CardSpendingCategory(
            card_master_id=card_master_id,
            category_name=cat_data["category_name"],
            category_display_name=cat_data["category_display_name"],
            reward_rate=cat_data["reward_rate"],
            reward_type=cat_data["reward_type"],
            reward_cap=cat_data["reward_cap"],
            reward_cap_period=cat_data["reward_cap_period"],
            is_active=cat_data["is_active"]
        )
        db.add(category)
        categories.append(category)
    
    db.commit()
    return categories

def create_default_merchant_rewards_for_card(card_master_id: int, card_tier: str, bank_name: str, db) -> List[CardMerchantReward]:
    """
    Create default merchant rewards for a card that users can edit.
    """
    default_merchants = get_default_merchant_rewards(card_tier, bank_name)
    merchants = []
    
    for merchant_data in default_merchants:
        merchant = CardMerchantReward(
            card_master_id=card_master_id,
            merchant_name=merchant_data["merchant_name"],
            merchant_display_name=merchant_data["merchant_display_name"],
            merchant_category=merchant_data["merchant_category"],
            reward_rate=merchant_data["reward_rate"],
            reward_type=merchant_data["reward_type"],
            reward_cap=merchant_data["reward_cap"],
            reward_cap_period=merchant_data["reward_cap_period"],
            is_active=merchant_data["is_active"]
        )
        db.add(merchant)
        merchants.append(merchant)
    
    db.commit()
    return merchants 