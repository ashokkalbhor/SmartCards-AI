import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from langchain.agents import create_sql_agent, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.vector_service import VectorService
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class SQLAgentService:
    """Main SQL Agent service using LangChain with MCP integration"""
    
    def __init__(self):
        self.agent = None
        self.db = None
        self.target_db = None  # Target business database
        self.vector_service = None
        self.cache_service = None
        self.memory = None
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize the SQL agent service"""
        try:
            # Initialize services
            self.vector_service = VectorService()
            self.cache_service = CacheService()
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Load tuning data into vector database
            await self.vector_service.load_tuning_data()

            # Connect to target business database for SQL queries
            self.logger.info(f"🔍 TARGET_DATABASE_URL: {settings.TARGET_DATABASE_URL}")
            self.logger.info(f"🔍 SQL_AGENT_TABLES: {settings.SQL_AGENT_TABLES}")
            self.target_db = SQLDatabase.from_uri(
                settings.TARGET_DATABASE_URL,
                include_tables=settings.SQL_AGENT_TABLES,
                sample_rows_in_table_info=3
            )
            
            # Connect to service database for chat operations
            self.logger.info(f"🔍 DATABASE_URL: {settings.DATABASE_URL}")
            self.db = SQLDatabase.from_uri(
                settings.DATABASE_URL,
                include_tables=["conversations", "conversation_messages"],
                sample_rows_in_table_info=3
            )

            # Initialize OpenAI
            llm = ChatOpenAI(
                model="gpt-4",
                temperature=0,
                openai_api_key=settings.OPENAI_API_KEY
            )

            # Create SQL toolkit
            self.toolkit = SQLDatabaseToolkit(db=self.target_db, llm=llm)

            # Create SQL agent
            self.agent = create_sql_agent(
                llm=llm,
                toolkit=self.toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                memory=self.memory
            )

            self.logger.info("SQL Agent Service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize SQL Agent Service: {e}")
            raise
    
    async def process_query(
        self,
        query: str,
        user_id: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
        include_sql: bool = False,
        include_explanation: bool = True,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """Process a natural language query using the SQL agent"""
        
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(query, user_id, context)
            cached_response = await self.cache_service.get(cache_key)
            if cached_response:
                return {
                    **cached_response,
                    "processing_time": time.time() - start_time,
                    "source": "cache"
                }
            
            # Search vector database for relevant context
            vector_context = await self._get_vector_context(query, user_id)
            
            # Enhance query with context
            enhanced_query = self._enhance_query_with_context(query, vector_context, context)
            
            # Generate SQL and execute query
            sql_query, results, explanation = await self._execute_sql_query(enhanced_query, user_id)
            
            # Format response
            response = await self._format_response(
                query, sql_query, results, explanation, 
                include_sql, include_explanation, max_results
            )
            
            # Validate response is based on actual data
            response = await self._validate_response(response, results, vector_context)
            
            # Calculate confidence
            confidence = self._calculate_confidence(results, vector_context)
            
            # Cache response
            await self.cache_service.set(cache_key, response, ttl=settings.CACHE_TTL)
            
            return {
                "response": response,
                "sql_query": sql_query if include_sql else None,
                "results": results[:max_results] if results else None,
                "explanation": explanation if include_explanation else None,
                "confidence": confidence,
                "processing_time": time.time() - start_time,
                "source": "sql_agent",
                "metadata": {
                    "vector_context_used": len(vector_context) > 0,
                    "user_id": user_id,
                    "query_enhanced": enhanced_query != query
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request. Please try rephrasing your question.",
                "sql_query": None,
                "results": None,
                "explanation": None,
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "source": "error",
                "metadata": {"error": str(e)}
            }
    
    async def _get_vector_context(self, query: str, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get relevant context from vector database"""
        try:
            # Search for relevant documents
            results = await self.vector_service.search(
                query=query,
                user_id=user_id,
                limit=5
            )
            
            return results
            
        except Exception as e:
            logger.warning(f"Failed to get vector context: {e}")
            return []
    
    def _enhance_query_with_context(
        self, 
        query: str, 
        vector_context: List[Dict[str, Any]], 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Enhance query with vector context and additional context"""
        
        enhanced_parts = [query]
        
        # Add vector context
        if vector_context:
            context_text = " ".join([doc.get("content", "") for doc in vector_context])
            enhanced_parts.append(f"Context from documents: {context_text}")
        
        # Add additional context
        if context and isinstance(context, dict):
            if "user_cards" in context and isinstance(context["user_cards"], list):
                try:
                    cards_info = ", ".join([f"{card.get('card_name', 'Unknown')} ({card.get('bank_name', 'Unknown')})" for card in context["user_cards"] if isinstance(card, dict)])
                    if cards_info:
                        enhanced_parts.append(f"User's cards: {cards_info}")
                except Exception as e:
                    logger.warning(f"Failed to process user cards: {e}")
            
            if "spending_pattern" in context:
                enhanced_parts.append(f"Spending pattern: {context['spending_pattern']}")
        
        return " ".join(enhanced_parts)
    
    async def _execute_sql_query(self, query: str, user_id: Optional[int] = None) -> Tuple[str, List[Dict[str, Any]], str]:
        """Execute SQL query using LangChain agent"""
        
        try:
            # Get relevant tuning examples
            tuning_examples = await self.vector_service.get_tuning_examples(query, limit=2)
            
            # Build examples context
            examples_context = ""
            if tuning_examples:
                examples_context = "\n\nRelevant examples:\n"
                for example in tuning_examples:
                    examples_context += f"Q: {example['metadata']['question']}\n"
                    examples_context += f"SQL: {example['metadata']['sql_query']}\n"
                    examples_context += f"A: {example['metadata']['answer']}\n\n"
            
            # Build user context
            user_context = ""
            if user_id:
                user_context = f"""
            USER CONTEXT:
            - Current user ID: {user_id}
            - When asked about "my cards", "my portfolio", "cards I have", "how many cards do I have", etc., query the credit_cards table for user_id = {user_id}
            - For user portfolio queries, use: SELECT * FROM credit_cards WHERE user_id = {user_id}
            - To get detailed card information for user's cards, join with card_master_data: 
              SELECT cc.*, cmd.* FROM credit_cards cc 
              LEFT JOIN card_master_data cmd ON cc.card_master_data_id = cmd.id 
              WHERE cc.user_id = {user_id}
            """
            
            # Create a more specific prompt for better results with guardrails
            enhanced_prompt = f"""
            You are a credit card recommendation assistant. CRITICAL RULES:
            1. ONLY use information from the SQL database (card_master_data, credit_cards, card_merchant_rewards, merchants) or vector database (uploaded documents)
            2. NEVER make up information about cards, banks, or reward rates
            3. If you cannot find relevant information in the database, respond with: "I don't have information about that in my database. I can help you with credit card recommendations, reward rates, merchant-specific offers, and banking product information. Please ask me about credit cards and other banking products."
            4. Always verify information exists in the database before providing it
            
            When asked about credit cards, always:
            1. Join tables to get complete card information (card names, bank names, reward rates)
            2. Order results by reward rate (highest first)
            3. Provide specific card names and bank names, not just IDs
            4. Include reward rates in your response
            5. Follow the style and format of the examples provided
            
            Database schema context:
            - credit_cards: user's cards with basic info (user_id, card_name, card_master_data_id, etc.)
            - card_master_data: market cards with detailed info (bank_name, card_name, reward rates, etc.)
            - card_merchant_rewards: specific merchant reward rates
            - merchants: merchant information
            
            {user_context}
            
            For Amazon queries, check card_merchant_rewards table where merchant_name = 'amazon'
            {examples_context}
            Query: {query}
            """
            
            # Use LangChain agent to generate and execute SQL
            result = await self.agent.ainvoke({"input": enhanced_prompt})
            
            # Extract SQL query and results
            explanation = result.get("output", "")
            
            # Try to extract SQL query from intermediate steps
            sql_query = ""
            results = []
            
            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                for step in intermediate_steps:
                    if isinstance(step, tuple) and len(step) >= 2:
                        action, action_input = step[0], step[1]
                        if action and hasattr(action, 'name') and action.name == 'sql_db_query':
                            sql_query = action_input
                            break
                    elif isinstance(step, dict):
                        if step.get('tool') == 'sql_db_query':
                            sql_query = step.get('tool_input', '')
                            break
            
            # Execute SQL to get actual results
            if sql_query:
                results = await self._execute_raw_sql(sql_query)
            else:
                # If no SQL query found, try to extract results from the explanation
                # This handles cases where the agent provides the answer directly
                if explanation and "reward rate" in explanation.lower():
                    results = [{"result": explanation}]
                else:
                    results = []
            

            
            return sql_query, results, explanation
            
        except Exception as e:
            logger.error(f"Error executing SQL query: {e}")
            return "", [], f"Error: {str(e)}"
    
    async def _execute_raw_sql(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query and return results"""
        try:
            # Use the database toolkit to execute SQL
            result = self.toolkit.db.run(sql_query)
            
            # Parse results properly
            if result:
                # If result is a string, try to parse it as JSON or return as is
                if isinstance(result, str):
                    try:
                        import json
                        parsed_result = json.loads(result)
                        if isinstance(parsed_result, list):
                            return parsed_result
                        else:
                            return [{"result": parsed_result}]
                    except json.JSONDecodeError:
                        return [{"result": result}]
                elif isinstance(result, list):
                    return result
                else:
                    return [{"result": result}]
            else:
                return []
            
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}")
            return []
    
    async def _validate_response(self, response: str, sql_results: List[Dict[str, Any]], vector_results: List[Dict[str, Any]]) -> str:
        """Validate that response is based on actual data"""
        
        # Check if we have any actual data
        has_sql_data = bool(sql_results and len(sql_results) > 0)
        has_vector_data = bool(vector_results and len(vector_results) > 0)
        
        # If no data found, return scope message
        if not has_sql_data and not has_vector_data:
            return "I don't have information about that in my database. I can help you with credit card recommendations, reward rates, merchant-specific offers, and banking product information. Please ask me about credit cards and other banking products."
        
        # If we have data, return the original response
        return response

    async def _format_response(
        self,
        original_query: str,
        sql_query: str,
        results: List[Dict[str, Any]],
        explanation: str,
        include_sql: bool,
        include_explanation: bool,
        max_results: int
    ) -> str:
        """Format the response in structured, user-friendly format"""
        
        # Handle edge cases first
        if not results:
            # Try web search as fallback
            try:
                web_search_result = await self._perform_web_search(original_query)
                if web_search_result:
                    return web_search_result
            except Exception as e:
                logger.warning(f"Web search fallback failed: {e}")
                # Continue to fallback message
            
            return "I don't have information about that in my database. I can help you with credit card recommendations, reward rates, merchant-specific offers, and banking product information. Please ask me about credit cards and other banking products."
        
        # Check if explanation is already included in results to avoid duplication
        explanation_in_results = False
        if results and len(results) == 1 and 'result' in results[0]:
            result_content = str(results[0]['result'])
            if explanation and explanation.strip() in result_content:
                explanation_in_results = True
        
        # If explanation is in results, use structured formatting
        if explanation_in_results:
            return self._format_structured_response(original_query, sql_query, results, max_results, include_sql)
        
        # Classify query type and categorize results
        query_type = self._classify_query_type(original_query, sql_query)
        user_cards, market_cards = self._categorize_results(results, sql_query, query_type)
        
        response_parts = []
        
        # Portfolio section (if user cards found)
        if user_cards:
            response_parts.append("1. Best Option from Your Card Portfolio")
            for i, card in enumerate(user_cards[:3]):
                benefit = self._format_card_benefit(card)
                response_parts.append(f"   a. {benefit}")
        
        # Market section (if market cards found)  
        if market_cards:
            section_number = "2" if user_cards else "1"
            response_parts.append(f"\n{section_number}. Best Option Available in the Market")
            for i, card in enumerate(market_cards[:3]):
                benefit = self._format_card_benefit(card)
                response_parts.append(f"   a. {benefit}")
        
        # Add SQL query if requested
        if include_sql and sql_query:
            response_parts.append(f"\nGenerated SQL: {sql_query}")
        
        return "\n".join(response_parts) if response_parts else "I couldn't find any relevant information."
    
    def _format_single_result(self, result: Dict[str, Any]) -> str:
        """Format a single result dictionary into readable text"""
        if not result:
            return "No data available"
        
        # If result has a 'result' key, extract that content
        if 'result' in result and len(result) == 1:
            return str(result['result'])
        
        # If result has multiple keys, format them nicely
        if len(result) > 1:
            formatted_parts = []
            for key, value in result.items():
                if value is not None and value != '':
                    # Convert key to readable format
                    readable_key = key.replace('_', ' ').title()
                    formatted_parts.append(f"{readable_key}: {value}")
            return ", ".join(formatted_parts)
        
        # If result has one key (not 'result'), format it
        if len(result) == 1:
            key, value = next(iter(result.items()))
            if key == 'result':
                return str(value)
            else:
                readable_key = key.replace('_', ' ').title()
                return f"{readable_key}: {value}"
        
        # Fallback: convert to string
        return str(result)
    
    def _classify_query_type(self, query: str, sql_query: str) -> str:
        """Classify query type based on keywords and SQL patterns"""
        query_lower = query.lower()
        sql_lower = sql_query.lower() if sql_query else ""
        
        # Portfolio keywords
        portfolio_keywords = ["my", "portfolio", "cards i have", "my cards", "own", "hold", "i have"]
        
        # Check for portfolio keywords in query
        if any(keyword in query_lower for keyword in portfolio_keywords):
            return "portfolio"
        
        # Check for user-specific SQL patterns
        if "user_id" in sql_lower or "credit_cards" in sql_lower:
            return "portfolio"
        
        # Default to showing both portfolio and market
        return "both"
    
    def _categorize_results(self, results: List[Dict[str, Any]], sql_query: str, query_type: str) -> tuple:
        """Categorize results into user portfolio cards vs market cards"""
        user_cards = []
        market_cards = []
        
        for result in results:
            # Check if this is a user portfolio card
            if ('user_id' in result or 
                'credit_limit' in result or 
                'current_balance' in result or
                'card_number_last4' in result):
                user_cards.append(result)
            else:
                market_cards.append(result)
        
        # If no clear categorization, treat based on query type
        if not user_cards and not market_cards and results:
            if query_type == "portfolio":
                user_cards = results
            else:
                market_cards = results
        
        return user_cards, market_cards
    
    def _format_card_benefit(self, card: Dict[str, Any]) -> str:
        """Format card information into user-friendly benefit description"""
        # Extract card information
        card_name = card.get('card_name', 'Unknown Card')
        bank_name = card.get('bank_name', 'Unknown Bank')
        
        # Get reward rate from various possible fields
        reward_rate = (card.get('reward_rate_general') or 
                      card.get('reward_rate') or 
                      card.get('cashback_rate') or 
                      card.get('reward_points', 0))
        
        # Format reward rate
        if reward_rate and float(reward_rate) > 0:
            reward_text = f"{float(reward_rate)}% cashback"
            if float(reward_rate) < 1:
                # Might be points instead of percentage
                reward_text = f"{float(reward_rate)}X reward points"
        else:
            reward_text = "attractive rewards"
        
        # Create benefit description
        return f"{card_name} from {bank_name} is an excellent choice for your spends, thanks to: {reward_text}"
    
    def _format_structured_response(self, query: str, sql_query: str, results: List[Dict[str, Any]], max_results: int, include_sql: bool) -> str:
        """Format structured response when explanation is in results"""
        if not results:
            return "I couldn't find any relevant information."
        
        # Extract the explanation content
        result_content = str(results[0].get('result', ''))
        
        # Check if this is a card recommendation query
        if self._is_card_recommendation_query(query, result_content):
            # Try to parse card information from the explanation
            parsed_cards = self._parse_cards_from_explanation(result_content)
            
            if parsed_cards:
                # Use our structured formatting for card recommendations
                query_type = self._classify_query_type(query, sql_query)
                user_cards, market_cards = self._categorize_parsed_cards(parsed_cards, query_type)
                
                response_parts = []
                
                # Portfolio section (if user cards found)
                if user_cards:
                    response_parts.append("1. Best Option from Your Card Portfolio")
                    for i, card in enumerate(user_cards[:3]):
                        benefit = self._format_card_benefit_simple(card)
                        response_parts.append(f"   a. {benefit}")
                
                # Market section (if market cards found)  
                if market_cards:
                    section_number = "2" if user_cards else "1"
                    response_parts.append(f"\n{section_number}. Best Option Available in the Market")
                    for i, card in enumerate(market_cards[:3]):
                        benefit = self._format_card_benefit_simple(card)
                        response_parts.append(f"   a. {benefit}")
                
                # Add SQL query if requested
                if include_sql and sql_query:
                    response_parts.append(f"\nGenerated SQL: {sql_query}")
                
                return "\n".join(response_parts) if response_parts else "I couldn't find any relevant information."
        
        # Fallback to cleaned response for non-card queries or if parsing fails
        cleaned_response = self._clean_response_text(result_content)
        
        # Add SQL query if requested
        if include_sql and sql_query:
            cleaned_response += f"\n\nGenerated SQL: {sql_query}"
        
        return cleaned_response
    
    def _clean_response_text(self, text: str) -> str:
        """Clean and format response text for better readability"""
        if not text:
            return "No information available."
        
        # Remove any JSON-like patterns that might have slipped through
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Format numbered lists properly
        text = re.sub(r'(\d+)\.\s*([A-Z])', r'\n\1. \2', text)
        
        # Ensure proper spacing after periods
        text = re.sub(r'\.([A-Z])', r'. \1', text)
        
        return text.strip()
    
    async def _perform_web_search(self, query: str) -> Optional[str]:
        """Perform web search as fallback when database can't answer"""
        try:
            # Use OpenAI's web search capabilities
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage
            
            # Initialize OpenAI client
            llm = ChatOpenAI(
                model="gpt-4",
                temperature=0,
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            # Create a focused search query for credit card information
            search_query = self._create_search_query(query)
            
            # Use OpenAI to search for information
            search_prompt = f"""
            Search for information about: {search_query}
            
            Focus on:
            - Official bank websites (SBI, HDFC, ICICI, Axis, etc.)
            - Legitimate financial websites
            - Credit card comparison sites
            - Bank product pages
            
            Provide:
            1. Card name and bank
            2. Key benefits and reward rates
            3. Source website URL
            4. Keep response concise and factual
            
            Format as:
            Card: [Card Name] from [Bank Name]
            Benefits: [Key benefits and reward rates]
            Source: [Website URL]
            """
            
            # Get search results
            response = await llm.ainvoke([HumanMessage(content=search_prompt)])
            search_result = response.content
            
            # Add disclaimer and format
            if search_result and len(search_result.strip()) > 50:
                formatted_result = f"{search_result}\n\n⚠️ External Information: This information is from external sources and may not be up-to-date."
                return formatted_result
            
            return None
            
        except Exception as e:
            logger.warning(f"Web search failed: {e}")
            return None
    
    def _create_search_query(self, original_query: str) -> str:
        """Create a focused search query for credit card information"""
        # Extract key terms from the original query
        query_lower = original_query.lower()
        
        # Identify the category/merchant
        if "flipkart" in query_lower:
            return "best credit card for Flipkart shopping rewards"
        elif "amazon" in query_lower:
            return "best credit card for Amazon shopping rewards"
        elif "swiggy" in query_lower:
            return "best credit card for Swiggy food delivery rewards"
        elif "zomato" in query_lower:
            return "best credit card for Zomato food delivery rewards"
        elif "uber" in query_lower or "ola" in query_lower:
            return "best credit card for ride sharing Uber Ola rewards"
        elif "online" in query_lower:
            return "best credit card for online shopping rewards"
        elif "fuel" in query_lower or "petrol" in query_lower:
            return "best credit card for fuel petrol rewards"
        elif "dining" in query_lower or "restaurant" in query_lower:
            return "best credit card for dining restaurant rewards"
        elif "travel" in query_lower:
            return "best credit card for travel rewards"
        elif "cashback" in query_lower:
            return "best cashback credit card rewards"
        else:
            # General credit card search
            return f"best credit card {original_query}"
    
    def _is_card_recommendation_query(self, query: str, content: str) -> bool:
        """Check if this is a card recommendation query"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Keywords that indicate card recommendation
        card_keywords = ["card", "credit", "recommendation", "best", "portfolio", "reward"]
        
        # Check if query or content contains card-related keywords
        return any(keyword in query_lower for keyword in card_keywords) or any(keyword in content_lower for keyword in card_keywords)
    
    def _parse_cards_from_explanation(self, explanation: str) -> List[Dict[str, Any]]:
        """Parse card information from explanation text"""
        import re
        
        cards = []
        
        # Pattern to match card information like: "1. Airtel Credit Card from Axis Bank with a reward rate of 10.0%"
        # This handles both quoted and unquoted formats
        pattern = r"\d+\.\s*(?:'([^']+)'|([^\s]+(?:\s+[^\s]+)*?))\s+from\s+(?:'([^']+)'|([^\s]+(?:\s+[^\s]+)*?))\s+with\s+a\s+reward\s+rate\s+of\s+([\d.]+)(?:%|)"
        
        matches = re.findall(pattern, explanation)
        
        for match in matches:
            # Handle both quoted and unquoted formats
            # match[0] = quoted card name, match[1] = unquoted card name
            # match[2] = quoted bank name, match[3] = unquoted bank name
            # match[4] = reward rate
            card_name = match[0] if match[0] else match[1]
            bank_name = match[2] if match[2] else match[3]
            reward_rate = match[4]
            
            cards.append({
                'card_name': card_name,
                'bank_name': bank_name,
                'reward_rate': float(reward_rate),
                'reward_rate_general': float(reward_rate)
            })
        
        return cards
    
    def _categorize_parsed_cards(self, cards: List[Dict[str, Any]], query_type: str) -> tuple:
        """Categorize parsed cards into user portfolio vs market cards"""
        # For explanation-based results, treat as user portfolio cards if query indicates portfolio
        if query_type == "portfolio":
            return cards, []
        else:
            # For general queries, show as market cards
            return [], cards
    
    def _format_card_benefit_simple(self, card: Dict[str, Any]) -> str:
        """Format card information into simple benefit description"""
        # Extract card information
        card_name = card.get('card_name', 'Unknown Card')
        bank_name = card.get('bank_name', 'Unknown Bank')
        
        # Get reward rate from various possible fields
        reward_rate = (card.get('reward_rate_general') or 
                      card.get('reward_rate') or 
                      card.get('cashback_rate') or 
                      card.get('reward_points', 0))
        
        # Format reward rate
        if reward_rate and float(reward_rate) > 0:
            reward_text = f"{float(reward_rate)}% cashback on online spends"
            if float(reward_rate) < 1:
                # Might be points instead of percentage
                reward_text = f"{float(reward_rate)}X reward points"
        else:
            reward_text = "attractive rewards"
        
        # Create simple benefit description
        return f"{card_name} from {bank_name} - {reward_text}"
    
    def _calculate_confidence(self, results: List[Dict[str, Any]], vector_context: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on results and context"""
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence if we have results
        if results:
            confidence += 0.3
        
        # Increase confidence if we have vector context
        if vector_context:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _generate_cache_key(self, query: str, user_id: Optional[int], context: Optional[Dict[str, Any]]) -> str:
        """Generate cache key for query"""
        import hashlib
        
        key_parts = [query]
        if user_id:
            key_parts.append(str(user_id))
        if context and isinstance(context, dict):
            key_parts.append(str(sorted(context.items())))
        
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()


# Global SQL Agent Service instance
sql_agent_service = SQLAgentService()

# Initialize the service (will be called during FastAPI startup)
async def initialize_sql_agent_service():
    """Initialize the global SQL agent service instance"""
    try:
        await sql_agent_service.initialize()
        logger.info("✅ SQL Agent Service initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize SQL Agent Service: {e}")
        # Don't raise - allow service to run with degraded functionality
        return False
