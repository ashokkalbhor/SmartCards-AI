from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    credit_card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=True)
    
    # Transaction Information
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    transaction_date = Column(DateTime, nullable=False)
    posted_date = Column(DateTime, nullable=True)
    
    # Transaction Details
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    transaction_type = Column(String(50), nullable=False)  # Purchase, Payment, Refund, etc.
    
    # Merchant Information
    merchant_name = Column(String(200), nullable=True)
    merchant_category = Column(String(100), nullable=True)
    merchant_city = Column(String(100), nullable=True)
    merchant_state = Column(String(100), nullable=True)
    merchant_country = Column(String(100), nullable=True)
    
    # Payment Information
    payment_method = Column(String(50), default="credit_card")
    is_online = Column(Boolean, default=False)
    is_foreign = Column(Boolean, default=False)
    
    # Reward Information
    reward_rate_applied = Column(Float, nullable=True)
    reward_amount = Column(Float, default=0.0)
    reward_points = Column(Integer, default=0)
    reward_category = Column(String(100), nullable=True)
    
    # Transaction Status
    status = Column(String(50), default="completed")  # pending, completed, failed, refunded
    is_disputed = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    
    # Additional Information
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    transaction_metadata = Column(JSON, nullable=True)  # Additional transaction metadata
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    credit_card = relationship("CreditCard", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, description='{self.description}')>"
    
    @property
    def formatted_amount(self) -> str:
        """Get formatted amount with currency"""
        return f"{self.currency} {self.amount:,.2f}"
    
    @property
    def formatted_reward_amount(self) -> str:
        """Get formatted reward amount"""
        return f"{self.currency} {self.reward_amount:,.2f}"
    
    @property
    def is_reward_eligible(self) -> bool:
        """Check if transaction is eligible for rewards"""
        return (
            self.status == "completed" 
            and self.transaction_type == "purchase" 
            and self.amount > 0
            and not self.is_disputed
        )
    
    def calculate_reward(self, reward_rate: float) -> float:
        """Calculate reward amount based on reward rate"""
        if not self.is_reward_eligible:
            return 0.0
        
        return (self.amount * reward_rate) / 100
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "credit_card_id": self.credit_card_id,
            "merchant_id": self.merchant_id,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "formatted_amount": self.formatted_amount,
            "currency": self.currency,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "transaction_type": self.transaction_type,
            "merchant_name": self.merchant_name,
            "merchant_category": self.merchant_category,
            "merchant_city": self.merchant_city,
            "merchant_state": self.merchant_state,
            "merchant_country": self.merchant_country,
            "payment_method": self.payment_method,
            "is_online": self.is_online,
            "is_foreign": self.is_foreign,
            "reward_rate_applied": self.reward_rate_applied,
            "reward_amount": self.reward_amount,
            "formatted_reward_amount": self.formatted_reward_amount,
            "reward_points": self.reward_points,
            "reward_category": self.reward_category,
            "status": self.status,
            "is_disputed": self.is_disputed,
            "is_recurring": self.is_recurring,
            "is_reward_eligible": self.is_reward_eligible,
            "reference_number": self.reference_number,
            "notes": self.notes,
            "transaction_metadata": self.transaction_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 