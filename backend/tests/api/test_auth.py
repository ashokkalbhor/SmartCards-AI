import pytest
from fastapi.testclient import TestClient
from app.models.user import User
from app.core.security import verify_password

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_success(self, client, db):
        """Test successful user registration"""
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "testpassword123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert "hashed_password" not in data
        
        # Verify user was created in database
        user = db.query(User).filter(User.email == "newuser@example.com").first()
        assert user is not None
        assert user.full_name == "New User"
        assert verify_password("testpassword123", user.hashed_password)
    
    def test_register_existing_email(self, client, test_user):
        """Test registration with existing email"""
        response = client.post("/api/v1/auth/register", json={
            "email": test_user.email,
            "full_name": "Another User",
            "password": "testpassword123"
        })
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post("/api/v1/auth/register", json={
            "email": "invalid-email",
            "full_name": "Test User",
            "password": "testpassword123"
        })
        
        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "123"
        })
        
        assert response.status_code == 422
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post("/api/v1/auth/login", data={
            "username": test_user.email,
            "password": "password"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email
        assert data["user"]["full_name"] == test_user.full_name
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post("/api/v1/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_inactive_user(self, client, db):
        """Test login with inactive user"""
        # Create inactive user
        user = User(
            email="inactive@example.com",
            full_name="Inactive User",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK2",
            is_active=False
        )
        db.add(user)
        db.commit()
        
        response = client.post("/api/v1/auth/login", data={
            "username": "inactive@example.com",
            "password": "password"
        })
        
        assert response.status_code == 401
        assert "Inactive user" in response.json()["detail"]
    
    def test_get_current_user(self, client, auth_headers, test_user):
        """Test getting current user"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["full_name"] == test_user.full_name
        assert data["role"] == test_user.role
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token"})
        
        assert response.status_code == 401
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, auth_headers):
        """Test token refresh"""
        response = client.post("/api/v1/auth/refresh", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_logout(self, client, auth_headers):
        """Test logout"""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out" 