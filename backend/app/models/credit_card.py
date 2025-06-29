from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CreditCard(Base):
    __tablename__ = "credit_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_master_data_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=True)  # Link to master data
    
    # Card Information
    card_name = Column(String(200), nullable=False)
    card_type = Column(String(50), nullable=False)  # Visa, Mastercard, Amex, etc.
    card_network = Column(String(50), nullable=False)  # Visa, Mastercard, Amex, etc.
    card_number_last4 = Column(String(4), nullable=False)
    card_holder_name = Column(String(200), nullable=False)
    expiry_month = Column(Integer, nullable=False)
    expiry_year = Column(Integer, nullable=False)
    
    # Card Details
    credit_limit = Column(Float, nullable=True)
    available_credit = Column(Float, nullable=True)
    current_balance = Column(Float, default=0.0)
    due_date = Column(DateTime, nullable=True)
    minimum_payment = Column(Float, nullable=True)
    
    # Reward Information
    reward_rate_general = Column(Float, default=1.0)  # Default 1% cashback
    reward_rate_dining = Column(Float, nullable=True)
    reward_rate_groceries = Column(Float, nullable=True)
    reward_rate_travel = Column(Float, nullable=True)
    reward_rate_online_shopping = Column(Float, nullable=True)
    reward_rate_fuel = Column(Float, nullable=True)
    reward_rate_entertainment = Column(Float, nullable=True)
    
    # Special Benefits
    welcome_benefits = Column(Text, nullable=True)  # JSON string
    annual_fee = Column(Float, default=0.0)
    foreign_transaction_fee = Column(Float, default=0.0)
    late_payment_fee = Column(Float, nullable=True)
    
    # Card Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    is_primary = Column(Boolean, default=False)
    
    # Additional Features
    features = Column(JSON, nullable=True)  # JSON object for additional features
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="credit_cards")
    transactions = relationship("Transaction", back_populates="credit_card", cascade="all, delete-orphan")
    card_master_data = relationship("CardMasterData", back_populates="user_credit_cards")
    
    def __repr__(self):
        return f"<CreditCard(id={self.id}, card_name='{self.card_name}', user_id={self.user_id})>"
    
    @property
    def masked_number(self) -> str:
        """Get masked card number"""
        return f"**** **** **** {self.card_number_last4}"
    
    @property
    def expiry_date(self) -> str:
        """Get formatted expiry date"""
        return f"{self.expiry_month:02d}/{self.expiry_year}"
    
    @property
    def utilization_rate(self) -> float:
        """Calculate credit utilization rate"""
        if self.credit_limit and self.credit_limit > 0:
            return (self.current_balance / self.credit_limit) * 100
        return 0.0
    
    def get_reward_rate(self, category: str) -> float:
        """Get reward rate for specific category"""
        category_mapping = {
            "dining": self.reward_rate_dining,
            "groceries": self.reward_rate_groceries,
            "travel": self.reward_rate_travel,
            "online_shopping": self.reward_rate_online_shopping,
            "fuel": self.reward_rate_fuel,
            "entertainment": self.reward_rate_entertainment,
        }
        
        return category_mapping.get(category, self.reward_rate_general)
    
    def to_dict(self):
        """Convert credit card to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "card_name": self.card_name,
            "card_type": self.card_type,
            "card_network": self.card_network,
            "card_number_last4": self.card_number_last4,
            "masked_number": self.masked_number,
            "card_holder_name": self.card_holder_name,
            "expiry_month": self.expiry_month,
            "expiry_year": self.expiry_year,
            "expiry_date": self.expiry_date,
            "credit_limit": self.credit_limit,
            "available_credit": self.available_credit,
            "current_balance": self.current_balance,
            "utilization_rate": self.utilization_rate,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "minimum_payment": self.minimum_payment,
            "reward_rate_general": self.reward_rate_general,
            "reward_rate_dining": self.reward_rate_dining,
            "reward_rate_groceries": self.reward_rate_groceries,
            "reward_rate_travel": self.reward_rate_travel,
            "reward_rate_online_shopping": self.reward_rate_online_shopping,
            "reward_rate_fuel": self.reward_rate_fuel,
            "reward_rate_entertainment": self.reward_rate_entertainment,
            "welcome_benefits": self.welcome_benefits,
            "annual_fee": self.annual_fee,
            "foreign_transaction_fee": self.foreign_transaction_fee,
            "late_payment_fee": self.late_payment_fee,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "is_primary": self.is_primary,
            "features": self.features,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 