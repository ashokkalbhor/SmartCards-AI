# 100 Gen AI Interview Questions for Senior Architect Role
## Based on SmartCards AI Project Implementation

### Part 1: Foundational Concepts & OpenAI (Questions 1-25)

---

## 1. **Explain the difference between traditional ML and Generative AI. How does your SmartCards AI project leverage both?**

**Answer:** Traditional ML focuses on pattern recognition and prediction, while Gen AI creates new content. In SmartCards AI, we use:
- **Traditional ML**: Pattern matching for merchant recognition, query classification
- **Gen AI**: OpenAI GPT for generating personalized card recommendations

**Example from project:**
```python
# Traditional ML - Pattern matching in query_matcher.py
def match_query(self, query: str) -> Optional[str]:
    patterns = {
        "merchant_recommendation": r"best.*(?:card|credit).*for.*(swiggy|amazon|croma)",
        "card_list": r"(?:show|list|my).*(?:cards|credit cards)",
        "reward_inquiry": r"(?:rewards|cashback|points).*(?:earn|get)"
    }
    
# Gen AI - OpenAI integration in ai_service.py
async def _generate_llm_response(self, query: str, user_cards: List[Dict], 
                                vector_results: List[Dict], conversation_id: int, db: AsyncSession):
    prompt = self._build_contextual_prompt(query, user_cards, vector_results)
    response = await self.openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
```

---

## 2. **How do you handle API rate limiting and costs in production Gen AI applications?**

**Answer:** Implement caching, request batching, and fallback mechanisms.

**Example from SmartCards AI:**
```python
# Enhanced caching in enhanced_chatbot_service.py
async def process_query(self, user_id: int, query: str, conversation_id: Optional[int] = None):
    # Step 1: Check cache first
    cache_key = self._generate_cache_key(user_id, query)
    cached_response = await self.cache.get(cache_key)
    if cached_response:
        return {**cached_response, "source": "cache", "api_calls_saved": 1}
    
    # Step 2: Pattern matching to avoid LLM calls
    query_type = self.query_matcher.match_query(query)
    if query_type == "simple":
        return await self._handle_simple_query(user_id, query, query_type, db)
    
    # Step 3: LLM fallback only when necessary
    return await self._handle_complex_query(user_id, query, conversation_id, db)
```

---

## 3. **Explain the concept of prompt engineering. How do you design effective prompts for credit card recommendations?**

**Answer:** Prompt engineering involves crafting inputs to get desired outputs from LLMs.

**Example from SmartCards AI:**
```python
# Contextual prompt building in ai_service.py
def _build_contextual_prompt(self, query: str, user_cards: List[Dict], 
                            vector_results: List[Dict]) -> str:
    prompt = f"""
    You are a credit card expert assistant. The user has these cards: {user_cards}
    
    Relevant information from our database: {vector_results}
    
    User question: {query}
    
    Provide a helpful, accurate response focusing on:
    1. Which card to use for maximum rewards
    2. Current offers and benefits
    3. Alternative options if available
    
    Keep response under 200 words and be specific about reward percentages.
    """
    return prompt
```

---

## 4. **What are the key differences between GPT-3.5 and GPT-4? When would you choose one over the other?**

**Answer:** 
- **GPT-4**: Better reasoning, larger context, more accurate
- **GPT-3.5**: Faster, cheaper, sufficient for simple tasks

**Example from SmartCards AI:**
```python
# Model selection based on query complexity
async def _select_model(self, query_complexity: str, user_tier: str) -> str:
    if query_complexity == "complex" or user_tier == "premium":
        return "gpt-4"
    else:
        return "gpt-3.5-turbo"  # Cost-effective for simple queries
```

---

## 5. **How do you implement conversation memory and context management in a chatbot?**

**Answer:** Store conversation history and include relevant context in prompts.

**Example from SmartCards AI:**
```python
# Conversation management in chatbot.py
async def get_conversation_context(self, conversation_id: int, max_history: int = 5):
    messages = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.conversation_id == conversation_id)
        .order_by(ConversationMessage.created_at.desc())
        .limit(max_history)
    )
    
    context = []
    for msg in messages.scalars():
        context.append({
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.created_at
        })
    
    return context[::-1]  # Reverse to chronological order
```

---

## 6. **Explain the concept of function calling in OpenAI. How would you implement it for credit card operations?**

**Answer:** Function calling allows LLMs to invoke specific functions with structured parameters.

**Example implementation:**
```python
# Function calling for card operations
functions = [
    {
        "name": "get_card_recommendation",
        "description": "Get credit card recommendation for a merchant",
        "parameters": {
            "type": "object",
            "properties": {
                "merchant": {"type": "string", "description": "Merchant name"},
                "spend_amount": {"type": "number", "description": "Expected spend amount"},
                "user_cards": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["merchant"]
        }
    }
]

response = await openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Best card for Amazon purchase?"}],
    functions=functions,
    function_call="auto"
)
```

---

## 7. **How do you handle hallucinations in LLM responses? What strategies do you implement?**

**Answer:** Use retrieval-augmented generation (RAG), fact-checking, and confidence scoring.

**Example from SmartCards AI:**
```python
# RAG implementation in ai_service.py
async def _search_vector_db(self, query: str) -> List[Dict]:
    # Search vector database for factual information
    results = await self.vector_db.search_all_collections(
        query=query,
        n_results=5
    )
    return results

async def _generate_llm_response(self, query: str, user_cards: List[Dict], 
                                vector_results: List[Dict]):
    # Include factual data in prompt to reduce hallucinations
    factual_context = self._extract_facts(vector_results)
    prompt = f"Based on this factual information: {factual_context}\n\nUser question: {query}"
    
    # Add confidence scoring
    confidence = self._calculate_confidence(vector_results, query)
    if confidence < 0.7:
        return {"response": "I need more information to provide an accurate answer.", "confidence": confidence}
```

---

## 8. **What is the role of embeddings in Gen AI applications? How do you implement them?**

**Answer:** Embeddings convert text to vectors for semantic search and similarity matching.

**Example from SmartCards AI:**
```python
# Vector database service in vector_db.py
class VectorDBService:
    def __init__(self):
        self.client = chromadb.Client()
        self.collections = {
            "credit_cards": self.client.get_or_create_collection("credit_cards"),
            "merchants": self.client.get_or_create_collection("merchants"),
            "rewards": self.client.get_or_create_collection("rewards")
        }
    
    async def add_document(self, collection: str, document: str, metadata: Dict):
        embedding = self._generate_embedding(document)
        self.collections[collection].add(
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata]
        )
    
    async def search(self, query: str, collection: str, n_results: int = 5):
        query_embedding = self._generate_embedding(query)
        results = self.collections[collection].query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
```

---

## 9. **How do you implement streaming responses in a chatbot? What are the benefits?**

**Answer:** Streaming provides real-time responses and better user experience.

**Example implementation:**
```python
# Streaming chat endpoint
@router.post("/chat/stream")
async def stream_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    async def generate():
        async for chunk in openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.message}],
            stream=True
        ):
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")
```

---

## 10. **Explain the concept of fine-tuning vs. prompt engineering. When would you use each?**

**Answer:** 
- **Prompt engineering**: Quick, flexible, no training required
- **Fine-tuning**: Better performance, domain-specific, requires training data

**Example from SmartCards AI:**
```python
# Prompt engineering approach (current implementation)
def _build_specialized_prompt(self, query_type: str, context: Dict) -> str:
    if query_type == "merchant_recommendation":
        return f"""
        As a credit card expert, recommend the best card for {context['merchant']}.
        User cards: {context['user_cards']}
        Current offers: {context['offers']}
        Focus on reward percentages and cashback rates.
        """
    
    # Fine-tuning would require:
    # 1. Collect training data from user interactions
    # 2. Create fine-tuned model for credit card domain
    # 3. Deploy fine-tuned model for better performance
```

---

## 11. **How do you implement multi-modal AI in your application? What are the challenges?**

**Answer:** Multi-modal AI processes text, images, and other data types together.

**Example implementation:**
```python
# Multi-modal credit card analysis
async def analyze_card_image(self, image_data: bytes, user_query: str):
    # Extract text from card image
    card_text = await self._extract_text_from_image(image_data)
    
    # Analyze card features
    card_features = await self._analyze_card_features(image_data)
    
    # Combine with user query for comprehensive response
    combined_prompt = f"""
    Card information: {card_text}
    Visual features: {card_features}
    User question: {user_query}
    
    Provide detailed analysis and recommendations.
    """
    
    response = await self.openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": combined_prompt}],
        max_tokens=500
    )
```

---

## 12. **What is the role of temperature and top_p parameters in LLM generation?**

**Answer:** 
- **Temperature**: Controls randomness (0 = deterministic, 1 = creative)
- **Top_p**: Controls diversity by sampling from top probability mass

**Example from SmartCards AI:**
```python
# Parameter selection based on use case
def _select_generation_params(self, query_type: str) -> Dict:
    if query_type == "factual_recommendation":
        return {"temperature": 0.1, "top_p": 0.9}  # More deterministic
    elif query_type == "creative_suggestion":
        return {"temperature": 0.7, "top_p": 0.8}  # More creative
    else:
        return {"temperature": 0.3, "top_p": 0.9}  # Balanced
```

---

## 13. **How do you implement A/B testing for different prompt strategies?**

**Answer:** Use feature flags and metrics tracking to compare prompt effectiveness.

**Example implementation:**
```python
# A/B testing for prompts
class PromptABTest:
    def __init__(self):
        self.variants = {
            "A": self._build_prompt_variant_a,
            "B": self._build_prompt_variant_b,
            "C": self._build_prompt_variant_c
        }
    
    async def get_response(self, user_id: int, query: str):
        variant = self._assign_variant(user_id)
        prompt = self.variants[variant](query)
        
        response = await self._generate_response(prompt)
        
        # Track metrics
        await self._track_metrics(user_id, variant, query, response)
        
        return response
    
    async def _track_metrics(self, user_id: int, variant: str, query: str, response: str):
        metrics = {
            "user_id": user_id,
            "variant": variant,
            "query_length": len(query),
            "response_length": len(response),
            "timestamp": datetime.now(),
            "user_satisfaction": await self._get_user_feedback(user_id)
        }
        await self._store_metrics(metrics)
```

---

## 14. **Explain the concept of few-shot learning in prompt engineering.**

**Answer:** Few-shot learning provides examples in the prompt to guide the model's response format.

**Example from SmartCards AI:**
```python
# Few-shot prompt for card recommendations
def _build_few_shot_prompt(self, query: str) -> str:
    prompt = f"""
    You are a credit card expert. Here are examples of good responses:
    
    User: "Best card for Amazon?"
    Assistant: "For Amazon purchases, I recommend the Amazon Pay ICICI Credit Card which offers 5% cashback on Amazon and 2% on other purchases. If you don't have it, use your highest cashback card."
    
    User: "Which card for dining?"
    Assistant: "For dining, use cards with dining rewards like HDFC Diners Club (3X rewards) or SBI SimplyCLICK (10X rewards on dining). Check your cards for dining-specific offers."
    
    User: "{query}"
    Assistant:"""
    return prompt
```

---

## 15. **How do you implement content moderation in AI-generated responses?**

**Answer:** Use content filters, keyword detection, and human review workflows.

**Example implementation:**
```python
# Content moderation in ai_service.py
class ContentModerator:
    def __init__(self):
        self.blocked_keywords = ["fraud", "hack", "illegal", "scam"]
        self.sensitive_patterns = [
            r"password.*reset",
            r"account.*number",
            r"cvv.*code"
        ]
    
    async def moderate_response(self, response: str) -> Dict:
        # Check for blocked keywords
        for keyword in self.blocked_keywords:
            if keyword.lower() in response.lower():
                return {"approved": False, "reason": f"Contains blocked keyword: {keyword}"}
        
        # Check for sensitive patterns
        for pattern in self.sensitive_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return {"approved": False, "reason": "Contains sensitive information pattern"}
        
        # Check response length
        if len(response) > 1000:
            return {"approved": False, "reason": "Response too long"}
        
        return {"approved": True, "response": response}
```

---

## 16. **What is the role of system prompts in chat applications?**

**Answer:** System prompts define the AI's role, behavior, and constraints.

**Example from SmartCards AI:**
```python
# System prompt definition
SYSTEM_PROMPT = """
You are SmartCards AI, an expert credit card assistant. Your role is to:

1. Help users choose the best credit card for their purchases
2. Provide accurate reward and cashback information
3. Suggest optimal card usage strategies
4. Answer questions about credit card benefits and features

Guidelines:
- Always prioritize user's existing cards first
- Provide specific reward percentages when possible
- Mention current offers and promotions
- Keep responses concise and actionable
- Never provide financial advice beyond card recommendations
- Always verify information from reliable sources

Your responses should be helpful, accurate, and focused on maximizing user rewards.
"""
```

---

## 17. **How do you implement conversation summarization for long chat sessions?**

**Answer:** Use LLM to summarize conversation history and maintain context.

**Example implementation:**
```python
# Conversation summarization
async def summarize_conversation(self, conversation_id: int, db: AsyncSession):
    messages = await self._get_conversation_messages(conversation_id, db)
    
    if len(messages) > 10:  # Summarize if conversation is long
        conversation_text = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
        
        summary_prompt = f"""
        Summarize this credit card conversation in 2-3 sentences:
        {conversation_text}
        
        Focus on:
        - User's card portfolio
        - Key questions asked
        - Recommendations given
        """
        
        summary_response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=100
        )
        
        return summary_response.choices[0].message.content
    
    return None
```

---

## 18. **Explain the concept of chain-of-thought prompting.**

**Answer:** Chain-of-thought prompting encourages the model to show its reasoning process.

**Example from SmartCards AI:**
```python
# Chain-of-thought prompt for complex recommendations
def _build_cot_prompt(self, query: str, user_cards: List[Dict], merchant_info: Dict) -> str:
    prompt = f"""
    Let's think through this step by step:
    
    User question: {query}
    User's cards: {user_cards}
    Merchant information: {merchant_info}
    
    Step 1: What type of purchase is this?
    Step 2: Which cards offer rewards for this category?
    Step 3: What are the current offers and limits?
    Step 4: Which card provides the highest value?
    Step 5: Are there any restrictions or conditions?
    
    Based on this analysis, provide a clear recommendation.
    """
    return prompt
```

---

## 19. **How do you implement response caching in AI applications?**

**Answer:** Cache responses based on query similarity and user context.

**Example from SmartCards AI:**
```python
# Response caching in cache.py
class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    async def get(self, key: str) -> Optional[Dict]:
        cached = self.redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    async def set(self, key: str, value: Dict, ttl: int = 1800):
        self.redis_client.setex(key, ttl, json.dumps(value))
    
    def _generate_cache_key(self, user_id: int, query: str) -> str:
        # Normalize query for better cache hits
        normalized_query = self._normalize_query(query)
        return f"chat:{user_id}:{hash(normalized_query)}"
    
    def _normalize_query(self, query: str) -> str:
        # Remove case, extra spaces, common variations
        return re.sub(r'\s+', ' ', query.lower().strip())
```

---

## 20. **What is the role of confidence scoring in AI responses?**

**Answer:** Confidence scoring helps determine response reliability and when to fall back to human support.

**Example from SmartCards AI:**
```python
# Confidence scoring implementation
class ConfidenceScorer:
    def calculate_confidence(self, response: Dict, context: Dict) -> float:
        factors = {
            "vector_match_score": self._get_vector_match_score(context),
            "response_specificity": self._get_specificity_score(response),
            "source_reliability": self._get_source_reliability(context),
            "user_feedback_history": self._get_user_feedback_score(context)
        }
        
        # Weighted average of confidence factors
        weights = {
            "vector_match_score": 0.4,
            "response_specificity": 0.3,
            "source_reliability": 0.2,
            "user_feedback_history": 0.1
        }
        
        confidence = sum(factors[key] * weights[key] for key in factors)
        return min(confidence, 1.0)
    
    def _get_vector_match_score(self, context: Dict) -> float:
        # Higher score if vector search found relevant documents
        if context.get("vector_results"):
            return min(len(context["vector_results"]) / 5.0, 1.0)
        return 0.0
```

---

## 21. **How do you implement multi-turn conversation handling?**

**Answer:** Maintain conversation state and include relevant history in prompts.

**Example from SmartCards AI:**
```python
# Multi-turn conversation in chatbot.py
async def handle_conversation_turn(self, user_id: int, message: str, conversation_id: int):
    # Get conversation history
    history = await self._get_conversation_history(conversation_id, max_turns=5)
    
    # Build context-aware prompt
    context_prompt = self._build_contextual_prompt(message, history)
    
    # Generate response
    response = await self._generate_response(context_prompt)
    
    # Save to conversation
    await self._save_conversation_turn(conversation_id, "user", message)
    await self._save_conversation_turn(conversation_id, "assistant", response)
    
    return response

def _build_contextual_prompt(self, current_message: str, history: List[Dict]) -> str:
    context = ""
    for turn in history[-3:]:  # Last 3 turns
        context += f"{turn['role']}: {turn['content']}\n"
    
    prompt = f"""
    Previous conversation:
    {context}
    
    Current user message: {current_message}
    
    Provide a contextual response that builds on the conversation.
    """
    return prompt
```

---

## 22. **Explain the concept of prompt injection attacks and how to prevent them.**

**Answer:** Prompt injection manipulates AI responses by injecting malicious content into prompts.

**Example prevention:**
```python
# Prompt injection prevention
class PromptSanitizer:
    def __init__(self):
        self.dangerous_patterns = [
            r"ignore.*previous.*instructions",
            r"system.*prompt",
            r"role.*play",
            r"pretend.*to.*be"
        ]
    
    def sanitize_prompt(self, user_input: str) -> str:
        # Check for injection attempts
        for pattern in self.dangerous_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                raise ValueError("Potential prompt injection detected")
        
        # Escape special characters
        sanitized = html.escape(user_input)
        
        # Limit input length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized
    
    def validate_prompt(self, prompt: str) -> bool:
        # Additional validation checks
        if "system:" in prompt.lower() or "assistant:" in prompt.lower():
            return False
        return True
```

---

## 23. **How do you implement response validation and fact-checking?**

**Answer:** Use multiple sources, confidence thresholds, and verification mechanisms.

**Example from SmartCards AI:**
```python
# Response validation
class ResponseValidator:
    def __init__(self):
        self.fact_checkers = [
            self._check_against_vector_db,
            self._check_against_user_cards,
            self._check_against_merchant_data
        ]
    
    async def validate_response(self, response: str, context: Dict) -> Dict:
        validation_results = []
        
        for checker in self.fact_checkers:
            result = await checker(response, context)
            validation_results.append(result)
        
        # Calculate overall validation score
        valid_score = sum(r["valid"] for r in validation_results) / len(validation_results)
        
        return {
            "is_valid": valid_score > 0.8,
            "confidence": valid_score,
            "issues": [r["issues"] for r in validation_results if r["issues"]]
        }
    
    async def _check_against_vector_db(self, response: str, context: Dict) -> Dict:
        # Verify facts against our knowledge base
        facts = self._extract_facts(response)
        verified_facts = []
        
        for fact in facts:
            search_results = await self.vector_db.search(fact)
            if search_results:
                verified_facts.append(fact)
        
        return {
            "valid": len(verified_facts) / len(facts) if facts else 1.0,
            "issues": [f for f in facts if f not in verified_facts]
        }
```

---

## 24. **What is the role of temperature scheduling in conversation flows?**

**Answer:** Adjust temperature based on conversation stage and user intent.

**Example implementation:**
```python
# Temperature scheduling
class TemperatureScheduler:
    def get_temperature(self, conversation_stage: str, user_intent: str) -> float:
        if conversation_stage == "greeting":
            return 0.7  # More creative for greetings
        elif conversation_stage == "factual_query":
            return 0.1  # More deterministic for facts
        elif conversation_stage == "recommendation":
            return 0.3  # Balanced for recommendations
        elif conversation_stage == "clarification":
            return 0.5  # Moderate creativity for clarifications
        
        return 0.3  # Default temperature
    
    def adjust_temperature(self, base_temp: float, user_feedback: str) -> float:
        if "more creative" in user_feedback.lower():
            return min(base_temp + 0.2, 1.0)
        elif "more specific" in user_feedback.lower():
            return max(base_temp - 0.2, 0.0)
        return base_temp
```

---

## 25. **How do you implement conversation branching based on user intent?**

**Answer:** Use intent classification to route conversations to appropriate handlers.

**Example from SmartCards AI:**
```python
# Conversation branching
class ConversationRouter:
    def __init__(self):
        self.intent_handlers = {
            "card_recommendation": self._handle_card_recommendation,
            "reward_inquiry": self._handle_reward_inquiry,
            "merchant_specific": self._handle_merchant_specific,
            "general_question": self._handle_general_question,
            "comparison": self._handle_comparison
        }
    
    async def route_conversation(self, user_message: str, context: Dict):
        # Classify user intent
        intent = await self._classify_intent(user_message)
        
        # Route to appropriate handler
        if intent in self.intent_handlers:
            return await self.intent_handlers[intent](user_message, context)
        else:
            return await self._handle_general_question(user_message, context)
    
    async def _classify_intent(self, message: str) -> str:
        # Use LLM for intent classification
        classification_prompt = f"""
        Classify this user message into one of these intents:
        - card_recommendation: Asking for card suggestions
        - reward_inquiry: Asking about rewards/cashback
        - merchant_specific: Asking about specific merchant
        - comparison: Comparing cards
        - general_question: General credit card questions
        
        Message: {message}
        Intent:"""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": classification_prompt}],
            max_tokens=10
        )
        
        return response.choices[0].message.content.strip().lower()
```

---

*Continue to Part 2 for LangChain, LangGraph, and Advanced Architectures...*