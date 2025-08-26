from typing import List, Optional
from app.core.card_templates import create_default_spending_categories_for_card, create_default_merchant_rewards_for_card
from app.core.config import settings
from app.core.merchant_popularity import merchant_popularity_service
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from fastapi.security import HTTPAuthorizationCredentials

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
from app.core.security import get_current_user_sync, security, verify_token

def get_current_user_optional() -> Optional[User]:
    """Optional authentication dependency that returns None if not authenticated"""
    return None  # We'll handle authentication manually in the endpoint

router = APIRouter()


# Card Master Data endpoints
@router.get("/cards")
def get_card_master_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),  # Increased limit to 1000
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
    """Get specific card master data by ID with editable defaults"""
    try:
        # First try to get the card without joinedload to see if the card exists
        card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
        
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        # Now try to get with joinedload
        card_with_relations = db.query(CardMasterData).options(
        joinedload(CardMasterData.spending_categories),
        joinedload(CardMasterData.merchant_rewards)
    ).filter(CardMasterData.id == card_id).first()
    
        # Always show all spending categories and merchant rewards with default values
        # Get existing data and merge with default templates
        existing_categories = {cat.category_name: cat for cat in card_with_relations.spending_categories}
        existing_merchants = {merchant.merchant_name: merchant for merchant in card_with_relations.merchant_rewards}
        
        # Get default templates
        default_categories = create_default_spending_categories_for_card(
            card_id, 
            card_with_relations.card_tier or "basic", 
            card_with_relations.bank_name
        )
        
        default_merchants = create_default_merchant_rewards_for_card(
            card_id, 
            card_with_relations.card_tier or "basic", 
            card_with_relations.bank_name
        )
        
        # Merge existing data with defaults, showing "N/A" for missing data
        merged_categories = []
        for default_cat in default_categories:
            if default_cat["category_name"] in existing_categories:
                # Use existing data
                existing_cat = existing_categories[default_cat["category_name"]]
                merged_categories.append({
                    "id": existing_cat.id,
                    "card_master_id": existing_cat.card_master_id,
                    "category_name": existing_cat.category_name,
                    "category_display_name": existing_cat.category_display_name,
                    "reward_rate": existing_cat.reward_rate,
                    "reward_type": existing_cat.reward_type,
                    "reward_cap": existing_cat.reward_cap,
                    "reward_cap_period": existing_cat.reward_cap_period,
                    "minimum_transaction_amount": existing_cat.minimum_transaction_amount,
                    "is_active": existing_cat.is_active,
                    "valid_from": existing_cat.valid_from,
                    "valid_until": existing_cat.valid_until,
                    "additional_conditions": existing_cat.additional_conditions,
                    "created_at": existing_cat.created_at,
                    "updated_at": existing_cat.updated_at,
                    "reward_display": f"{existing_cat.reward_rate}%"
                })
            else:
                # Use default with "Not Available" indicator
                merged_categories.append({
                    "id": None,
                    "card_master_id": card_id,
                    "category_name": default_cat["category_name"],
                    "category_display_name": default_cat["category_display_name"],
                    "reward_rate": 0.0,  # Not Available
                    "reward_type": "points",
                    "reward_cap": None,
                    "reward_cap_period": None,
                    "minimum_transaction_amount": None,
                    "is_active": False,  # Mark as inactive for Not Available
                    "valid_from": None,
                    "valid_until": None,
                    "additional_conditions": "Not Available - No data available",
                    "created_at": None,
                    "updated_at": None,
                    "reward_display": "Not Available"
                })
        
        merged_merchants = []
        for default_merchant in default_merchants:
            if default_merchant["merchant_name"] in existing_merchants:
                # Use existing data
                existing_merchant = existing_merchants[default_merchant["merchant_name"]]
                merged_merchants.append({
                    "id": existing_merchant.id,
                    "card_master_id": existing_merchant.card_master_id,
                    "merchant_name": existing_merchant.merchant_name,
                    "merchant_display_name": existing_merchant.merchant_display_name,
                    "merchant_category": existing_merchant.merchant_category,
                    "reward_rate": existing_merchant.reward_rate,
                    "reward_type": existing_merchant.reward_type or "cashback",
                    "reward_cap": existing_merchant.reward_cap,
                    "reward_cap_period": existing_merchant.reward_cap_period,
                    "minimum_transaction_amount": existing_merchant.minimum_transaction_amount,
                    "is_active": existing_merchant.is_active,
                    "valid_from": existing_merchant.valid_from,
                    "valid_until": existing_merchant.valid_until,
                    "requires_registration": existing_merchant.requires_registration if existing_merchant.requires_registration is not None else False,
                    "additional_conditions": existing_merchant.additional_conditions,
                    "created_at": existing_merchant.created_at,
                    "updated_at": existing_merchant.updated_at,
                    "reward_display": f"{existing_merchant.reward_rate}%"
                })
            else:
                # Use default with "Not Available" indicator
                merged_merchants.append({
                    "id": None,
                    "card_master_id": card_id,
                    "merchant_name": default_merchant["merchant_name"],
                    "merchant_display_name": default_merchant["merchant_display_name"],
                    "merchant_category": default_merchant["merchant_category"],
                    "reward_rate": 0.0,  # Not Available
                    "reward_type": "cashback",
                    "reward_cap": None,
                    "reward_cap_period": None,
                    "minimum_transaction_amount": None,
                    "is_active": False,  # Mark as inactive for Not Available
                    "valid_from": None,
                    "valid_until": None,
                    "requires_registration": False,
                    "additional_conditions": "Not Available - No data available",
                    "created_at": None,
                    "updated_at": None,
                    "reward_display": "Not Available"
                })
        
        # Convert to dict and back to handle None values properly
        card_dict = {
            "id": card_with_relations.id,
            "bank_name": card_with_relations.bank_name,
            "card_name": card_with_relations.card_name,
            "card_variant": card_with_relations.card_variant,
            "card_network": card_with_relations.card_network,
            "card_tier": card_with_relations.card_tier.lower() if card_with_relations.card_tier else "basic",
            "joining_fee": card_with_relations.joining_fee,
            "annual_fee": card_with_relations.annual_fee,
            "is_lifetime_free": card_with_relations.is_lifetime_free,
            "annual_fee_waiver_spend": card_with_relations.annual_fee_waiver_spend,
            "foreign_transaction_fee": card_with_relations.foreign_transaction_fee,
            "late_payment_fee": card_with_relations.late_payment_fee,
            "overlimit_fee": card_with_relations.overlimit_fee,
            "cash_advance_fee": card_with_relations.cash_advance_fee,
            "domestic_lounge_visits": card_with_relations.domestic_lounge_visits,
            "international_lounge_visits": card_with_relations.international_lounge_visits,
            "lounge_spend_requirement": card_with_relations.lounge_spend_requirement,
            "lounge_spend_period": card_with_relations.lounge_spend_period,
            "welcome_bonus_points": card_with_relations.welcome_bonus_points,
            "welcome_bonus_spend_requirement": card_with_relations.welcome_bonus_spend_requirement,
            "welcome_bonus_timeframe": card_with_relations.welcome_bonus_timeframe,
            "minimum_credit_limit": card_with_relations.minimum_credit_limit,
            "maximum_credit_limit": card_with_relations.maximum_credit_limit,
            "minimum_salary": card_with_relations.minimum_salary,
            "minimum_age": card_with_relations.minimum_age,
            "maximum_age": card_with_relations.maximum_age,
            "contactless_enabled": card_with_relations.contactless_enabled,
            "chip_enabled": card_with_relations.chip_enabled,
            "mobile_wallet_support": card_with_relations.mobile_wallet_support,
            "insurance_benefits": card_with_relations.insurance_benefits,
            "concierge_service": card_with_relations.concierge_service if card_with_relations.concierge_service is not None else False,
            "milestone_benefits": card_with_relations.milestone_benefits,
            "reward_program_name": card_with_relations.reward_program_name,
            "reward_expiry_period": card_with_relations.reward_expiry_period,
            "reward_conversion_rate": card_with_relations.reward_conversion_rate,
            "minimum_redemption_points": card_with_relations.minimum_redemption_points,
            "is_active": card_with_relations.is_active,
            "is_available_online": card_with_relations.is_available_online,
            "launch_date": card_with_relations.launch_date,
            "discontinue_date": card_with_relations.discontinue_date,
            "description": card_with_relations.description,
            "terms_and_conditions_url": card_with_relations.terms_and_conditions_url,
            "application_url": card_with_relations.application_url,
            "additional_features": card_with_relations.additional_features,
            "created_at": card_with_relations.created_at,
            "updated_at": card_with_relations.updated_at,
            "display_name": card_with_relations.display_name,
            "joining_fee_display": card_with_relations.joining_fee_display,
            "annual_fee_display": card_with_relations.annual_fee_display,
            "spending_categories": merged_categories,
            "merchant_rewards": merged_merchants
        }
        
        # Create response using the schema
        return CardMasterDataResponse(**card_dict)
        
    except Exception as e:
        print(f"Error getting card {card_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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
@router.get("/comparison", response_model=List[CardComparisonData])
def get_card_comparison_data(
    request: Request,
    user_cards_only: bool = Query(False, description="Show only user's cards"),
    card_ids: Optional[List[int]] = Query(None, description="Specific card IDs to compare"),
    db: Session = Depends(get_db)
):
    """Get card comparison data for the comparison page"""
    
    # Handle authentication manually
    current_user = None
    if user_cards_only:
        try:
            authorization = request.headers.get("Authorization")
            if authorization and authorization.startswith("Bearer "):
                token = authorization.replace("Bearer ", "")
                user_id = verify_token(token)
                if user_id:
                    current_user = db.query(User).filter(User.id == int(user_id)).first()
                    if current_user and not current_user.is_active:
                        current_user = None
        except Exception as e:
            print(f"Error authenticating user: {e}")
    
    print(f"Comparison request - user_cards_only: {user_cards_only}, current_user: {current_user.id if current_user else None}")
    
    # If user_cards_only is requested but no user is authenticated, return empty
    if user_cards_only and not current_user:
        print(f"User cards only requested but no user authenticated")
        return []
    
    if user_cards_only and current_user:
        print(f"Getting user cards for user ID: {current_user.id}")
        
        # Debug: Check all user cards first
        all_user_cards = db.query(CreditCard).filter(
            CreditCard.user_id == current_user.id
        ).all()
        print(f"User has {len(all_user_cards)} total cards in CreditCard table")
        for card in all_user_cards:
            print(f"  - Card ID: {card.id}, Master Data ID: {card.card_master_data_id}, Card Name: {card.card_name}")
        
        # Get cards that the user owns with card_master_data_id
        user_cards_with_master = db.query(CreditCard).filter(
            and_(
                CreditCard.user_id == current_user.id,
                CreditCard.card_master_data_id.isnot(None)
            )
        ).all()
        print(f"User has {len(user_cards_with_master)} cards with card_master_data_id")
        
        if user_cards_with_master:
            user_card_master_ids = [card.card_master_data_id for card in user_cards_with_master]
            print(f"Master data IDs: {user_card_master_ids}")
            
            # Debug: Check if these master data IDs exist in CardMasterData table
            master_data_cards = db.query(CardMasterData).filter(
                CardMasterData.id.in_(user_card_master_ids)
            ).all()
            print(f"Found {len(master_data_cards)} cards in CardMasterData table")
            for card in master_data_cards:
                print(f"  - Master Data ID: {card.id}, Bank: {card.bank_name}, Card: {card.card_name}")
            
            query = db.query(CardMasterData).filter(
                CardMasterData.id.in_(user_card_master_ids)
            )
        else:
            print("No cards found with card_master_data_id")
            return []
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
    
    print(f"Found {len(cards)} cards for comparison")
    for card in cards:
        print(f"  - {card.bank_name} {card.card_name}")
    
    # Calculate popularity scores for categories and merchants
    category_popularity = {}
    merchant_popularity = {}
    
    # Collect all categories and merchants with their reward rates
    for card in cards:
        for category in card.spending_categories:
            if category.is_active:
                category_name = category.category_name
                if category_name not in category_popularity:
                    category_popularity[category_name] = {
                        'total_cards': 0,
                        'total_reward_rate': 0,
                        'max_reward_rate': 0
                    }
                category_popularity[category_name]['total_cards'] += 1
                category_popularity[category_name]['total_reward_rate'] += category.reward_rate
                category_popularity[category_name]['max_reward_rate'] = max(
                    category_popularity[category_name]['max_reward_rate'], 
                    category.reward_rate
                )
        
        for merchant in card.merchant_rewards:
            if merchant.is_active:
                merchant_name = merchant.merchant_name
                if merchant_name not in merchant_popularity:
                    merchant_popularity[merchant_name] = {
                        'total_cards': 0,
                        'total_reward_rate': 0,
                        'max_reward_rate': 0
                    }
                merchant_popularity[merchant_name]['total_cards'] += 1
                merchant_popularity[merchant_name]['total_reward_rate'] += merchant.reward_rate
                merchant_popularity[merchant_name]['max_reward_rate'] = max(
                    merchant_popularity[merchant_name]['max_reward_rate'], 
                    merchant.reward_rate
                )
    
    # Calculate enhanced popularity scores using market research data
    def calculate_enhanced_popularity_score(merchant_name, stats):
        """Calculate enhanced popularity score combining market data with card coverage"""
        avg_reward_rate = stats['total_reward_rate'] / stats['total_cards'] if stats['total_cards'] > 0 else 0
        coverage_percent = stats['total_cards'] / len(cards)  # Percentage of cards offering this
        
        # Use market research-based popularity service
        enhanced_score = merchant_popularity_service.calculate_enhanced_popularity_score(
            merchant_name=merchant_name,
            card_coverage_percent=coverage_percent,
            avg_reward_rate=avg_reward_rate
        )
        
        return enhanced_score
    
    # Sort categories by traditional method (still useful for spending categories)
    def calculate_category_popularity_score(stats):
        avg_reward_rate = stats['total_reward_rate'] / stats['total_cards'] if stats['total_cards'] > 0 else 0
        coverage_score = stats['total_cards'] / len(cards)  # Percentage of cards offering this
        reward_score = avg_reward_rate / 10  # Normalize reward rate (assuming max ~10%)
        max_reward_bonus = stats['max_reward_rate'] / 20  # Bonus for having high max rates
        
        return (coverage_score * settings.POPULARITY_COVERAGE_WEIGHT + 
                reward_score * settings.POPULARITY_REWARD_WEIGHT + 
                max_reward_bonus * settings.POPULARITY_MAX_REWARD_WEIGHT)
    
    # Sort categories by traditional method
    sorted_categories = sorted(
        category_popularity.keys(),
        key=lambda x: calculate_category_popularity_score(category_popularity[x]),
        reverse=True
    )
    
    # Sort merchants by enhanced market research-based popularity
    sorted_merchants = sorted(
        merchant_popularity.keys(),
        key=lambda x: calculate_enhanced_popularity_score(x, merchant_popularity[x]),
        reverse=True
    )
    
    # Limit merchants to top N for better usability
    top_merchants = sorted_merchants[:settings.TOP_MERCHANTS_LIMIT]
    
    # Format data for comparison page
    comparison_data = []
    for card in cards:
        # Build categories dict (sorted by popularity)
        categories = {}
        for category_name in sorted_categories:
            category = next((c for c in card.spending_categories if c.category_name == category_name and c.is_active), None)
            if category:
                categories[category_name] = category.reward_display
        
        # Build merchants dict (only top N popular merchants)
        merchants = {}
        for merchant_name in top_merchants:
            merchant = next((m for m in card.merchant_rewards if m.merchant_name == merchant_name and m.is_active), None)
            if merchant:
                merchants[merchant_name] = merchant.reward_display
        
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

@router.get("/debug/user")
def debug_user_info(request: Request, db: Session = Depends(get_db)):
    """Debug endpoint to check user authentication"""
    try:
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            user_id = verify_token(token)
            if user_id:
                current_user = db.query(User).filter(User.id == int(user_id)).first()
                if current_user and current_user.is_active:
                    return {
                        "authenticated": True,
                        "user_id": current_user.id,
                        "email": current_user.email
                    }
    except Exception as e:
        return {"authenticated": False, "error": str(e)}
    
    return {"authenticated": False} 
