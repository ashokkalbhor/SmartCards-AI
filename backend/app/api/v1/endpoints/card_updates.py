"""
API endpoints for automated card data updates
"""
import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.user_role import UserRole
from app.models.card_master_data import CardMasterData
from app.models.credit_card import CreditCard
from app.services.card_update_scheduler import card_update_scheduler
from app.services.card_update_service import CardUpdateService
# from app.services.web_scraping_service import WebScrapingService
from app.core.agent_graph import card_update_graph

logger = logging.getLogger(__name__)
router = APIRouter()


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verify current user has admin role"""
    admin_role = db.query(UserRole).filter(
        UserRole.user_id == current_user.id,
        UserRole.role_type == "admin",
        UserRole.status == "active"
    ).first()
    
    if not admin_role:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    return current_user


@router.post("/trigger-all")
async def trigger_all_updates(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, str]:
    """
    Manually trigger update process for all active cards
    Admin only
    """
    if card_update_scheduler.is_running:
        raise HTTPException(status_code=409, detail="Update process is already running")
    
    # Run in background to avoid timeout
    background_tasks.add_task(card_update_scheduler.run_now)
    
    return {
        "status": "started",
        "message": "Card update process started in background"
    }


@router.post("/trigger-portfolio")
async def trigger_portfolio_updates(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Manually trigger update process for cards in user portfolios only
    (cards with at least one active holder)
    Admin only
    """
    if card_update_scheduler.is_running:
        raise HTTPException(status_code=409, detail="Update process is already running")
    
    # Check if any cards have holders before starting
    from sqlalchemy import func
    portfolio_card_count = db.query(func.count(func.distinct(CreditCard.card_master_data_id))).filter(
        CreditCard.is_active == True
    ).scalar() or 0
    
    if portfolio_card_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No cards found in user portfolios. Please add cards to portfolios before triggering updates."
        )
    
    # Run in background to avoid timeout
    background_tasks.add_task(card_update_scheduler.run_portfolio_update)
    
    return {
        "status": "started",
        "message": f"Portfolio card update started for {portfolio_card_count} cards in background",
        "portfolio_cards": portfolio_card_count
    }


@router.post("/trigger-card/{card_id}")
async def trigger_single_card_update(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Manually trigger update for a specific card
    Admin only
    """
    # Verify card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    try:
        if card_update_scheduler.is_running:
            raise HTTPException(status_code=409, detail="Update process is already running")

        result = await card_update_scheduler.run_single_card(card, db)
        summary = result.get("status", {})

        return {
            "status": "completed",
            "card_id": card_id,
            "card_name": card.display_name,
            "message": "Card update completed",
            "suggestions_created": result.get("suggestions_created", 0),
            "skipped": result.get("skipped", 0),
            "failed": result.get("failed", 0),
            "details": summary,
        }
    
    except Exception as e:
        logger.error(f"Error updating card {card_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.get("/status")
async def get_update_status(
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Get current status of automated update process
    Admin only
    """
    return card_update_scheduler.get_status()


@router.post("/extract-from-url")
async def extract_from_url(
    url: str,
    card_name: str,
    bank_name: str,
    card_variant: str = None,
    current_user: User = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """
    Extract card data from a given URL (testing/debugging endpoint)
    Admin only
    """
    try:
        # Agent Invocation
        initial_state = {
            "card_name": card_name,
            "bank_name": bank_name,
            "official_url": url,
            "scraped_content": None,
            "extracted_data": None,
            "errors": [],
            "messages": []
        }
        
        result = await card_update_graph.ainvoke(initial_state)
        
        if result.get("errors") or not result.get("extracted_data"):
             error_msg = "; ".join(result.get("errors", [])) or "Agent returned no data"
             raise HTTPException(status_code=500, detail=f"Agent failed: {error_msg}")
        
        return {
            "status": "success",
            "extracted_data": result["extracted_data"],
            "content_length": len(result.get("scraped_content", "") or "")
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting from URL {url}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
