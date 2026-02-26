import pytest
from fastapi.testclient import TestClient
from app.models.community import CommunityPost, CommunityComment
from app.models.card_master_data import CardMasterData

class TestCommunity:
    """Test community API endpoints"""
    
    def test_get_community_posts(self, client, test_card, test_user, db):
        """Test getting community posts"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Best credit card for travel",
            body="I'm looking for a good travel credit card. Any recommendations?"
        )
        db.add(post)
        db.commit()
        
        response = client.get(f"/api/v1/community/cards/{test_card.id}/posts")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["posts"]) >= 1
        assert data["posts"][0]["title"] == "Best credit card for travel"
        assert data["posts"][0]["user_name"] == test_user.full_name
        assert data["posts"][0]["card_name"] == test_card.card_name
    
    def test_get_community_posts_with_filters(self, client, test_card, test_user, db):
        """Test getting community posts with filters"""
        # Create posts with different content
        posts = [
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Question 1", body="Test question"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Discussion 1", body="Test discussion"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Review 1", body="Test review")
        ]
        db.add_all(posts)
        db.commit()
        
        # Test search filter
        response = client.get(f"/api/v1/community/cards/{test_card.id}/posts?search=Question")
        assert response.status_code == 200
        data = response.json()
        assert len(data["posts"]) >= 1
    
    def test_create_community_post(self, client, auth_headers, test_card):
        """Test creating a new community post"""
        post_data = {
            "title": "New credit card comparison",
            "body": "I want to compare different credit cards for daily spending",
            "card_master_id": test_card.id
        }
        
        response = client.post(
            f"/api/v1/community/cards/{test_card.id}/posts",
            json=post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New credit card comparison"
        assert data["body"] == "I want to compare different credit cards for daily spending"
        assert data["user_name"] == "Test User"
    
    def test_create_community_post_invalid_data(self, client, auth_headers, test_card):
        """Test creating post with invalid data"""
        post_data = {
            "title": "",  # Empty title
            "body": "Test content",
            "card_master_id": test_card.id
        }
        
        response = client.post(
            f"/api/v1/community/cards/{test_card.id}/posts",
            json=post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_get_community_post_by_id(self, client, test_card, test_user, db):
        """Test getting a specific community post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        response = client.get(f"/api/v1/community/posts/{post.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == post.id
        assert data["title"] == "Test post"
        assert data["body"] == "Test content"
        assert data["user_name"] == test_user.full_name
    
    def test_get_community_post_not_found(self, client):
        """Test getting non-existent post"""
        response = client.get("/api/v1/community/posts/99999")
        
        assert response.status_code == 404
    
    def test_update_community_post(self, client, auth_headers, test_card, test_user, db):
        """Test updating a community post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Original title",
            body="Original content"
        )
        db.add(post)
        db.commit()
        
        update_data = {
            "title": "Updated title",
            "body": "Updated content"
        }
        
        response = client.put(
            f"/api/v1/community/posts/{post.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["body"] == "Updated content"
    
    def test_update_community_post_unauthorized(self, client, auth_headers, test_card, db):
        """Test updating post by different user"""
        # Create a post with a different user
        from app.models.user import User
        other_user = User(
            email="other@example.com",
            first_name="Other",
            last_name="User",
            hashed_password="hashed",
            is_active=True
        )
        db.add(other_user)
        db.commit()
        
        post = CommunityPost(
            user_id=other_user.id,
            card_master_id=test_card.id,
            title="Original title",
            body="Original content"
        )
        db.add(post)
        db.commit()
        
        update_data = {
            "title": "Updated title",
            "body": "Updated content"
        }
        
        response = client.put(
            f"/api/v1/community/posts/{post.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_delete_community_post(self, client, auth_headers, test_card, test_user, db):
        """Test deleting a community post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        response = client.delete(
            f"/api/v1/community/posts/{post.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Post deleted successfully"
    
    def test_create_community_comment(self, client, auth_headers, test_card, test_user, db):
        """Test creating a comment on a post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        comment_data = {
            "body": "This is a helpful comment"
        }
        
        response = client.post(
            f"/api/v1/community/posts/{post.id}/comments",
            json=comment_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["body"] == "This is a helpful comment"
        assert data["user_name"] == test_user.full_name
        assert data["post_id"] == post.id
    
    def test_create_community_comment_reply(self, client, auth_headers, test_card, test_user, db):
        """Test creating a reply to a comment"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        # Create a parent comment
        parent_comment = CommunityComment(
            user_id=test_user.id,
            post_id=post.id,
            body="Parent comment"
        )
        db.add(parent_comment)
        db.commit()
        
        reply_data = {
            "body": "This is a reply",
            "parent_id": parent_comment.id
        }
        
        response = client.post(
            f"/api/v1/community/posts/{post.id}/comments",
            json=reply_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["body"] == "This is a reply"
        assert data["parent_id"] == parent_comment.id
    
    def test_get_community_comments(self, client, test_card, test_user, db):
        """Test getting comments for a post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        # Create comments
        comments = [
            CommunityComment(user_id=test_user.id, post_id=post.id, body="Comment 1"),
            CommunityComment(user_id=test_user.id, post_id=post.id, body="Comment 2"),
            CommunityComment(user_id=test_user.id, post_id=post.id, body="Comment 3")
        ]
        db.add_all(comments)
        db.commit()
        
        response = client.get(f"/api/v1/community/posts/{post.id}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(comment["post_id"] == post.id for comment in data)
    
    def test_vote_on_post(self, client, auth_headers, test_card, test_user, db):
        """Test voting on a post"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        # Vote up
        response = client.post(
            f"/api/v1/community/posts/{post.id}/vote",
            json={"vote_type": "upvote"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Vote recorded successfully"
    
    def test_vote_on_comment(self, client, auth_headers, test_card, test_user, db):
        """Test voting on a comment"""
        # Create a test post
        post = CommunityPost(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test post",
            body="Test content"
        )
        db.add(post)
        db.commit()
        
        # Create a comment
        comment = CommunityComment(
            user_id=test_user.id,
            post_id=post.id,
            body="Test comment"
        )
        db.add(comment)
        db.commit()
        
        # Vote up
        response = client.post(
            f"/api/v1/community/comments/{comment.id}/vote",
            json={"vote_type": "upvote"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Vote recorded successfully"
    
    def test_get_community_stats(self, client, test_card, test_user, db):
        """Test getting community statistics"""
        # Create posts and comments
        posts = [
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 1", body="Content"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 2", body="Content"),
            CommunityPost(user_id=test_user.id, card_master_id=test_card.id, title="Post 3", body="Content")
        ]
        db.add_all(posts)
        db.commit()
        
        # Create comments
        comments = [
            CommunityComment(user_id=test_user.id, post_id=posts[0].id, body="Comment 1"),
            CommunityComment(user_id=test_user.id, post_id=posts[1].id, body="Comment 2")
        ]
        db.add_all(comments)
        db.commit()
        
        response = client.get("/api/v1/community/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_posts" in data
        assert "total_comments" in data
        assert "total_users" in data
        assert data["total_posts"] >= 3
        assert data["total_comments"] >= 2 