# 100 Gen AI Interview Questions for Senior Architect Role
## Based on SmartCards AI Project Implementation

### Part 2: LangChain, LangGraph & Advanced Architectures (Questions 26-50)

---

## 26. **What is LangChain and how would you integrate it into your SmartCards AI project?**

**Answer:** LangChain is a framework for building LLM applications with chains, agents, and memory.

**Example integration:**
```python
# LangChain integration for SmartCards AI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class SmartCardsLangChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are a credit card expert assistant. Use this information:
        
        User's cards: {user_cards}
        Merchant info: {merchant_info}
        Chat history: {chat_history}
        
        User question: {user_question}
        
        Provide a helpful recommendation.
        """)
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )
    
    async def get_recommendation(self, user_question: str, user_cards: List[Dict], 
                                merchant_info: Dict) -> str:
        response = await self.chain.arun(
            user_question=user_question,
            user_cards=user_cards,
            merchant_info=merchant_info
        )
        return response
```

---

## 27. **Explain the concept of LangChain agents and how you would implement them for credit card recommendations.**

**Answer:** LangChain agents use tools to perform actions and make decisions.

**Example implementation:**
```python
# LangChain agent for credit card recommendations
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from typing import Optional

class CardRecommendationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        # Define tools
        self.tools = [
            Tool(
                name="search_merchant_rewards",
                func=self._search_merchant_rewards,
                description="Search for reward rates for a specific merchant"
            ),
            Tool(
                name="get_user_cards",
                func=self._get_user_cards,
                description="Get user's credit card portfolio"
            ),
            Tool(
                name="check_current_offers",
                func=self._check_current_offers,
                description="Check current offers and promotions"
            ),
            Tool(
                name="calculate_rewards",
                func=self._calculate_rewards,
                description="Calculate potential rewards for a purchase"
            )
        ]
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )
    
    async def get_recommendation(self, user_query: str, user_id: int) -> str:
        # Set user context
        self.current_user_id = user_id
        
        # Run agent
        response = await self.agent.arun(user_query)
        return response
    
    async def _search_merchant_rewards(self, merchant: str) -> str:
        # Search vector database for merchant rewards
        results = await self.vector_db.search(f"rewards {merchant}")
        return f"Reward information for {merchant}: {results}"
    
    async def _get_user_cards(self, user_id: Optional[int] = None) -> str:
        user_id = user_id or self.current_user_id
        cards = await self._fetch_user_cards(user_id)
        return f"User's cards: {cards}"
    
    async def _check_current_offers(self, card_name: str) -> str:
        offers = await self._fetch_card_offers(card_name)
        return f"Current offers for {card_name}: {offers}"
    
    async def _calculate_rewards(self, card_name: str, amount: float, merchant: str) -> str:
        reward_rate = await self._get_reward_rate(card_name, merchant)
        reward_amount = amount * reward_rate
        return f"Potential reward: ₹{reward_amount:.2f} ({reward_rate*100}%)"
```

---

## 28. **How would you implement LangChain chains for complex credit card analysis workflows?**

**Answer:** Use sequential chains to break down complex tasks into steps.

**Example implementation:**
```python
# LangChain chains for credit card analysis
from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.prompts import PromptTemplate

class CreditCardAnalysisChains:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
        # Chain 1: Analyze user's spending pattern
        self.spending_analysis_prompt = PromptTemplate(
            input_variables=["user_transactions"],
            template="""
            Analyze this user's spending pattern:
            {user_transactions}
            
            Identify:
            1. Top spending categories
            2. Average transaction amounts
            3. Preferred merchants
            4. Spending frequency
            """
        )
        
        self.spending_chain = LLMChain(
            llm=self.llm,
            prompt=self.spending_analysis_prompt
        )
        
        # Chain 2: Generate card recommendations
        self.recommendation_prompt = PromptTemplate(
            input_variables=["spending_analysis", "user_cards", "merchant_info"],
            template="""
            Based on this spending analysis:
            {spending_analysis}
            
            User's current cards: {user_cards}
            Merchant information: {merchant_info}
            
            Provide specific card recommendations with:
            1. Which card to use for maximum rewards
            2. Alternative options
            3. Expected reward amounts
            4. Any limitations or conditions
            """
        )
        
        self.recommendation_chain = LLMChain(
            llm=self.llm,
            prompt=self.recommendation_prompt
        )
        
        # Combine chains
        self.full_chain = SimpleSequentialChain(
            chains=[self.spending_chain, self.recommendation_chain],
            verbose=True
        )
    
    async def analyze_and_recommend(self, user_transactions: List[Dict], 
                                   user_cards: List[Dict], merchant_info: Dict) -> str:
        # Prepare input for first chain
        spending_input = self._format_transactions(user_transactions)
        
        # Run the full chain
        result = await self.full_chain.arun(spending_input)
        
        # Add merchant info to final recommendation
        final_prompt = f"""
        {result}
        
        Additional merchant context: {merchant_info}
        
        Provide a final, actionable recommendation.
        """
        
        final_response = await self.llm.apredict(final_prompt)
        return final_response
```

---

## 29. **What is LangGraph and how would you use it to build a credit card recommendation workflow?**

**Answer:** LangGraph is a library for building stateful, multi-actor applications with LLMs.

**Example implementation:**
```python
# LangGraph workflow for credit card recommendations
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class CreditCardState(TypedDict):
    user_query: str
    user_cards: List[Dict]
    merchant_info: Dict
    spending_analysis: str
    card_recommendations: List[Dict]
    final_recommendation: str
    confidence_score: float

class CreditCardWorkflow:
    def __init__(self):
        self.workflow = StateGraph(CreditCardState)
        
        # Add nodes
        self.workflow.add_node("analyze_query", self._analyze_query)
        self.workflow.add_node("fetch_user_data", self._fetch_user_data)
        self.workflow.add_node("search_merchant_info", self._search_merchant_info)
        self.workflow.add_node("analyze_spending", self._analyze_spending)
        self.workflow.add_node("generate_recommendations", self._generate_recommendations)
        self.workflow.add_node("validate_recommendations", self._validate_recommendations)
        self.workflow.add_node("format_response", self._format_response)
        
        # Define edges
        self.workflow.set_entry_point("analyze_query")
        self.workflow.add_edge("analyze_query", "fetch_user_data")
        self.workflow.add_edge("fetch_user_data", "search_merchant_info")
        self.workflow.add_edge("search_merchant_info", "analyze_spending")
        self.workflow.add_edge("analyze_spending", "generate_recommendations")
        self.workflow.add_edge("generate_recommendations", "validate_recommendations")
        self.workflow.add_edge("validate_recommendations", "format_response")
        self.workflow.add_edge("format_response", END)
        
        self.app = self.workflow.compile()
    
    async def _analyze_query(self, state: CreditCardState) -> CreditCardState:
        """Analyze user query to understand intent"""
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        analysis_prompt = f"""
        Analyze this user query: {state['user_query']}
        
        Extract:
        1. Intent (recommendation, comparison, inquiry)
        2. Merchant mentioned
        3. Purchase amount (if any)
        4. Specific requirements
        """
        
        analysis = await llm.apredict(analysis_prompt)
        state["query_analysis"] = analysis
        return state
    
    async def _fetch_user_data(self, state: CreditCardState) -> CreditCardState:
        """Fetch user's credit card portfolio"""
        # This would fetch from database
        state["user_cards"] = await self._get_user_cards_from_db()
        return state
    
    async def _search_merchant_info(self, state: CreditCardState) -> CreditCardState:
        """Search for merchant-specific information"""
        merchant = self._extract_merchant(state["user_query"])
        merchant_info = await self.vector_db.search(merchant)
        state["merchant_info"] = merchant_info
        return state
    
    async def _analyze_spending(self, state: CreditCardState) -> CreditCardState:
        """Analyze user's spending patterns"""
        spending_data = await self._get_user_spending(state["user_id"])
        
        analysis_prompt = f"""
        Analyze spending patterns: {spending_data}
        User cards: {state["user_cards"]}
        
        Identify optimal card usage patterns.
        """
        
        analysis = await self.llm.apredict(analysis_prompt)
        state["spending_analysis"] = analysis
        return state
    
    async def _generate_recommendations(self, state: CreditCardState) -> CreditCardState:
        """Generate card recommendations"""
        recommendation_prompt = f"""
        Based on:
        - User query: {state["user_query"]}
        - User cards: {state["user_cards"]}
        - Merchant info: {state["merchant_info"]}
        - Spending analysis: {state["spending_analysis"]}
        
        Generate specific card recommendations with reward calculations.
        """
        
        recommendations = await self.llm.apredict(recommendation_prompt)
        state["card_recommendations"] = recommendations
        return state
    
    async def _validate_recommendations(self, state: CreditCardState) -> CreditCardState:
        """Validate recommendations against factual data"""
        validation_result = await self._validate_against_knowledge_base(
            state["card_recommendations"]
        )
        state["validation_result"] = validation_result
        return state
    
    async def _format_response(self, state: CreditCardState) -> CreditCardState:
        """Format final response"""
        final_prompt = f"""
        Format this recommendation for the user:
        {state["card_recommendations"]}
        
        Make it concise, actionable, and user-friendly.
        """
        
        final_response = await self.llm.apredict(final_prompt)
        state["final_recommendation"] = final_response
        return state
    
    async def run_workflow(self, user_query: str, user_id: int) -> str:
        """Run the complete workflow"""
        initial_state = CreditCardState(
            user_query=user_query,
            user_id=user_id,
            user_cards=[],
            merchant_info={},
            spending_analysis="",
            card_recommendations=[],
            final_recommendation="",
            confidence_score=0.0
        )
        
        result = await self.app.ainvoke(initial_state)
        return result["final_recommendation"]
```

---

## 30. **How would you implement a LangChain agent with custom tools for credit card operations?**

**Answer:** Create custom tools that integrate with your existing services.

**Example implementation:**
```python
# Custom LangChain tools for credit card operations
from langchain.tools import BaseTool
from typing import Optional
from pydantic import BaseModel, Field

class MerchantSearchInput(BaseModel):
    merchant_name: str = Field(description="Name of the merchant to search for")

class CardRecommendationInput(BaseModel):
    merchant: str = Field(description="Merchant name")
    amount: float = Field(description="Purchase amount")
    user_cards: List[str] = Field(description="User's credit cards")

class SmartCardsTools:
    class MerchantSearchTool(BaseTool):
        name = "merchant_search"
        description = "Search for merchant-specific reward information"
        args_schema = MerchantSearchInput
        
        def __init__(self, vector_db_service):
            super().__init__()
            self.vector_db = vector_db_service
        
        async def _arun(self, merchant_name: str) -> str:
            results = await self.vector_db.search(merchant_name)
            return f"Merchant rewards for {merchant_name}: {results}"
    
    class CardRecommendationTool(BaseTool):
        name = "card_recommendation"
        description = "Get credit card recommendation for a specific purchase"
        args_schema = CardRecommendationInput
        
        def __init__(self, ai_service):
            super().__init__()
            self.ai_service = ai_service
        
        async def _arun(self, merchant: str, amount: float, user_cards: List[str]) -> str:
            recommendation = await self.ai_service.get_card_recommendation(
                merchant=merchant,
                amount=amount,
                user_cards=user_cards
            )
            return recommendation
    
    class OfferCheckTool(BaseTool):
        name = "check_offers"
        description = "Check current offers and promotions for credit cards"
        
        async def _arun(self, card_name: str) -> str:
            offers = await self._fetch_current_offers(card_name)
            return f"Current offers for {card_name}: {offers}"
    
    class RewardCalculatorTool(BaseTool):
        name = "calculate_rewards"
        description = "Calculate potential rewards for a purchase"
        
        async def _arun(self, card_name: str, merchant: str, amount: float) -> str:
            reward_rate = await self._get_reward_rate(card_name, merchant)
            reward_amount = amount * reward_rate
            return f"Potential reward: ₹{reward_amount:.2f} ({reward_rate*100}%)"

# Agent with custom tools
class SmartCardsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
        # Initialize tools
        self.tools = [
            SmartCardsTools.MerchantSearchTool(vector_db_service),
            SmartCardsTools.CardRecommendationTool(ai_service),
            SmartCardsTools.OfferCheckTool(),
            SmartCardsTools.RewardCalculatorTool()
        ]
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True
        )
    
    async def get_recommendation(self, user_query: str, user_context: Dict) -> str:
        # Add user context to the query
        contextualized_query = f"""
        User context: {user_context}
        User question: {user_query}
        
        Use the available tools to provide the best recommendation.
        """
        
        response = await self.agent.arun(contextualized_query)
        return response
```

---

## 31. **How would you implement LangChain memory for maintaining conversation context in a credit card chatbot?**

**Answer:** Use different memory types based on conversation requirements.

**Example implementation:**
```python
# LangChain memory for credit card conversations
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory

class SmartCardsMemory:
    def __init__(self):
        # Short-term memory for recent conversation
        self.short_term_memory = ConversationBufferWindowMemory(
            k=5,  # Keep last 5 exchanges
            return_messages=True,
            memory_key="recent_history"
        )
        
        # Long-term memory for conversation summary
        self.long_term_memory = ConversationSummaryMemory(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            return_messages=True,
            memory_key="conversation_summary"
        )
        
        # Redis-based persistent memory
        self.persistent_memory = RedisChatMessageHistory(
            session_id="user_session",
            url="redis://localhost:6379"
        )
    
    async def add_user_message(self, message: str, user_id: int):
        """Add user message to all memory types"""
        # Add to short-term memory
        self.short_term_memory.chat_memory.add_user_message(message)
        
        # Add to long-term memory
        self.long_term_memory.chat_memory.add_user_message(message)
        
        # Add to persistent memory
        await self.persistent_memory.add_user_message(message)
    
    async def add_ai_message(self, message: str, user_id: int):
        """Add AI response to all memory types"""
        self.short_term_memory.chat_memory.add_ai_message(message)
        self.long_term_memory.chat_memory.add_ai_message(message)
        await self.persistent_memory.add_ai_message(message)
    
    def get_conversation_context(self) -> Dict:
        """Get combined conversation context"""
        return {
            "recent_history": self.short_term_memory.load_memory_variables({}),
            "conversation_summary": self.long_term_memory.load_memory_variables({}),
            "persistent_history": self.persistent_memory.messages
        }

# Enhanced chatbot with memory
class MemoryEnhancedChatbot:
    def __init__(self):
        self.memory = SmartCardsMemory()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are SmartCards AI, a credit card expert assistant.
        
        Conversation Summary: {conversation_summary}
        Recent History: {recent_history}
        
        User's cards: {user_cards}
        Current question: {user_question}
        
        Provide a contextual response that builds on our conversation.
        """)
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory.short_term_memory
        )
    
    async def chat(self, user_message: str, user_id: int, user_cards: List[Dict]) -> str:
        # Add message to memory
        await self.memory.add_user_message(user_message, user_id)
        
        # Get conversation context
        context = self.memory.get_conversation_context()
        
        # Generate response
        response = await self.chain.arun(
            user_question=user_message,
            user_cards=user_cards,
            conversation_summary=context["conversation_summary"],
            recent_history=context["recent_history"]
        )
        
        # Add response to memory
        await self.memory.add_ai_message(response, user_id)
        
        return response
```

---

## 32. **How would you implement LangChain callbacks for monitoring and logging in production?**

**Answer:** Use callbacks to track performance, costs, and user interactions.

**Example implementation:**
```python
# LangChain callbacks for monitoring
from langchain.callbacks import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
import time
import json

class SmartCardsCallbackHandler(BaseCallbackHandler):
    def __init__(self, user_id: int, session_id: str):
        self.user_id = user_id
        self.session_id = session_id
        self.start_time = None
        self.token_usage = {}
        self.costs = {}
    
    def on_llm_start(self, serialized: Dict, prompts: List[str], **kwargs):
        """Called when LLM starts"""
        self.start_time = time.time()
        print(f"LLM started for user {self.user_id}")
    
    def on_llm_end(self, response, **kwargs):
        """Called when LLM ends"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        # Log token usage and costs
        if hasattr(response, 'llm_output') and response.llm_output:
            self.token_usage = response.llm_output.get('token_usage', {})
            self.costs = self._calculate_costs(self.token_usage)
        
        # Log to monitoring system
        self._log_llm_usage(duration)
    
    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs):
        """Called when LLM errors"""
        print(f"LLM error for user {self.user_id}: {error}")
        self._log_error(error)
    
    def on_chain_start(self, serialized: Dict, inputs: Dict, **kwargs):
        """Called when chain starts"""
        print(f"Chain started: {serialized.get('name', 'unknown')}")
    
    def on_chain_end(self, outputs: Dict, **kwargs):
        """Called when chain ends"""
        print(f"Chain completed with {len(outputs)} outputs")
    
    def on_tool_start(self, serialized: Dict, input_str: str, **kwargs):
        """Called when tool starts"""
        print(f"Tool started: {serialized.get('name', 'unknown')}")
    
    def on_tool_end(self, output: str, **kwargs):
        """Called when tool ends"""
        print(f"Tool completed with output length: {len(output)}")
    
    def _calculate_costs(self, token_usage: Dict) -> Dict:
        """Calculate costs based on token usage"""
        # OpenAI pricing (example)
        input_cost_per_1k = 0.03
        output_cost_per_1k = 0.06
        
        input_tokens = token_usage.get('prompt_tokens', 0)
        output_tokens = token_usage.get('completion_tokens', 0)
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }
    
    def _log_llm_usage(self, duration: float):
        """Log LLM usage to monitoring system"""
        log_data = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "duration": duration,
            "token_usage": self.token_usage,
            "costs": self.costs,
            "timestamp": time.time()
        }
        
        # Send to monitoring system (e.g., Prometheus, DataDog)
        print(f"Usage logged: {json.dumps(log_data, indent=2)}")
    
    def _log_error(self, error: Exception):
        """Log errors to monitoring system"""
        error_data = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "error": str(error),
            "error_type": type(error).__name__,
            "timestamp": time.time()
        }
        
        # Send to error tracking system (e.g., Sentry)
        print(f"Error logged: {json.dumps(error_data, indent=2)}")

# Enhanced agent with callbacks
class MonitoredSmartCardsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            callbacks=[]  # Will be set per request
        )
        
        self.tools = [
            SmartCardsTools.MerchantSearchTool(vector_db_service),
            SmartCardsTools.CardRecommendationTool(ai_service)
        ]
    
    async def get_recommendation(self, user_query: str, user_id: int, session_id: str) -> str:
        # Create callback handler for this request
        callback_handler = SmartCardsCallbackHandler(user_id, session_id)
        callback_manager = CallbackManager([callback_handler])
        
        # Set callbacks for this request
        self.llm.callbacks = [callback_handler]
        
        # Initialize agent with callbacks
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=True,
            callback_manager=callback_manager
        )
        
        # Run agent
        response = await agent.arun(user_query)
        return response
```

---

## 33. **How would you implement LangChain document loaders for processing credit card information?**

**Answer:** Use document loaders to process structured and unstructured credit card data.

**Example implementation:**
```python
# LangChain document loaders for credit card data
from langchain.document_loaders import CSVLoader, JSONLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class CreditCardDataProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = OpenAIEmbeddings()
    
    async def process_credit_card_database(self, file_path: str) -> List[Document]:
        """Process credit card database CSV"""
        loader = CSVLoader(
            file_path=file_path,
            csv_args={
                "delimiter": ",",
                "quotechar": '"',
                "fieldnames": ["card_name", "bank", "reward_rate", "annual_fee", "features"]
            }
        )
        
        documents = loader.load()
        
        # Transform CSV data into structured documents
        processed_docs = []
        for doc in documents:
            # Create structured content
            content = f"""
            Credit Card: {doc.page_content}
            
            Key Information:
            - Card Name: {doc.metadata.get('card_name', 'N/A')}
            - Bank: {doc.metadata.get('bank', 'N/A')}
            - Reward Rate: {doc.metadata.get('reward_rate', 'N/A')}
            - Annual Fee: {doc.metadata.get('annual_fee', 'N/A')}
            - Features: {doc.metadata.get('features', 'N/A')}
            """
            
            processed_doc = Document(
                page_content=content,
                metadata=doc.metadata
            )
            processed_docs.append(processed_doc)
        
        return processed_docs
    
    async def process_merchant_rewards_data(self, json_file_path: str) -> List[Document]:
        """Process merchant rewards JSON data"""
        loader = JSONLoader(
            file_path=json_file_path,
            jq_schema='.[]',
            text_content=False
        )
        
        documents = loader.load()
        
        # Process merchant data
        processed_docs = []
        for doc in documents:
            merchant_data = doc.metadata
            
            content = f"""
            Merchant: {merchant_data.get('merchant_name', 'N/A')}
            Category: {merchant_data.get('category', 'N/A')}
            Reward Rates:
            {self._format_reward_rates(merchant_data.get('reward_rates', {}))}
            
            Special Offers: {merchant_data.get('special_offers', 'None')}
            """
            
            processed_doc = Document(
                page_content=content,
                metadata=merchant_data
            )
            processed_docs.append(processed_doc)
        
        return processed_docs
    
    async def process_card_terms_documents(self, terms_directory: str) -> List[Document]:
        """Process credit card terms and conditions documents"""
        documents = []
        
        # Load text documents
        text_loader = TextLoader(f"{terms_directory}/card_terms.txt")
        text_docs = text_loader.load()
        
        # Split into chunks
        split_docs = self.text_splitter.split_documents(text_docs)
        documents.extend(split_docs)
        
        return documents
    
    def _format_reward_rates(self, reward_rates: Dict) -> str:
        """Format reward rates for document content"""
        formatted = []
        for card_type, rate in reward_rates.items():
            formatted.append(f"- {card_type}: {rate}%")
        return "\n".join(formatted)
    
    async def create_vector_store(self, documents: List[Document], collection_name: str):
        """Create vector store from processed documents"""
        # Split documents if needed
        split_docs = self.text_splitter.split_documents(documents)
        
        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            collection_name=collection_name
        )
        
        return vectorstore
    
    async def update_knowledge_base(self):
        """Update the entire knowledge base"""
        # Process different data sources
        card_docs = await self.process_credit_card_database("data/credit_cards.csv")
        merchant_docs = await self.process_merchant_rewards_data("data/merchant_rewards.json")
        terms_docs = await self.process_card_terms_documents("data/terms/")
        
        # Create vector stores
        card_vectorstore = await self.create_vector_store(card_docs, "credit_cards")
        merchant_vectorstore = await self.create_vector_store(merchant_docs, "merchants")
        terms_vectorstore = await self.create_vector_store(terms_docs, "terms")
        
        return {
            "credit_cards": card_vectorstore,
            "merchants": merchant_vectorstore,
            "terms": terms_vectorstore
        }
```

---

## 34. **How would you implement LangChain output parsers for structured credit card recommendations?**

**Answer:** Use output parsers to ensure consistent, structured responses.

**Example implementation:**
```python
# LangChain output parsers for structured responses
from langchain.output_parsers import PydanticOutputParser, ResponseSchema, StructuredOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

class CardRecommendation(BaseModel):
    recommended_card: str = Field(description="Name of the recommended credit card")
    reward_rate: float = Field(description="Reward rate percentage")
    expected_reward: float = Field(description="Expected reward amount")
    reasoning: str = Field(description="Reason for recommendation")
    alternatives: List[str] = Field(description="Alternative card options")
    limitations: Optional[str] = Field(description="Any limitations or conditions")

class MerchantAnalysis(BaseModel):
    merchant_name: str = Field(description="Name of the merchant")
    category: str = Field(description="Merchant category")
    best_cards: List[str] = Field(description="Best cards for this merchant")
    average_reward_rate: float = Field(description="Average reward rate")
    special_offers: List[str] = Field(description="Current special offers")

class SmartCardsOutputParser:
    def __init__(self):
        # Pydantic parser for card recommendations
        self.card_parser = PydanticOutputParser(pydantic_object=CardRecommendation)
        
        # Pydantic parser for merchant analysis
        self.merchant_parser = PydanticOutputParser(pydantic_object=MerchantAnalysis)
        
        # Structured parser for general responses
        self.general_parser = StructuredOutputParser.from_response_schemas([
            ResponseSchema(name="recommendation", description="Main recommendation"),
            ResponseSchema(name="confidence", description="Confidence score (0-1)"),
            ResponseSchema(name="supporting_info", description="Supporting information"),
            ResponseSchema(name="next_steps", description="Suggested next steps")
        ])
    
    def get_card_recommendation_prompt(self) -> str:
        """Get prompt template for card recommendations"""
        return f"""
        Provide a credit card recommendation in the following format:
        
        {self.card_parser.get_format_instructions()}
        
        User query: {{user_query}}
        User's cards: {{user_cards}}
        Merchant info: {{merchant_info}}
        """
    
    def get_merchant_analysis_prompt(self) -> str:
        """Get prompt template for merchant analysis"""
        return f"""
        Analyze the merchant and provide information in this format:
        
        {self.merchant_parser.get_format_instructions()}
        
        Merchant: {{merchant_name}}
        User context: {{user_context}}
        """
    
    def get_general_response_prompt(self) -> str:
        """Get prompt template for general responses"""
        return f"""
        Provide a response in this format:
        
        {self.general_parser.get_format_instructions()}
        
        User question: {{user_question}}
        """
    
    async def parse_card_recommendation(self, llm_response: str) -> CardRecommendation:
        """Parse LLM response into structured card recommendation"""
        try:
            return self.card_parser.parse(llm_response)
        except Exception as e:
            # Fallback parsing
            return await self._fallback_parse_card_recommendation(llm_response)
    
    async def parse_merchant_analysis(self, llm_response: str) -> MerchantAnalysis:
        """Parse LLM response into structured merchant analysis"""
        try:
            return self.merchant_parser.parse(llm_response)
        except Exception as e:
            # Fallback parsing
            return await self._fallback_parse_merchant_analysis(llm_response)
    
    async def parse_general_response(self, llm_response: str) -> Dict:
        """Parse LLM response into structured general response"""
        try:
            return self.general_parser.parse(llm_response)
        except Exception as e:
            # Fallback to simple response
            return {
                "recommendation": llm_response,
                "confidence": 0.5,
                "supporting_info": "",
                "next_steps": ""
            }
    
    async def _fallback_parse_card_recommendation(self, response: str) -> CardRecommendation:
        """Fallback parsing when structured parsing fails"""
        # Use regex or simple text processing
        import re
        
        card_match = re.search(r"recommend.*?([A-Za-z\s]+card)", response, re.IGNORECASE)
        rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", response)
        
        return CardRecommendation(
            recommended_card=card_match.group(1) if card_match else "Unknown",
            reward_rate=float(rate_match.group(1)) if rate_match else 0.0,
            expected_reward=0.0,
            reasoning=response[:200],
            alternatives=[],
            limitations=""
        )

# Enhanced chatbot with output parsing
class StructuredSmartCardsChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        self.parser = SmartCardsOutputParser()
        
        # Create prompt templates
        self.card_prompt = ChatPromptTemplate.from_template(
            self.parser.get_card_recommendation_prompt()
        )
        
        self.merchant_prompt = ChatPromptTemplate.from_template(
            self.parser.get_merchant_analysis_prompt()
        )
        
        self.general_prompt = ChatPromptTemplate.from_template(
            self.parser.get_general_response_prompt()
        )
    
    async def get_structured_recommendation(self, user_query: str, user_cards: List[Dict], 
                                          merchant_info: Dict) -> CardRecommendation:
        """Get structured card recommendation"""
        # Generate response
        response = await self.llm.apredict(
            self.card_prompt.format(
                user_query=user_query,
                user_cards=user_cards,
                merchant_info=merchant_info
            )
        )
        
        # Parse response
        return await self.parser.parse_card_recommendation(response)
    
    async def get_merchant_analysis(self, merchant_name: str, user_context: Dict) -> MerchantAnalysis:
        """Get structured merchant analysis"""
        response = await self.llm.apredict(
            self.merchant_prompt.format(
                merchant_name=merchant_name,
                user_context=user_context
            )
        )
        
        return await self.parser.parse_merchant_analysis(response)
    
    async def get_general_response(self, user_question: str) -> Dict:
        """Get structured general response"""
        response = await self.llm.apredict(
            self.general_prompt.format(user_question=user_question)
        )
        
        return await self.parser.parse_general_response(response)
```

---

## 35. **How would you implement LangChain retriever chains for credit card information retrieval?**

**Answer:** Use retriever chains to combine vector search with LLM processing.

**Example implementation:**
```python
# LangChain retriever chains for credit card information
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.retrievers import VectorStoreRetriever
from langchain.vectorstores import Chroma

class SmartCardsRetrieverChains:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
        # Initialize vector stores
        self.card_vectorstore = Chroma(
            collection_name="credit_cards",
            embedding_function=OpenAIEmbeddings()
        )
        
        self.merchant_vectorstore = Chroma(
            collection_name="merchants",
            embedding_function=OpenAIEmbeddings()
        )
        
        # Create retrievers
        self.card_retriever = VectorStoreRetriever(
            vectorstore=self.card_vectorstore,
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        self.merchant_retriever = VectorStoreRetriever(
            vectorstore=self.merchant_vectorstore,
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Create retrieval chains
        self.card_qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.card_retriever,
            return_source_documents=True
        )
        
        self.merchant_qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.merchant_retriever,
            return_source_documents=True
        )
        
        # Conversational retrieval chain
        self.conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.card_retriever,
            return_source_documents=True,
            verbose=True
        )
    
    async def get_card_information(self, query: str) -> Dict:
        """Get credit card information using retrieval QA"""
        response = await self.card_qa_chain.arun(query)
        
        # Extract source documents
        source_docs = self.card_qa_chain.source_documents
        
        return {
            "answer": response,
            "sources": [doc.page_content for doc in source_docs],
            "metadata": [doc.metadata for doc in source_docs]
        }
    
    async def get_merchant_information(self, query: str) -> Dict:
        """Get merchant information using retrieval QA"""
        response = await self.merchant_qa_chain.arun(query)
        
        source_docs = self.merchant_qa_chain.source_documents
        
        return {
            "answer": response,
            "sources": [doc.page_content for doc in source_docs],
            "metadata": [doc.metadata for doc in source_docs]
        }
    
    async def conversational_search(self, question: str, chat_history: List[Dict]) -> Dict:
        """Perform conversational search"""
        # Convert chat history to LangChain format
        lc_history = []
        for msg in chat_history:
            if msg["role"] == "user":
                lc_history.append((msg["content"], ""))
            else:
                if lc_history:
                    lc_history[-1] = (lc_history[-1][0], msg["content"])
        
        response = await self.conversational_chain.acall({
            "question": question,
            "chat_history": lc_history
        })
        
        return {
            "answer": response["answer"],
            "sources": [doc.page_content for doc in response["source_documents"]],
            "chat_history": lc_history
        }
    
    async def hybrid_search(self, query: str, user_cards: List[Dict]) -> Dict:
        """Perform hybrid search combining multiple retrievers"""
        # Search both card and merchant information
        card_result = await self.get_card_information(query)
        merchant_result = await self.get_merchant_information(query)
        
        # Combine results
        combined_context = f"""
        Card Information: {card_result['answer']}
        Merchant Information: {merchant_result['answer']}
        User's Cards: {user_cards}
        """
        
        # Generate final response
        final_prompt = f"""
        Based on this information:
        {combined_context}
        
        Answer the user's question: {query}
        
        Provide a comprehensive response that considers both card and merchant information.
        """
        
        final_response = await self.llm.apredict(final_prompt)
        
        return {
            "answer": final_response,
            "card_sources": card_result["sources"],
            "merchant_sources": merchant_result["sources"],
            "combined_context": combined_context
        }
    
    async def update_retrievers(self, new_documents: List[Document], collection: str):
        """Update retrievers with new documents"""
        if collection == "credit_cards":
            self.card_vectorstore.add_documents(new_documents)
        elif collection == "merchants":
            self.merchant_vectorstore.add_documents(new_documents)
        
        # Refresh retrievers
        self.card_retriever = VectorStoreRetriever(
            vectorstore=self.card_vectorstore,
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        self.merchant_retriever = VectorStoreRetriever(
            vectorstore=self.merchant_vectorstore,
            search_type="similarity",
            search_kwargs={"k": 3}
        )
```

---

*Continue to Part 3 for Deployment, CI/CD, and Production Considerations...*