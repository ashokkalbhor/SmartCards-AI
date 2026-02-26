
# Import all model modules to ensure Base.metadata is fully populated before any DB setup
import app.models.user
import app.models.card_master_data
import app.models.edit_suggestion
import app.models.analytics

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.edit_suggestion import EditSuggestion
from app.models.analytics import AnalyticsEvent

from app.core.database import get_db, get_async_db
from app.main import app
from app.core.security import create_access_token
from app.core.config import settings

from tests.utils import (
    TestingSessionLocal,
    get_test_db,
    get_test_sync_db,
    init_test_db,
    run_async
)

# Override database dependencies for testing
app.dependency_overrides[get_db] = get_test_sync_db
app.dependency_overrides[get_async_db] = get_test_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Initialize test database"""
    await init_test_db()

@pytest.fixture
def db() -> Generator:
    """Get synchronous database session"""
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@pytest_asyncio.fixture
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async for session in get_test_db():
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@pytest.fixture
def client():
    """Get test client"""
    return TestClient(app)

@pytest.fixture
def test_user(db):
    """Create test user"""
    user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",  # "password"
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin_user(db):
    """Create test admin user with admin role"""
    from app.models.user_role import UserRole
    
    admin = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",  # "password"
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Create admin role
    admin_role = UserRole(
        user_id=admin.id,
        role_type="admin",
        status="active"
    )
    db.add(admin_role)
    db.commit()
    
    return admin

@pytest.fixture
def test_moderator_user(db):
    """Create test moderator user"""
    moderator = User(
        email="moderator@example.com",
        first_name="Moderator",
        last_name="User",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",  # "password"
        is_active=True
    )
    db.add(moderator)
    db.commit()
    db.refresh(moderator)
    return moderator

@pytest.fixture
def test_card(db):
    """Create test card"""
    card = CardMasterData(
        bank_name="Test Bank",
        card_name="Test Card",
        card_network="Visa",
        card_tier="basic",
        joining_fee=999,
        annual_fee=999,
        is_lifetime_free=False,
        description="Test card description",
        is_active=True
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@pytest.fixture
def test_spending_category(db, test_card):
    """Create test spending category"""
    category = CardSpendingCategory(
        card_master_id=test_card.id,
        category_name="general",
        category_display_name="General Spends",
        reward_rate=5.0,
        reward_type="cashback",
        reward_cap=500,
        reward_cap_period="monthly",
        is_active=True
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@pytest.fixture
def test_merchant_reward(db, test_card):
    """Create test merchant reward"""
    merchant = CardMerchantReward(
        card_master_id=test_card.id,
        merchant_name="amazon",
        merchant_display_name="Amazon",
        merchant_category="ecommerce",
        reward_rate=5.0,
        reward_type="cashback",
        reward_cap=500,
        reward_cap_period="monthly",
        is_active=True
    )
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    return merchant

@pytest.fixture
def auth_headers(test_user):
    """Create auth headers for test user"""
    access_token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def user_headers(test_user):
    """Create auth headers for regular user (alias for auth_headers)"""
    access_token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_headers(test_admin_user):
    """Create auth headers for admin user"""
    access_token = create_access_token(str(test_admin_user.id))
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def moderator_headers(test_moderator_user):
    """Create auth headers for moderator user"""
    access_token = create_access_token(str(test_moderator_user.id))
    return {"Authorization": f"Bearer {access_token}"}