import pytest
from fastapi.testclient import TestClient
from app.models.card_review import CardReview
from app.models.card_master_data import CardMasterData

class TestCardReviews:
    """Test card reviews API endpoints"""
    
    def test_get_card_reviews(self, client, test_card, test_user, db):
        """Test getting reviews for a card"""
        # Create a test review
        review = CardReview(
            user_id=test_user.id,
            card_master_id=test_card.id,
            rating=5,
            review_text="Great card with excellent rewards!",
            pros="Good cashback, no annual fee",
            cons="Limited lounge access",
            is_verified_purchase=True
        )
        db.add(review)
        db.commit()
        
        response = client.get(f"/api/v1/cards/{test_card.id}/reviews")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["rating"] == 5
        assert data[0]["review_text"] == "Great card with excellent rewards!"
        assert data[0]["user_name"] == test_user.full_name
    
    def test_get_card_reviews_empty(self, client, test_card):
        """Test getting reviews for card with no reviews"""
        response = client.get(f"/api/v1/cards/{test_card.id}/reviews")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_get_card_reviews_with_filters(self, client, test_card, test_user, db):
        """Test getting reviews with filters"""
        # Create reviews with different ratings
        reviews = [
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=5, review_text="Great", is_verified_purchase=True),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=3, review_text="Average", is_verified_purchase=False),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=1, review_text="Poor", is_verified_purchase=False)
        ]
        db.add_all(reviews)
        db.commit()
        
        # Test rating filter
        response = client.get(f"/api/v1/cards/{test_card.id}/reviews?min_rating=4")
        assert response.status_code == 200
        data = response.json()
        assert all(review["rating"] >= 4 for review in data)
        
        # Test verified purchase filter
        response = client.get(f"/api/v1/cards/{test_card.id}/reviews?verified_only=true")
        assert response.status_code == 200
        data = response.json()
        assert all(review["is_verified_purchase"] == True for review in data)
    
    def test_create_card_review(self, client, auth_headers, test_card):
        """Test creating a new card review"""
        review_data = {
            "rating": 4,
            "review_text": "Good card with decent rewards",
            "pros": "No annual fee, good cashback",
            "cons": "Limited benefits",
            "is_verified_purchase": True
        }
        
        response = client.post(
            f"/api/v1/cards/{test_card.id}/reviews",
            json=review_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 4
        assert data["review_text"] == "Good card with decent rewards"
        assert data["pros"] == "No annual fee, good cashback"
        assert data["cons"] == "Limited benefits"
        assert data["is_verified_purchase"] == True
    
    def test_create_card_review_invalid_rating(self, client, auth_headers, test_card):
        """Test creating review with invalid rating"""
        review_data = {
            "rating": 6,  # Invalid rating
            "review_text": "Test review",
            "is_verified_purchase": False
        }
        
        response = client.post(
            f"/api/v1/cards/{test_card.id}/reviews",
            json=review_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_create_card_review_card_not_found(self, client, auth_headers):
        """Test creating review for non-existent card"""
        review_data = {
            "rating": 5,
            "review_text": "Test review",
            "is_verified_purchase": False
        }
        
        response = client.post(
            "/api/v1/cards/99999/reviews",
            json=review_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_update_card_review(self, client, auth_headers, test_card, test_user, db):
        """Test updating a card review"""
        # Create a review
        review = CardReview(
            user_id=test_user.id,
            card_master_id=test_card.id,
            rating=3,
            review_text="Original review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        update_data = {
            "rating": 5,
            "review_text": "Updated review",
            "pros": "Great benefits",
            "cons": "High annual fee"
        }
        
        response = client.put(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["rating"] == 5
        assert data["review_text"] == "Updated review"
        assert data["pros"] == "Great benefits"
        assert data["cons"] == "High annual fee"
    
    def test_update_card_review_unauthorized(self, client, auth_headers, test_card, db):
        """Test updating review by different user"""
        # Create a review with a different user
        from app.models.user import User
        other_user = User(
            email="other@example.com",
            full_name="Other User",
            hashed_password="hashed",
            is_active=True
        )
        db.add(other_user)
        db.commit()
        
        review = CardReview(
            user_id=other_user.id,
            card_master_id=test_card.id,
            rating=3,
            review_text="Original review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        update_data = {
            "rating": 5,
            "review_text": "Updated review"
        }
        
        response = client.put(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_delete_card_review(self, client, auth_headers, test_card, test_user, db):
        """Test deleting a card review"""
        # Create a review
        review = CardReview(
            user_id=test_user.id,
            card_master_id=test_card.id,
            rating=3,
            review_text="Test review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        response = client.delete(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Review deleted successfully"
    
    def test_delete_card_review_unauthorized(self, client, auth_headers, test_card, db):
        """Test deleting review by different user"""
        # Create a review with a different user
        from app.models.user import User
        other_user = User(
            email="other@example.com",
            full_name="Other User",
            hashed_password="hashed",
            is_active=True
        )
        db.add(other_user)
        db.commit()
        
        review = CardReview(
            user_id=other_user.id,
            card_master_id=test_card.id,
            rating=3,
            review_text="Test review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        response = client.delete(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_get_review_stats(self, client, test_card, test_user, db):
        """Test getting review statistics"""
        # Create reviews with different ratings
        reviews = [
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=5, review_text="Great", is_verified_purchase=True),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=4, review_text="Good", is_verified_purchase=True),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=3, review_text="Average", is_verified_purchase=False),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=2, review_text="Poor", is_verified_purchase=False),
            CardReview(user_id=test_user.id, card_master_id=test_card.id, rating=1, review_text="Very Poor", is_verified_purchase=False)
        ]
        db.add_all(reviews)
        db.commit()
        
        response = client.get(f"/api/v1/cards/{test_card.id}/reviews/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_reviews" in data
        assert "average_rating" in data
        assert "rating_distribution" in data
        assert data["total_reviews"] == 5
        assert data["average_rating"] == 3.0
        assert len(data["rating_distribution"]) == 5
    
    def test_vote_on_review(self, client, auth_headers, test_card, test_user, db):
        """Test voting on a review"""
        # Create a review
        review = CardReview(
            user_id=test_user.id,
            card_master_id=test_card.id,
            rating=4,
            review_text="Test review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        # Vote helpful
        response = client.post(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}/vote",
            json={"vote_type": "helpful"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Vote recorded successfully"
    
    def test_vote_on_review_invalid_type(self, client, auth_headers, test_card, test_user, db):
        """Test voting with invalid vote type"""
        # Create a review
        review = CardReview(
            user_id=test_user.id,
            card_master_id=test_card.id,
            rating=4,
            review_text="Test review",
            is_verified_purchase=False
        )
        db.add(review)
        db.commit()
        
        response = client.post(
            f"/api/v1/cards/{test_card.id}/reviews/{review.id}/vote",
            json={"vote_type": "invalid"},
            headers=auth_headers
        )
        
        assert response.status_code == 422 