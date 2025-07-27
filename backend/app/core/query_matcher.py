"""
Query pattern matcher for classifying user queries
"""

import re
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class QueryPatternMatcher:
    def __init__(self):
        self.patterns = {
            "merchant_recommendation": [
                r"which card.*best.*for",
                r"best card.*for",
                r"should i use.*for",
                r"recommend.*card.*for",
                r"card.*for.*",
                r"which card.*best.*(amazon|flipkart|myntra|swiggy|zomato|uber|ola|netflix|prime|hotstar|bigbasket|grofers|zepto|blinkit|makemytrip|goibibo|booking|airbnb|reliance|hp|bp|shell|airtel|jio|vodafone|pharmeasy|1mg|coursera|udemy|steam)",
                r"best card.*(amazon|flipkart|myntra|swiggy|zomato|uber|ola|netflix|prime|hotstar|bigbasket|grofers|zepto|blinkit|makemytrip|goibibo|booking|airbnb|reliance|hp|bp|shell|airtel|jio|vodafone|pharmeasy|1mg|coursera|udemy|steam)",
                r"should i use.*(amazon|flipkart|myntra|swiggy|zomato|uber|ola|netflix|prime|hotstar|bigbasket|grofers|zepto|blinkit|makemytrip|goibibo|booking|airbnb|reliance|hp|bp|shell|airtel|jio|vodafone|pharmeasy|1mg|coursera|udemy|steam)",
                r"recommend.*card.*(amazon|flipkart|myntra|swiggy|zomato|uber|ola|netflix|prime|hotstar|bigbasket|grofers|zepto|blinkit|makemytrip|goibibo|booking|airbnb|reliance|hp|bp|shell|airtel|jio|vodafone|pharmeasy|1mg|coursera|udemy|steam)"
            ],
            "general_recommendation": [
                r"which card.*best",
                r"best card",
                r"recommend.*card",
                r"should i use",
                r"card.*recommendation"
            ],
            "card_comparison": [
                r"compare.*card",
                r"difference.*card",
                r"which.*better",
                r"vs.*card"
            ],
            "reward_inquiry": [
                r"reward.*point",
                r"cashback",
                r"rewards.*earned",
                r"how many.*reward",
                r"point.*balance"
            ],
            "card_list": [
                r"my.*card",
                r"show.*card",
                r"list.*card",
                r"what.*card.*have",
                r"all.*card"
            ],
            "help": [
                r"help",
                r"what.*can.*do",
                r"how.*work",
                r"guide"
            ]
        }
        
        # Keywords for merchant detection
        self.merchant_keywords = [
            "amazon", "flipkart", "myntra", "nykaa", "ajio", "snapdeal",
            "swiggy", "zomato", "dunzo", "bigbasket", "grofers", "zepto", "blinkit",
            "uber", "ola", "makemytrip", "goibibo", "booking.com", "airbnb",
            "netflix", "prime", "hotstar", "bookmyshow", "spotify", "youtube",
            "reliance", "hp", "bp", "shell", "indian oil", "bharat petroleum",
            "airtel", "jio", "vodafone", "bsnl", "tata power", "adani electricity",
            "pharmeasy", "1mg", "netmeds", "apollo", "medplus",
            "coursera", "udemy", "byju's", "unacademy", "vedantu",
            "steam", "epic games", "playstation", "xbox", "nintendo"
        ]
    
    def match_query(self, query: str) -> Optional[str]:
        """Match query to pattern and return handler type"""
        query_lower = query.lower()
        
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    return pattern_type
        
        return None
    
    def extract_merchant(self, query: str) -> Optional[str]:
        """Extract merchant name from query"""
        query_lower = query.lower()
        
        for merchant in self.merchant_keywords:
            if merchant in query_lower:
                return merchant
        
        return None
    
    def is_merchant_query(self, query: str) -> bool:
        """Check if query is about a specific merchant"""
        return self.extract_merchant(query) is not None
    
    def get_query_confidence(self, query: str) -> float:
        """Get confidence score for query classification"""
        query_lower = query.lower()
        
        # Check for multiple patterns
        matched_patterns = 0
        total_patterns = 0
        
        for patterns in self.patterns.values():
            for pattern in patterns:
                total_patterns += 1
                if re.search(pattern, query_lower, re.IGNORECASE):
                    matched_patterns += 1
        
        if total_patterns == 0:
            return 0.0
        
        return matched_patterns / total_patterns
    
    def get_suggested_queries(self, query_type: str) -> List[str]:
        """Get suggested queries based on query type"""
        suggestions = {
            "merchant_recommendation": [
                "Which card is best for Amazon?",
                "Should I use my HDFC card for Swiggy?",
                "Best card for Netflix subscription"
            ],
            "general_recommendation": [
                "Which card should I use for online shopping?",
                "Recommend a card for travel",
                "Best card for dining rewards"
            ],
            "card_comparison": [
                "Compare my HDFC and SBI cards",
                "Which is better: HDFC Regalia or SBI Elite?",
                "Difference between my cards"
            ],
            "reward_inquiry": [
                "How many reward points do I have?",
                "Show my cashback earned this month",
                "What's my reward balance?"
            ],
            "card_list": [
                "Show my credit cards",
                "List all my cards",
                "What cards do I have?"
            ],
            "help": [
                "How does this work?",
                "What can you help me with?",
                "Show me available features"
            ]
        }
        
        return suggestions.get(query_type, [])
    
    def classify_query_complexity(self, query: str) -> str:
        """Classify query as simple or complex"""
        query_lower = query.lower()
        
        # Simple patterns (can be handled without LLM)
        simple_patterns = [
            "which card for",
            "best card for",
            "should i use",
            "my cards",
            "show cards",
            "reward points",
            "cashback"
        ]
        
        # Complex patterns (need LLM)
        complex_patterns = [
            "compare",
            "difference",
            "which is better",
            "strategy",
            "optimize",
            "analysis",
            "recommendation based on"
        ]
        
        # Check for simple patterns
        for pattern in simple_patterns:
            if pattern in query_lower:
                return "simple"
        
        # Check for complex patterns
        for pattern in complex_patterns:
            if pattern in query_lower:
                return "complex"
        
        # Default to simple for unknown patterns
        return "simple"

# Create global instance
query_matcher = QueryPatternMatcher() 