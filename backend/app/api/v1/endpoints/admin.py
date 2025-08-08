from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.admin import is_admin, can_manage_users, get_admin_emails
from app.models.user import User
from app.models.user_role import UserRole, ModeratorRequest
from app.models.edit_suggestion import EditSuggestion
from app.models.card_document import CardDocument
from app.models.audit_log import AuditLog
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.schemas.user_role import (
    UserRoleCreate, UserRoleUpdate, UserRoleResponse,
    ModeratorRequestCreate, ModeratorRequestUpdate, ModeratorRequestResponse,
    UserWithRoles, AdminUserInfo
)
from app.schemas.edit_suggestion import EditSuggestionResponse, EditSuggestionStats, EditSuggestionUpdate
from app.schemas.card_document import CardDocumentResponse, CardDocumentStats, CardDocumentUpdate
from datetime import datetime, timedelta
import json

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require admin access"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/admin-info")
def get_admin_info(current_user: User = Depends(require_admin)):
    """Get admin information"""
    return {
        "is_admin": True,
        "admin_emails": get_admin_emails(),
        "user_email": current_user.email
    }


@router.get("/users", response_model=List[AdminUserInfo])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    role_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users with role information"""
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search))
        )
    
    users = query.offset(skip).limit(limit).all()
    
    result = []
    for user in users:
        # Get current role
        current_role = None
        active_role = db.query(UserRole).filter(
            UserRole.user_id == user.id,
            UserRole.status == "active"
        ).first()
        if active_role:
            current_role = active_role.role_type
        
        # Check for moderator request
        has_moderator_request = db.query(ModeratorRequest).filter(
            ModeratorRequest.user_id == user.id
        ).first() is not None
        
        moderator_request_status = None
        if has_moderator_request:
            request = db.query(ModeratorRequest).filter(
                ModeratorRequest.user_id == user.id
            ).first()
            moderator_request_status = request.status if request else None
        
        result.append(AdminUserInfo(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            current_role=current_role,
            has_moderator_request=has_moderator_request,
            moderator_request_status=moderator_request_status
        ))
    
    return result


@router.get("/moderator-requests", response_model=List[ModeratorRequestResponse])
def get_moderator_requests(
    status_filter: Optional[str] = Query(None, regex="^(pending|approved|rejected)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all moderator requests"""
    query = db.query(ModeratorRequest)
    
    if status_filter:
        query = query.filter(ModeratorRequest.status == status_filter)
    
    requests = query.order_by(desc(ModeratorRequest.created_at)).offset(skip).limit(limit).all()
    return requests


@router.put("/moderator-requests/{request_id}")
def review_moderator_request(
    request_id: int,
    review_data: ModeratorRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Review a moderator request"""
    request = db.query(ModeratorRequest).filter(ModeratorRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Moderator request not found")
    
    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Request has already been reviewed")
    
    # Update request
    request.status = review_data.status
    request.reviewed_by = current_user.id
    request.reviewed_at = datetime.utcnow()
    
    # If approved, create user role
    if review_data.status == "approved":
        # Check if user already has a role
        existing_role = db.query(UserRole).filter(
            UserRole.user_id == request.user_id,
            UserRole.status == "active"
        ).first()
        
        if existing_role:
            existing_role.status = "inactive"
        
        # Create new moderator role
        new_role = UserRole(
            user_id=request.user_id,
            role_type="moderator",
            approved_by=current_user.id,
            approved_at=datetime.utcnow(),
            status="active"
        )
        db.add(new_role)
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action_type="moderator_request_review",
        table_name="moderator_requests",
        record_id=request_id,
        old_values={"status": "pending"},
        new_values={"status": review_data.status},
        change_summary=f"Moderator request {review_data.status} by {current_user.email}"
    )
    db.add(audit_log)
    
    db.commit()
    
    return {"message": f"Moderator request {review_data.status}"}


@router.get("/edit-suggestions", response_model=List[EditSuggestionResponse])
def get_edit_suggestions(
    status_filter: Optional[str] = Query(None, regex="^(pending|approved|rejected)$"),
    field_type: Optional[str] = Query(None, regex="^(spending_category|merchant_reward)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all edit suggestions"""
    query = db.query(EditSuggestion)
    
    if status_filter:
        query = query.filter(EditSuggestion.status == status_filter)
    
    if field_type:
        query = query.filter(EditSuggestion.field_type == field_type)
    
    suggestions = query.order_by(desc(EditSuggestion.created_at)).offset(skip).limit(limit).all()
    
    # Add user and card information
    result = []
    for suggestion in suggestions:
        user = db.query(User).filter(User.id == suggestion.user_id).first()
        card = db.query(CardMasterData).filter(CardMasterData.id == suggestion.card_master_id).first()
        
        suggestion_dict = EditSuggestionResponse.from_orm(suggestion)
        suggestion_dict.user_name = user.full_name if user else "Unknown User"
        suggestion_dict.card_name = card.card_name if card else "Unknown Card"
        suggestion_dict.bank_name = card.bank_name if card else "Unknown Bank"
        
        result.append(suggestion_dict)
    
    return result


@router.put("/edit-suggestions/{suggestion_id}")
def review_edit_suggestion(
    suggestion_id: int,
    review_data: EditSuggestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Review an edit suggestion"""
    suggestion = db.query(EditSuggestion).filter(EditSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Edit suggestion not found")
    
    if suggestion.status != "pending":
        raise HTTPException(status_code=400, detail="Suggestion has already been reviewed")
    
    # Update suggestion
    suggestion.status = review_data.status
    suggestion.reviewed_by = current_user.id
    suggestion.reviewed_at = datetime.utcnow()
    suggestion.review_notes = review_data.review_notes
    
    # If approved, apply the change to the card data
    if review_data.status == "approved":
        # Apply the change to the card data
        card = db.query(CardMasterData).filter(CardMasterData.id == suggestion.card_master_id).first()
        if card:
            if suggestion.field_type == "spending_category":
                # Find or create spending category
                category = db.query(CardSpendingCategory).filter(
                    CardSpendingCategory.card_master_id == suggestion.card_master_id,
                    CardSpendingCategory.category_name == suggestion.field_name
                ).first()
                
                if category:
                    # Update existing category
                    category.reward_rate = float(suggestion.new_value)
                else:
                    # Create new category
                    from app.core.card_templates import get_default_spending_categories
                    default_categories = get_default_spending_categories(card.card_tier, card.bank_name)
                    
                    # Find the matching default category
                    default_category = next(
                        (cat for cat in default_categories if cat["category_name"] == suggestion.field_name),
                        None
                    )
                    
                    if default_category:
                        new_category = CardSpendingCategory(
                            card_master_id=suggestion.card_master_id,
                            category_name=default_category["category_name"],
                            category_display_name=default_category["category_display_name"],
                            reward_rate=float(suggestion.new_value),
                            reward_type=default_category["reward_type"],
                            reward_cap=default_category["reward_cap"],
                            reward_cap_period=default_category["reward_cap_period"],
                            minimum_transaction_amount=default_category["minimum_transaction_amount"],
                            is_active=True,
                            additional_conditions=default_category["additional_conditions"]
                        )
                        db.add(new_category)
                    else:
                        # Fallback: create with basic info
                        new_category = CardSpendingCategory(
                            card_master_id=suggestion.card_master_id,
                            category_name=suggestion.field_name,
                            category_display_name=suggestion.field_name.replace('_', ' ').title(),
                            reward_rate=float(suggestion.new_value),
                            reward_type="points",
                            is_active=True
                        )
                        db.add(new_category)
                        
            elif suggestion.field_type == "merchant_reward":
                # Find or create merchant reward
                merchant = db.query(CardMerchantReward).filter(
                    CardMerchantReward.card_master_id == suggestion.card_master_id,
                    CardMerchantReward.merchant_name == suggestion.field_name
                ).first()
                
                if merchant:
                    # Update existing merchant
                    merchant.reward_rate = float(suggestion.new_value)
                else:
                    # Create new merchant
                    from app.core.card_templates import get_default_merchant_rewards
                    default_merchants = get_default_merchant_rewards(card.card_tier, card.bank_name)
                    
                    # Find the matching default merchant
                    default_merchant = next(
                        (merch for merch in default_merchants if merch["merchant_name"] == suggestion.field_name),
                        None
                    )
                    
                    if default_merchant:
                        new_merchant = CardMerchantReward(
                            card_master_id=suggestion.card_master_id,
                            merchant_name=default_merchant["merchant_name"],
                            merchant_display_name=default_merchant["merchant_display_name"],
                            reward_rate=float(suggestion.new_value),
                            reward_type=default_merchant["reward_type"],
                            reward_cap=default_merchant["reward_cap"],
                            reward_cap_period=default_merchant["reward_cap_period"],
                            minimum_transaction_amount=default_merchant["minimum_transaction_amount"],
                            is_active=True,
                            additional_conditions=default_merchant["additional_conditions"]
                        )
                        db.add(new_merchant)
                    else:
                        # Fallback: create with basic info
                        new_merchant = CardMerchantReward(
                            card_master_id=suggestion.card_master_id,
                            merchant_name=suggestion.field_name,
                            merchant_display_name=suggestion.field_name.replace('_', ' ').title(),
                            reward_rate=float(suggestion.new_value),
                            reward_type="points",
                            is_active=True
                        )
                        db.add(new_merchant)
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action_type="edit_suggestion_review",
        table_name="edit_suggestions",
        record_id=suggestion_id,
        old_values={"status": "pending"},
        new_values={"status": review_data.status},
        change_summary=f"Edit suggestion {review_data.status} by {current_user.email}"
    )
    db.add(audit_log)
    
    db.commit()
    
    return {"message": f"Edit suggestion {review_data.status}"}


@router.get("/card-documents", response_model=List[CardDocumentResponse])
def get_card_documents(
    status_filter: Optional[str] = Query(None, regex="^(pending|approved|rejected)$"),
    document_type: Optional[str] = Query(None, regex="^(link|file|policy_update|terms_change)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all card document submissions"""
    query = db.query(CardDocument)
    
    if status_filter:
        query = query.filter(CardDocument.status == status_filter)
    
    if document_type:
        query = query.filter(CardDocument.document_type == document_type)
    
    documents = query.order_by(desc(CardDocument.created_at)).offset(skip).limit(limit).all()
    
    # Add user and card information
    result = []
    for document in documents:
        user = db.query(User).filter(User.id == document.user_id).first()
        card = db.query(CardMasterData).filter(CardMasterData.id == document.card_master_id).first()
        
        document_dict = CardDocumentResponse.from_orm(document)
        document_dict.user_name = user.full_name if user else "Unknown User"
        document_dict.card_name = card.card_name if card else "Unknown Card"
        document_dict.bank_name = card.bank_name if card else "Unknown Bank"
        
        result.append(document_dict)
    
    return result


@router.put("/card-documents/{document_id}")
def review_card_document(
    document_id: int,
    review_data: CardDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Review a card document submission"""
    document = db.query(CardDocument).filter(CardDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Card document not found")
    
    if document.status != "pending":
        raise HTTPException(status_code=400, detail="Document has already been reviewed")
    
    # Update document
    document.status = review_data.status
    document.reviewed_by = current_user.id
    document.reviewed_at = datetime.utcnow()
    document.review_notes = review_data.review_notes
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action_type="card_document_review",
        table_name="card_documents",
        record_id=document_id,
        old_values={"status": "pending"},
        new_values={"status": review_data.status},
        change_summary=f"Card document {review_data.status} by {current_user.email}"
    )
    db.add(audit_log)
    
    db.commit()
    
    return {"message": f"Card document {review_data.status}"}


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Get admin dashboard statistics"""
    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Role stats
    moderators = db.query(func.count(UserRole.id)).filter(
        UserRole.role_type == "moderator",
        UserRole.status == "active"
    ).scalar()
    
    # Moderator request stats
    pending_requests = db.query(func.count(ModeratorRequest.id)).filter(
        ModeratorRequest.status == "pending"
    ).scalar()
    
    # Edit suggestion stats
    pending_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.status == "pending"
    ).scalar()
    
    approved_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.status == "approved"
    ).scalar()
    
    rejected_suggestions = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.status == "rejected"
    ).scalar()
    
    # Card document stats
    pending_documents = db.query(func.count(CardDocument.id)).filter(
        CardDocument.status == "pending"
    ).scalar()
    
    approved_documents = db.query(func.count(CardDocument.id)).filter(
        CardDocument.status == "approved"
    ).scalar()
    
    rejected_documents = db.query(func.count(CardDocument.id)).filter(
        CardDocument.status == "rejected"
    ).scalar()
    
    # Recent activity
    recent_audit_logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(10).all()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "moderators": moderators
        },
        "moderator_requests": {
            "pending": pending_requests
        },
        "edit_suggestions": {
            "pending": pending_suggestions,
            "approved": approved_suggestions,
            "rejected": rejected_suggestions
        },
        "card_documents": {
            "pending": pending_documents,
            "approved": approved_documents,
            "rejected": rejected_documents
        },
        "recent_activity": [
            {
                "action": log.action_type,
                "user": log.user.email if log.user else "System",
                "timestamp": log.created_at.isoformat(),
                "summary": log.change_summary
            }
            for log in recent_audit_logs
        ]
    } 