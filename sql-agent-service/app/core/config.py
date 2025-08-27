import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    # Basic settings
    PROJECT_NAME: str = "SQL Agent Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # SQL Agent Service Database (for chat history, user sessions, documents)
    DATABASE_URL: str = "sqlite:///./data/sql_agent_service.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./data/sql_agent_service.db"
    
    # Target Business Database (for business data - credit cards, transactions, etc.)
    TARGET_DATABASE_URL: str = "sqlite:///./data/smartcards_ai.db"
    TARGET_ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./data/smartcards_ai.db"
    
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
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_MAX_TOKENS: int = 2000
    
    # Vector database settings
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "credit_card_knowledge"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    VECTOR_SIMILARITY_THRESHOLD: float = 0.7
    MAX_VECTOR_RESULTS: int = 5
    
    # JWT Authentication settings
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Chat History settings
    CHAT_HISTORY_RETENTION_DAYS: int = 90
    MAX_CONVERSATIONS_PER_USER: int = 50
    MAX_MESSAGES_PER_CONVERSATION: int = 100
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 1000
    CACHE_TTL: int = 3600  # Alias for CACHE_TTL_SECONDS
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Health check settings
    HEALTH_CHECK_INTERVAL: int = 30
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite:///./sql_agent_service.db"

    @field_validator("ASYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_async_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite+aiosqlite:///./sql_agent_service.db"
    
    @field_validator("JWT_SECRET_KEY", mode="before")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if v == "your-super-secret-jwt-key-change-in-production":
            # Generate a secure random key if not provided
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    @field_validator("OPENAI_API_KEY", mode="before")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v:
            raise ValueError("OPENAI_API_KEY is required")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
