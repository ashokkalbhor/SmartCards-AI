from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reward(Base):
    __tablename__ = "rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    credit_card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    
    # Reward Information
    reward_type = Column(String(50), nullable=False)  # cashback, points, miles, etc.
    reward_category = Column(String(100), nullable=True)  # dining, travel, groceries, etc.
    amount = Column(Float, nullable=False)
    points = Column(Integer, default=0)
    currency = Column(String(3), default="INR")
    
    # Reward Details
    description = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)  # transaction, welcome_bonus, referral, etc.
    reward_rate = Column(Float, nullable=True)
    multiplier = Column(Float, default=1.0)
    
    # Reward Status
    status = Column(String(50), default="pending")  # pending, earned, redeemed, expired
    is_credited = Column(Boolean, default=False)
    credited_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    
    # Redemption Information
    redemption_amount = Column(Float, nullable=True)
    redemption_date = Column(DateTime, nullable=True)
    redemption_method = Column(String(100), nullable=True)  # statement_credit, gift_card, etc.
    
    # Additional Information
    notes = Column(Text, nullable=True)
    reward_metadata = Column(JSON, nullable=True)  # Additional reward metadata
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="rewards")
    credit_card = relationship("CreditCard")
    transaction = relationship("Transaction")
    
    def __repr__(self):
        return f"<Reward(id={self.id}, amount={self.amount}, type='{self.reward_type}')>"
    
    @property
    def formatted_amount(self) -> str:
        """Get formatted reward amount"""
        return f"{self.currency} {self.amount:,.2f}"
    
    @property
    def is_expired(self) -> bool:
        """Check if reward is expired"""
        if not self.expiry_date:
            return False
        from datetime import datetime
        return datetime.utcnow() > self.expiry_date
    
    @property
    def is_redeemable(self) -> bool:
        """Check if reward is redeemable"""
        return (
            self.status == "earned" 
            and self.is_credited 
            and not self.is_expired
            and self.amount > 0
        )
    
    @property
    def days_until_expiry(self) -> int:
        """Get days until reward expires"""
        if not self.expiry_date:
            return None
        
        from datetime import datetime
        delta = self.expiry_date - datetime.utcnow()
        return max(0, delta.days)
    
    def to_dict(self):
        """Convert reward to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "credit_card_id": self.credit_card_id,
            "transaction_id": self.transaction_id,
            "reward_type": self.reward_type,
            "reward_category": self.reward_category,
            "amount": self.amount,
            "formatted_amount": self.formatted_amount,
            "points": self.points,
            "currency": self.currency,
            "description": self.description,
            "source": self.source,
            "reward_rate": self.reward_rate,
            "multiplier": self.multiplier,
            "status": self.status,
            "is_credited": self.is_credited,
            "credited_date": self.credited_date.isoformat() if self.credited_date else None,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "is_expired": self.is_expired,
            "is_redeemable": self.is_redeemable,
            "days_until_expiry": self.days_until_expiry,
            "redemption_amount": self.redemption_amount,
            "redemption_date": self.redemption_date.isoformat() if self.redemption_date else None,
            "redemption_method": self.redemption_method,
            "notes": self.notes,
            "reward_metadata": self.reward_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 