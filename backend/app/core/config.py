from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "UNGI SmartCards AI"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database - Using SQLite for development
    DATABASE_URL: str = "sqlite:///./smartcards_ai.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./smartcards_ai.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,https://smartcards-ai-frontend.onrender.com,https://smartcards-ai-backend.onrender.com"
    
    # Allowed Hosts
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Email Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    UPLOAD_DIR: str = "uploads"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Admin Configuration
    ADMIN_EMAILS: List[str] = ["ashokkalbhor@gmail.com"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # External APIs
    MERCHANT_API_URL: Optional[str] = None
    MERCHANT_API_KEY: Optional[str] = None
    
    # AI/ML Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # Target Database Configuration (for SQL Agent)
    TARGET_DATABASE_URL: Optional[str] = None
    TARGET_ASYNC_DATABASE_URL: Optional[str] = None
    
    # Vector Database Configuration
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "credit_card_knowledge"
    
    # AI Settings
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    VECTOR_SEARCH_LIMIT: int = 5
    SIMILARITY_THRESHOLD: float = 0.75
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 1000
    CACHE_TTL: int = 3600  # Alias for CACHE_TTL_SECONDS
    
    # SQL Agent settings
    SQL_AGENT_TABLES: list = [
        "credit_cards",
        "card_master_data", 
        "card_spending_categories",
        "card_merchant_rewards",
        "merchants",
        "transactions",
        "rewards",
        "users"
    ]
    SQL_AGENT_MAX_RETRIES: int = 3
    SQL_AGENT_TIMEOUT: int = 30
    
    # Chatbot Configuration
    MAX_CONVERSATION_HISTORY: int = 10
    FALLBACK_TO_LLM_THRESHOLD: float = 0.6
    
    # Comparison Configuration
    TOP_MERCHANTS_LIMIT: int = 10
    POPULARITY_COVERAGE_WEIGHT: float = 0.4
    POPULARITY_REWARD_WEIGHT: float = 0.4
    POPULARITY_MAX_REWARD_WEIGHT: float = 0.2
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite:///./smartcards_ai.db"
    
    @field_validator("ASYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_async_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite+aiosqlite:///./smartcards_ai.db"
    
    @field_validator("TARGET_DATABASE_URL", mode="before")
    @classmethod
    def assemble_target_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite:///./smartcards_ai.db"
    
    @field_validator("TARGET_ASYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_target_async_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite+aiosqlite:///./smartcards_ai.db"
    
    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v or v == "your-secret-key-here-change-in-production":
            raise ValueError("SECRET_KEY must be set in production")
        return v
    
    @field_validator("ALLOWED_ORIGINS", mode="after")
    @classmethod
    def validate_origins(cls, v: str) -> List[str]:
        # Split by comma and strip whitespace
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return ["http://localhost:3000"]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.ALLOWED_HOSTS = [
        "smartcardsai.com",
        "www.smartcardsai.com",
        "api.smartcardsai.com",
        "smartcards-ai-2.onrender.com",
        "smartcards-ai-frontend.onrender.com"
    ]
    # Ensure production CORS origins are properly set
    if "https://smartcards-ai-frontend.onrender.com" not in settings.ALLOWED_ORIGINS:
        settings.ALLOWED_ORIGINS.append("https://smartcards-ai-frontend.onrender.com")
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO" 