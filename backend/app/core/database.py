from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import structlog
from typing import AsyncGenerator

from app.core.config import settings

logger = structlog.get_logger()

# Create async engine
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sync engine for migrations
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


def get_db():
    """Dependency to get sync database session"""
    db = SessionLocal()
    try:
        yield db
    except HTTPException:
        # Re-raise HTTPExceptions without logging them as database errors
        db.rollback()
        raise
    except Exception as e:
        logger.error("Database session error", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    try:
        # Import all models to ensure they are registered
        from app.models import user, credit_card, transaction, merchant, reward, conversation, card_master_data
        
        # Check if tables exist
        async with async_engine.begin() as conn:
            # Get existing tables
            from sqlalchemy import text
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            existing_tables = [row[0] for row in result.fetchall()]
            
            logger.info(f"Existing tables: {existing_tables}")
            
            # Create all tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        # Don't raise the exception, just log it
        logger.warning("Continuing with startup despite database initialization error")


async def close_db():
    """Close database connections"""
    await async_engine.dispose()
    logger.info("Database connections closed") 