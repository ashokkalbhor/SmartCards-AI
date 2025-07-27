from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Merchant(Base):
    """
    Merchants table for dynamic merchant management
    """
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)  # "amazon", "flipkart"
    display_name = Column(String(200), nullable=False)  # "Amazon", "Flipkart"
    primary_category = Column(String(100), nullable=False, index=True)  # "online_shopping", "dining"
    is_active = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="merchant")
    # card_rewards = relationship("CardMerchantReward", back_populates="merchant")
    
    def __repr__(self):
        return f"<Merchant(id={self.id}, name='{self.name}', category='{self.primary_category}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "merchant_name": self.name,  # For backward compatibility
            "display_name": self.display_name,
            "category": self.primary_category,
            "primary_category": self.primary_category,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 