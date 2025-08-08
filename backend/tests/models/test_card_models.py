import pytest
from datetime import datetime
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward

class TestCardMasterData:
    """Test card master data models"""
    
    def test_card_master_data_creation(self):
        """Test creating card master data"""
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
        
        assert card.bank_name == "Test Bank"
        assert card.card_name == "Test Card"
        assert card.card_network == "Visa"
        assert card.card_tier == "basic"
        assert card.joining_fee == 999
        assert card.annual_fee == 999
        assert card.is_lifetime_free == False
        assert card.description == "Test card description"
        assert card.is_active == True
    
    def test_card_display_name_property(self):
        """Test card display name property"""
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            card_variant="Gold",
            card_network="Visa",
            card_tier="basic"
        )
        
        assert card.display_name == "Test Bank Test Card Gold"
        
        # Test without variant
        card.card_variant = None
        assert card.display_name == "Test Bank Test Card"
    
    def test_card_joining_fee_display_property(self):
        """Test joining fee display property"""
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            card_network="Visa",
            card_tier="basic",
            joining_fee=999
        )
        
        assert card.joining_fee_display == "₹999"
        
        # Test lifetime free
        card.is_lifetime_free = True
        assert card.joining_fee_display == "Lifetime Free"
        
        # Test waived fee
        card.is_lifetime_free = False
        card.joining_fee = 0
        assert card.joining_fee_display == "₹0 (Waived)"
    
    def test_card_annual_fee_display_property(self):
        """Test annual fee display property"""
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            card_network="Visa",
            card_tier="basic",
            annual_fee=999,
            annual_fee_waiver_spend=200000
        )
        
        assert card.annual_fee_display == "₹999 (Waived on ₹200,000 spend)"
        
        # Test without waiver
        card.annual_fee_waiver_spend = None
        assert card.annual_fee_display == "₹999"
        
        # Test lifetime free
        card.is_lifetime_free = True
        assert card.annual_fee_display == "Lifetime Free"
    
    def test_card_to_dict_method(self):
        """Test card to_dict method"""
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            card_network="Visa",
            card_tier="basic",
            joining_fee=999,
            annual_fee=999,
            is_active=True
        )
        
        card_dict = card.to_dict()
        
        assert card_dict["bank_name"] == "Test Bank"
        assert card_dict["card_name"] == "Test Card"
        assert card_dict["card_network"] == "Visa"
        assert card_dict["card_tier"] == "basic"
        assert card_dict["joining_fee"] == 999
        assert card_dict["annual_fee"] == 999
        assert card_dict["is_active"] == True

class TestCardSpendingCategory:
    """Test spending category model"""
    
    def test_spending_category_creation(self):
        """Test creating spending category"""
        category = CardSpendingCategory(
            card_master_id=1,
            category_name="general",
            category_display_name="General Spends",
            reward_rate=5.0,
            reward_type="cashback",
            reward_cap=500,
            reward_cap_period="monthly",
            is_active=True
        )
        
        assert category.card_master_id == 1
        assert category.category_name == "general"
        assert category.category_display_name == "General Spends"
        assert category.reward_rate == 5.0
        assert category.reward_type == "cashback"
        assert category.reward_cap == 500
        assert category.reward_cap_period == "monthly"
        assert category.is_active == True
    
    def test_spending_category_reward_display_property(self):
        """Test spending category reward display property"""
        category = CardSpendingCategory(
            card_master_id=1,
            category_name="general",
            category_display_name="General Spends",
            reward_rate=5.0,
            reward_type="cashback",
            reward_cap=500,
            reward_cap_period="monthly"
        )
        
        assert category.reward_display == "5.0% (capped at ₹500 monthly)"
        
        # Test without cap
        category.reward_cap = None
        assert category.reward_display == "5.0%"
        
        # Test zero reward rate
        category.reward_rate = 0
        assert category.reward_display == "-"
    
    def test_spending_category_repr(self):
        """Test spending category repr method"""
        category = CardSpendingCategory(
            card_master_id=1,
            category_name="general",
            category_display_name="General Spends",
            reward_rate=5.0
        )
        
        assert str(category) == "<CardSpendingCategory(card_id=1, category='general', rate=5.0%)>"

class TestCardMerchantReward:
    """Test merchant reward model"""
    
    def test_merchant_reward_creation(self):
        """Test creating merchant reward"""
        merchant = CardMerchantReward(
            card_master_id=1,
            merchant_name="amazon",
            merchant_display_name="Amazon",
            merchant_category="ecommerce",
            reward_rate=5.0,
            reward_type="cashback",
            reward_cap=500,
            reward_cap_period="monthly",
            is_active=True
        )
        
        assert merchant.card_master_id == 1
        assert merchant.merchant_name == "amazon"
        assert merchant.merchant_display_name == "Amazon"
        assert merchant.merchant_category == "ecommerce"
        assert merchant.reward_rate == 5.0
        assert merchant.reward_type == "cashback"
        assert merchant.reward_cap == 500
        assert merchant.reward_cap_period == "monthly"
        assert merchant.is_active == True
    
    def test_merchant_reward_reward_display_property(self):
        """Test merchant reward display property"""
        merchant = CardMerchantReward(
            card_master_id=1,
            merchant_name="amazon",
            merchant_display_name="Amazon",
            reward_rate=5.0,
            reward_type="cashback",
            reward_cap=500,
            reward_cap_period="monthly"
        )
        
        assert merchant.reward_display == "5.0% (capped at ₹500 monthly)"
        
        # Test without cap
        merchant.reward_cap = None
        assert merchant.reward_display == "5.0%"
        
        # Test zero reward rate
        merchant.reward_rate = 0
        assert merchant.reward_display == "-"
    
    def test_merchant_reward_repr(self):
        """Test merchant reward repr method"""
        merchant = CardMerchantReward(
            card_master_id=1,
            merchant_name="amazon",
            merchant_display_name="Amazon",
            reward_rate=5.0
        )
        
        assert str(merchant) == "<CardMerchantReward(card_id=1, merchant='amazon', rate=5.0%)>"
    
    def test_merchant_reward_requires_registration_default(self):
        """Test merchant reward requires_registration default"""
        merchant = CardMerchantReward(
            card_master_id=1,
            merchant_name="amazon",
            merchant_display_name="Amazon",
            reward_rate=5.0
        )
        
        assert merchant.requires_registration == False 