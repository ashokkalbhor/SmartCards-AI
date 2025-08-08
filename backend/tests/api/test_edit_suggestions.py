import pytest
from fastapi.testclient import TestClient
from app.models.edit_suggestion import EditSuggestion

class TestEditSuggestions:
    """Test edit suggestions functionality"""
    
    def test_submit_spending_category_suggestion(self, client, auth_headers, test_card, test_spending_category):
        """Test submitting spending category edit suggestion"""
        suggestion_data = {
            "field_type": "spending_category",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Increase reward rate for better customer value"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion submitted successfully"
    
    def test_submit_merchant_reward_suggestion(self, client, auth_headers, test_card, test_merchant_reward):
        """Test submitting merchant reward edit suggestion"""
        suggestion_data = {
            "field_type": "merchant_reward",
            "field_name": "amazon",
            "new_value": "7.0",
            "suggestion_reason": "Increase Amazon rewards for better customer experience"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion submitted successfully"
    
    def test_submit_spending_category_cap_suggestion(self, client, auth_headers, test_card, test_spending_category):
        """Test submitting spending category cap edit suggestion"""
        suggestion_data = {
            "field_type": "spending_category_cap",
            "field_name": "general",
            "new_value": "600",
            "suggestion_reason": "Increase cap for better customer benefits"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion submitted successfully"
    
    def test_submit_merchant_reward_cap_suggestion(self, client, auth_headers, test_card, test_merchant_reward):
        """Test submitting merchant reward cap edit suggestion"""
        suggestion_data = {
            "field_type": "merchant_reward_cap",
            "field_name": "amazon",
            "new_value": "600",
            "suggestion_reason": "Increase Amazon cap for better rewards"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion submitted successfully"
    
    def test_submit_suggestion_card_not_found(self, client, auth_headers):
        """Test submitting suggestion for non-existent card"""
        suggestion_data = {
            "field_type": "spending_category",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Test reason"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": 99999})
        
        assert response.status_code == 404
        assert "Card not found" in response.json()["detail"]
    
    def test_submit_suggestion_invalid_field_type(self, client, auth_headers, test_card):
        """Test submitting suggestion with invalid field type"""
        suggestion_data = {
            "field_type": "invalid_field",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Test reason"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 400
        assert "Invalid field type" in response.json()["detail"]
    
    def test_submit_duplicate_suggestion(self, client, auth_headers, test_card, test_spending_category, db):
        """Test submitting duplicate suggestion"""
        # Create existing suggestion
        suggestion = EditSuggestion(
            user_id=1,  # Will be set by the endpoint
            card_master_id=test_card.id,
            field_type="spending_category",
            field_name="general",
            old_value="5.0",
            new_value="6.0",
            suggestion_reason="Test reason",
            status="pending"
        )
        db.add(suggestion)
        db.commit()
        
        # Try to submit same suggestion again
        suggestion_data = {
            "field_type": "spending_category",
            "field_name": "general",
            "new_value": "6.0",
            "suggestion_reason": "Test reason"
        }
        
        response = client.post(f"/api/v1/user-roles/edit-suggestions", 
                             json=suggestion_data, 
                             headers=auth_headers,
                             params={"card_id": test_card.id})
        
        assert response.status_code == 400
        assert "already have a pending suggestion" in response.json()["detail"]
    
    def test_get_my_suggestions(self, client, auth_headers, test_card, test_user, db):
        """Test getting user's own suggestions"""
        # Create a suggestion for the test user
        suggestion = EditSuggestion(
            user_id=test_user.id,
            card_master_id=test_card.id,
            field_type="spending_category",
            field_name="general",
            old_value="5.0",
            new_value="6.0",
            suggestion_reason="Test reason",
            status="pending"
        )
        db.add(suggestion)
        db.commit()
        
        response = client.get("/api/v1/user-roles/my-suggestions", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["field_type"] == "spending_category"
        assert data[0]["field_name"] == "general"
        assert data[0]["new_value"] == "6.0"
    
    def test_get_my_suggestions_with_filter(self, client, auth_headers, test_card, test_user, db):
        """Test getting user's suggestions with status filter"""
        # Create suggestions with different statuses
        pending_suggestion = EditSuggestion(
            user_id=test_user.id,
            card_master_id=test_card.id,
            field_type="spending_category",
            field_name="general",
            old_value="5.0",
            new_value="6.0",
            suggestion_reason="Test reason",
            status="pending"
        )
        approved_suggestion = EditSuggestion(
            user_id=test_user.id,
            card_master_id=test_card.id,
            field_type="merchant_reward",
            field_name="amazon",
            old_value="5.0",
            new_value="7.0",
            suggestion_reason="Test reason",
            status="approved"
        )
        db.add_all([pending_suggestion, approved_suggestion])
        db.commit()
        
        # Test pending filter
        response = client.get("/api/v1/user-roles/my-suggestions?status_filter=pending", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(s["status"] == "pending" for s in data)
        
        # Test approved filter
        response = client.get("/api/v1/user-roles/my-suggestions?status_filter=approved", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(s["status"] == "approved" for s in data)
    
    def test_get_my_suggestions_stats(self, client, auth_headers, test_card, test_user, db):
        """Test getting user's suggestion statistics"""
        # Create suggestions with different statuses
        suggestions = [
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="general", old_value="5.0", new_value="6.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="merchant_reward", field_name="amazon", old_value="5.0", new_value="7.0", suggestion_reason="Test", status="approved"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="fuel", old_value="3.0", new_value="4.0", suggestion_reason="Test", status="rejected")
        ]
        db.add_all(suggestions)
        db.commit()
        
        response = client.get("/api/v1/user-roles/my-suggestions/stats", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_suggestions" in data
        assert "pending_count" in data
        assert "approved_count" in data
        assert "rejected_count" in data
        assert data["total_suggestions"] == 3
        assert data["pending_count"] == 1
        assert data["approved_count"] == 1
        assert data["rejected_count"] == 1 