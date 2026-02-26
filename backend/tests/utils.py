"""Testing utilities for FastAPI and SQLAlchemy"""
import asyncio
from typing import AsyncGenerator
from sqlalchemy import event, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base


# Test database URL

# Use a file-backed SQLite DB for tests so sync and async engines can access
# the same database. In-memory aiosqlite connections are isolated per connection
# which leads to issues when mixing sync and async engines.
DB_FILENAME = ".test_sqlite.db"
SYNC_DB_URL = f"sqlite:///{DB_FILENAME}"
ASYNC_DB_URL = f"sqlite+aiosqlite:///{DB_FILENAME}"

# Create async test engine
async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create async test session
AsyncTestingSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync engine that points to the same sqlite file
sync_engine = create_engine(
    SYNC_DB_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

# Enable SQLite foreign keys on sync engine
@event.listens_for(sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

async def init_test_db():
    """Initialize test database (drop/create)"""
    # Ensure the tables are created using the async engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_test_db():
    """Get async database session for testing"""
    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_test_sync_db():
    """Get sync database session for testing"""
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Helper to run async code in sync context
def run_async(coro):
    """Run async coroutine in the running event loop or create one."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)