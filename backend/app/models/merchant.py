from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Merchant(Base):
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Merchant Information
    name = Column(String(200), nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    # Merchant Categories
    primary_category = Column(String(100), nullable=False, index=True)
    secondary_categories = Column(JSON, nullable=True)  # Array of categories
    mcc_code = Column(String(10), nullable=True)  # Merchant Category Code
    
    # Location Information
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Business Information
    business_type = Column(String(100), nullable=True)  # Online, Offline, Both
    is_chain = Column(Boolean, default=False)
    parent_company = Column(String(200), nullable=True)
    
    # Reward Information
    reward_multipliers = Column(JSON, nullable=True)  # JSON object with card_id: multiplier
    special_offers = Column(JSON, nullable=True)  # JSON array of special offers
    cashback_offers = Column(JSON, nullable=True)  # JSON array of cashback offers
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Additional Information
    tags = Column(JSON, nullable=True)  # Array of tags
    merchant_metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="merchant")
    
    def __repr__(self):
        return f"<Merchant(id={self.id}, name='{self.name}', category='{self.primary_category}')>"
    
    @property
    def full_address(self) -> str:
        """Get full address string"""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.country:
            parts.append(self.country)
        
        return ", ".join(parts) if parts else None
    
    def get_reward_multiplier(self, card_id: int) -> float:
        """Get reward multiplier for specific card"""
        if self.reward_multipliers and str(card_id) in self.reward_multipliers:
            return self.reward_multipliers[str(card_id)]
        return 1.0
    
    def has_special_offer(self, card_id: int = None) -> bool:
        """Check if merchant has special offers"""
        if not self.special_offers:
            return False
        
        if card_id is None:
            return len(self.special_offers) > 0
        
        # Check if there's a special offer for the specific card
        for offer in self.special_offers:
            if offer.get("card_id") == card_id:
                return True
        return False
    
    def get_special_offers(self, card_id: int = None):
        """Get special offers for merchant"""
        if not self.special_offers:
            return []
        
        if card_id is None:
            return self.special_offers
        
        # Filter offers for specific card
        return [offer for offer in self.special_offers if offer.get("card_id") == card_id]
    
    def to_dict(self):
        """Convert merchant to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "website": self.website,
            "logo_url": self.logo_url,
            "primary_category": self.primary_category,
            "secondary_categories": self.secondary_categories,
            "mcc_code": self.mcc_code,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
            "full_address": self.full_address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "business_type": self.business_type,
            "is_chain": self.is_chain,
            "parent_company": self.parent_company,
            "reward_multipliers": self.reward_multipliers,
            "special_offers": self.special_offers,
            "cashback_offers": self.cashback_offers,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_featured": self.is_featured,
            "tags": self.tags,
            "merchant_metadata": self.merchant_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 