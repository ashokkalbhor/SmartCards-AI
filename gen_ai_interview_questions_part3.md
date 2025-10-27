# 100 Gen AI Interview Questions for Senior Architect Role
## Based on SmartCards AI Project Implementation

### Part 3: Deployment, CI/CD & Production (Questions 36-60)

---

## 36. **How would you design a production deployment architecture for your SmartCards AI application?**

**Answer:** Use containerized microservices with proper scaling, monitoring, and security.

**Example from SmartCards AI:**
```yaml
# docker-compose.yml - Production Architecture
version: '3.8'
services:
  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

  # Backend API (Scalable)
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (Static)
  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=${API_URL}
    deploy:
      replicas: 2

  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: smartcards_ai
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      placement:
        constraints:
          - node.role == manager

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    deploy:
      replicas: 2

  # Vector Database
  chroma:
    image: chromadb/chroma:latest
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    volumes:
      - chroma_data:/chroma/chroma

  # Monitoring Stack
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3001:3000"

volumes:
  postgres_data:
  redis_data:
  chroma_data:
  grafana_data:
```

---

## 37. **How would you implement CI/CD pipelines for your Gen AI application?**

**Answer:** Use GitHub Actions or GitLab CI with automated testing, building, and deployment.

**Example from SmartCards AI:**
```yaml
# .github/workflows/ci-cd.yml
name: SmartCards AI CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run backend tests
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:test@localhost:5432/test_db
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push backend
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        push: true
        tags: smartcards-ai/backend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Build and push frontend
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        push: true
        tags: smartcards-ai/frontend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Deploy to cloud platform (AWS, GCP, Azure)
        echo "Deploying to production..."
        
        # Example for AWS ECS
        aws ecs update-service \
          --cluster smartcards-cluster \
          --service smartcards-service \
          --force-new-deployment
```

---

## 38. **How would you implement monitoring and observability for your Gen AI application?**

**Answer:** Use comprehensive monitoring with metrics, logging, and tracing.

**Example from SmartCards AI:**
```python
# monitoring/setup.py
import structlog
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Prometheus metrics
REQUEST_COUNT = Counter('smartcards_requests_total', 'Total requests', ['endpoint', 'method'])
REQUEST_DURATION = Histogram('smartcards_request_duration_seconds', 'Request duration')
OPENAI_API_CALLS = Counter('openai_api_calls_total', 'OpenAI API calls', ['model', 'status'])
VECTOR_SEARCH_DURATION = Histogram('vector_search_duration_seconds', 'Vector search duration')
ACTIVE_CONVERSATIONS = Gauge('active_conversations', 'Active conversations')

# Structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Monitoring decorators
def monitor_request(endpoint: str, method: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()
            
            try:
                result = await func(*args, **kwargs)
                REQUEST_DURATION.observe(time.time() - start_time)
                return result
            except Exception as e:
                logger.error("Request failed", 
                           endpoint=endpoint, 
                           method=method, 
                           error=str(e),
                           duration=time.time() - start_time)
                raise
        return wrapper
    return decorator

def monitor_openai_call(model: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                OPENAI_API_CALLS.labels(model=model, status="success").inc()
                return result
            except Exception as e:
                OPENAI_API_CALLS.labels(model=model, status="error").inc()
                logger.error("OpenAI API call failed", 
                           model=model, 
                           error=str(e),
                           duration=time.time() - start_time)
                raise
        return wrapper
    return decorator

# Enhanced AI service with monitoring
class MonitoredAIService:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI()
        self.vector_db = vector_db_service
    
    @monitor_openai_call("gpt-4")
    async def generate_response(self, prompt: str) -> str:
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    
    @monitor_request("vector_search", "POST")
    async def search_vector_db(self, query: str) -> List[Dict]:
        start_time = time.time()
        results = await self.vector_db.search(query)
        VECTOR_SEARCH_DURATION.observe(time.time() - start_time)
        return results
    
    async def process_user_query(self, user_id: int, query: str) -> Dict:
        # Track active conversations
        ACTIVE_CONVERSATIONS.inc()
        
        try:
            # Log user interaction
            logger.info("Processing user query",
                       user_id=user_id,
                       query_length=len(query),
                       timestamp=time.time())
            
            # Process query
            response = await self._process_query(user_id, query)
            
            # Log successful response
            logger.info("Query processed successfully",
                       user_id=user_id,
                       response_length=len(response),
                       processing_time=response.get("processing_time", 0))
            
            return response
            
        except Exception as e:
            logger.error("Query processing failed",
                        user_id=user_id,
                        error=str(e),
                        exc_info=True)
            raise
        finally:
            ACTIVE_CONVERSATIONS.dec()
```

---

## 39. **How would you implement rate limiting and cost control for OpenAI API calls?**

**Answer:** Use token buckets, caching, and intelligent request routing.

**Example from SmartCards AI:**
```python
# rate_limiting/cost_controller.py
import asyncio
import time
from collections import defaultdict
from typing import Dict, Optional
import redis.asyncio as redis

class CostController:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        # Rate limits per user
        self.user_limits = {
            "free": {"requests_per_minute": 10, "daily_budget": 1.0},
            "premium": {"requests_per_minute": 60, "daily_budget": 10.0},
            "enterprise": {"requests_per_minute": 200, "daily_budget": 50.0}
        }
        
        # OpenAI costs (per 1K tokens)
        self.model_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
    
    async def check_rate_limit(self, user_id: int, user_tier: str) -> bool:
        """Check if user has exceeded rate limits"""
        current_time = int(time.time())
        minute_key = f"rate_limit:{user_id}:{current_time // 60}"
        daily_key = f"daily_budget:{user_id}:{current_time // 86400}"
        
        # Check per-minute limit
        requests_this_minute = await self.redis_client.incr(minute_key)
        await self.redis_client.expire(minute_key, 60)
        
        if requests_this_minute > self.user_limits[user_tier]["requests_per_minute"]:
            return False
        
        # Check daily budget
        daily_spent = await self.redis_client.get(daily_key)
        if daily_spent and float(daily_spent) > self.user_limits[user_tier]["daily_budget"]:
            return False
        
        return True
    
    async def track_cost(self, user_id: int, model: str, input_tokens: int, output_tokens: int):
        """Track API costs for user"""
        current_time = int(time.time())
        daily_key = f"daily_budget:{user_id}:{current_time // 86400}"
        
        # Calculate cost
        input_cost = (input_tokens / 1000) * self.model_costs[model]["input"]
        output_cost = (output_tokens / 1000) * self.model_costs[model]["output"]
        total_cost = input_cost + output_cost
        
        # Update daily spending
        await self.redis_client.incrbyfloat(daily_key, total_cost)
        await self.redis_client.expire(daily_key, 86400)
        
        # Log cost
        logger.info("API cost tracked",
                   user_id=user_id,
                   model=model,
                   input_tokens=input_tokens,
                   output_tokens=output_tokens,
                   total_cost=total_cost)
    
    async def get_user_usage(self, user_id: int) -> Dict:
        """Get user's current usage statistics"""
        current_time = int(time.time())
        daily_key = f"daily_budget:{user_id}:{current_time // 86400}"
        
        daily_spent = await self.redis_client.get(daily_key)
        if daily_spent:
            daily_spent = float(daily_spent)
        else:
            daily_spent = 0.0
        
        return {
            "daily_spent": daily_spent,
            "daily_budget": self.user_limits["premium"]["daily_budget"],  # Assume premium
            "remaining_budget": self.user_limits["premium"]["daily_budget"] - daily_spent
        }

# Enhanced AI service with cost control
class CostControlledAIService:
    def __init__(self):
        self.cost_controller = CostController()
        self.openai_client = openai.AsyncOpenAI()
    
    async def generate_response(self, user_id: int, user_tier: str, prompt: str) -> Dict:
        # Check rate limits
        if not await self.cost_controller.check_rate_limit(user_id, user_tier):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please upgrade your plan or try again later."
            )
        
        # Select model based on user tier and query complexity
        model = self._select_model(user_tier, prompt)
        
        try:
            # Make API call
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Track costs
            await self.cost_controller.track_cost(
                user_id=user_id,
                model=model,
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "cost": self._calculate_cost(response.usage, model)
            }
            
        except Exception as e:
            logger.error("OpenAI API call failed", user_id=user_id, error=str(e))
            raise
    
    def _select_model(self, user_tier: str, prompt: str) -> str:
        """Select appropriate model based on user tier and query complexity"""
        if user_tier == "free":
            return "gpt-3.5-turbo"  # Cheaper model for free users
        
        # Use GPT-4 for complex queries, GPT-3.5 for simple ones
        if len(prompt) > 500 or "complex" in prompt.lower():
            return "gpt-4"
        else:
            return "gpt-3.5-turbo"
    
    def _calculate_cost(self, usage, model: str) -> float:
        """Calculate cost for the API call"""
        input_cost = (usage.prompt_tokens / 1000) * self.cost_controller.model_costs[model]["input"]
        output_cost = (usage.completion_tokens / 1000) * self.cost_controller.model_costs[model]["output"]
        return input_cost + output_cost
```

---

## 40. **How would you implement A/B testing for different AI models and prompts?**

**Answer:** Use feature flags and statistical analysis to compare performance.

**Example from SmartCards AI:**
```python
# ab_testing/model_comparison.py
import random
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import statistics

@dataclass
class ABTestConfig:
    test_name: str
    variants: Dict[str, float]  # variant_name: traffic_percentage
    metrics: List[str]
    duration_days: int
    min_sample_size: int

class ABTestManager:
    def __init__(self):
        self.active_tests = {}
        self.results = defaultdict(list)
        self.user_assignments = {}
    
    def create_test(self, config: ABTestConfig):
        """Create a new A/B test"""
        self.active_tests[config.test_name] = config
        logger.info(f"Created A/B test: {config.test_name}")
    
    def assign_variant(self, user_id: int, test_name: str) -> str:
        """Assign user to a test variant"""
        if test_name not in self.active_tests:
            return "control"  # Default variant
        
        # Check if user already assigned
        assignment_key = f"{user_id}:{test_name}"
        if assignment_key in self.user_assignments:
            return self.user_assignments[assignment_key]
        
        # Assign based on traffic distribution
        config = self.active_tests[test_name]
        rand = random.random()
        cumulative = 0
        
        for variant, percentage in config.variants.items():
            cumulative += percentage
            if rand <= cumulative:
                self.user_assignments[assignment_key] = variant
                return variant
        
        # Fallback to control
        self.user_assignments[assignment_key] = "control"
        return "control"
    
    async def track_metric(self, test_name: str, variant: str, user_id: int, 
                          metric_name: str, value: float):
        """Track a metric for A/B test"""
        if test_name not in self.active_tests:
            return
        
        metric_key = f"{test_name}:{variant}:{metric_name}"
        self.results[metric_key].append({
            "user_id": user_id,
            "value": value,
            "timestamp": time.time()
        })
        
        logger.info(f"Tracked metric: {metric_key} = {value}")
    
    def analyze_results(self, test_name: str) -> Dict:
        """Analyze A/B test results"""
        if test_name not in self.active_tests:
            return {}
        
        config = self.active_tests[test_name]
        analysis = {}
        
        for metric in config.metrics:
            metric_results = {}
            
            for variant in config.variants.keys():
                metric_key = f"{test_name}:{variant}:{metric}"
                values = [r["value"] for r in self.results[metric_key]]
                
                if values:
                    metric_results[variant] = {
                        "mean": statistics.mean(values),
                        "std": statistics.stdev(values) if len(values) > 1 else 0,
                        "count": len(values),
                        "min": min(values),
                        "max": max(values)
                    }
            
            analysis[metric] = metric_results
        
        return analysis
    
    def is_statistically_significant(self, test_name: str, metric: str, 
                                   confidence_level: float = 0.95) -> bool:
        """Check if results are statistically significant"""
        analysis = self.analyze_results(test_name)
        if metric not in analysis:
            return False
        
        # Simple t-test for two variants
        variants = list(analysis[metric].keys())
        if len(variants) != 2:
            return False
        
        var1, var2 = variants
        data1 = [r["value"] for r in self.results[f"{test_name}:{var1}:{metric}"]]
        data2 = [r["value"] for r in self.results[f"{test_name}:{var2}:{metric}"]]
        
        if len(data1) < 30 or len(data2) < 30:  # Need sufficient sample size
            return False
        
        # Calculate t-statistic (simplified)
        mean1, mean2 = statistics.mean(data1), statistics.mean(data2)
        std1, std2 = statistics.stdev(data1), statistics.stdev(data2)
        
        # Pooled standard error
        pooled_se = ((std1**2 / len(data1)) + (std2**2 / len(data2))) ** 0.5
        t_stat = abs(mean1 - mean2) / pooled_se
        
        # For 95% confidence, t > 1.96 indicates significance
        return t_stat > 1.96

# Enhanced AI service with A/B testing
class ABTestAIService:
    def __init__(self):
        self.ab_manager = ABTestManager()
        self.openai_client = openai.AsyncOpenAI()
        
        # Set up A/B tests
        self._setup_tests()
    
    def _setup_tests(self):
        """Set up active A/B tests"""
        # Test different models
        model_test = ABTestConfig(
            test_name="model_comparison",
            variants={"gpt-4": 0.5, "gpt-3.5-turbo": 0.5},
            metrics=["response_quality", "response_time", "user_satisfaction"],
            duration_days=14,
            min_sample_size=100
        )
        
        # Test different prompts
        prompt_test = ABTestConfig(
            test_name="prompt_variants",
            variants={"detailed": 0.33, "concise": 0.33, "conversational": 0.34},
            metrics=["response_length", "user_satisfaction", "follow_up_questions"],
            duration_days=14,
            min_sample_size=100
        )
        
        self.ab_manager.create_test(model_test)
        self.ab_manager.create_test(prompt_test)
    
    async def generate_response(self, user_id: int, query: str) -> Dict:
        start_time = time.time()
        
        # Assign variants
        model_variant = self.ab_manager.assign_variant(user_id, "model_comparison")
        prompt_variant = self.ab_manager.assign_variant(user_id, "prompt_variants")
        
        # Generate prompt based on variant
        prompt = self._generate_prompt(query, prompt_variant)
        
        # Make API call
        response = await self.openai_client.chat.completions.create(
            model=model_variant,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        response_time = time.time() - start_time
        response_text = response.choices[0].message.content
        
        # Track metrics
        await self.ab_manager.track_metric("model_comparison", model_variant, 
                                         user_id, "response_time", response_time)
        await self.ab_manager.track_metric("prompt_variants", prompt_variant, 
                                         user_id, "response_length", len(response_text))
        
        return {
            "response": response_text,
            "model_variant": model_variant,
            "prompt_variant": prompt_variant,
            "response_time": response_time,
            "tokens_used": response.usage.total_tokens
        }
    
    def _generate_prompt(self, query: str, variant: str) -> str:
        """Generate prompt based on variant"""
        if variant == "detailed":
            return f"""
            As a credit card expert, provide a detailed analysis for this query:
            {query}
            
            Include:
            - Specific reward percentages
            - Alternative options
            - Pros and cons
            - Recommendations
            """
        elif variant == "concise":
            return f"Credit card recommendation for: {query}"
        else:  # conversational
            return f"""
            Hey! I'm here to help with your credit card question: {query}
            
            Let me give you a friendly recommendation based on what I know.
            """
    
    async def get_test_results(self, test_name: str) -> Dict:
        """Get A/B test results"""
        results = self.ab_manager.analyze_results(test_name)
        significant = {}
        
        for metric in results.keys():
            significant[metric] = self.ab_manager.is_statistically_significant(test_name, metric)
        
        return {
            "results": results,
            "statistically_significant": significant,
            "sample_sizes": {metric: sum(len(results[metric][v]["count"]) 
                                       for v in results[metric].keys()) 
                           for metric in results.keys()}
        }
```

---

## 41. **How would you implement security measures for your Gen AI application?**

**Answer:** Implement comprehensive security including input validation, rate limiting, and data protection.

**Example from SmartCards AI:**
```python
# security/security_manager.py
import re
import hashlib
import jwt
from typing import Optional, Dict
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class SecurityManager:
    def __init__(self):
        self.security = HTTPBearer()
        self.blocked_patterns = [
            r"password.*reset",
            r"account.*number",
            r"cvv.*code",
            r"ssn|social.*security",
            r"credit.*card.*number"
        ]
        
        # Rate limiting
        self.rate_limits = {
            "login": {"requests": 5, "window": 300},  # 5 attempts per 5 minutes
            "api": {"requests": 100, "window": 3600},  # 100 requests per hour
            "chat": {"requests": 50, "window": 3600}   # 50 chat messages per hour
        }
    
    async def validate_input(self, text: str) -> bool:
        """Validate user input for security"""
        # Check for sensitive information
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        
        # Check for potential injection attacks
        injection_patterns = [
            r"<script",
            r"javascript:",
            r"onload=",
            r"onerror=",
            r"eval\(",
            r"exec\("
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        
        # Check length limits
        if len(text) > 10000:  # 10KB limit
            return False
        
        return True
    
    async def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize prompt for LLM"""
        # Remove any system prompt injections
        prompt = re.sub(r"system:.*?assistant:", "", prompt, flags=re.IGNORECASE | re.DOTALL)
        prompt = re.sub(r"ignore.*previous.*instructions", "", prompt, flags=re.IGNORECASE)
        
        # Escape special characters
        prompt = prompt.replace("<", "&lt;").replace(">", "&gt;")
        
        return prompt
    
    async def check_rate_limit(self, user_id: int, action: str) -> bool:
        """Check rate limiting for user actions"""
        current_time = int(time.time())
        key = f"rate_limit:{user_id}:{action}:{current_time // self.rate_limits[action]['window']}"
        
        requests = await self.redis_client.incr(key)
        await self.redis_client.expire(key, self.rate_limits[action]['window'])
        
        return requests <= self.rate_limits[action]['requests']
    
    async def authenticate_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Dict:
        """Authenticate user from JWT token"""
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            # Check if user exists and is active
            user = await self.get_user_by_id(user_id)
            if not user or not user.is_active:
                raise HTTPException(status_code=401, detail="User not found or inactive")
            
            return {"user_id": user_id, "user": user}
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        # Use Fernet for symmetric encryption
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data.decode()
    
    async def log_security_event(self, event_type: str, user_id: Optional[int], 
                                details: Dict, severity: str = "info"):
        """Log security events"""
        log_data = {
            "event_type": event_type,
            "user_id": user_id,
            "details": details,
            "severity": severity,
            "timestamp": time.time(),
            "ip_address": self.get_client_ip(),
            "user_agent": self.get_user_agent()
        }
        
        logger.warning(f"Security event: {log_data}")
        
        # Send to security monitoring system
        await self.send_to_security_monitor(log_data)

# Enhanced AI service with security
class SecureAIService:
    def __init__(self):
        self.security_manager = SecurityManager()
        self.openai_client = openai.AsyncOpenAI()
    
    async def process_user_query(self, user_id: int, query: str) -> Dict:
        # Validate input
        if not await self.security_manager.validate_input(query):
            raise HTTPException(status_code=400, detail="Invalid input detected")
        
        # Check rate limits
        if not await self.security_manager.check_rate_limit(user_id, "chat"):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Sanitize prompt
        sanitized_query = await self.security_manager.sanitize_prompt(query)
        
        # Log security event
        await self.security_manager.log_security_event(
            "user_query",
            user_id,
            {"query_length": len(query), "sanitized": True}
        )
        
        # Process query
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": sanitized_query}],
            temperature=0.3
        )
        
        # Validate response
        response_text = response.choices[0].message.content
        if not await self.security_manager.validate_input(response_text):
            # Log potential security issue
            await self.security_manager.log_security_event(
                "suspicious_response",
                user_id,
                {"response_length": len(response_text)},
                severity="warning"
            )
            response_text = "I apologize, but I cannot provide that information."
        
        return {
            "response": response_text,
            "tokens_used": response.usage.total_tokens,
            "security_validated": True
        }
```

---

## 42. **How would you implement data privacy and GDPR compliance in your Gen AI application?**

**Answer:** Implement data minimization, user consent, and right to be forgotten.

**Example from SmartCards AI:**
```python
# privacy/gdpr_manager.py
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

class GDPRManager:
    def __init__(self):
        self.data_retention_policies = {
            "conversation_history": 90,  # days
            "user_preferences": 365,     # days
            "analytics_data": 30,        # days
            "temporary_data": 7          # days
        }
    
    async def get_user_consent(self, user_id: int) -> Dict:
        """Get user's consent status"""
        consent_data = await self.redis_client.get(f"consent:{user_id}")
        if consent_data:
            return json.loads(consent_data)
        
        return {
            "data_collection": False,
            "data_processing": False,
            "data_sharing": False,
            "marketing": False,
            "last_updated": None
        }
    
    async def update_user_consent(self, user_id: int, consent_data: Dict):
        """Update user's consent preferences"""
        consent_data["last_updated"] = datetime.now().isoformat()
        
        await self.redis_client.set(
            f"consent:{user_id}",
            json.dumps(consent_data),
            ex=86400 * 365  # 1 year
        )
        
        # Log consent update
        logger.info("User consent updated", user_id=user_id, consent=consent_data)
    
    async def can_process_data(self, user_id: int, data_type: str) -> bool:
        """Check if we can process user data based on consent"""
        consent = await self.get_user_consent(user_id)
        
        if data_type == "conversation":
            return consent.get("data_processing", False)
        elif data_type == "analytics":
            return consent.get("data_collection", False)
        elif data_type == "marketing":
            return consent.get("marketing", False)
        
        return False
    
    async def anonymize_data(self, data: Dict) -> Dict:
        """Anonymize user data"""
        anonymized = data.copy()
        
        # Remove PII
        pii_fields = ["email", "phone", "address", "credit_card_number", "ssn"]
        for field in pii_fields:
            if field in anonymized:
                anonymized[field] = "[REDACTED]"
        
        # Hash user ID
        if "user_id" in anonymized:
            anonymized["user_id"] = hashlib.sha256(
                str(anonymized["user_id"]).encode()
            ).hexdigest()[:16]
        
        return anonymized
    
    async def export_user_data(self, user_id: int) -> Dict:
        """Export all user data (GDPR right to data portability)"""
        if not await self.can_process_data(user_id, "data_processing"):
            raise HTTPException(status_code=403, detail="Consent required for data export")
        
        # Collect all user data
        user_data = {
            "profile": await self.get_user_profile(user_id),
            "conversations": await self.get_user_conversations(user_id),
            "preferences": await self.get_user_preferences(user_id),
            "activity_log": await self.get_user_activity(user_id)
        }
        
        # Remove sensitive data
        user_data = await self.anonymize_data(user_data)
        
        return user_data
    
    async def delete_user_data(self, user_id: int) -> bool:
        """Delete all user data (GDPR right to be forgotten)"""
        try:
            # Delete from all data stores
            await self.delete_user_profile(user_id)
            await self.delete_user_conversations(user_id)
            await self.delete_user_preferences(user_id)
            await self.delete_user_activity(user_id)
            
            # Mark as deleted (soft delete)
            await self.redis_client.set(f"deleted_user:{user_id}", "1", ex=86400 * 365)
            
            # Log deletion
            logger.info("User data deleted", user_id=user_id)
            
            return True
            
        except Exception as e:
            logger.error("Failed to delete user data", user_id=user_id, error=str(e))
            return False
    
    async def cleanup_expired_data(self):
        """Clean up data that has exceeded retention periods"""
        current_time = datetime.now()
        
        for data_type, retention_days in self.data_retention_policies.items():
            cutoff_date = current_time - timedelta(days=retention_days)
            
            # Clean up expired data
            await self._cleanup_data_type(data_type, cutoff_date)
    
    async def _cleanup_data_type(self, data_type: str, cutoff_date: datetime):
        """Clean up specific data type"""
        if data_type == "conversation_history":
            await self._cleanup_conversations(cutoff_date)
        elif data_type == "analytics_data":
            await self._cleanup_analytics(cutoff_date)
        elif data_type == "temporary_data":
            await self._cleanup_temporary_data(cutoff_date)

# Enhanced AI service with privacy controls
class PrivacyAwareAIService:
    def __init__(self):
        self.gdpr_manager = GDPRManager()
        self.openai_client = openai.AsyncOpenAI()
    
    async def process_user_query(self, user_id: int, query: str) -> Dict:
        # Check consent for data processing
        if not await self.gdpr_manager.can_process_data(user_id, "conversation"):
            raise HTTPException(
                status_code=403, 
                detail="Data processing consent required. Please update your privacy settings."
            )
        
        # Process query
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
            temperature=0.3
        )
        
        # Store conversation with privacy controls
        conversation_data = {
            "user_id": user_id,
            "query": query,
            "response": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat(),
            "tokens_used": response.usage.total_tokens
        }
        
        # Anonymize before storage if needed
        if not await self.gdpr_manager.get_user_consent(user_id)["data_collection"]:
            conversation_data = await self.gdpr_manager.anonymize_data(conversation_data)
        
        await self.store_conversation(conversation_data)
        
        return {
            "response": response.choices[0].message.content,
            "privacy_compliant": True,
            "data_retention_days": 90
        }
    
    async def get_user_insights(self, user_id: int) -> Dict:
        """Get personalized insights with privacy controls"""
        consent = await self.gdpr_manager.get_user_consent(user_id)
        
        if not consent["data_processing"]:
            return {"message": "Personalized insights require data processing consent"}
        
        # Get user data
        conversations = await self.get_user_conversations(user_id)
        preferences = await self.get_user_preferences(user_id)
        
        # Generate insights
        insights = await self._generate_insights(conversations, preferences)
        
        return {
            "insights": insights,
            "data_used": ["conversations", "preferences"],
            "privacy_level": "personalized"
        }
```

---

*Continue to Part 4 for Frontend Integration and Advanced Topics...*