import pytest
from fastapi.testclient import TestClient
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward

class TestCardMasterData:
    """Test card master data endpoints"""
    
    def test_get_cards_list(self, client, test_card):
        """Test getting list of cards"""
        response = client.get("/api/v1/cards")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(card["bank_name"] == test_card.bank_name for card in data)
    
    def test_get_cards_with_filters(self, client, test_card):
        """Test getting cards with filters"""
        response = client.get("/api/v1/cards?bank_name=Test Bank&is_active=true")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(card["bank_name"] == "Test Bank" for card in data)
        assert all(card["is_active"] == True for card in data)
    
    def test_get_card_by_id(self, client, test_card):
        """Test getting card by ID"""
        response = client.get(f"/api/v1/cards/{test_card.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_card.id
        assert data["bank_name"] == test_card.bank_name
        assert data["card_name"] == test_card.card_name
    
    def test_get_card_by_id_not_found(self, client):
        """Test getting non-existent card"""
        response = client.get("/api/v1/cards/99999")
        
        assert response.status_code == 404
        assert "Card not found" in response.json()["detail"]
    
    def test_get_card_with_categories_and_merchants(self, client, test_card, test_spending_category, test_merchant_reward):
        """Test getting card with spending categories and merchant rewards"""
        response = client.get(f"/api/v1/cards/{test_card.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "spending_categories" in data
        assert "merchant_rewards" in data
        
        # Check spending categories
        categories = data["spending_categories"]
        assert len(categories) >= 1
        category = next((cat for cat in categories if cat["category_name"] == "general"), None)
        assert category is not None
        assert category["reward_rate"] == 5.0
        assert category["reward_cap"] == 500
        
        # Check merchant rewards
        merchants = data["merchant_rewards"]
        assert len(merchants) >= 1
        merchant = next((merch for merch in merchants if merch["merchant_name"] == "amazon"), None)
        assert merchant is not None
        assert merchant["reward_rate"] == 5.0
        assert merchant["reward_cap"] == 500
    
    def test_create_card(self, client, admin_headers):
        """Test creating new card (admin only)"""
        card_data = {
            "bank_name": "New Bank",
            "card_name": "New Card",
            "card_network": "Mastercard",
            "card_tier": "premium",
            "joining_fee": 1499,
            "annual_fee": 1499,
            "is_lifetime_free": False,
            "description": "New test card"
        }
        
        response = client.post("/api/v1/cards", json=card_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["bank_name"] == "New Bank"
        assert data["card_name"] == "New Card"
        assert data["card_network"] == "Mastercard"
    
    def test_create_card_duplicate(self, client, admin_headers, test_card):
        """Test creating duplicate card"""
        card_data = {
            "bank_name": test_card.bank_name,
            "card_name": test_card.card_name,
            "card_network": test_card.card_network,
            "card_tier": test_card.card_tier
        }
        
        response = client.post("/api/v1/cards", json=card_data, headers=admin_headers)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_update_card(self, client, admin_headers, test_card):
        """Test updating card"""
        update_data = {
            "description": "Updated description",
            "annual_fee": 1999
        }
        
        response = client.put(f"/api/v1/cards/{test_card.id}", json=update_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
        assert data["annual_fee"] == 1999
    
    def test_delete_card(self, client, admin_headers, test_card):
        """Test deleting card"""
        response = client.delete(f"/api/v1/cards/{test_card.id}", headers=admin_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Card deleted successfully"
    
    def test_create_spending_category(self, client, admin_headers, test_card):
        """Test creating spending category"""
        category_data = {
            "category_name": "fuel",
            "category_display_name": "Fuel & Petrol",
            "reward_rate": 3.0,
            "reward_type": "cashback",
            "reward_cap": 300,
            "reward_cap_period": "monthly"
        }
        
        response = client.post(f"/api/v1/cards/{test_card.id}/categories", json=category_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["category_name"] == "fuel"
        assert data["reward_rate"] == 3.0
        assert data["reward_cap"] == 300
    
    def test_update_spending_category(self, client, admin_headers, test_spending_category):
        """Test updating spending category"""
        update_data = {
            "reward_rate": 4.0,
            "reward_cap": 400
        }
        
        response = client.put(f"/api/v1/categories/{test_spending_category.id}", json=update_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["reward_rate"] == 4.0
        assert data["reward_cap"] == 400
    
    def test_delete_spending_category(self, client, admin_headers, test_spending_category):
        """Test deleting spending category"""
        response = client.delete(f"/api/v1/categories/{test_spending_category.id}", headers=admin_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Category deleted successfully"
    
    def test_create_merchant_reward(self, client, admin_headers, test_card):
        """Test creating merchant reward"""
        merchant_data = {
            "merchant_name": "flipkart",
            "merchant_display_name": "Flipkart",
            "merchant_category": "ecommerce",
            "reward_rate": 4.0,
            "reward_type": "cashback",
            "reward_cap": 400,
            "reward_cap_period": "monthly"
        }
        
        response = client.post(f"/api/v1/cards/{test_card.id}/merchants", json=merchant_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["merchant_name"] == "flipkart"
        assert data["reward_rate"] == 4.0
        assert data["reward_cap"] == 400
    
    def test_update_merchant_reward(self, client, admin_headers, test_merchant_reward):
        """Test updating merchant reward"""
        update_data = {
            "reward_rate": 6.0,
            "reward_cap": 600
        }
        
        response = client.put(f"/api/v1/merchants/{test_merchant_reward.id}", json=update_data, headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["reward_rate"] == 6.0
        assert data["reward_cap"] == 600
    
    def test_delete_merchant_reward(self, client, admin_headers, test_merchant_reward):
        """Test deleting merchant reward"""
        response = client.delete(f"/api/v1/merchants/{test_merchant_reward.id}", headers=admin_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Merchant reward deleted successfully"
    
    def test_get_card_comparison(self, client, test_card):
        """Test getting card comparison data"""
        response = client.get(f"/api/v1/cards/comparison?card_ids={test_card.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(card["id"] == test_card.id for card in data)
    
    def test_get_available_banks(self, client):
        """Test getting available banks"""
        response = client.get("/api/v1/cards/banks")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "Test Bank" in data
    
    def test_get_available_categories(self, client):
        """Test getting available categories"""
        response = client.get("/api/v1/cards/categories")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "general" in data
    
    def test_get_available_merchants(self, client):
        """Test getting available merchants"""
        response = client.get("/api/v1/cards/merchants")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "amazon" in data 