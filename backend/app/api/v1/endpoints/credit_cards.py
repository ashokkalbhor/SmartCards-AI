from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.credit_card import CreditCard
from app.schemas.credit_card import (
    CreditCardCreate,
    CreditCardUpdate,
    CreditCardResponse,
    CreditCardSummary
)
from app.models.user import User
from app.core.security import get_current_user_sync

router = APIRouter()


@router.post("/", response_model=CreditCardResponse)
def create_credit_card(
    card_data: CreditCardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Create a new credit card for the current user"""
    db_card = CreditCard(
        user_id=current_user.id,
        **card_data.dict()
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    
    return db_card


@router.get("/", response_model=List[CreditCardResponse])
def get_credit_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Get all credit cards for the current user"""
    query = db.query(CreditCard).filter(
        CreditCard.user_id == current_user.id
    )
    
    if is_active is not None:
        query = query.filter(CreditCard.is_active == is_active)
    
    cards = query.offset(skip).limit(limit).all()
    return cards


@router.get("/{card_id}", response_model=CreditCardResponse)
def get_credit_card(
    card_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific credit card by ID"""
    card = db.query(CreditCard).filter(
        CreditCard.id == card_id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Credit card not found")
    
    return card


@router.put("/{card_id}", response_model=CreditCardResponse)
def update_credit_card(
    card_id: int,
    card_data: CreditCardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Update a credit card"""
    card = db.query(CreditCard).filter(
        CreditCard.id == card_id,
        CreditCard.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Credit card not found")
    
    update_data = card_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)
    
    db.commit()
    db.refresh(card)
    
    return card


@router.delete("/{card_id}")
def delete_credit_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Delete a credit card"""
    card = db.query(CreditCard).filter(
        CreditCard.id == card_id,
        CreditCard.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Credit card not found")
    
    db.delete(card)
    db.commit()
    
    return {"message": "Credit card deleted successfully"}


@router.get("/summary/list", response_model=List[CreditCardSummary])
def get_credit_cards_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_sync)
):
    """Get summary list of user's credit cards for dashboard"""
    cards = db.query(CreditCard).filter(
        CreditCard.user_id == current_user.id,
        CreditCard.is_active == True
    ).all()
    
    return cards 