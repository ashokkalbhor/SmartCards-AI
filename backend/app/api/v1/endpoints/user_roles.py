from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.admin import is_admin, is_moderator
from app.models.user import User
from app.models.user_role import UserRole, ModeratorRequest
from app.models.edit_suggestion import EditSuggestion
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.schemas.user_role import (
    ModeratorRequestCreate, ModeratorRequestResponse
)
from app.schemas.edit_suggestion import (
    CardEditSuggestionRequest, EditSuggestionResponse
)
from datetime import datetime
import json

router = APIRouter()


@router.post("/request-moderator")
def request_moderator_status(
    request_data: ModeratorRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Request moderator status"""
    # Check if user already has a moderator request
    existing_request = db.query(ModeratorRequest).filter(
        ModeratorRequest.user_id == current_user.id
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="You already have a moderator request pending"
        )
    
    # Check if user is already a moderator
    existing_role = db.query(UserRole).filter(
        UserRole.user_id == current_user.id,
        UserRole.role_type == "moderator",
        UserRole.status == "active"
    ).first()
    
    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="You are already a moderator"
        )
    
    # Calculate user activity summary
    activity_summary = {
        "days_active": (datetime.utcnow() - current_user.created_at).days,
        "total_posts": len(current_user.community_posts),
        "total_comments": len(current_user.community_comments),
        "total_reviews": len(current_user.card_reviews),
        "total_cards": len(current_user.credit_cards)
    }
    
    # Create moderator request
    moderator_request = ModeratorRequest(
        user_id=current_user.id,
        request_reason=request_data.request_reason,
        user_activity_summary=json.dumps(activity_summary),
        status="pending"
    )
    
    db.add(moderator_request)
    db.commit()
    db.refresh(moderator_request)
    
    return {"message": "Moderator request submitted successfully"}


@router.get("/my-moderator-request")
def get_my_moderator_request(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's moderator request"""
    request = db.query(ModeratorRequest).filter(
        ModeratorRequest.user_id == current_user.id
    ).first()
    
    if not request:
        return {"has_request": False}
    
    return {
        "has_request": True,
        "request": ModeratorRequestResponse.from_orm(request)
    }


@router.get("/my-role")
def get_my_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's role"""
    active_role = db.query(UserRole).filter(
        UserRole.user_id == current_user.id,
        UserRole.status == "active"
    ).first()
    
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": active_role.role_type if active_role else "user",
        "is_admin": is_admin(current_user),
        "is_moderator": is_moderator(current_user)
    }


@router.post("/edit-suggestions")
def submit_edit_suggestion(
    card_id: int,
    suggestion_data: CardEditSuggestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit an edit suggestion for card data"""
    # Verify card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Validate field type
    if suggestion_data.field_type not in ["spending_category", "merchant_reward"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid field type. Must be 'spending_category' or 'merchant_reward'"
        )
    
    # Get current value for comparison
    old_value = None
    if suggestion_data.field_type == "spending_category":
        category = db.query(CardSpendingCategory).filter(
            CardSpendingCategory.card_master_id == card_id,
            CardSpendingCategory.category_name == suggestion_data.field_name
        ).first()
        if category:
            old_value = str(category.reward_rate)
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Spending category '{suggestion_data.field_name}' not found for this card"
            )
    elif suggestion_data.field_type == "merchant_reward":
        merchant = db.query(CardMerchantReward).filter(
            CardMerchantReward.card_master_id == card_id,
            CardMerchantReward.merchant_name == suggestion_data.field_name
        ).first()
        if merchant:
            old_value = str(merchant.reward_rate)
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Merchant reward '{suggestion_data.field_name}' not found for this card"
            )
    
    # Check if suggestion already exists
    existing_suggestion = db.query(EditSuggestion).filter(
        EditSuggestion.user_id == current_user.id,
        EditSuggestion.card_master_id == card_id,
        EditSuggestion.field_type == suggestion_data.field_type,
        EditSuggestion.field_name == suggestion_data.field_name,
        EditSuggestion.status == "pending"
    ).first()
    
    if existing_suggestion:
        raise HTTPException(
            status_code=400,
            detail="You already have a pending suggestion for this field"
        )
    
    # Create edit suggestion
    edit_suggestion = EditSuggestion(
        user_id=current_user.id,
        card_master_id=card_id,
        field_type=suggestion_data.field_type,
        field_name=suggestion_data.field_name,
        old_value=old_value,
        new_value=suggestion_data.new_value,
        suggestion_reason=suggestion_data.suggestion_reason,
        status="pending"
    )
    
    db.add(edit_suggestion)
    db.commit()
    db.refresh(edit_suggestion)
    
    return {"message": "Edit suggestion submitted successfully"}


@router.get("/my-suggestions", response_model=List[EditSuggestionResponse])
def get_my_suggestions(
    status_filter: Optional[str] = Query(None, regex="^(pending|approved|rejected)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's edit suggestions"""
    query = db.query(EditSuggestion).filter(EditSuggestion.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(EditSuggestion.status == status_filter)
    
    suggestions = query.order_by(desc(EditSuggestion.created_at)).offset(skip).limit(limit).all()
    
    # Add card information
    result = []
    for suggestion in suggestions:
        card = db.query(CardMasterData).filter(CardMasterData.id == suggestion.card_master_id).first()
        
        suggestion_dict = EditSuggestionResponse.from_orm(suggestion)
        suggestion_dict.user_name = current_user.full_name
        suggestion_dict.card_name = card.card_name if card else "Unknown Card"
        suggestion_dict.bank_name = card.bank_name if card else "Unknown Bank"
        
        result.append(suggestion_dict)
    
    return result


@router.get("/my-suggestions/stats")
def get_my_suggestions_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's suggestion statistics"""
    total_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.user_id == current_user.id
    ).scalar()
    
    pending_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.user_id == current_user.id,
        EditSuggestion.status == "pending"
    ).scalar()
    
    approved_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.user_id == current_user.id,
        EditSuggestion.status == "approved"
    ).scalar()
    
    rejected_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.user_id == current_user.id,
        EditSuggestion.status == "rejected"
    ).scalar()
    
    return {
        "total": total_suggestions,
        "pending": pending_suggestions,
        "approved": approved_suggestions,
        "rejected": rejected_suggestions
    } 