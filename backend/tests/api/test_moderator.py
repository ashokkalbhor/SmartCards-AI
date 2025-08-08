import pytest
from fastapi.testclient import TestClient
from app.models.edit_suggestion import EditSuggestion
from app.models.card_document import CardDocument
from app.models.community import CommunityPost

class TestModerator:
    """Test moderator API endpoints"""
    
    def test_get_moderator_dashboard(self, client, moderator_headers):
        """Test getting moderator dashboard"""
        response = client.get("/api/v1/moderator/dashboard", headers=moderator_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "pending_suggestions" in data
        assert "pending_documents" in data
        assert "pending_posts" in data
        assert "total_reviewed" in data
    
    def test_get_pending_edit_suggestions(self, client, moderator_headers, test_card, test_user, db):
        """Test getting pending edit suggestions"""
        # Create pending suggestions
        suggestions = [
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="general", old_value="5.0", new_value="6.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="merchant_reward", field_name="amazon", old_value="5.0", new_value="7.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="fuel", old_value="3.0", new_value="4.0", suggestion_reason="Test", status="approved")
        ]
        db.add_all(suggestions)
        db.commit()
        
        response = client.get("/api/v1/moderator/edit-suggestions", headers=moderator_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # Should have at least 2 pending suggestions
        assert all(suggestion["status"] == "pending" for suggestion in data)
    
    def test_get_pending_edit_suggestions_with_filters(self, client, moderator_headers, test_card, test_user, db):
        """Test getting pending edit suggestions with filters"""
        # Create suggestions with different field types
        suggestions = [
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="general", old_value="5.0", new_value="6.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="merchant_reward", field_name="amazon", old_value="5.0", new_value="7.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="fuel", old_value="3.0", new_value="4.0", suggestion_reason="Test", status="pending")
        ]
        db.add_all(suggestions)
        db.commit()
        
        # Test field type filter
        response = client.get("/api/v1/moderator/edit-suggestions?field_type=spending_category", headers=moderator_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(suggestion["field_type"] == "spending_category" for suggestion in data)
        
        # Test status filter
        response = client.get("/api/v1/moderator/edit-suggestions?status_filter=pending", headers=moderator_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(suggestion["status"] == "pending" for suggestion in data)
    
    def test_review_edit_suggestion_approve(self, client, moderator_headers, test_card, test_user, test_spending_category, db):
        """Test approving an edit suggestion"""
        # Create a pending suggestion
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
        
        response = client.put(
            f"/api/v1/moderator/edit-suggestions/{suggestion.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion approved"
        
        # Check that the card data was updated
        db.refresh(test_spending_category)
        assert test_spending_category.reward_rate == 6.0
    
    def test_review_edit_suggestion_reject(self, client, moderator_headers, test_card, test_user, db):
        """Test rejecting an edit suggestion"""
        # Create a pending suggestion
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
        
        response = client.put(
            f"/api/v1/moderator/edit-suggestions/{suggestion.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Edit suggestion rejected"
    
    def test_review_edit_suggestion_already_reviewed(self, client, moderator_headers, test_card, test_user, db):
        """Test reviewing already reviewed suggestion"""
        # Create an approved suggestion
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
        
        response = client.put(
            f"/api/v1/moderator/edit-suggestions/{suggestion.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 400
        assert "already been reviewed" in response.json()["detail"]
    
    def test_get_pending_documents(self, client, moderator_headers, test_card, test_user, db):
        """Test getting pending documents"""
        # Create documents with different statuses
        documents = [
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 1", document_type="link", content="https://example.com", status="pending"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 2", document_type="file", content="/uploads/2.pdf", status="approved"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 3", document_type="link", content="https://example.com", status="rejected")
        ]
        db.add_all(documents)
        db.commit()
        
        response = client.get("/api/v1/moderator/documents", headers=moderator_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(doc["status"] == "pending" for doc in data)
    
    def test_review_document_approve(self, client, moderator_headers, test_card, test_user, db):
        """Test approving a document"""
        # Create a pending document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="link",
            content="https://example.com",
            status="pending"
        )
        db.add(document)
        db.commit()
        
        review_data = {
            "status": "approved",
            "review_notes": "Good document"
        }
        
        response = client.put(
            f"/api/v1/moderator/documents/{document.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Document approved"
    
    def test_review_document_reject(self, client, moderator_headers, test_card, test_user, db):
        """Test rejecting a document"""
        # Create a pending document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="link",
            content="https://example.com",
            status="pending"
        )
        db.add(document)
        db.commit()
        
        review_data = {
            "status": "rejected",
            "review_notes": "Inappropriate content"
        }
        
        response = client.put(
            f"/api/v1/moderator/documents/{document.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Document rejected"
    
    def test_get_pending_posts(self, client, moderator_headers, test_card, test_user, db):
        """Test getting pending community posts"""
        # Create posts with different statuses
        posts = [
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 1", content="Content", post_type="question", is_active=True, status="pending"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 2", content="Content", post_type="discussion", is_active=True, status="approved"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 3", content="Content", post_type="review", is_active=True, status="rejected")
        ]
        db.add_all(posts)
        db.commit()
        
        response = client.get("/api/v1/moderator/posts", headers=moderator_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(post["status"] == "pending" for post in data)
    
    def test_review_post_approve(self, client, moderator_headers, test_card, test_user, db):
        """Test approving a community post"""
        # Create a pending post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            content="Test content",
            post_type="discussion",
            is_active=True,
            status="pending"
        )
        db.add(post)
        db.commit()
        
        review_data = {
            "status": "approved",
            "review_notes": "Good post"
        }
        
        response = client.put(
            f"/api/v1/moderator/posts/{post.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Post approved"
    
    def test_review_post_reject(self, client, moderator_headers, test_card, test_user, db):
        """Test rejecting a community post"""
        # Create a pending post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            content="Test content",
            post_type="discussion",
            is_active=True,
            status="pending"
        )
        db.add(post)
        db.commit()
        
        review_data = {
            "status": "rejected",
            "review_notes": "Inappropriate content"
        }
        
        response = client.put(
            f"/api/v1/moderator/posts/{post.id}",
            json=review_data,
            headers=moderator_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Post rejected"
    
    def test_get_moderator_stats(self, client, moderator_headers, test_card, test_user, db):
        """Test getting moderator statistics"""
        # Create various items for moderation
        suggestions = [
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="spending_category", field_name="general", old_value="5.0", new_value="6.0", suggestion_reason="Test", status="pending"),
            EditSuggestion(user_id=test_user.id, card_master_id=test_card.id, field_type="merchant_reward", field_name="amazon", old_value="5.0", new_value="7.0", suggestion_reason="Test", status="approved")
        ]
        documents = [
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 1", document_type="link", content="https://example.com", status="pending"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 2", document_type="file", content="/uploads/2.pdf", status="approved")
        ]
        posts = [
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 1", content="Content", post_type="question", is_active=True, status="pending"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 2", content="Content", post_type="discussion", is_active=True, status="approved")
        ]
        
        db.add_all(suggestions + documents + posts)
        db.commit()
        
        response = client.get("/api/v1/moderator/stats", headers=moderator_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "pending_suggestions" in data
        assert "pending_documents" in data
        assert "pending_posts" in data
        assert "total_reviewed" in data
        assert data["pending_suggestions"] >= 1
        assert data["pending_documents"] >= 1
        assert data["pending_posts"] >= 1
    
    def test_moderator_access_denied_for_user(self, client, auth_headers):
        """Test that regular users cannot access moderator endpoints"""
        response = client.get("/api/v1/moderator/dashboard", headers=auth_headers)
        
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]
    
    def test_moderator_access_denied_for_admin(self, client, admin_headers):
        """Test that admins cannot access moderator endpoints"""
        response = client.get("/api/v1/moderator/dashboard", headers=admin_headers)
        
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"] 