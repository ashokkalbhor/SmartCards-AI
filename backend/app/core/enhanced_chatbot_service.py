"""
Enhanced chatbot service with pattern matching and LLM fallback
"""

import logging
import hashlib
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.core.merchant_service import merchant_service
from app.core.query_matcher import query_matcher
from app.core.cache import CacheManager
from app.core.ai_service import ai_service
from app.models.user import User
from app.models.credit_card import CreditCard
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

logger = logging.getLogger(__name__)

class EnhancedChatbotService:
    def __init__(self):
        self.cache = CacheManager()
        self.merchant_service = merchant_service
        self.query_matcher = query_matcher
        self.ai_service = ai_service
    
    async def process_query(
        self,
        user_id: int,
        query: str,
        conversation_id: Optional[int] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Main entry point for processing user queries"""
        
        start_time = time.time()
        
        try:
            # Step 1: Check cache first
            cache_key = self._generate_cache_key(user_id, query)
            cached_response = await self.cache.get(cache_key)
            if cached_response:
                return {
                    **cached_response,
                    "processing_time": time.time() - start_time,
                    "source": "cache"
                }
            
            # Step 2: Classify query
            query_type = self.query_matcher.match_query(query)
            complexity = self.query_matcher.classify_query_complexity(query)
            
            # Step 3: Route to appropriate handler
            if complexity == "simple" and query_type:
                response = await self._handle_simple_query(user_id, query, query_type, db)
            else:
                response = await self._handle_complex_query(user_id, query, conversation_id, db)
            
            # Step 4: Cache response
            await self.cache.set(cache_key, response, ttl=1800)  # 30 minutes
            
            return {
                **response,
                "processing_time": time.time() - start_time,
                "query_type": query_type,
                "complexity": complexity
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now. Please try again.",
                "source": "error",
                "confidence": 0.0,
                "api_calls_saved": 0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def _handle_simple_query(
        self,
        user_id: int,
        query: str,
        query_type: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Handle simple queries without LLM"""
        
        try:
            if query_type == "merchant_recommendation":
                return await self._handle_merchant_recommendation(user_id, query, db)
            
            elif query_type == "card_list":
                return await self._handle_card_list(user_id, db)
            
            elif query_type == "reward_inquiry":
                return await self._handle_reward_inquiry(user_id, db)
            
            elif query_type == "help":
                return await self._handle_help_query()
            
            else:
                # Fallback to LLM for unknown simple queries
                return await self._fallback_to_llm(query, user_id, conversation_id=None, db=db)
                
        except Exception as e:
            logger.error(f"Error handling simple query: {e}")
            return await self._fallback_to_llm(query, user_id, conversation_id=None, db=db)
    
    async def _handle_merchant_recommendation(
        self,
        user_id: int,
        query: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Handle merchant recommendation queries"""
        
        # Extract merchant from query
        merchant_info = await self.merchant_service.extract_merchant_from_query(query, db)
        
        if not merchant_info:
            return {
                "response": "I couldn't identify which merchant you're asking about. Could you please specify the merchant name?",
                "source": "pattern_matching",
                "confidence": 0.3,
                "api_calls_saved": 1
            }
        
        # Get user's cards
        user_cards = await self.merchant_service.get_user_cards_with_rewards(user_id, db)
        
        if not user_cards:
            return {
                "response": "You don't have any active credit cards. Please add your cards first to get recommendations.",
                "source": "pattern_matching",
                "confidence": 0.9,
                "api_calls_saved": 1
            }
        
        # Get best card for merchant
        recommendation = await self.merchant_service.get_best_card_for_merchant(
            user_cards, merchant_info["merchant_name"], db
        )
        
        # Format response
        response = self._format_merchant_recommendation(recommendation, merchant_info)
        
        return {
            "response": response,
            "source": "pattern_matching",
            "confidence": 0.95,
            "api_calls_saved": 1,
            "recommendation": recommendation,
            "merchant": merchant_info
        }
    
    async def _handle_card_list(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Handle card list queries"""
        
        user_cards = await self.merchant_service.get_user_cards_with_rewards(user_id, db)
        
        if not user_cards:
            return {
                "response": "You don't have any active credit cards. Please add your cards first.",
                "source": "pattern_matching",
                "confidence": 0.9,
                "api_calls_saved": 1
            }
        
        # Format card list
        card_names = [card["card_name"] for card in user_cards]
        response = f"**Your Credit Cards:**\n\n"
        for i, card in enumerate(user_cards, 1):
            response += f"{i}. **{card['card_name']}** ({card['card_network']})\n"
            if card.get('reward_rate_general'):
                response += f"   • General rewards: {card['reward_rate_general']}%\n"
            if card.get('reward_rate_online_shopping'):
                response += f"   • Online shopping: {card['reward_rate_online_shopping']}%\n"
            if card.get('reward_rate_dining'):
                response += f"   • Dining: {card['reward_rate_dining']}%\n"
            response += "\n"
        
        return {
            "response": response,
            "source": "pattern_matching",
            "confidence": 0.95,
            "api_calls_saved": 1,
            "cards": user_cards
        }
    
    async def _handle_reward_inquiry(self, user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Handle reward inquiry queries"""
        
        # For MVP, return a generic response since we don't store reward data
        response = "I can help you with card recommendations for different merchants. To check your actual reward points, please visit your bank's website or mobile app."
        
        return {
            "response": response,
            "source": "pattern_matching",
            "confidence": 0.8,
            "api_calls_saved": 1
        }
    
    async def _handle_help_query(self) -> Dict[str, Any]:
        """Handle help queries"""
        
        response = """**How I Can Help You:**

• **Card Recommendations**: "Which card is best for Amazon?"
• **Merchant Queries**: "Should I use my HDFC card for Swiggy?"
• **Card Information**: "Show my credit cards"
• **General Advice**: "Best card for online shopping"

**Just ask me about your cards and I'll help you optimize your spending!**"""
        
        return {
            "response": response,
            "source": "pattern_matching",
            "confidence": 0.95,
            "api_calls_saved": 1
        }
    
    async def _handle_complex_query(
        self,
        user_id: int,
        query: str,
        conversation_id: Optional[int],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Handle complex queries with LLM"""
        
        return await self._fallback_to_llm(query, user_id, conversation_id, db)
    
    async def _fallback_to_llm(
        self,
        query: str,
        user_id: int,
        conversation_id: Optional[int],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Fallback to LLM for complex queries"""
        
        try:
            # Use existing AI service
            response = await self.ai_service.process_user_query(
                user_id=user_id,
                query=query,
                conversation_id=conversation_id,
                db=db
            )
            
            return {
                "response": response["response"],
                "source": "llm",
                "confidence": response["confidence"],
                "api_calls_saved": 0,
                "metadata": response.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error in LLM fallback: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request. Please try rephrasing your question.",
                "source": "llm_error",
                "confidence": 0.0,
                "api_calls_saved": 0
            }
    
    def _format_merchant_recommendation(self, recommendation: Dict, merchant_info: Dict) -> str:
        """Format merchant recommendation response"""
        
        if recommendation["recommended_card"] == "No cards found":
            return "You don't have any active credit cards. Please add your cards first to get recommendations."
        
        if recommendation["recommended_card"] == "Error occurred":
            return "I'm sorry, I encountered an error while processing your request. Please try again."
        
        merchant_name = merchant_info["display_name"]
        card_name = recommendation["recommended_card"]
        reward_rate = recommendation["reward_rate"]
        category = recommendation["category"]
        
        response = f"**Recommendation for {merchant_name}:**\n\n"
        response += f"**Section 1: Best Card from Your Portfolio**\n\n"
        response += f"**Recommended Card:** {card_name}\n"
        response += f"**Reward Rate:** {reward_rate}%\n"
        response += f"**Category:** {category.replace('_', ' ').title()}\n\n"
        response += f"**Why this card?** {recommendation['reason']}\n\n"
        response += f"**Section 2: Best Card from the Market**\n\n"
        response += f"For {merchant_name}, consider these market-leading options:\n\n"
        
        # Provide specific recommendations based on merchant category
        if category == "online_shopping":
            response += f"• **Amazon Pay ICICI Card:** 5% cashback on Amazon\n"
            response += f"• **Flipkart Axis Bank Card:** 5% rewards on Flipkart\n"
            response += f"• **HDFC Millennia:** 5% cashback on online shopping\n"
            response += f"• **SBI SimplyCLICK:** 10X rewards on online shopping\n\n"
        elif category == "dining":
            response += f"• **HDFC Swiggy Card:** 10% cashback on Swiggy\n"
            response += f"• **SBI Card Elite:** 5X rewards on dining\n"
            response += f"• **Axis Bank Neo Card:** 5% cashback on food delivery\n"
            response += f"• **ICICI Bank Coral:** 4X rewards on dining\n\n"
        elif category == "travel":
            response += f"• **HDFC Regalia:** 4X rewards on travel\n"
            response += f"• **Axis Bank Magnus:** 5X rewards on travel\n"
            response += f"• **SBI Card Elite:** 5X rewards on travel\n"
            response += f"• **ICICI Bank Sapphiro:** 4X rewards on travel\n\n"
        elif category == "fuel":
            response += f"• **BPCL SBI Card:** 4.25% value back on fuel\n"
            response += f"• **HPCL SBI Card:** 4.25% value back on fuel\n"
            response += f"• **IOCL HDFC Card:** 4X rewards on fuel\n"
            response += f"• **Axis Bank IOCL Card:** 4X rewards on fuel\n\n"
        else:
            response += f"• **Co-branded Cards:** Look for {merchant_name}-specific credit cards\n"
            response += f"• **Online Shopping Cards:** Cards with 5-10% rewards on e-commerce\n"
            response += f"• **Cashback Cards:** Flat-rate cashback cards for general spending\n\n"
        response += f"**Section 3: Conclusion & Additional Tips**\n\n"
        response += f"• **Current Best:** Use your {card_name} for {reward_rate}% rewards\n"
        
        # Add category-specific tips
        if category == "online_shopping":
            response += f"• **Festival Sales:** Look for 10-15% cashback during sales\n"
            response += f"• **Bank Offers:** Check for instant discounts on {merchant_name}\n"
            response += f"• **Payment Methods:** Use UPI for additional ₹100-200 discounts\n"
            response += f"• **Reward Multipliers:** Some cards offer 2X-5X rewards on weekends\n"
        elif category == "dining":
            response += f"• **First Order Offers:** New users get 50-100% cashback\n"
            response += f"• **Weekend Bonuses:** Extra rewards on Friday-Sunday\n"
            response += f"• **Restaurant Partnerships:** Check for specific restaurant offers\n"
            response += f"• **Delivery Fees:** Some cards waive delivery charges\n"
        elif category == "travel":
            response += f"• **Booking Bonuses:** Extra rewards on travel bookings\n"
            response += f"• **Insurance Coverage:** Many travel cards include free insurance\n"
            response += f"• **Lounge Access:** Premium cards offer airport lounge access\n"
            response += f"• **Fuel Surcharge Waiver:** Save on fuel surcharge\n"
        elif category == "fuel":
            response += f"• **Fuel Surcharge Waiver:** Save 1-2.5% on fuel surcharge\n"
            response += f"• **Co-branded Benefits:** Extra rewards at partner fuel stations\n"
            response += f"• **Monthly Caps:** Most cards have ₹400-500 monthly fuel rewards\n"
            response += f"• **Weekend Bonuses:** Extra rewards on weekends\n"
        else:
            response += f"• **Maximize Rewards:** Check for {merchant_name} offers and promotions\n"
            response += f"• **Seasonal Deals:** Look for festival sales and special cashback offers\n"
            response += f"• **Payment Methods:** Consider using UPI or net banking for additional discounts\n"
            response += f"• **Reward Tracking:** Monitor your reward points regularly"
        
        return response
    
    def _generate_cache_key(self, user_id: int, query: str) -> str:
        """Generate cache key for response caching"""
        content = f"{user_id}:{query.lower().strip()}"
        return hashlib.md5(content.encode()).hexdigest()

# Create global instance
enhanced_chatbot_service = EnhancedChatbotService() 