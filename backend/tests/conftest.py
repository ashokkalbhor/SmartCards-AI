import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.edit_suggestion import EditSuggestion
from app.core.security import create_access_token
from app.core.config import settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db():
    """Database fixture"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Test client fixture"""
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
    """Create test admin user"""
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
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_headers(test_admin_user):
    """Create auth headers for admin user"""
    access_token = create_access_token(data={"sub": test_admin_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def moderator_headers(test_moderator_user):
    """Create auth headers for moderator user"""
    access_token = create_access_token(data={"sub": test_moderator_user.email})
    return {"Authorization": f"Bearer {access_token}"} 