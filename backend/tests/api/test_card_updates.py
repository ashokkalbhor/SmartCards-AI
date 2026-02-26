"""
Tests for Card Updates API endpoints
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models.card_master_data import CardMasterData
from app.models.credit_card import CreditCard
from app.models.user import User


class TestCardUpdatesAPI:
    """Test card updates endpoints"""

    def test_trigger_all_unauthorized(self, client):
        """Test trigger-all without authentication"""
        response = client.post("/api/v1/card-updates/trigger-all")
        assert response.status_code == 401

    def test_trigger_all_non_admin(self, client, user_headers):
        """Test trigger-all with non-admin user"""
        response = client.post("/api/v1/card-updates/trigger-all", headers=user_headers)
        assert response.status_code == 403
        assert "Admin privileges required" in response.json()["detail"]

    @patch('app.services.card_update_scheduler.card_update_scheduler.run_now')
    def test_trigger_all_success(self, mock_run, client, admin_headers):
        """Test trigger-all with admin user"""
        mock_run.return_value = AsyncMock()
        
        response = client.post("/api/v1/card-updates/trigger-all", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        assert "Card update process started" in data["message"]

    @patch('app.services.card_update_scheduler.card_update_scheduler.is_running', True)
    def test_trigger_all_already_running(self, client, admin_headers):
        """Test trigger-all when update is already running"""
        response = client.post("/api/v1/card-updates/trigger-all", headers=admin_headers)
        
        assert response.status_code == 409
        assert "already running" in response.json()["detail"]

    def test_trigger_portfolio_unauthorized(self, client):
        """Test trigger-portfolio without authentication"""
        response = client.post("/api/v1/card-updates/trigger-portfolio")
        assert response.status_code == 401

    def test_trigger_portfolio_non_admin(self, client, user_headers):
        """Test trigger-portfolio with non-admin user"""
        response = client.post("/api/v1/card-updates/trigger-portfolio", headers=user_headers)
        assert response.status_code == 403

    def test_trigger_portfolio_no_cards(self, client, admin_headers, db):
        """Test trigger-portfolio when no cards exist in portfolios"""
        # Ensure no active credit cards in DB
        db.query(CreditCard).delete()
        db.commit()
        
        response = client.post("/api/v1/card-updates/trigger-portfolio", headers=admin_headers)
        
        assert response.status_code == 400
        assert "No cards found in user portfolios" in response.json()["detail"]

    @patch('app.services.card_update_scheduler.card_update_scheduler.run_portfolio_update')
    def test_trigger_portfolio_success(self, mock_run, client, admin_headers, db, test_user):
        """Test trigger-portfolio with cards in portfolio"""
        mock_run.return_value = AsyncMock()
        
        # Create test card and add to user portfolio
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            is_active=True
        )
        db.add(card)
        db.flush()
        
        user_card = CreditCard(
            user_id=test_user.id,
            card_master_data_id=card.id,
            card_name="Test Card",
            card_type="Credit",
            card_network="Visa",
            card_number_last4="1234",
            card_holder_name="Test User",
            expiry_month=12,
            expiry_year=2027,
            is_active=True
        )
        db.add(user_card)
        db.commit()
        
        response = client.post("/api/v1/card-updates/trigger-portfolio", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        assert data["portfolio_cards"] >= 1
        assert "Portfolio update started" in data["message"]

    @patch('app.services.card_update_scheduler.card_update_scheduler.is_running', True)
    def test_trigger_portfolio_already_running(self, client, admin_headers, db, test_user):
        """Test trigger-portfolio when update is already running"""
        # Create test card in portfolio
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            is_active=True
        )
        db.add(card)
        db.flush()
        
        user_card = CreditCard(
            user_id=test_user.id,
            card_master_data_id=card.id,
            card_name="Test Card",
            card_type="Credit",
            card_network="Visa",
            card_number_last4="1234",
            card_holder_name="Test User",
            expiry_month=12,
            expiry_year=2027,
            is_active=True
        )
        db.add(user_card)
        db.commit()
        
        response = client.post("/api/v1/card-updates/trigger-portfolio", headers=admin_headers)
        
        assert response.status_code == 409
        assert "already running" in response.json()["detail"]

    def test_trigger_card_unauthorized(self, client):
        """Test trigger-card without authentication"""
        response = client.post("/api/v1/card-updates/trigger-card/1")
        assert response.status_code == 401

    def test_trigger_card_non_admin(self, client, user_headers):
        """Test trigger-card with non-admin user"""
        response = client.post("/api/v1/card-updates/trigger-card/1", headers=user_headers)
        assert response.status_code == 403

    def test_trigger_card_not_found(self, client, admin_headers, db):
        """Test trigger-card with non-existent card"""
        response = client.post("/api/v1/card-updates/trigger-card/999999", headers=admin_headers)
        assert response.status_code == 404
        assert "Card not found" in response.json()["detail"]

    @patch('app.services.card_update_scheduler.card_update_scheduler.run_single_card')
    def test_trigger_card_success(self, mock_run, client, admin_headers, db):
        """Test trigger-card with valid card"""
        # Create test card
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            is_active=True
        )
        db.add(card)
        db.commit()
        
        mock_run.return_value = {
            "status": {},
            "suggestions_created": 2,
            "skipped": 0,
            "failed": 0
        }
        
        response = client.post(f"/api/v1/card-updates/trigger-card/{card.id}", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["card_id"] == card.id
        assert data["suggestions_created"] == 2

    def test_get_status_unauthorized(self, client):
        """Test status endpoint without authentication"""
        response = client.get("/api/v1/card-updates/status")
        assert response.status_code == 401

    def test_get_status_non_admin(self, client, user_headers):
        """Test status endpoint with non-admin user"""
        response = client.get("/api/v1/card-updates/status", headers=user_headers)
        assert response.status_code == 403

    @patch('app.services.card_update_scheduler.card_update_scheduler.get_status')
    def test_get_status_success(self, mock_status, client, admin_headers):
        """Test status endpoint with admin user"""
        mock_status.return_value = {
            "is_running": False,
            "scheduler_running": True,
            "next_run": "2026-03-01T00:00:00",
            "progress": {
                "total_cards": 0,
                "processed_cards": 0,
                "current": None
            },
            "last_run_summary": None,
            "last_error": None
        }
        
        response = client.get("/api/v1/card-updates/status", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "is_running" in data
        assert "scheduler_running" in data
        assert "next_run" in data


class TestCardUpdateScheduler:
    """Test CardUpdateScheduler methods"""

    @pytest.mark.asyncio
    @patch('app.services.card_update_scheduler.card_update_scheduler.process_card_update')
    async def test_portfolio_update_filters_correctly(self, mock_process, db, test_user):
        """Test that portfolio update only processes cards with holders"""
        from app.services.card_update_scheduler import card_update_scheduler
        
        # Create cards: 2 with holders, 1 without
        card_with_holder1 = CardMasterData(
            bank_name="Bank A",
            card_name="Card A",
            is_active=True
        )
        card_with_holder2 = CardMasterData(
            bank_name="Bank B",
            card_name="Card B",
            is_active=True
        )
        card_without_holder = CardMasterData(
            bank_name="Bank C",
            card_name="Card C",
            is_active=True
        )
        
        db.add_all([card_with_holder1, card_with_holder2, card_without_holder])
        db.flush()
        
        # Add to user portfolio
        user_card1 = CreditCard(
            user_id=test_user.id,
            card_master_data_id=card_with_holder1.id,
            is_active=True
        )
        user_card2 = CreditCard(
            user_id=test_user.id,
            card_master_data_id=card_with_holder2.id,
            is_active=True
        )
        db.add_all([user_card1, user_card2])
        db.commit()
        
        mock_process.return_value = AsyncMock()
        
        # Run portfolio update
        await card_update_scheduler.run_portfolio_update()
        
        # Should process 2 cards (not 3)
        assert mock_process.call_count == 2

    @pytest.mark.asyncio
    @patch('app.services.card_update_scheduler.card_update_scheduler.process_card_update')
    async def test_monthly_update_uses_portfolio_filter(self, mock_process, db, test_user):
        """Test that monthly update now uses portfolio filtering"""
        from app.services.card_update_scheduler import card_update_scheduler
        
        # Create card with holder
        card = CardMasterData(
            bank_name="Test Bank",
            card_name="Test Card",
            is_active=True
        )
        db.add(card)
        db.flush()
        
        user_card = CreditCard(
            user_id=test_user.id,
            card_master_data_id=card.id,
            is_active=True
        )
        db.add(user_card)
        db.commit()
        
        mock_process.return_value = AsyncMock()
        
        # Run monthly update
        await card_update_scheduler.run_monthly_update()
        
        # Should process the card
        assert mock_process.call_count >= 1
        
        # Check last_run_summary
        assert card_update_scheduler.last_run_summary is not None
        assert card_update_scheduler.last_run_summary["total_cards"] >= 1
