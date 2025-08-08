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
    # Standard spending categories ordered by relevance
    standard_categories = [
        {
            "category_name": "general",
            "category_display_name": "General Spends",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "dining",
            "category_display_name": "Dining & Restaurants",
            "reward_rate": 2.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "fuel",
            "category_display_name": "Fuel & Petrol",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "groceries",
            "category_display_name": "Groceries & Supermarkets",
            "reward_rate": 2.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "online_shopping",
            "category_display_name": "Online Shopping",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "entertainment",
            "category_display_name": "Entertainment & Movies",
            "reward_rate": 2.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "travel",
            "category_display_name": "Travel & Hotels",
            "reward_rate": 3.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "utilities",
            "category_display_name": "Utility Bills",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "healthcare",
            "category_display_name": "Healthcare & Pharmacy",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "education",
            "category_display_name": "Education & Books",
            "reward_rate": 1.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        }
    ]
    
    # Adjust rates based on card tier
    if card_tier == "premium":
        for category in standard_categories:
            if category["reward_rate"] < 3.0:
                category["reward_rate"] += 0.5
    elif card_tier == "super_premium":
        for category in standard_categories:
            if category["reward_rate"] < 4.0:
                category["reward_rate"] += 1.0
    elif card_tier == "elite":
        for category in standard_categories:
            if category["reward_rate"] < 5.0:
                category["reward_rate"] += 1.5
    
    return standard_categories

def get_default_merchant_rewards(card_tier: str, bank_name: str) -> List[Dict[str, Any]]:
    """
    Generate default merchant rewards based on Indian popularity ranking.
    These serve as editable templates for users.
    """
    # Indian merchants ordered by popularity (based on research and usage)
    popular_merchants = [
        # Tier 1: Most Popular (E-commerce & Food Delivery)
        {
            "merchant_name": "amazon",
            "merchant_display_name": "Amazon",
            "merchant_category": "ecommerce",
            "popularity_rank": 1,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "flipkart",
            "merchant_display_name": "Flipkart",
            "merchant_category": "ecommerce",
            "popularity_rank": 2,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "swiggy",
            "merchant_display_name": "Swiggy",
            "merchant_category": "food_delivery",
            "popularity_rank": 3,
            "reward_rate": 10.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "zomato",
            "merchant_display_name": "Zomato",
            "merchant_category": "food_delivery",
            "popularity_rank": 4,
            "reward_rate": 10.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        
        # Tier 2: Entertainment & Transport
        {
            "merchant_name": "bookmyshow",
            "merchant_display_name": "BookMyShow",
            "merchant_category": "entertainment",
            "popularity_rank": 5,
            "reward_rate": 10.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "uber",
            "merchant_display_name": "Uber",
            "merchant_category": "transport",
            "popularity_rank": 6,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "ola",
            "merchant_display_name": "Ola",
            "merchant_category": "transport",
            "popularity_rank": 7,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        
        # Tier 3: Grocery & Fashion
        {
            "merchant_name": "bigbasket",
            "merchant_display_name": "BigBasket",
            "merchant_category": "grocery",
            "popularity_rank": 8,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 300,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "myntra",
            "merchant_display_name": "Myntra",
            "merchant_category": "fashion",
            "popularity_rank": 9,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 300,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "ajio",
            "merchant_display_name": "AJIO",
            "merchant_category": "fashion",
            "popularity_rank": 10,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 300,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        
        # Tier 4: Digital Wallets & Streaming
        {
            "merchant_name": "paytm",
            "merchant_display_name": "Paytm",
            "merchant_category": "digital_wallet",
            "popularity_rank": 11,
            "reward_rate": 2.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "phonepe",
            "merchant_display_name": "PhonePe",
            "merchant_category": "digital_wallet",
            "popularity_rank": 12,
            "reward_rate": 2.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "google_pay",
            "merchant_display_name": "Google Pay",
            "merchant_category": "digital_wallet",
            "popularity_rank": 13,
            "reward_rate": 2.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "netflix",
            "merchant_display_name": "Netflix",
            "merchant_category": "entertainment",
            "popularity_rank": 14,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        
        # Tier 5: Additional Popular Services
        {
            "merchant_name": "grofers",
            "merchant_display_name": "Grofers",
            "merchant_category": "grocery",
            "popularity_rank": 15,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 300,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "dunzo",
            "merchant_display_name": "Dunzo",
            "merchant_category": "delivery",
            "popularity_rank": 16,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 200,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "hotstar",
            "merchant_display_name": "Disney+ Hotstar",
            "merchant_category": "entertainment",
            "popularity_rank": 17,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        },
        {
            "merchant_name": "prime_video",
            "merchant_display_name": "Amazon Prime Video",
            "merchant_category": "entertainment",
            "popularity_rank": 18,
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 100,
            "reward_cap_period": "monthly",
            "minimum_transaction_amount": None,
            "is_active": True,
            "requires_registration": False,
            "additional_conditions": None
        }
    ]
    
    # Adjust rates based on card tier
    if card_tier == "premium":
        for merchant in popular_merchants:
            if merchant["reward_rate"] < 8.0:
                merchant["reward_rate"] += 1.0
    elif card_tier == "super_premium":
        for merchant in popular_merchants:
            if merchant["reward_rate"] < 10.0:
                merchant["reward_rate"] += 2.0
    elif card_tier == "elite":
        for merchant in popular_merchants:
            if merchant["reward_rate"] < 12.0:
                merchant["reward_rate"] += 3.0
    
    return popular_merchants

def create_default_spending_categories_for_card(card_id: int, card_tier: str, bank_name: str) -> List[Dict[str, Any]]:
    """
    Create default spending categories for a specific card.
    Returns a list of category dictionaries that can be used to create CardSpendingCategory objects.
    """
    categories = get_default_spending_categories(card_tier, bank_name)
    
    # Add card_master_id to each category
    for category in categories:
        category["card_master_id"] = card_id
        category["reward_display"] = f"{category['reward_rate']}% {category['reward_type']}"
    
    return categories

def create_default_merchant_rewards_for_card(card_id: int, card_tier: str, bank_name: str) -> List[Dict[str, Any]]:
    """
    Create default merchant rewards for a specific card.
    Returns a list of merchant reward dictionaries that can be used to create CardMerchantReward objects.
    """
    merchants = get_default_merchant_rewards(card_tier, bank_name)
    
    # Add card_master_id to each merchant
    for merchant in merchants:
        merchant["card_master_id"] = card_id
        merchant["reward_display"] = f"{merchant['reward_rate']}% {merchant['reward_type']}"
    
    return merchants 