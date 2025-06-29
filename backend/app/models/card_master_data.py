from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class CardTierEnum(enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    SUPER_PREMIUM = "super_premium"
    ELITE = "elite"


class CardMasterData(Base):
    """
    Master data table for all credit card variants available in the market.
    This stores comprehensive information for comparison purposes.
    """
    __tablename__ = "card_master_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Card Basic Information
    bank_name = Column(String(100), nullable=False, index=True)
    card_name = Column(String(200), nullable=False)
    card_variant = Column(String(100), nullable=True)  # e.g., "Gold", "Platinum"
    card_network = Column(String(50), nullable=False)  # Visa, Mastercard, Amex, RuPay
    card_tier = Column(Enum(CardTierEnum), nullable=False, default=CardTierEnum.BASIC)
    
    # Fees and Charges
    joining_fee = Column(Float, nullable=True)
    annual_fee = Column(Float, nullable=True)
    is_lifetime_free = Column(Boolean, default=False)
    annual_fee_waiver_spend = Column(Float, nullable=True)  # Spend required to waive annual fee
    foreign_transaction_fee = Column(Float, nullable=True)  # Percentage
    late_payment_fee = Column(Float, nullable=True)
    overlimit_fee = Column(Float, nullable=True)
    cash_advance_fee = Column(Float, nullable=True)  # Percentage
    
    # Lounge Benefits
    domestic_lounge_visits = Column(Integer, nullable=True)  # Per year
    international_lounge_visits = Column(Integer, nullable=True)  # Per year
    lounge_spend_requirement = Column(Float, nullable=True)  # Quarterly spend for lounge access
    lounge_spend_period = Column(String(20), nullable=True)  # "quarterly", "monthly", "yearly"
    
    # Welcome Benefits
    welcome_bonus_points = Column(Float, nullable=True)
    welcome_bonus_spend_requirement = Column(Float, nullable=True)
    welcome_bonus_timeframe = Column(Integer, nullable=True)  # Days
    
    # Credit Limit
    minimum_credit_limit = Column(Float, nullable=True)
    maximum_credit_limit = Column(Float, nullable=True)
    
    # Eligibility Criteria
    minimum_salary = Column(Float, nullable=True)
    minimum_age = Column(Integer, nullable=True)
    maximum_age = Column(Integer, nullable=True)
    
    # Card Features
    contactless_enabled = Column(Boolean, default=True)
    chip_enabled = Column(Boolean, default=True)
    mobile_wallet_support = Column(JSON, nullable=True)  # ["Apple Pay", "Google Pay", "Samsung Pay"]
    
    # Additional Benefits
    insurance_benefits = Column(JSON, nullable=True)  # Travel, Purchase protection, etc.
    concierge_service = Column(Boolean, default=False)
    milestone_benefits = Column(JSON, nullable=True)  # Spending milestone rewards
    
    # Reward Program Details
    reward_program_name = Column(String(100), nullable=True)
    reward_expiry_period = Column(Integer, nullable=True)  # In months
    reward_conversion_rate = Column(Float, nullable=True)  # Points to currency
    minimum_redemption_points = Column(Float, nullable=True)
    
    # Status and Metadata
    is_active = Column(Boolean, default=True)
    is_available_online = Column(Boolean, default=True)
    launch_date = Column(DateTime, nullable=True)
    discontinue_date = Column(DateTime, nullable=True)
    
    # Additional Information
    description = Column(Text, nullable=True)
    terms_and_conditions_url = Column(String(500), nullable=True)
    application_url = Column(String(500), nullable=True)
    additional_features = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    spending_categories = relationship("CardSpendingCategory", back_populates="card_master", cascade="all, delete-orphan")
    merchant_rewards = relationship("CardMerchantReward", back_populates="card_master", cascade="all, delete-orphan")
    user_credit_cards = relationship("CreditCard", back_populates="card_master_data")
    
    def __repr__(self):
        return f"<CardMasterData(id={self.id}, bank='{self.bank_name}', card='{self.card_name}')>"
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        if self.card_variant:
            return f"{self.bank_name} {self.card_name} {self.card_variant}"
        return f"{self.bank_name} {self.card_name}"
    
    @property
    def joining_fee_display(self) -> str:
        """Get formatted joining fee"""
        if self.is_lifetime_free:
            return "LTF"
        elif self.joining_fee:
            return f"₹{self.joining_fee:,.0f}"
        else:
            return "₹0"
    
    @property
    def annual_fee_display(self) -> str:
        """Get formatted annual fee with waiver info"""
        if self.is_lifetime_free:
            return "LTF"
        elif self.annual_fee:
            fee_text = f"₹{self.annual_fee:,.0f}"
            if self.annual_fee_waiver_spend:
                fee_text += f" (Waived on ₹{self.annual_fee_waiver_spend:,.0f} spend)"
            return fee_text
        else:
            return "₹0"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "bank_name": self.bank_name,
            "card_name": self.card_name,
            "card_variant": self.card_variant,
            "display_name": self.display_name,
            "card_network": self.card_network,
            "card_tier": self.card_tier.value if self.card_tier else None,
            "joining_fee": self.joining_fee,
            "annual_fee": self.annual_fee,
            "is_lifetime_free": self.is_lifetime_free,
            "joining_fee_display": self.joining_fee_display,
            "annual_fee_display": self.annual_fee_display,
            "annual_fee_waiver_spend": self.annual_fee_waiver_spend,
            "foreign_transaction_fee": self.foreign_transaction_fee,
            "domestic_lounge_visits": self.domestic_lounge_visits,
            "international_lounge_visits": self.international_lounge_visits,
            "lounge_spend_requirement": self.lounge_spend_requirement,
            "lounge_spend_period": self.lounge_spend_period,
            "welcome_bonus_points": self.welcome_bonus_points,
            "welcome_bonus_spend_requirement": self.welcome_bonus_spend_requirement,
            "minimum_credit_limit": self.minimum_credit_limit,
            "maximum_credit_limit": self.maximum_credit_limit,
            "minimum_salary": self.minimum_salary,
            "reward_program_name": self.reward_program_name,
            "reward_expiry_period": self.reward_expiry_period,
            "is_active": self.is_active,
            "is_available_online": self.is_available_online,
            "description": self.description,
            "additional_features": self.additional_features,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class CardSpendingCategory(Base):
    """
    Reward rates for different spending categories for each card
    """
    __tablename__ = "card_spending_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Category Information
    category_name = Column(String(100), nullable=False)  # education, fuel, jewelry, etc.
    category_display_name = Column(String(100), nullable=False)
    
    # Reward Details
    reward_rate = Column(Float, nullable=False)  # Percentage
    reward_type = Column(String(50), default="cashback")  # cashback, points, miles
    reward_cap = Column(Float, nullable=True)  # Maximum reward per month/quarter
    reward_cap_period = Column(String(20), nullable=True)  # monthly, quarterly, yearly
    minimum_transaction_amount = Column(Float, nullable=True)
    
    # Conditions
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    additional_conditions = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    card_master = relationship("CardMasterData", back_populates="spending_categories")
    
    def __repr__(self):
        return f"<CardSpendingCategory(card_id={self.card_master_id}, category='{self.category_name}', rate={self.reward_rate}%)>"
    
    @property
    def reward_display(self) -> str:
        """Get formatted reward rate display"""
        if self.reward_rate == 0:
            return "-"
        
        reward_text = f"{self.reward_rate}%"
        if self.reward_cap:
            cap_period = self.reward_cap_period or "monthly"
            reward_text += f" (capped at ₹{self.reward_cap:,.0f} {cap_period})"
        
        return reward_text


class CardMerchantReward(Base):
    """
    Merchant-specific reward rates for each card
    """
    __tablename__ = "card_merchant_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Merchant Information
    merchant_name = Column(String(100), nullable=False)  # amazon, swiggy, flipkart, etc.
    merchant_display_name = Column(String(100), nullable=False)
    merchant_category = Column(String(100), nullable=True)  # e-commerce, food delivery, etc.
    
    # Reward Details
    reward_rate = Column(Float, nullable=False)  # Percentage
    reward_type = Column(String(50), default="cashback")  # cashback, points, miles
    reward_cap = Column(Float, nullable=True)  # Maximum reward per month/quarter
    reward_cap_period = Column(String(20), nullable=True)  # monthly, quarterly, yearly
    minimum_transaction_amount = Column(Float, nullable=True)
    
    # Conditions
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    requires_registration = Column(Boolean, default=False)
    additional_conditions = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    card_master = relationship("CardMasterData", back_populates="merchant_rewards")
    
    def __repr__(self):
        return f"<CardMerchantReward(card_id={self.card_master_id}, merchant='{self.merchant_name}', rate={self.reward_rate}%)>"
    
    @property
    def reward_display(self) -> str:
        """Get formatted reward rate display"""
        if self.reward_rate == 0:
            return "-"
        
        reward_text = f"{self.reward_rate}%"
        if self.reward_cap:
            cap_period = self.reward_cap_period or "monthly"
            reward_text += f" (capped at ₹{self.reward_cap:,.0f} {cap_period})"
        
        return reward_text 