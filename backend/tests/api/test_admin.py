import pytest
from fastapi.testclient import TestClient
from app.models.edit_suggestion import EditSuggestion
from app.models.user import User

class TestAdmin:
    """Test admin functionality"""
    
    def test_get_admin_info(self, client, admin_headers):
        """Test getting admin information"""
        response = client.get("/api/v1/admin/admin-info", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_cards" in data
        assert "pending_suggestions" in data
    
    def test_get_all_users(self, client, admin_headers, test_user):
        """Test getting all users"""
        response = client.get("/api/v1/admin/users", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(user["email"] == test_user.email for user in data)
    
    def test_get_users_with_filters(self, client, admin_headers, test_user):
        """Test getting users with filters"""
        response = client.get("/api/v1/admin/users?search=test&role_filter=user", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all("test" in user["email"].lower() or "test" in user["full_name"].lower() for user in data)
        assert all(user["role"] == "user" for user in data)
    
    def test_get_moderator_requests(self, client, admin_headers, test_user, db):
        """Test getting moderator requests"""
        # Create a moderator request
        from app.models.user_role import ModeratorRequest
        request = ModeratorRequest(
            user_id=test_user.id,
            reason="I want to help moderate the platform",
            status="pending"
        )
        db.add(request)
        db.commit()
        
        response = client.get("/api/v1/admin/moderator-requests", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["user_name"] == test_user.full_name
        assert data[0]["status"] == "pending"
    
    def test_review_moderator_request(self, client, admin_headers, test_user, db):
        """Test reviewing moderator request"""
        # Create a moderator request
        from app.models.user_role import ModeratorRequest
        request = ModeratorRequest(
            user_id=test_user.id,
            reason="I want to help moderate the platform",
            status="pending"
        )
        db.add(request)
        db.commit()
        
        review_data = {
            "status": "approved",
            "review_notes": "User seems qualified"
        }
        
        response = client.put(f"/api/v1/admin/moderator-requests/{request.id}", 
                            json=review_data, 
                            headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Moderator request approved"
        
        # Check that user role was updated
        db.refresh(test_user)
        assert test_user.role == "moderator"
    
    def test_get_edit_suggestions(self, client, admin_headers, test_card, test_user, db):
        """Test getting edit suggestions"""
        # Create edit suggestions
        suggestions = [
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="general", old_value="5.0", new_value="6.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="merchant_reward", field_name="amazon", old_value="5.0", new_value="7.0", suggestion_reason="Test", status="approved")
        ]
        db.add_all(suggestions)
        db.commit()
        
        response = client.get("/api/v1/admin/edit-suggestions", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert data[0]["user_name"] == test_user.full_name
        assert data[0]["card_name"] == test_card.card_name
    
    def test_review_edit_suggestion_approve(self, client, admin_headers, test_card, test_user, test_spending_category, db):
        """Test approving edit suggestion"""
        # Create edit suggestion
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
        
        review_data = {
            "status": "approved",
            "review_notes": "Good suggestion"
        }
        
        response = client.put(f"/api/v1/admin/edit-suggestions/{suggestion.id}", 
                            json=review_data, 
                            headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion approved"
        
        # Check that the card data was updated
        db.refresh(test_spending_category)
        assert test_spending_category.reward_rate == 6.0
    
    def test_review_edit_suggestion_reject(self, client, admin_headers, test_card, test_user, db):
        """Test rejecting edit suggestion"""
        # Create edit suggestion
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
        
        review_data = {
            "status": "rejected",
            "review_notes": "Not appropriate"
        }
        
        response = client.put(f"/api/v1/admin/edit-suggestions/{suggestion.id}", 
                            json=review_data, 
                            headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion rejected"
    
    def test_review_edit_suggestion_already_reviewed(self, client, admin_headers, test_card, test_user, db):
        """Test reviewing already reviewed suggestion"""
        # Create approved suggestion
        suggestion = EditSuggestion(
            user_id=test_user.id,
            card_master_id=test_card.id,
            field_type="spending_category",
            field_name="general",
            old_value="5.0",
            new_value="6.0",
            suggestion_reason="Test reason",
            status="approved"
        )
        db.add(suggestion)
        db.commit()
        
        review_data = {
            "status": "rejected",
            "review_notes": "Change mind"
        }
        
        response = client.put(f"/api/v1/admin/edit-suggestions/{suggestion.id}", 
                            json=review_data, 
                            headers=admin_headers)
        
        assert response.status_code == 400
        assert "already been reviewed" in response.json()["detail"]
    
    def test_get_admin_stats(self, client, admin_headers, test_user, test_card, db):
        """Test getting admin statistics"""
        response = client.get("/api/v1/admin/stats", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_cards" in data
        assert "pending_suggestions" in data
        assert "pending_moderator_requests" in data
        assert data["total_users"] >= 1
        assert data["total_cards"] >= 1
    
    def test_admin_access_denied_for_user(self, client, auth_headers):
        """Test that regular users cannot access admin endpoints"""
        response = client.get("/api/v1/admin/admin-info", headers=auth_headers)
        
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]
    
    def test_admin_access_denied_for_moderator(self, client, moderator_headers):
        """Test that moderators cannot access admin endpoints"""
        response = client.get("/api/v1/admin/admin-info", headers=moderator_headers)
        
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"] 