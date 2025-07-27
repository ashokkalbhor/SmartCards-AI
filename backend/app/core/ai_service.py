import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import re

import openai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.vector_db import vector_db_service
from app.models.credit_card import CreditCard
from app.models.conversation import Conversation, ConversationMessage
from app.models.merchant import Merchant

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_db = vector_db_service
    
    async def process_user_query(
        self, 
        user_id: int, 
        query: str, 
        conversation_id: Optional[int] = None,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """
        Main method to process user queries through the chatbot pipeline
        """
        try:
            # Step 1: Get user's credit cards
            user_cards = await self._get_user_cards(user_id, db)
            
            # Step 2: Search vector database for relevant information
            vector_results = await self._search_vector_db(query)
            
            # Step 3: Determine if we need to make an LLM call
            should_use_llm = self._should_use_llm(vector_results, query)
            
            # Step 4: Generate response
            if should_use_llm:
                response = await self._generate_llm_response(
                    query, user_cards, vector_results, conversation_id, db
                )
            else:
                response = await self._generate_vector_response(
                    query, user_cards, vector_results
                )
            
            return {
                "response": response["content"],
                "source": response["source"],
                "confidence": response["confidence"],
                "metadata": response.get("metadata", {}),
                "user_cards_used": len(user_cards) > 0
            }
            
        except Exception as e:
            logger.error(f"Error processing user query: {str(e)}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
                "source": "error",
                "confidence": 0.0,
                "metadata": {"error": str(e)}
            }
    
    async def _get_user_cards(self, user_id: int, db: AsyncSession) -> List[Dict]:
        """Get user's credit cards from database"""
        if not db:
            return []
        
        try:
            result = await db.execute(
                select(CreditCard).where(
                    CreditCard.user_id == user_id,
                    CreditCard.is_active == True
                )
            )
            cards = result.scalars().all()
            return [card.to_dict() for card in cards]
        except Exception as e:
            logger.error(f"Error fetching user cards: {str(e)}")
            return []
    
    async def _search_vector_db(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Search vector database for relevant credit card information"""
        try:
            # Search across all collections
            all_results = await self.vector_db.search_all_collections(
                query=query,
                filters=filters,
                n_results=settings.VECTOR_SEARCH_LIMIT
            )
            
            # Combine and sort results by similarity
            combined_results = []
            for collection_name, results in all_results.items():
                combined_results.extend(results)
            
            # Sort by similarity (highest first)
            combined_results.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Return top results
            return combined_results[:settings.VECTOR_SEARCH_LIMIT]
            
        except Exception as e:
            logger.error(f"Error searching vector database: {str(e)}")
            return []
    
    def _should_use_llm(self, vector_results: List[Dict], query: str) -> bool:
        """Determine if we should use LLM based on vector search results"""
        if not vector_results:
            return True
        
        # Check if any result has high similarity
        best_similarity = max(result["similarity"] for result in vector_results)
        
        # Use LLM if no good matches found
        if best_similarity < settings.FALLBACK_TO_LLM_THRESHOLD:
            return True
        
        # Use LLM for complex queries that require reasoning
        complex_keywords = [
            "compare", "which is better", "recommend", "should i", 
            "analysis", "calculate", "optimize", "strategy"
        ]
        
        return any(keyword in query.lower() for keyword in complex_keywords)
    
    async def _generate_vector_response(
        self, 
        query: str, 
        user_cards: List[Dict], 
        vector_results: List[Dict]
    ) -> Dict[str, Any]:
        """Generate response primarily based on vector search results"""
        if not vector_results:
            return {
                "content": "I don't have specific information about that. Could you please rephrase your question?",
                "source": "vector_fallback",
                "confidence": 0.3
            }
        
        # Get the best matching result
        best_result = max(vector_results, key=lambda x: x["similarity"])
        
        # Format response with user's cards context if relevant
        response_content = best_result["content"]
        
        if user_cards and "card" in query.lower():
            card_names = [card["card_name"] for card in user_cards]
            response_content += f"\n\nBased on your current cards ({', '.join(card_names)}), this information might be particularly relevant to you."
        
        return {
            "content": response_content,
            "source": "vector_db",
            "confidence": best_result["similarity"],
            "metadata": best_result["metadata"]
        }
    
    async def _generate_llm_response(
        self, 
        query: str, 
        user_cards: List[Dict], 
        vector_results: List[Dict],
        conversation_id: Optional[int] = None,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """Generate response using LLM with context from user cards and vector results"""
        
        # Build context for LLM
        context_parts = []
        
        # Add user cards context
        if user_cards:
            context_parts.append("USER'S CURRENT CREDIT CARDS:")
            for card in user_cards:
                card_info = f"- {card['card_name']} ({card['card_network']})"
                if card.get('reward_rate_general'):
                    card_info += f" - General reward rate: {card['reward_rate_general']}%"
                context_parts.append(card_info)
        
        # Add vector search results context
        if vector_results:
            context_parts.append("\nRELEVANT CREDIT CARD INFORMATION:")
            for result in vector_results[:3]:  # Top 3 results
                context_parts.append(f"- {result['content'][:200]}...")
        
        # Get conversation history if available
        conversation_history = []
        if conversation_id and db:
            conversation_history = await self._get_conversation_history(conversation_id, db)
        
        # Build the prompt
        system_prompt = """You are a helpful credit card advisor AI assistant. You help users make informed decisions about credit cards, rewards optimization, and spending strategies.

Guidelines:
1. Always be helpful, accurate, and concise
2. If you have information about the user's current cards, use it to provide personalized advice
3. Base your recommendations on the provided credit card information
4. If you don't have enough information, ask for clarification
5. Always mention if you're making assumptions
6. Focus on practical, actionable advice
7. Use proper formatting with line breaks, bullet points, and numbered lists for better readability
8. Separate different sections with double line breaks
9. Use **bold** text for important points and section headers
10. Use bullet points (•) for lists and numbered lists (1. 2. 3.) for step-by-step instructions

**IMPORTANT: When recommending cards for specific platforms, merchants, or events, ALWAYS follow this format:**

**Section 1: Best Card from Your Portfolio**
• Analyze the user's current cards
• Recommend the best card from their existing portfolio
• Include reward rates and benefits specific to the platform/merchant

**Section 2: Best Card from the Market**
• Suggest the best card available in the market for this specific use case
• Include card name, bank, reward rates, and key benefits
• Mention any co-branded or specialized cards for the platform

**Section 3: Conclusion & Additional Tips**
• Summarize the recommendation
• Include any additional tips, offers, or strategies
• Mention any seasonal promotions, cashback offers, or special deals
• Provide practical advice for maximizing rewards"""

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current context and query
        context_content = "\n".join(context_parts)
        user_message = f"Context:\n{context_content}\n\nUser Query: {query}"
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            return {
                "content": response.choices[0].message.content,
                "source": "llm",
                "confidence": 0.9,
                "metadata": {
                    "model": settings.OPENAI_MODEL,
                    "tokens_used": response.usage.total_tokens if response.usage else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return {
                "content": "I'm having trouble generating a response right now. Please try again.",
                "source": "llm_error",
                "confidence": 0.0,
                "metadata": {"error": str(e)}
            }
    
    async def _get_conversation_history(
        self, 
        conversation_id: int, 
        db: AsyncSession
    ) -> List[Dict]:
        """Get recent conversation history"""
        try:
            result = await db.execute(
                select(ConversationMessage)
                .where(ConversationMessage.conversation_id == conversation_id)
                .order_by(ConversationMessage.created_at.desc())
                .limit(settings.MAX_CONVERSATION_HISTORY)
            )
            messages = result.scalars().all()
            
            # Reverse to get chronological order
            return [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.created_at
                }
                for msg in reversed(messages)
            ]
        except Exception as e:
            logger.error(f"Error fetching conversation history: {str(e)}")
            return []
    
    async def add_knowledge_to_vector_db(
        self, 
        documents: List[str], 
        metadatas: List[Dict],
        ids: List[str],
        collection_name: Optional[str] = None
    ) -> bool:
        """Add credit card knowledge to vector database"""
        try:
            # Determine collection if not specified
            if not collection_name and metadatas:
                collection_name = self.vector_db.determine_collection_for_document(metadatas[0])
            elif not collection_name:
                collection_name = "credit_card_features"  # Default
            
            return await self.vector_db.add_documents_to_collection(
                collection_name, documents, metadatas, ids
            )
        except Exception as e:
            logger.error(f"Error adding knowledge to vector DB: {str(e)}")
            return False
    
    async def find_best_card_for_merchant(
        self, 
        user_cards: List[Dict], 
        merchant_name: str,
        merchant_category: str = None
    ) -> Dict[str, Any]:
        """Find the best card for a specific merchant or category"""
        if not user_cards:
            return {
                "recommendation": "No cards found",
                "reason": "User has no active credit cards"
            }
        
        # Category mapping for reward rates
        category_mapping = {
            "myntra": "online_shopping",
            "amazon": "online_shopping", 
            "flipkart": "online_shopping",
            "swiggy": "dining",
            "zomato": "dining",
            "uber": "travel",
            "ola": "travel",
            "reliance": "fuel",
            "hp": "fuel"
        }
        
        merchant_lower = merchant_name.lower()
        reward_category = None
        
        # Find matching category
        for merchant_key, category in category_mapping.items():
            if merchant_key in merchant_lower:
                reward_category = category
                break
        
        if not reward_category and merchant_category:
            reward_category = merchant_category.lower()
        
        # Find best card
        best_card = None
        best_reward_rate = 0
        
        for card in user_cards:
            if reward_category:
                reward_rate = card.get(f"reward_rate_{reward_category}", card.get("reward_rate_general", 1.0))
            else:
                reward_rate = card.get("reward_rate_general", 1.0)
            
            if reward_rate and reward_rate > best_reward_rate:
                best_reward_rate = reward_rate
                best_card = card
        
        if best_card:
            return {
                "recommendation": best_card["card_name"],
                "reward_rate": best_reward_rate,
                "reason": f"Best reward rate of {best_reward_rate}% for {merchant_name}",
                "category": reward_category or "general"
            }
        
        return {
            "recommendation": user_cards[0]["card_name"],
            "reward_rate": user_cards[0].get("reward_rate_general", 1.0),
            "reason": "Default card recommendation",
            "category": "general"
        }


# Create global instance
ai_service = AIService() 