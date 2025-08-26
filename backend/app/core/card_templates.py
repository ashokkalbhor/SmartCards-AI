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
            "category_name": "offline_spends",
            "category_display_name": "Offline Spends",
            "reward_rate": 0.0,
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
            "category_name": "education",
            "category_display_name": "Education",
            "reward_rate": 0.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "jewelry",
            "category_display_name": "Jewelry",
            "reward_rate": 0.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "government_payments",
            "category_display_name": "Govt. Payments",
            "reward_rate": 0.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "insurance",
            "category_display_name": "Insurance",
            "reward_rate": 0.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "rent",
            "category_display_name": "Rent",
            "reward_rate": 0.0,
            "reward_type": "points",
            "reward_cap": None,
            "reward_cap_period": None,
            "minimum_transaction_amount": None,
            "is_active": True,
            "additional_conditions": None
        },
        {
            "category_name": "wallets",
            "category_display_name": "Wallets",
            "reward_rate": 0.0,
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
    Generate default merchant rewards based on market research and actual market demand.
    These serve as editable templates for users.
    """
    # Import the merchant popularity service
    from app.core.merchant_popularity import merchant_popularity_service
    
    # Get merchants sorted by market research-based popularity
    sorted_merchant_names = merchant_popularity_service.get_sorted_merchants_by_popularity()
    
    # Create merchant templates based on market research ranking
    popular_merchants = []
    
    # Default reward rates by category (will be adjusted by card tier)
    default_reward_rates = {
        "ecommerce": 5.0,
        "food_delivery": 10.0,
        "transport": 5.0,
        "grocery": 5.0,
        "fashion": 5.0,
        "entertainment": 5.0,
        "digital_wallet": 2.0,
        "investments": 0.0
    }
    
    # Default reward caps by category
    default_reward_caps = {
        "ecommerce": 500,
        "food_delivery": 200,
        "transport": 200,
        "grocery": 300,
        "fashion": 300,
        "entertainment": 100,
        "digital_wallet": 100,
        "investments": None
    }
    
    # Create merchant templates based on market research ranking
    for rank, merchant_name in enumerate(sorted_merchant_names, 1):
        market_data = merchant_popularity_service.get_merchant_market_data(merchant_name)
        if market_data:
            popular_merchants.append({
                "merchant_name": merchant_name,
                "merchant_display_name": market_data.display_name,
                "merchant_category": market_data.category,
                "popularity_rank": rank,
                "reward_rate": default_reward_rates.get(market_data.category, 2.0),
                "reward_type": "cashback",
                "reward_cap": default_reward_caps.get(market_data.category),
                "reward_cap_period": "monthly" if default_reward_caps.get(market_data.category) else None,
                "minimum_transaction_amount": None,
                "is_active": True,
                "requires_registration": False,
                "additional_conditions": None
            })
    
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