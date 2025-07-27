"""
Merchant service for handling merchant lookups and recommendations
"""

import logging
from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.models.merchant import Merchant
from app.models.credit_card import CreditCard
from app.models.card_master_data import CardMasterData, CardMerchantReward
from app.core.cache import CacheManager

logger = logging.getLogger(__name__)

class MerchantService:
    def __init__(self):
        self.cache = CacheManager()
        self.category_patterns = {
            "online_shopping": ["amazon", "flipkart", "myntra", "nykaa", "ajio", "snapdeal"],
            "dining": ["swiggy", "zomato", "dunzo"],
            "travel": ["uber", "ola", "makemytrip", "goibibo", "booking.com"],
            "fuel": ["reliance", "hp", "bp", "shell", "indian oil"],
            "entertainment": ["netflix", "prime", "hotstar", "bookmyshow"],
            "groceries": ["bigbasket", "grofers", "zepto", "blinkit"],
            "utilities": ["airtel", "jio", "vodafone", "bsnl"],
            "healthcare": ["pharmeasy", "1mg", "netmeds", "apollo"],
            "education": ["coursera", "udemy", "byju's", "unacademy"],
            "gaming": ["steam", "epic games", "playstation", "xbox"]
        }
    
    async def get_merchant_category(self, merchant_name: str, db: AsyncSession) -> Optional[str]:
        """Get merchant category from database"""
        try:
            # Check cache first
            cache_key = f"merchant_category:{merchant_name.lower()}"
            cached_category = await self.cache.get(cache_key)
            if cached_category:
                return cached_category
            
            # Query database
            result = await db.execute(
                select(Merchant.category)
                .where(Merchant.merchant_name.ilike(f"%{merchant_name}%"))
                .where(Merchant.is_active == True)
            )
            
            merchant = result.scalar_one_or_none()
            if merchant:
                category = merchant
                # Cache for 1 hour
                await self.cache.set(cache_key, category, ttl=3600)
                return category
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting merchant category: {e}")
            return None
    
    async def find_similar_merchants(self, query: str, db: AsyncSession) -> List[Dict]:
        """Find merchants similar to query using fuzzy matching"""
        try:
            query_lower = query.lower()
            similar_merchants = []
            
            # Get all active merchants
            result = await db.execute(
                select(Merchant)
                .where(Merchant.is_active == True)
            )
            all_merchants = result.scalars().all()
            
            # Check if any merchant name appears in query
            for merchant in all_merchants:
                merchant_name = merchant.merchant_name.lower()
                display_name = merchant.display_name.lower()
                
                if merchant_name in query_lower or display_name in query_lower:
                    similar_merchants.append({
                        "merchant_name": merchant.merchant_name,
                        "display_name": merchant.display_name,
                        "category": merchant.category
                    })
            
            return similar_merchants
            
        except Exception as e:
            logger.error(f"Error finding similar merchants: {e}")
            return []
    
    async def extract_merchant_from_query(self, query: str, db: AsyncSession) -> Optional[Dict]:
        """Extract merchant information from user query"""
        try:
            # Step 1: Check database first
            similar_merchants = await self.find_similar_merchants(query, db)
            if similar_merchants:
                return similar_merchants[0]  # Return first match
            
            # Step 2: Use pattern matching for common merchants
            query_lower = query.lower()
            for category, merchants in self.category_patterns.items():
                for merchant in merchants:
                    if merchant in query_lower:
                        return {
                            "merchant_name": merchant,
                            "display_name": merchant.title(),
                            "category": category
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting merchant from query: {e}")
            return None
    
    async def get_best_card_for_merchant(
        self, 
        user_cards: List[Dict], 
        merchant_name: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get best card for specific merchant"""
        
        if not user_cards:
            return {
                "recommended_card": "No cards found",
                "reward_rate": 0,
                "category": "general",
                "merchant": merchant_name,
                "reason": "User has no active credit cards"
            }
        
        try:
            # Get merchant category
            category = await self.get_merchant_category(merchant_name, db)
            
            if not category:
                # Fallback to pattern matching
                for cat, merchants in self.category_patterns.items():
                    if merchant_name.lower() in merchants:
                        category = cat
                        break
                
                if not category:
                    category = "general"
            
            # Find best card for category
            best_card = None
            best_reward_rate = 0
            
            for card in user_cards:
                reward_rate = self._get_reward_rate_for_category(card, category)
                if reward_rate and reward_rate > best_reward_rate:
                    best_reward_rate = reward_rate
                    best_card = card
            
            if best_card:
                return {
                    "recommended_card": best_card["card_name"],
                    "reward_rate": best_reward_rate,
                    "category": category,
                    "merchant": merchant_name,
                    "reason": f"Best reward rate of {best_reward_rate}% for {category} category"
                }
            else:
                # Return first card as fallback
                return {
                    "recommended_card": user_cards[0]["card_name"],
                    "reward_rate": user_cards[0].get("reward_rate_general", 1.0),
                    "category": "general",
                    "merchant": merchant_name,
                    "reason": "Default card recommendation"
                }
                
        except Exception as e:
            logger.error(f"Error getting best card for merchant: {e}")
            return {
                "recommended_card": "Error occurred",
                "reward_rate": 0,
                "category": "general",
                "merchant": merchant_name,
                "reason": "Error processing request"
            }
    
    def _get_reward_rate_for_category(self, card: Dict, category: str) -> float:
        """Get reward rate for specific category"""
        category_mapping = {
            "online_shopping": card.get("reward_rate_online_shopping"),
            "dining": card.get("reward_rate_dining"),
            "travel": card.get("reward_rate_travel"),
            "fuel": card.get("reward_rate_fuel"),
            "entertainment": card.get("reward_rate_entertainment"),
            "groceries": card.get("reward_rate_groceries"),
            "utilities": card.get("reward_rate_general"),
            "healthcare": card.get("reward_rate_general"),
            "education": card.get("reward_rate_general"),
            "gaming": card.get("reward_rate_general"),
            "general": card.get("reward_rate_general")
        }
        
        return category_mapping.get(category, card.get("reward_rate_general", 1.0))
    
    async def get_user_cards_with_rewards(self, user_id: int, db: AsyncSession) -> List[Dict]:
        """Get user's cards with all reward rates"""
        try:
            result = await db.execute(
                select(CreditCard)
                .where(CreditCard.user_id == user_id)
                .where(CreditCard.is_active == True)
            )
            cards = result.scalars().all()
            
            return [card.to_dict() for card in cards]
            
        except Exception as e:
            logger.error(f"Error getting user cards: {e}")
            return []

# Create global instance
merchant_service = MerchantService() 