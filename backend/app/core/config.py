from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "UNGI SmartCards AI"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database - Using SQLite for development
    DATABASE_URL: str = "sqlite:///./smartcards_ai.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./smartcards_ai.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
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
    
    # Vector Database Configuration
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "credit_card_knowledge"
    
    # AI Settings
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    VECTOR_SEARCH_LIMIT: int = 5
    SIMILARITY_THRESHOLD: float = 0.75
    
    # Chatbot Configuration
    MAX_CONVERSATION_HISTORY: int = 10
    FALLBACK_TO_LLM_THRESHOLD: float = 0.6
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        
        # For development, use SQLite
        if os.getenv("ENVIRONMENT", "development") == "development":
            return "sqlite:///./smartcards_ai.db"
        
        # Build from components if not provided (for production)
        user = os.getenv("DB_USER", "smartcards_user")
        password = os.getenv("DB_PASSWORD", "smartcards_password")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db = os.getenv("DB_NAME", "smartcards_ai")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    @field_validator("ASYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_async_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        
        # For development, use SQLite
        if os.getenv("ENVIRONMENT", "development") == "development":
            return "sqlite+aiosqlite:///./smartcards_ai.db"
        
        # Build from components if not provided (for production)
        user = os.getenv("DB_USER", "smartcards_user")
        password = os.getenv("DB_PASSWORD", "smartcards_password")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db = os.getenv("DB_NAME", "smartcards_ai")
        
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    
    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v or v == "your-secret-key-here-change-in-production":
            raise ValueError("SECRET_KEY must be set in production")
        return v
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def validate_origins(cls, v: List[str]) -> List[str]:
        if not v:
            return ["http://localhost:3000"]
        return v
    
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
        "api.smartcardsai.com"
    ]
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO" 