import pytest
from app.core.card_templates import (
    get_default_spending_categories,
    get_default_merchant_rewards,
    create_default_spending_categories_for_card,
    create_default_merchant_rewards_for_card
)

class TestCardTemplates:
    """Test card templates functionality"""
    
    def test_get_default_spending_categories(self):
        """Test getting default spending categories"""
        categories = get_default_spending_categories("basic", "Test Bank")
        
        assert len(categories) == 10
        assert all("category_name" in cat for cat in categories)
        assert all("category_display_name" in cat for cat in categories)
        assert all("reward_rate" in cat for cat in categories)
        assert all("reward_type" in cat for cat in categories)
        
        # Check specific categories
        category_names = [cat["category_name"] for cat in categories]
        assert "offline_spends" in category_names
        assert "fuel" in category_names
        assert "online_shopping" in category_names
        assert "utilities" in category_names
        assert "education" in category_names
        assert "jewelry" in category_names
        assert "government_payments" in category_names
        assert "insurance" in category_names
        assert "rent" in category_names
        assert "wallets" in category_names
    
    def test_get_default_spending_categories_premium_tier(self):
        """Test getting default spending categories for premium tier"""
        categories = get_default_spending_categories("premium", "Test Bank")
        
        assert len(categories) == 10
        
        # Premium tier should have higher reward rates
        offline_category = next(cat for cat in categories if cat["category_name"] == "offline_spends")
        assert offline_category["reward_rate"] > 0.0  # Higher than basic tier
    
    def test_get_default_merchant_rewards(self):
        """Test getting default merchant rewards"""
        merchants = get_default_merchant_rewards("basic", "Test Bank")
        
        assert len(merchants) == 21
        assert all("merchant_name" in merch for merch in merchants)
        assert all("merchant_display_name" in merch for merch in merchants)
        assert all("reward_rate" in merch for merch in merchants)
        assert all("reward_type" in merch for merch in merchants)
        
        # Check specific merchants
        merchant_names = [merch["merchant_name"] for merch in merchants]
        assert "amazon" in merchant_names
        assert "amazon_fresh" in merchant_names
        assert "flipkart" in merchant_names
        assert "flipkart_grocery" in merchant_names
        assert "swiggy" in merchant_names
        assert "zomato" in merchant_names
        assert "bookmyshow" in merchant_names
        assert "uber" in merchant_names
        assert "ola" in merchant_names
        assert "rapido" in merchant_names
        assert "bigbasket" in merchant_names
        assert "blinkit" in merchant_names
        assert "myntra" in merchant_names
        assert "ajio" in merchant_names
        assert "paytm" in merchant_names
        assert "phonepe" in merchant_names
        assert "google_pay" in merchant_names
        assert "nps" in merchant_names
        assert "netflix" in merchant_names
        assert "hotstar" in merchant_names  # Fixed: was "disney_plus_hotstar"
        assert "prime_video" in merchant_names
    
    def test_get_default_merchant_rewards_premium_tier(self):
        """Test getting default merchant rewards for premium tier"""
        merchants = get_default_merchant_rewards("premium", "Test Bank")
        
        assert len(merchants) == 21
        
        # Premium tier should have higher reward rates
        amazon_merchant = next(merch for merch in merchants if merch["merchant_name"] == "amazon")
        assert amazon_merchant["reward_rate"] > 5.0  # Higher than basic tier
    
    def test_create_default_spending_categories_for_card(self):
        """Test creating default spending categories for a card"""
        card_id = 1
        card_tier = "basic"
        bank_name = "Test Bank"
        
        categories = create_default_spending_categories_for_card(card_id, card_tier, bank_name)
        
        assert len(categories) == 10
        assert all("card_master_id" in cat for cat in categories)
        assert all(cat["card_master_id"] == card_id for cat in categories)
        assert all("reward_display" in cat for cat in categories)
        
        # Check reward display format
        offline_category = next(cat for cat in categories if cat["category_name"] == "offline_spends")
        assert offline_category["reward_display"] == f"{offline_category['reward_rate']}% {offline_category['reward_type']}"
    
    def test_create_default_merchant_rewards_for_card(self):
        """Test creating default merchant rewards for a card"""
        card_id = 1
        card_tier = "basic"
        bank_name = "Test Bank"
        
        merchants = create_default_merchant_rewards_for_card(card_id, card_tier, bank_name)
        
        assert len(merchants) == 21
        assert all("card_master_id" in merch for merch in merchants)
        assert all(merch["card_master_id"] == card_id for merch in merchants)
        assert all("reward_display" in merch for merch in merchants)
        
        # Check reward display format
        amazon_merchant = next(merch for merch in merchants if merch["merchant_name"] == "amazon")
        assert amazon_merchant["reward_display"] == f"{amazon_merchant['reward_rate']}% {amazon_merchant['reward_type']}"
    
    def test_merchant_popularity_order(self):
        """Test that merchants are ordered by popularity"""
        merchants = get_default_merchant_rewards("basic", "Test Bank")
        
        # Check that popular merchants come first
        merchant_names = [merch["merchant_name"] for merch in merchants]
        
        # Amazon should be first (most popular)
        assert merchant_names[0] == "amazon"
        
        # Amazon Fresh should be second
        assert merchant_names[1] == "amazon_fresh"
        
        # Flipkart should be third
        assert merchant_names[2] == "flipkart"
        
        # FlipKart Grocery should be fourth
        assert merchant_names[3] == "flipkart_grocery"
        
        # Swiggy should be fifth
        assert merchant_names[4] == "swiggy"
        
        # Zomato should be sixth
        assert merchant_names[5] == "zomato"
        
        # NPS should be positioned after digital wallets (rank 18)
        assert merchant_names[17] == "nps"
    
    def test_category_standard_order(self):
        """Test that categories are in standard order"""
        categories = get_default_spending_categories("basic", "Test Bank")
        
        # Check standard order
        category_names = [cat["category_name"] for cat in categories]
        expected_order = [
            "offline_spends", "fuel", "online_shopping", "utilities", "education",
            "jewelry", "government_payments", "insurance", "rent", "wallets"
        ]
        
        assert category_names == expected_order
    
    def test_reward_rates_by_tier(self):
        """Test that reward rates vary by card tier"""
        basic_categories = get_default_spending_categories("basic", "Test Bank")
        premium_categories = get_default_spending_categories("premium", "Test Bank")
        elite_categories = get_default_spending_categories("elite", "Test Bank")
        
        # Premium should have higher rates than basic
        for basic_cat, premium_cat in zip(basic_categories, premium_categories):
            if basic_cat["category_name"] == premium_cat["category_name"]:
                assert premium_cat["reward_rate"] >= basic_cat["reward_rate"]
        
        # Elite should have higher rates than premium
        for premium_cat, elite_cat in zip(premium_categories, elite_categories):
            if premium_cat["category_name"] == elite_cat["category_name"]:
                assert elite_cat["reward_rate"] >= premium_cat["reward_rate"]
    
    def test_merchant_reward_rates_by_tier(self):
        """Test that merchant reward rates vary by card tier"""
        basic_merchants = get_default_merchant_rewards("basic", "Test Bank")
        premium_merchants = get_default_merchant_rewards("premium", "Test Bank")
        elite_merchants = get_default_merchant_rewards("elite", "Test Bank")
        
        # Premium should have higher rates than basic
        for basic_merch, premium_merch in zip(basic_merchants, premium_merchants):
            if basic_merch["merchant_name"] == premium_merch["merchant_name"]:
                assert premium_merch["reward_rate"] >= basic_merch["reward_rate"]
        
        # Elite should have higher rates than premium
        for premium_merch, elite_merch in zip(premium_merchants, elite_merchants):
            if premium_merch["merchant_name"] == elite_merch["merchant_name"]:
                assert elite_merch["reward_rate"] >= premium_merch["reward_rate"] 