from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from app.core.database import get_db
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.credit_card import CreditCard
from app.schemas.card_master_data import (
    CardMasterDataCreate,
    CardMasterDataUpdate,
    CardMasterDataResponse,
    CardSpendingCategoryCreate,
    CardSpendingCategoryUpdate,
    CardSpendingCategoryResponse,
    CardMerchantRewardCreate,
    CardMerchantRewardUpdate,
    CardMerchantRewardResponse,
    CardComparisonData
)
from app.models.user import User
from app.core.security import get_current_user_sync

router = APIRouter()


# Card Master Data endpoints
@router.get("/cards")
def get_card_master_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    bank_name: Optional[str] = Query(None),
    card_tier: Optional[str] = Query(None),
    is_active: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all card master data with optional filters"""
    query = db.query(CardMasterData)
    
    if bank_name:
        query = query.filter(CardMasterData.bank_name.ilike(f"%{bank_name}%"))
    if card_tier:
        query = query.filter(CardMasterData.card_tier == card_tier)
    if is_active is not None:
        query = query.filter(CardMasterData.is_active == is_active)
    
    cards = query.offset(skip).limit(limit).all()
    
    # Return basic card information
    result = []
    for card in cards:
        result.append({
            "id": card.id,
            "bank_name": card.bank_name,
            "card_name": card.card_name,
            "display_name": card.display_name,
            "card_network": card.card_network,
            "joining_fee_display": card.joining_fee_display,
            "annual_fee_display": card.annual_fee_display,
            "is_active": card.is_active
        })
    
    return result


@router.get("/cards/{card_id}", response_model=CardMasterDataResponse)
def get_card_master_data_by_id(card_id: int, db: Session = Depends(get_db)):
    """Get specific card master data by ID"""
    card = db.query(CardMasterData).options(
        joinedload(CardMasterData.spending_categories),
        joinedload(CardMasterData.merchant_rewards)
    ).filter(CardMasterData.id == card_id).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    return card


@router.post("/cards", response_model=CardMasterDataResponse)
def create_card_master_data(
    card_data: CardMasterDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Create new card master data (Admin only)"""
    # TODO: Add admin permission check
    
    # Check if card already exists
    existing_card = db.query(CardMasterData).filter(
        and_(
            CardMasterData.bank_name == card_data.bank_name,
            CardMasterData.card_name == card_data.card_name,
            CardMasterData.card_variant == card_data.card_variant
        )
    ).first()
    
    if existing_card:
        raise HTTPException(
            status_code=400, 
            detail="Card with this bank, name, and variant already exists"
        )
    
    db_card = CardMasterData(**card_data.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    
    return db_card


@router.put("/cards/{card_id}", response_model=CardMasterDataResponse)
def update_card_master_data(
    card_id: int,
    card_data: CardMasterDataUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Update card master data (Admin only)"""
    # TODO: Add admin permission check
    
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    update_data = card_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)
    
    db.commit()
    db.refresh(card)
    
    return card


@router.delete("/cards/{card_id}")
def delete_card_master_data(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Delete card master data (Admin only)"""
    # TODO: Add admin permission check
    
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(card)
    db.commit()
    
    return {"message": "Card deleted successfully"}


# Spending Categories endpoints
@router.post("/cards/{card_id}/categories", response_model=CardSpendingCategoryResponse)
def create_spending_category(
    card_id: int,
    category_data: CardSpendingCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Add spending category to a card"""
    # Verify card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    category_data.card_master_id = card_id
    db_category = CardSpendingCategory(**category_data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/categories/{category_id}", response_model=CardSpendingCategoryResponse)
def update_spending_category(
    category_id: int,
    category_data: CardSpendingCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Update spending category"""
    category = db.query(CardSpendingCategory).filter(CardSpendingCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/categories/{category_id}")
def delete_spending_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Delete spending category"""
    category = db.query(CardSpendingCategory).filter(CardSpendingCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}


# Merchant Rewards endpoints
@router.post("/cards/{card_id}/merchants", response_model=CardMerchantRewardResponse)
def create_merchant_reward(
    card_id: int,
    merchant_data: CardMerchantRewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Add merchant reward to a card"""
    # Verify card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    merchant_data.card_master_id = card_id
    db_merchant = CardMerchantReward(**merchant_data.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    
    return db_merchant


@router.put("/merchants/{merchant_id}", response_model=CardMerchantRewardResponse)
def update_merchant_reward(
    merchant_id: int,
    merchant_data: CardMerchantRewardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Update merchant reward"""
    merchant = db.query(CardMerchantReward).filter(CardMerchantReward.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant reward not found")
    
    update_data = merchant_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(merchant, field, value)
    
    db.commit()
    db.refresh(merchant)
    
    return merchant


@router.delete("/merchants/{merchant_id}")
def delete_merchant_reward(
    merchant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Delete merchant reward"""
    merchant = db.query(CardMerchantReward).filter(CardMerchantReward.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant reward not found")
    
    db.delete(merchant)
    db.commit()
    
    return {"message": "Merchant reward deleted successfully"}


# Comparison endpoint
def get_current_user_optional():
    """Optional authentication dependency"""
    try:
        from app.core.security import get_current_user_sync
        return get_current_user_sync()
    except:
        return None

@router.get("/comparison", response_model=List[CardComparisonData])
def get_card_comparison_data(
    user_cards_only: bool = Query(False, description="Show only user's cards"),
    card_ids: Optional[List[int]] = Query(None, description="Specific card IDs to compare"),
    db: Session = Depends(get_db)
):
    """Get card comparison data for the comparison page"""
    
    # Try to get current user optionally
    current_user = None
    try:
        current_user = get_current_user_optional()
    except:
        pass
    
    # If user_cards_only is requested but no user is authenticated, return empty
    if user_cards_only and not current_user:
        return []
    
    if user_cards_only and current_user:
        # Get cards that the user owns
        user_card_master_ids = db.query(CreditCard.card_master_data_id).filter(
            and_(
                CreditCard.user_id == current_user.id,
                CreditCard.card_master_data_id.isnot(None)
            )
        ).subquery()
        
        query = db.query(CardMasterData).filter(
            CardMasterData.id.in_(user_card_master_ids)
        )
    elif card_ids:
        # Get specific cards by IDs
        query = db.query(CardMasterData).filter(CardMasterData.id.in_(card_ids))
    else:
        # Get all active cards
        query = db.query(CardMasterData).filter(CardMasterData.is_active == True)
    
    cards = query.options(
        joinedload(CardMasterData.spending_categories),
        joinedload(CardMasterData.merchant_rewards)
    ).all()
    
    # Format data for comparison page
    comparison_data = []
    for card in cards:
        # Build categories dict
        categories = {}
        for category in card.spending_categories:
            if category.is_active:
                categories[category.category_name] = category.reward_display
        
        # Build merchants dict
        merchants = {}
        for merchant in card.merchant_rewards:
            if merchant.is_active:
                merchants[merchant.merchant_name] = merchant.reward_display
        
        # Build additional info
        additional_info_parts = []
        if card.annual_fee_waiver_spend:
            additional_info_parts.append(f"Annual fee waived on ₹{card.annual_fee_waiver_spend:,.0f} spend")
        if card.reward_program_name:
            additional_info_parts.append(f"Reward Program: {card.reward_program_name}")
        if card.minimum_salary:
            additional_info_parts.append(f"Min. salary: ₹{card.minimum_salary:,.0f}")
        
        comparison_item = CardComparisonData(
            id=card.id,
            bank_name=card.bank_name,
            card_name=card.card_name,
            display_name=card.display_name,
            joining_fee_display=card.joining_fee_display,
            annual_fee_display=card.annual_fee_display,
            annual_fee_waiver_spend=card.annual_fee_waiver_spend,
            domestic_lounge_visits=card.domestic_lounge_visits,
            lounge_spend_requirement=card.lounge_spend_requirement,
            lounge_spend_period=card.lounge_spend_period,
            categories=categories,
            merchants=merchants,
            additional_info=" | ".join(additional_info_parts)
        )
        comparison_data.append(comparison_item)
    
    return comparison_data


@router.get("/banks", response_model=List[str])
def get_available_banks(db: Session = Depends(get_db)):
    """Get list of available banks"""
    banks = db.query(CardMasterData.bank_name).distinct().all()
    return [bank[0] for bank in banks]


@router.get("/categories", response_model=List[str])
def get_available_categories(db: Session = Depends(get_db)):
    """Get list of available spending categories"""
    categories = db.query(CardSpendingCategory.category_name).distinct().all()
    return [category[0] for category in categories]


@router.get("/merchants", response_model=List[str])
def get_available_merchants(db: Session = Depends(get_db)):
    """Get list of available merchants"""
    merchants = db.query(CardMerchantReward.merchant_name).distinct().all()
    return [merchant[0] for merchant in merchants] 
