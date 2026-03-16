from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.admin import is_moderator, can_approve_suggestions
from app.models.user import User
from app.models.edit_suggestion import EditSuggestion
from app.models.audit_log import AuditLog
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.schemas.edit_suggestion import (
    EditSuggestionResponse, EditSuggestionUpdate, EditSuggestionStats
)
from app.core.allowed_names import validate_category_name, validate_merchant_name
from datetime import datetime

router = APIRouter()


def require_moderator(current_user: User = Depends(get_current_user)):
    """Dependency to require moderator access"""
    if not is_moderator(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator access required"
        )
    return current_user


@router.get("/moderator-info")
def get_moderator_info(current_user: User = Depends(require_moderator)):
    """Get moderator information"""
    return {
        "is_moderator": True,
        "can_approve_suggestions": can_approve_suggestions(current_user),
        "user_email": current_user.email
    }


@router.get("/edit-suggestions", response_model=List[EditSuggestionResponse])
def get_pending_suggestions(
    status_filter: Optional[str] = Query("pending", regex="^(pending|approved|rejected|needs_review)$"),
    field_type: Optional[str] = Query(None, regex="^(spending_category|spending_category_cap|merchant_reward|merchant_reward_cap|basic_info)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """Get edit suggestions for review"""
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
def review_suggestion(
    suggestion_id: int,
    review_data: EditSuggestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator)
):
    """Review an edit suggestion"""
    if not can_approve_suggestions(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to approve suggestions"
        )
    
    suggestion = db.query(EditSuggestion).filter(EditSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Edit suggestion not found")
    
    if suggestion.status not in ("pending", "needs_review"):
        raise HTTPException(status_code=400, detail="Suggestion has already been reviewed")
    
    # Update suggestion
    suggestion.status = review_data.status
    suggestion.reviewed_by = current_user.id
    suggestion.reviewed_at = datetime.utcnow()
    suggestion.review_notes = review_data.review_notes
    
    # If approved, apply the change to the card data
    if review_data.status == "approved":
        # Resolve override rate: use verifier's value when moderator chose "Keep Verified"
        override_rate = None
        if review_data.use_verified_value:
            verifier_data = (suggestion.additional_data or {}).get("verifier", {})
            raw_verified = verifier_data.get("verified_value")
            if raw_verified is None:
                raise HTTPException(status_code=400, detail="No verified value found for this suggestion")
            # Verifier may return "2.0%", "5%", or a plain number — strip % before parsing
            cleaned_verified = str(raw_verified).strip().rstrip('%').strip()
            try:
                override_rate = float(cleaned_verified)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"AI Verifier's value '{raw_verified}' is descriptive, not a number. Use 'Keep Extracted' or 'Override' instead."
                )

        def _safe_float_rate(val: Any, field_label: str) -> float:
            """Convert val to float; raise 400 if None/null/invalid/negative."""
            if val is None or str(val).strip().lower() in ("none", "null", ""):
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot approve '{field_label}': no valid rate value found. Reject this suggestion instead."
                )
            try:
                result = float(val)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot approve '{field_label}': value '{val}' is not a valid number."
                )
            if result < 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot approve '{field_label}': reward rate cannot be negative ({result}%). Reject this suggestion instead."
                )
            return result

        # Apply the change to the card data
        card = db.query(CardMasterData).filter(CardMasterData.id == suggestion.card_master_id).first()
        if card:
            if suggestion.field_type == "spending_category":
                # Find or create spending category
                category = db.query(CardSpendingCategory).filter(
                    CardSpendingCategory.card_master_id == suggestion.card_master_id,
                    CardSpendingCategory.category_name == suggestion.field_name
                ).first()

                # Parse JSON new_value to extract rate; fall back to points computation
                parsed_cat = None
                if suggestion.new_value:
                    try:
                        p = json.loads(suggestion.new_value)
                        if isinstance(p, dict):
                            parsed_cat = p
                    except (json.JSONDecodeError, TypeError):
                        pass

                if override_rate is not None:
                    cat_rate = override_rate
                elif parsed_cat:
                    cat_rate = parsed_cat.get("reward_rate")
                    if cat_rate is None:
                        pts = parsed_cat.get("points_per_100")
                        val = parsed_cat.get("rupee_value_per_point")
                        if pts and val:
                            try:
                                cat_rate = round(float(pts) * float(val), 2) or None
                            except (ValueError, TypeError):
                                pass
                    cat_rate = _safe_float_rate(cat_rate, suggestion.field_name)
                else:
                    cat_rate = _safe_float_rate(suggestion.new_value, suggestion.field_name)

                if category:
                    # Update existing category
                    category.reward_rate = cat_rate
                else:
                    # Validate against whitelist before creating
                    try:
                        validated_name = validate_category_name(suggestion.field_name)
                    except ValueError as e:
                        raise HTTPException(status_code=400, detail=str(e))

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
                            category_name=validated_name,
                            category_display_name=default_category["category_display_name"],
                            reward_rate=cat_rate,
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
                            category_name=validated_name,
                            category_display_name=validated_name.replace('_', ' ').title(),
                            reward_rate=cat_rate,
                            reward_type="points",
                            is_active=True
                        )
                        db.add(new_category)
            elif suggestion.field_type == "spending_category_cap":
                # Update spending category cap only
                category = db.query(CardSpendingCategory).filter(
                    CardSpendingCategory.card_master_id == suggestion.card_master_id,
                    CardSpendingCategory.category_name == suggestion.field_name
                ).first()
                
                if category:
                    # Only update the cap, leave reward_rate unchanged
                    cap_val = _safe_float_rate(suggestion.new_value, f"{suggestion.field_name} cap")
                    category.reward_cap = cap_val if cap_val > 0 else None
                    category.reward_cap_period = "monthly"  # Default period
                else:
                    # If category doesn't exist, don't create it just for cap editing
                    # This should be handled by editing the reward rate first
                    raise HTTPException(
                        status_code=400,
                        detail=f"Cannot edit cap for non-existent category '{suggestion.field_name}'. Please add the category first."
                    )
                        
            elif suggestion.field_type == "merchant_reward":
                # Find or create merchant reward
                merchant = db.query(CardMerchantReward).filter(
                    CardMerchantReward.card_master_id == suggestion.card_master_id,
                    CardMerchantReward.merchant_name == suggestion.field_name
                ).first()

                # Parse JSON new_value to extract rate; fall back to points computation
                parsed_merch = None
                if suggestion.new_value:
                    try:
                        pm = json.loads(suggestion.new_value)
                        if isinstance(pm, dict):
                            parsed_merch = pm
                    except (json.JSONDecodeError, TypeError):
                        pass

                if override_rate is not None:
                    merch_rate = override_rate
                elif parsed_merch:
                    merch_rate = parsed_merch.get("reward_rate")
                    if merch_rate is None:
                        pts_m = parsed_merch.get("points_per_100")
                        val_m = parsed_merch.get("rupee_value_per_point")
                        if pts_m and val_m:
                            try:
                                merch_rate = round(float(pts_m) * float(val_m), 2) or None
                            except (ValueError, TypeError):
                                pass
                    merch_rate = _safe_float_rate(merch_rate, suggestion.field_name)
                else:
                    merch_rate = _safe_float_rate(suggestion.new_value, suggestion.field_name)

                if merchant:
                    # Update existing merchant
                    merchant.reward_rate = merch_rate
                else:
                    # Validate against whitelist before creating
                    try:
                        validated_name = validate_merchant_name(suggestion.field_name)
                    except ValueError as e:
                        raise HTTPException(status_code=400, detail=str(e))

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
                            merchant_name=validated_name,
                            merchant_display_name=default_merchant["merchant_display_name"],
                            reward_rate=merch_rate,
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
                            merchant_name=validated_name,
                            merchant_display_name=validated_name.replace('_', ' ').title(),
                            reward_rate=merch_rate,
                            reward_type="points",
                            is_active=True
                        )
                        db.add(new_merchant)
            elif suggestion.field_type == "merchant_reward_cap":
                # Update merchant reward cap only
                merchant = db.query(CardMerchantReward).filter(
                    CardMerchantReward.card_master_id == suggestion.card_master_id,
                    CardMerchantReward.merchant_name == suggestion.field_name
                ).first()
                
                if merchant:
                    # Only update the cap, leave reward_rate unchanged
                    cap_val_m = _safe_float_rate(suggestion.new_value, f"{suggestion.field_name} cap")
                    merchant.reward_cap = cap_val_m if cap_val_m > 0 else None
                    merchant.reward_cap_period = "monthly"  # Default period
                else:
                    # If merchant doesn't exist, don't create it just for cap editing
                    # This should be handled by editing the reward rate first
                    raise HTTPException(
                        status_code=400,
                        detail=f"Cannot edit cap for non-existent merchant '{suggestion.field_name}'. Please add the merchant first."
                    )
            elif suggestion.field_type == "basic_info":
                # Handle basic information fields
                if suggestion.field_name == "joining_fee":
                    # Parse the new value - handle different formats
                    new_value = suggestion.new_value.strip()
                    if new_value.lower() == "ltf" or new_value.lower() == "lifetime free":
                        card.is_lifetime_free = True
                        card.joining_fee = 0
                    else:
                        # Extract numeric value from string like "₹500" or "500"
                        import re
                        numeric_match = re.search(r'[\d,]+', new_value.replace(',', ''))
                        if numeric_match:
                            card.joining_fee = float(numeric_match.group().replace(',', ''))
                            card.is_lifetime_free = False
                        else:
                            raise HTTPException(
                                status_code=400,
                                detail="Invalid joining fee format. Please use format like '₹500' or 'LTF'"
                            )
                elif suggestion.field_name == "annual_fee":
                    # Parse the new value - handle different formats
                    new_value = suggestion.new_value.strip()
                    if new_value.lower() == "ltf" or new_value.lower() == "lifetime free":
                        card.is_lifetime_free = True
                        card.annual_fee = 0
                    else:
                        # Extract numeric value from string like "₹500 (Waived on ₹50,000 spend)" or "₹500"
                        import re
                        numeric_match = re.search(r'[\d,]+', new_value.replace(',', ''))
                        if numeric_match:
                            card.annual_fee = float(numeric_match.group().replace(',', ''))
                            card.is_lifetime_free = False
                        else:
                            raise HTTPException(
                                status_code=400,
                                detail="Invalid annual fee format. Please use format like '₹500' or 'LTF'"
                            )
                elif suggestion.field_name == "annual_fee_waiver_spend":
                    new_value = suggestion.new_value.strip()
                    import re
                    numeric_match = re.search(r'[\d,]+', new_value.replace(',', ''))
                    if numeric_match:
                        card.annual_fee_waiver_spend = float(numeric_match.group().replace(',', ''))
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid fee waiver spend format. Please use format like '₹2,00,000' or '200000'"
                        )

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


@router.get("/stats")
def get_moderator_stats(db: Session = Depends(get_db), current_user: User = Depends(require_moderator)):
    """Get moderator dashboard statistics"""
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
    
    # Suggestions by type
    spending_category_pending = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.status == "pending",
        EditSuggestion.field_type == "spending_category"
    ).scalar()
    
    merchant_reward_pending = db.query(func.count(EditSuggestion.id)).filter(
        EditSuggestion.status == "pending",
        EditSuggestion.field_type == "merchant_reward"
    ).scalar()
    
    # Recent reviews by this moderator
    recent_reviews = db.query(EditSuggestion).filter(
        EditSuggestion.reviewed_by == current_user.id
    ).order_by(desc(EditSuggestion.reviewed_at)).limit(10).all()
    
    return {
        "edit_suggestions": {
            "pending": pending_suggestions,
            "approved": approved_suggestions,
            "rejected": rejected_suggestions,
            "by_type": {
                "spending_category": spending_category_pending,
                "merchant_reward": merchant_reward_pending
            }
        },
        "recent_reviews": [
            {
                "id": review.id,
                "field_type": review.field_type,
                "field_name": review.field_name,
                "status": review.status,
                "reviewed_at": review.reviewed_at.isoformat() if review.reviewed_at else None
            }
            for review in recent_reviews
        ]
    } 