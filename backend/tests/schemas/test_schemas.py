import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.card_master_data import (
    CardMasterDataCreate, 
    CardMasterDataResponse, 
    CardMasterDataUpdate,
    CardSpendingCategoryCreate,
    CardSpendingCategoryResponse,
    CardMerchantRewardCreate,
    CardMerchantRewardResponse
)
from app.schemas.edit_suggestion import (
    EditSuggestionCreate,
    EditSuggestionResponse,
    EditSuggestionUpdate,
    CardEditSuggestionRequest
)

class TestUserSchemas:
    """Test user-related schemas"""
    
    def test_user_create_valid(self):
        """Test valid user creation"""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
        
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.password == "testpassword123"
    
    def test_user_create_invalid_email(self):
        """Test invalid email format"""
        user_data = {
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "testpassword123"
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_create_weak_password(self):
        """Test weak password validation"""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "123"
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_response(self):
        """Test user response schema"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "role": "user",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        user = UserResponse(**user_data)
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active == True
        assert user.role == "user"
        assert "hashed_password" not in user.dict()
    
    def test_user_update(self):
        """Test user update schema"""
        update_data = {
            "full_name": "Updated Name",
            "is_active": False
        }
        
        user = UserUpdate(**update_data)
        assert user.full_name == "Updated Name"
        assert user.is_active == False

class TestCardMasterDataSchemas:
    """Test card master data schemas"""
    
    def test_card_master_data_create_valid(self):
        """Test valid card creation"""
        card_data = {
            "bank_name": "Test Bank",
            "card_name": "Test Card",
            "card_network": "Visa",
            "card_tier": "basic",
            "joining_fee": 999,
            "annual_fee": 999,
            "is_lifetime_free": False,
            "description": "Test card"
        }
        
        card = CardMasterDataCreate(**card_data)
        assert card.bank_name == "Test Bank"
        assert card.card_name == "Test Card"
        assert card.card_network == "Visa"
        assert card.card_tier == "basic"
    
    def test_card_master_data_create_missing_required(self):
        """Test missing required fields"""
        card_data = {
            "bank_name": "Test Bank",
            "card_name": "Test Card"
            # Missing required fields
        }
        
        with pytest.raises(ValidationError):
            CardMasterDataCreate(**card_data)
    
    def test_card_master_data_response(self):
        """Test card response schema"""
        card_data = {
            "id": 1,
            "bank_name": "Test Bank",
            "card_name": "Test Card",
            "card_network": "Visa",
            "card_tier": "basic",
            "joining_fee": 999,
            "annual_fee": 999,
            "is_lifetime_free": False,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "display_name": "Test Bank Test Card",
            "joining_fee_display": "₹999",
            "annual_fee_display": "₹999",
            "spending_categories": [],
            "merchant_rewards": []
        }
        
        card = CardMasterDataResponse(**card_data)
        assert card.id == 1
        assert card.bank_name == "Test Bank"
        assert card.display_name == "Test Bank Test Card"
    
    def test_card_master_data_update(self):
        """Test card update schema"""
        update_data = {
            "description": "Updated description",
            "annual_fee": 1999
        }
        
        card = CardMasterDataUpdate(**update_data)
        assert card.description == "Updated description"
        assert card.annual_fee == 1999

class TestSpendingCategorySchemas:
    """Test spending category schemas"""
    
    def test_spending_category_create_valid(self):
        """Test valid spending category creation"""
        category_data = {
            "category_name": "general",
            "category_display_name": "General Spends",
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly"
        }
        
        category = CardSpendingCategoryCreate(**category_data)
        assert category.category_name == "general"
        assert category.reward_rate == 5.0
        assert category.reward_type == "cashback"
    
    def test_spending_category_create_invalid_reward_rate(self):
        """Test invalid reward rate"""
        category_data = {
            "category_name": "general",
            "category_display_name": "General Spends",
            "reward_rate": 150.0,  # Too high
            "reward_type": "cashback"
        }
        
        with pytest.raises(ValidationError):
            CardSpendingCategoryCreate(**category_data)
    
    def test_spending_category_response(self):
        """Test spending category response schema"""
        category_data = {
            "id": 1,
            "card_master_id": 1,
            "category_name": "general",
            "category_display_name": "General Spends",
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly",
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        category = CardSpendingCategoryResponse(**category_data)
        assert category.id == 1
        assert category.category_name == "general"
        assert category.reward_rate == 5.0

class TestMerchantRewardSchemas:
    """Test merchant reward schemas"""
    
    def test_merchant_reward_create_valid(self):
        """Test valid merchant reward creation"""
        merchant_data = {
            "merchant_name": "amazon",
            "merchant_display_name": "Amazon",
            "merchant_category": "ecommerce",
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly"
        }
        
        merchant = CardMerchantRewardCreate(**merchant_data)
        assert merchant.merchant_name == "amazon"
        assert merchant.reward_rate == 5.0
        assert merchant.reward_type == "cashback"
    
    def test_merchant_reward_response(self):
        """Test merchant reward response schema"""
        merchant_data = {
            "id": 1,
            "card_master_id": 1,
            "merchant_name": "amazon",
            "merchant_display_name": "Amazon",
            "merchant_category": "ecommerce",
            "reward_rate": 5.0,
            "reward_type": "cashback",
            "reward_cap": 500,
            "reward_cap_period": "monthly",
            "is_active": True,
            "requires_registration": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        merchant = CardMerchantRewardResponse(**merchant_data)
        assert merchant.id == 1
        assert merchant.merchant_name == "amazon"
        assert merchant.reward_rate == 5.0

class TestEditSuggestionSchemas:
    """Test edit suggestion schemas"""
    
    def test_edit_suggestion_create_valid(self):
        """Test valid edit suggestion creation"""
        suggestion_data = {
            "field_type": "spending_category",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Increase reward rate"
        }
        
        suggestion = EditSuggestionCreate(**suggestion_data)
        assert suggestion.field_type == "spending_category"
        assert suggestion.field_name == "general"
        assert suggestion.new_value == "6.0"
        assert suggestion.suggestion_reason == "Increase reward rate"
    
    def test_edit_suggestion_create_invalid_field_type(self):
        """Test invalid field type"""
        suggestion_data = {
            "field_type": "invalid_field",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Test"
        }
        
        with pytest.raises(ValidationError):
            EditSuggestionCreate(**suggestion_data)
    
    def test_edit_suggestion_response(self):
        """Test edit suggestion response schema"""
        suggestion_data = {
            "id": 1,
            "user_id": 1,
            "card_master_id": 1,
            "field_type": "spending_category",
            "field_name": "general",
            "old_value": "5.0",
            "new_value": "6.0",
            "suggestion_reason": "Increase reward rate",
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "user_name": "Test User",
            "card_name": "Test Card",
            "bank_name": "Test Bank"
        }
        
        suggestion = EditSuggestionResponse(**suggestion_data)
        assert suggestion.id == 1
        assert suggestion.field_type == "spending_category"
        assert suggestion.status == "pending"
        assert suggestion.user_name == "Test User"
    
    def test_edit_suggestion_update(self):
        """Test edit suggestion update schema"""
        update_data = {
            "status": "approved",
            "review_notes": "Good suggestion"
        }
        
        suggestion = EditSuggestionUpdate(**update_data)
        assert suggestion.status == "approved"
        assert suggestion.review_notes == "Good suggestion"
    
    def test_card_edit_suggestion_request(self):
        """Test card edit suggestion request schema"""
        request_data = {
            "field_type": "spending_category",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Increase reward rate"
        }
        
        request = CardEditSuggestionRequest(**request_data)
        assert request.field_type == "spending_category"
        assert request.field_name == "general"
        assert request.new_value == "6.0"
        assert request.suggestion_reason == "Increase reward rate" 