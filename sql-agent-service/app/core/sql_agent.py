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
from app.core.database import get_database_schema
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
            self.target_db = SQLDatabase.from_uri(
                settings.TARGET_DATABASE_URL,
                include_tables=settings.SQL_AGENT_TABLES,
                sample_rows_in_table_info=3
            )
            
            # Connect to service database for chat operations
            self.db = SQLDatabase.from_uri(
                settings.DATABASE_URL,
                include_tables=["chat_users", "conversations", "chat_messages", "user_sessions", "documents"],
                sample_rows_in_table_info=3
            )

            # Initialize OpenAI
            llm = ChatOpenAI(
                model="gpt-4",
                temperature=0,
                openai_api_key=settings.OPENAI_API_KEY
            )

            # Create SQL toolkit
            toolkit = SQLDatabaseToolkit(db=self.target_db, llm=llm)

            # Create SQL agent
            self.agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
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
            sql_query, results, explanation = await self._execute_sql_query(enhanced_query)
            
            # Format response
            response = await self._format_response(
                query, sql_query, results, explanation, 
                include_sql, include_explanation, max_results
            )
            
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
        if context:
            if "user_cards" in context:
                cards_info = ", ".join([f"{card['card_name']} ({card['bank_name']})" for card in context["user_cards"]])
                enhanced_parts.append(f"User's cards: {cards_info}")
            
            if "spending_pattern" in context:
                enhanced_parts.append(f"Spending pattern: {context['spending_pattern']}")
        
        return " ".join(enhanced_parts)
    
    async def _execute_sql_query(self, query: str) -> Tuple[str, List[Dict[str, Any]], str]:
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
            
            # Create a more specific prompt for better results
            enhanced_prompt = f"""
            You are a credit card recommendation assistant. When asked about credit cards, always:
            1. Join tables to get complete card information (card names, bank names, reward rates)
            2. Order results by reward rate (highest first)
            3. Provide specific card names and bank names, not just IDs
            4. Include reward rates in your response
            5. Follow the style and format of the examples provided
            
            Database schema context:
            - credit_cards: user's cards with basic info
            - card_master_data: market cards with detailed info
            - card_merchant_rewards: specific merchant reward rates
            - merchants: merchant information
            
            For Amazon queries, check card_merchant_rewards table where merchant_name = 'amazon'
            {examples_context}
            Query: {query}
            """
            
            # Use LangChain agent to generate and execute SQL
            result = await self.agent.ainvoke({"input": enhanced_prompt})
            
            # Extract SQL query and results
            sql_query = result.get("intermediate_steps", [{}])[-1].get("tool_input", "")
            explanation = result.get("output", "")
            
            # Execute SQL to get actual results
            if sql_query:
                results = await self._execute_raw_sql(sql_query)
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
            result = await self.toolkit.db.arun(sql_query)
            
            # Parse results (this is a simplified version)
            # In a real implementation, you'd parse the result properly
            return [{"result": result}] if result else []
            
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}")
            return []
    
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
        """Format the response in natural language"""
        
        response_parts = []
        
        # Add explanation if requested
        if include_explanation and explanation:
            response_parts.append(explanation)
        
        # Add results summary
        if results:
            if len(results) > max_results:
                response_parts.append(f"I found {len(results)} results. Here are the top {max_results}:")
            else:
                response_parts.append(f"I found {len(results)} results:")
            
            # Add formatted results
            for i, result in enumerate(results[:max_results]):
                response_parts.append(f"{i+1}. {result}")
        
        # Add SQL query if requested
        if include_sql and sql_query:
            response_parts.append(f"\nGenerated SQL: {sql_query}")
        
        return "\n".join(response_parts) if response_parts else "I couldn't find any relevant information."
    
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
        if context:
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
