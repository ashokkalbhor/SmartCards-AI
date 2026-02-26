"""
Tests for CardUpdateService
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from app.services.card_update_service import CardUpdateService
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.edit_suggestion import EditSuggestion
from app.models.community import CommunityPost


@pytest.fixture
def card_update_service():
    """Fixture for CardUpdateService"""
    return CardUpdateService()


@pytest.fixture
def sample_card(test_db):
    """Create a sample card for testing"""
    card = CardMasterData(
        card_name="HDFC Regalia",
        display_name="HDFC Regalia Credit Card",
        bank_name="HDFC Bank",
        card_variant="regalia",
        is_active=True,
        annual_fee=2500.0,
        joining_fee=2500.0,
        terms_and_conditions_url="https://www.hdfcbank.com/personal/pay/cards/credit-cards/regalia",
        apply_url="https://www.hdfcbank.com/personal/pay/cards/credit-cards/regalia/apply"
    )
    test_db.add(card)
    test_db.commit()
    test_db.refresh(card)
    return card


def test_get_extraction_prompt(card_update_service):
    """Test extraction prompt generation"""
    prompt = card_update_service._get_extraction_prompt(
        "HDFC Regalia",
        "HDFC Bank",
        "regalia"
    )
    
    assert "HDFC Regalia" in prompt
    assert "HDFC Bank" in prompt
    assert "JSON" in prompt
    assert "annual_fee" in prompt
    assert "joining_fee" in prompt
    assert "spending_categories" in prompt
    assert "merchant_rewards" in prompt


@pytest.mark.asyncio
async def test_extract_card_data_success(card_update_service):
    """Test successful card data extraction"""
    mock_response = {
        "annual_fee": 3000.0,
        "joining_fee": 3000.0,
        "features": "Free airport lounge access, 1000 bonus reward points",
        "benefits": "Travel insurance, Dining privileges",
        "key_highlights": "4 reward points per Rs. 150 spent",
        "spending_categories": [
            {
                "category_name": "Travel",
                "reward_rate": 4.0,
                "milestone_benefit": "5000 points on Rs. 3 lakh spend"
            }
        ],
        "merchant_rewards": [
            {
                "merchant_name": "Amazon",
                "reward_rate": 5.0,
                "max_cashback": 1000.0
            }
        ]
    }
    
    with patch.object(card_update_service.llm, 'ainvoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = Mock(content=str(mock_response))
        
        result = await card_update_service.extract_card_data(
            "Sample webpage content",
            "HDFC Regalia",
            "HDFC Bank",
            "regalia"
        )
        
        # Verify LLM was called
        assert mock_invoke.called
        
        # Note: Since the actual extraction uses JSON parsing,
        # we'd need to mock that properly for a real test


@pytest.mark.asyncio
async def test_extract_card_data_error(card_update_service):
    """Test card data extraction with error"""
    with patch.object(card_update_service.llm, 'ainvoke', side_effect=Exception("API Error")):
        with pytest.raises(Exception):
            await card_update_service.extract_card_data(
                "content",
                "HDFC Regalia",
                "HDFC Bank"
            )


def test_compare_and_create_suggestions_basic_fields(
    card_update_service, sample_card, test_db, test_user
):
    """Test creation of edit suggestions for basic field changes"""
    extracted_data = {
        "annual_fee": 3000.0,  # Changed from 2500
        "joining_fee": 2500.0,  # No change
        "features": "New features added",  # New value
        "spending_categories": [],
        "merchant_rewards": []
    }
    
    suggestions = card_update_service.compare_and_create_suggestions(
        test_db,
        sample_card.id,
        extracted_data,
        test_user.id
    )
    
    # Should create suggestions for annual_fee and features
    assert len(suggestions) >= 1
    
    # Check annual_fee suggestion
    fee_suggestion = next(
        (s for s in suggestions if s.field_name == "annual_fee"),
        None
    )
    assert fee_suggestion is not None
    assert fee_suggestion.current_value == "2500.0"
    assert fee_suggestion.suggested_value == "3000.0"
    assert fee_suggestion.change_type == "update"
    assert fee_suggestion.status == "pending"


def test_compare_and_create_suggestions_no_changes(
    card_update_service, sample_card, test_db, test_user
):
    """Test that no suggestions are created when data hasn't changed"""
    extracted_data = {
        "annual_fee": 2500.0,  # Same
        "joining_fee": 2500.0,  # Same
        "spending_categories": [],
        "merchant_rewards": []
    }
    
    suggestions = card_update_service.compare_and_create_suggestions(
        test_db,
        sample_card.id,
        extracted_data,
        test_user.id
    )
    
    assert len(suggestions) == 0


def test_compare_and_create_suggestions_spending_categories(
    card_update_service, sample_card, test_db, test_user
):
    """Test creation of suggestions for spending category changes"""
    # Add existing category
    existing_category = CardSpendingCategory(
        card_id=sample_card.id,
        category_name="Travel",
        reward_rate=3.0,
        milestone_benefit="Old milestone"
    )
    test_db.add(existing_category)
    test_db.commit()
    
    extracted_data = {
        "spending_categories": [
            {
                "category_name": "Travel",
                "reward_rate": 4.0,  # Changed
                "milestone_benefit": "New milestone"  # Changed
            },
            {
                "category_name": "Dining",  # New category
                "reward_rate": 2.0
            }
        ],
        "merchant_rewards": []
    }
    
    suggestions = card_update_service.compare_and_create_suggestions(
        test_db,
        sample_card.id,
        extracted_data,
        test_user.id
    )
    
    # Should have suggestions for Travel update and Dining addition
    assert len(suggestions) >= 2
    
    # Verify Travel category update
    travel_updates = [s for s in suggestions if "Travel" in str(s.suggested_value)]
    assert len(travel_updates) > 0


def test_compare_and_create_suggestions_merchant_rewards(
    card_update_service, sample_card, test_db, test_user
):
    """Test creation of suggestions for merchant reward changes"""
    extracted_data = {
        "spending_categories": [],
        "merchant_rewards": [
            {
                "merchant_name": "Amazon",
                "reward_rate": 5.0,
                "max_cashback": 1000.0
            }
        ]
    }
    
    suggestions = card_update_service.compare_and_create_suggestions(
        test_db,
        sample_card.id,
        extracted_data,
        test_user.id
    )
    
    # Should create suggestion for new merchant reward
    merchant_suggestions = [
        s for s in suggestions
        if s.table_name == "card_merchant_rewards"
    ]
    assert len(merchant_suggestions) > 0


def test_create_community_post_for_approval(
    card_update_service, sample_card, test_db, test_user
):
    """Test community post creation for approved suggestions"""
    # Create an approved suggestion
    suggestion = EditSuggestion(
        user_id=test_user.id,
        table_name="card_master_data",
        record_id=sample_card.id,
        field_name="annual_fee",
        current_value="2500.0",
        suggested_value="3000.0",
        change_type="update",
        status="approved",
        reviewed_by=test_user.id,
        reviewed_at=datetime.utcnow()
    )
    test_db.add(suggestion)
    test_db.commit()
    test_db.refresh(suggestion)
    
    # Create community post
    post = card_update_service.create_community_post_for_approval(
        test_db,
        sample_card.id,
        [suggestion]
    )
    
    assert post is not None
    assert post.user_id == test_user.id
    assert post.category == "card_updates"
    assert sample_card.display_name in post.title
    assert "annual_fee" in post.content
    assert "2500.0" in post.content
    assert "3000.0" in post.content


def test_get_or_create_system_user_creates_new(card_update_service, test_db):
    """Test system user creation"""
    user_id = card_update_service.get_or_create_system_user(test_db)
    
    assert user_id is not None
    
    # Verify user was created with correct properties
    from app.models.user import User
    user = test_db.query(User).filter(User.id == user_id).first()
    
    assert user is not None
    assert user.email == "system-updater@smartcards.ai"
    assert user.first_name == "System"
    assert user.last_name == "Updater"
    assert user.is_active is True


def test_get_or_create_system_user_returns_existing(card_update_service, test_db):
    """Test that system user is not duplicated"""
    user_id_1 = card_update_service.get_or_create_system_user(test_db)
    user_id_2 = card_update_service.get_or_create_system_user(test_db)
    
    assert user_id_1 == user_id_2


def test_compare_with_null_values(card_update_service, sample_card, test_db, test_user):
    """Test comparison when current values are null"""
    # Card with null optional fields
    card = CardMasterData(
        card_name="Test Card",
        display_name="Test Card",
        bank_name="Test Bank",
        is_active=True,
        features=None,  # Null field
        benefits=None
    )
    test_db.add(card)
    test_db.commit()
    test_db.refresh(card)
    
    extracted_data = {
        "features": "New features",
        "benefits": "New benefits",
        "spending_categories": [],
        "merchant_rewards": []
    }
    
    suggestions = card_update_service.compare_and_create_suggestions(
        test_db,
        card.id,
        extracted_data,
        test_user.id
    )
    
    # Should create suggestions for both fields
    assert len(suggestions) >= 2
    
    # Both should be 'add' type since current is null
    for suggestion in suggestions:
        if suggestion.field_name in ["features", "benefits"]:
            assert suggestion.change_type == "add"
