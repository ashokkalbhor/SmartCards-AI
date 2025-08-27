from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.sql import func
from typing import List, Dict, Any, Optional
import logging
from .config import settings

logger = logging.getLogger(__name__)

# Database engines
engine = create_engine(settings.DATABASE_URL)
async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# SQL Agent Service Models
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    conversation_id = Column(String, nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    confidence = Column(Float, nullable=True)
    sql_query = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    conversation_id = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    message_count = Column(Integer, default=0)

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    session_id = Column(String, nullable=False, unique=True, index=True)
    session_start = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class ChatUser(Base):
    __tablename__ = "chat_users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    client_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    document_type = Column(String, nullable=False)  # pdf, image, text
    status = Column(String, nullable=False, default="pending")  # pending, processing, completed, failed
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON string of tags
    user_id = Column(String, nullable=False, index=True)
    uploaded_at = Column(DateTime, default=func.now())
    processed_at = Column(DateTime, nullable=True)
    text_content = Column(Text, nullable=True)
    vector_id = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)

# Database functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_database_schema() -> Dict[str, Any]:
    """Get database schema information for the main business database"""
    try:
        inspector = inspect(engine)
        schema_info = {}
        
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "primary_key": column.get("primary_key", False)
                })
            
            # Get foreign keys
            foreign_keys = []
            for fk in inspector.get_foreign_keys(table_name):
                foreign_keys.append({
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"]
                })
            
            schema_info[table_name] = {
                "columns": columns,
                "foreign_keys": foreign_keys
            }
        
        return schema_info
    except Exception as e:
        logger.error(f"Error getting database schema: {e}")
        return {}

def get_configured_tables() -> List[str]:
    """Get list of tables that the SQL agent is configured to access"""
    # This will be configurable via settings
    return settings.SQL_AGENT_TABLES

def create_tables():
    """Create all tables for the SQL agent service"""
    Base.metadata.create_all(bind=engine)

async def create_async_tables():
    """Create all tables for the SQL agent service (async)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
