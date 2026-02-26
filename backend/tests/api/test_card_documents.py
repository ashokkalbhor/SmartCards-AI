import pytest
from fastapi.testclient import TestClient
from app.models.card_document import CardDocument
from app.models.card_master_data import CardMasterData
import os
import tempfile

class TestCardDocuments:
    """Test card documents API endpoints"""
    
    def test_get_card_documents(self, client, test_card, test_user, db):
        """Test getting documents for a card"""
        # Create a test document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Card Terms and Conditions",
            description="Official terms and conditions document",
            document_type="file",
            content="/uploads/test.pdf",
            file_name="terms.pdf",
            file_size=1024,
            file_type="application/pdf",
            status="approved"
        )
        db.add(document)
        db.commit()
        
        response = client.get(f"/api/v1/cards/{test_card.id}/documents")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Card Terms and Conditions"
        assert data[0]["user_name"] == test_user.full_name
        assert data[0]["status"] == "approved"
    
    def test_get_card_documents_with_filters(self, client, test_card, test_user, db):
        """Test getting documents with filters"""
        # Create documents with different statuses
        documents = [
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 1", document_type="file", content="/uploads/1.pdf", status="approved"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 2", document_type="link", content="https://example.com", status="pending"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 3", document_type="file", content="/uploads/3.pdf", status="rejected")
        ]
        db.add_all(documents)
        db.commit()
        
        # Test status filter
        response = client.get(f"/api/v1/cards/{test_card.id}/documents?status_filter=approved")
        assert response.status_code == 200
        data = response.json()
        assert all(doc["status"] == "approved" for doc in data)
        
        # Test document type filter
        response = client.get(f"/api/v1/cards/{test_card.id}/documents?document_type=file")
        assert response.status_code == 200
        data = response.json()
        assert all(doc["document_type"] == "file" for doc in data)
    
    def test_create_card_document(self, client, auth_headers, test_card):
        """Test creating a new card document"""
        document_data = {
            "title": "Card Benefits Guide",
            "description": "Comprehensive guide to card benefits",
            "document_type": "link",
            "content": "https://example.com/benefits",
            "submission_reason": "Official benefits documentation"
        }
        
        response = client.post(
            f"/api/v1/cards/{test_card.id}/documents",
            json=document_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Card Benefits Guide"
        assert data["description"] == "Comprehensive guide to card benefits"
        assert data["document_type"] == "link"
        assert data["content"] == "https://example.com/benefits"
        assert data["status"] == "pending"
        assert data["user_name"] == "Test User"
    
    def test_create_card_document_invalid_type(self, client, auth_headers, test_card):
        """Test creating document with invalid type"""
        document_data = {
            "title": "Test document",
            "description": "Test description",
            "document_type": "invalid_type",
            "content": "https://example.com",
            "submission_reason": "Test reason"
        }
        
        response = client.post(
            f"/api/v1/cards/{test_card.id}/documents",
            json=document_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_create_card_document_card_not_found(self, client, auth_headers):
        """Test creating document for non-existent card"""
        document_data = {
            "title": "Test document",
            "description": "Test description",
            "document_type": "link",
            "content": "https://example.com",
            "submission_reason": "Test reason"
        }
        
        response = client.post(
            "/api/v1/cards/99999/documents",
            json=document_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_upload_card_document_file(self, client, auth_headers, test_card):
        """Test uploading a file document"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(b"Test PDF content")
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, "rb") as file:
                response = client.post(
                    f"/api/v1/cards/{test_card.id}/documents/upload",
                    files={"file": ("test.pdf", file, "application/pdf")},
                    data={
                        "title": "Uploaded PDF",
                        "description": "Test PDF upload",
                        "submission_reason": "Testing file upload"
                    },
                    headers=auth_headers
                )
            
            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "Uploaded PDF"
            assert data["description"] == "Test PDF upload"
            assert data["document_type"] == "file"
            assert data["file_name"] == "test.pdf"
            assert data["file_type"] == "application/pdf"
            assert data["status"] == "pending"
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def test_upload_card_document_invalid_file(self, client, auth_headers, test_card):
        """Test uploading invalid file"""
        # Create a temporary file with invalid extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
            temp_file.write(b"Test executable content")
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, "rb") as file:
                response = client.post(
                    f"/api/v1/cards/{test_card.id}/documents/upload",
                    files={"file": ("test.exe", file, "application/octet-stream")},
                    data={
                        "title": "Invalid file",
                        "description": "Test invalid file upload",
                        "submission_reason": "Testing invalid file"
                    },
                    headers=auth_headers
                )
            
            assert response.status_code == 400
            assert "Invalid file type" in response.json()["detail"]
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def test_get_card_document_by_id(self, client, test_card, test_user, db):
        """Test getting a specific document"""
        # Create a test document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="link",
            content="https://example.com",
            status="approved"
        )
        db.add(document)
        db.commit()
        
        response = client.get(f"/api/v1/documents/{document.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == document.id
        assert data["title"] == "Test document"
        assert data["description"] == "Test description"
        assert data["document_type"] == "link"
        assert data["content"] == "https://example.com"
        assert data["status"] == "approved"
    
    def test_get_card_document_not_found(self, client):
        """Test getting non-existent document"""
        response = client.get("/api/v1/documents/99999")
        
        assert response.status_code == 404
    
    def test_update_card_document(self, client, auth_headers, test_card, test_user, db):
        """Test updating a document"""
        # Create a test document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Original title",
            description="Original description",
            document_type="link",
            content="https://original.com",
            status="pending"
        )
        db.add(document)
        db.commit()
        
        update_data = {
            "title": "Updated title",
            "description": "Updated description",
            "content": "https://updated.com"
        }
        
        response = client.put(
            f"/api/v1/documents/{document.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["description"] == "Updated description"
        assert data["content"] == "https://updated.com"
    
    def test_update_card_document_unauthorized(self, client, auth_headers, test_card, db):
        """Test updating document by different user"""
        # Create a document with a different user
        from app.models.user import User
        other_user = User(
            email="other@example.com",
            full_name="Other User",
            hashed_password="hashed",
            is_active=True
        )
        db.add(other_user)
        db.commit()
        
        document = CardDocument(
            user_id=other_user.id,
            card_master_id=test_card.id,
            title="Original title",
            description="Original description",
            document_type="link",
            content="https://original.com",
            status="pending"
        )
        db.add(document)
        db.commit()
        
        update_data = {
            "title": "Updated title",
            "description": "Updated description"
        }
        
        response = client.put(
            f"/api/v1/documents/{document.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 403
    
    def test_delete_card_document(self, client, auth_headers, test_card, test_user, db):
        """Test deleting a document"""
        # Create a test document
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
        
        response = client.delete(
            f"/api/v1/documents/{document.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Document deleted successfully"
    
    def test_download_card_document(self, client, test_card, test_user, db):
        """Test downloading a document"""
        # Create a test document
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="file",
            content="/uploads/test.pdf",
            file_name="test.pdf",
            file_size=1024,
            file_type="application/pdf",
            status="approved"
        )
        db.add(document)
        db.commit()
        
        response = client.get(f"/api/v1/documents/{document.id}/download")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "test.pdf" in response.headers["content-disposition"]
    
    def test_download_card_document_not_approved(self, client, test_card, test_user, db):
        """Test downloading non-approved document"""
        # Create a test document with pending status
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="file",
            content="/uploads/test.pdf",
            file_name="test.pdf",
            file_size=1024,
            file_type="application/pdf",
            status="pending"
        )
        db.add(document)
        db.commit()
        
        response = client.get(f"/api/v1/documents/{document.id}/download")
        
        assert response.status_code == 403
    
    def test_download_card_document_not_file(self, client, test_card, test_user, db):
        """Test downloading non-file document"""
        # Create a test document with link type
        document = CardDocument(
            user_id=test_user.id,
            card_master_id=test_card.id,
            title="Test document",
            description="Test description",
            document_type="link",
            content="https://example.com",
            status="approved"
        )
        db.add(document)
        db.commit()
        
        response = client.get(f"/api/v1/documents/{document.id}/download")
        
        assert response.status_code == 400
    
    def test_get_my_documents(self, client, auth_headers, test_card, test_user, db):
        """Test getting user's own documents"""
        # Create documents for the test user
        documents = [
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 1", document_type="link", content="https://example.com", status="approved"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 2", document_type="file", content="/uploads/2.pdf", status="pending"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 3", document_type="link", content="https://example.com", status="rejected")
        ]
        db.add_all(documents)
        db.commit()
        
        response = client.get("/api/v1/documents/my-documents", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(doc["user_name"] == test_user.full_name for doc in data)
    
    def test_get_my_documents_with_filter(self, client, auth_headers, test_card, test_user, db):
        """Test getting user's documents with status filter"""
        # Create documents with different statuses
        documents = [
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 1", document_type="link", content="https://example.com", status="approved"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 2", document_type="file", content="/uploads/2.pdf", status="pending"),
            CardDocument(user_id=test_user.id, card_master_id=test_card.id, title="Doc 3", document_type="link", content="https://example.com", status="rejected")
        ]
        db.add_all(documents)
        db.commit()
        
        # Test approved filter
        response = client.get("/api/v1/documents/my-documents?status_filter=approved", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(doc["status"] == "approved" for doc in data)
        
        # Test pending filter
        response = client.get("/api/v1/documents/my-documents?status_filter=pending", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(doc["status"] == "pending" for doc in data) 