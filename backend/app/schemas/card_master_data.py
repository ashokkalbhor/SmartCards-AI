from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class CardTierEnum(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    SUPER_PREMIUM = "super_premium"
    SUPER_PREMIUM_HYPHEN = "super-premium"
    ELITE = "elite"
    STANDARD = "standard"
    GOLD = "gold"
    PLATINUM = "platinum"
    BUSINESS = "business"
    MID_PREMIUM = "mid_premium"
    ULTRA_PREMIUM = "ultra_premium"
    ULTRA_PREMIUM_HYPHEN = "ultra-premium"


class RewardTypeEnum(str, Enum):
    CASHBACK = "cashback"
    POINTS = "points"
    MILES = "miles"


class CardMasterDataBase(BaseModel):
    bank_name: str = Field(..., max_length=100)
    card_name: str = Field(..., max_length=200)
    card_variant: Optional[str] = Field(None, max_length=100)
    card_network: str = Field(..., max_length=50)
    card_tier: CardTierEnum = CardTierEnum.BASIC
    
    # Fees and Charges
    joining_fee: Optional[float] = None
    annual_fee: Optional[float] = None
    is_lifetime_free: bool = False
    annual_fee_waiver_spend: Optional[float] = None
    foreign_transaction_fee: Optional[float] = None
    late_payment_fee: Optional[float] = None
    overlimit_fee: Optional[float] = None
    cash_advance_fee: Optional[float] = None
    
    # Lounge Benefits
    domestic_lounge_visits: Optional[int] = None
    international_lounge_visits: Optional[int] = None
    lounge_spend_requirement: Optional[float] = None
    lounge_spend_period: Optional[str] = Field(None, max_length=20)
    
    # Welcome Benefits
    welcome_bonus_points: Optional[float] = None
    welcome_bonus_spend_requirement: Optional[float] = None
    welcome_bonus_timeframe: Optional[int] = None
    
    # Credit Limit
    minimum_credit_limit: Optional[float] = None
    maximum_credit_limit: Optional[float] = None
    
    # Eligibility
    minimum_salary: Optional[float] = None
    minimum_age: Optional[int] = None
    maximum_age: Optional[int] = None
    
    # Features
    contactless_enabled: bool = True
    chip_enabled: bool = True
    mobile_wallet_support: Optional[List[str]] = None
    
    # Benefits
    insurance_benefits: Optional[Dict[str, Any]] = None
    concierge_service: bool = False
    milestone_benefits: Optional[Dict[str, Any]] = None
    
    # Reward Program
    reward_program_name: Optional[str] = Field(None, max_length=100)
    reward_expiry_period: Optional[int] = None
    reward_conversion_rate: Optional[float] = None
    minimum_redemption_points: Optional[float] = None
    
    # Status
    is_active: bool = True
    is_available_online: bool = True
    launch_date: Optional[datetime] = None
    discontinue_date: Optional[datetime] = None
    
    # Additional Info
    description: Optional[str] = None
    terms_and_conditions_url: Optional[str] = Field(None, max_length=500)
    application_url: Optional[str] = Field(None, max_length=500)
    additional_features: Optional[Dict[str, Any]] = None


class CardMasterDataCreate(CardMasterDataBase):
    pass


class CardMasterDataUpdate(BaseModel):
    bank_name: Optional[str] = Field(None, max_length=100)
    card_name: Optional[str] = Field(None, max_length=200)
    card_variant: Optional[str] = Field(None, max_length=100)
    card_network: Optional[str] = Field(None, max_length=50)
    card_tier: Optional[CardTierEnum] = None
    
    joining_fee: Optional[float] = None
    annual_fee: Optional[float] = None
    is_lifetime_free: Optional[bool] = None
    annual_fee_waiver_spend: Optional[float] = None
    foreign_transaction_fee: Optional[float] = None
    
    domestic_lounge_visits: Optional[int] = None
    international_lounge_visits: Optional[int] = None
    lounge_spend_requirement: Optional[float] = None
    lounge_spend_period: Optional[str] = None
    
    welcome_bonus_points: Optional[float] = None
    welcome_bonus_spend_requirement: Optional[float] = None
    
    minimum_credit_limit: Optional[float] = None
    maximum_credit_limit: Optional[float] = None
    minimum_salary: Optional[float] = None
    
    is_active: Optional[bool] = None
    is_available_online: Optional[bool] = None
    description: Optional[str] = None
    additional_features: Optional[Dict[str, Any]] = None


class CardSpendingCategoryBase(BaseModel):
    category_name: str = Field(..., max_length=100)
    category_display_name: str = Field(..., max_length=100)
    reward_rate: float = Field(..., ge=0, le=100)
    reward_type: str = Field(default="cashback", max_length=50)  # Changed from enum to string
    reward_cap: Optional[float] = None
    reward_cap_period: Optional[str] = Field(None, max_length=20)
    minimum_transaction_amount: Optional[float] = None
    is_active: Optional[bool] = True
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    additional_conditions: Optional[str] = None


class CardSpendingCategoryCreate(CardSpendingCategoryBase):
    card_master_id: int


class CardSpendingCategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(None, max_length=100)
    category_display_name: Optional[str] = Field(None, max_length=100)
    reward_rate: Optional[float] = Field(None, ge=0, le=100)
    reward_type: Optional[str] = Field(None, max_length=50)
    reward_cap: Optional[float] = None
    reward_cap_period: Optional[str] = Field(None, max_length=20)
    minimum_transaction_amount: Optional[float] = None
    is_active: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    additional_conditions: Optional[str] = None


class CardMerchantRewardBase(BaseModel):
    merchant_name: str = Field(..., max_length=100)
    merchant_display_name: str = Field(..., max_length=100)
    merchant_category: Optional[str] = Field(None, max_length=100)
    reward_rate: float = Field(..., ge=0, le=100)
    reward_type: str = Field(default="cashback", max_length=50)  # Changed from enum to string
    reward_cap: Optional[float] = None
    reward_cap_period: Optional[str] = Field(None, max_length=20)
    minimum_transaction_amount: Optional[float] = None
    is_active: Optional[bool] = True
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    requires_registration: bool = False
    additional_conditions: Optional[str] = None


class CardMerchantRewardCreate(CardMerchantRewardBase):
    card_master_id: int


class CardMerchantRewardUpdate(BaseModel):
    merchant_name: Optional[str] = Field(None, max_length=100)
    merchant_display_name: Optional[str] = Field(None, max_length=100)
    merchant_category: Optional[str] = Field(None, max_length=100)
    reward_rate: Optional[float] = Field(None, ge=0, le=100)
    reward_type: Optional[str] = Field(None, max_length=50)
    reward_cap: Optional[float] = None
    reward_cap_period: Optional[str] = Field(None, max_length=20)
    minimum_transaction_amount: Optional[float] = None
    is_active: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    requires_registration: Optional[bool] = None
    additional_conditions: Optional[str] = None


# Response schemas
class CardSpendingCategoryResponse(CardSpendingCategoryBase):
    id: Optional[int] = None
    card_master_id: int
    reward_display: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CardMerchantRewardResponse(CardMerchantRewardBase):
    id: Optional[int] = None
    card_master_id: int
    reward_display: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CardMasterDataResponse(CardMasterDataBase):
    id: int
    display_name: str
    joining_fee_display: str
    annual_fee_display: str
    spending_categories: List[CardSpendingCategoryResponse] = []
    merchant_rewards: List[CardMerchantRewardResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CardComparisonData(BaseModel):
    """Schema for comparison page data"""
    id: int
    bank_name: str
    card_name: str
    display_name: str
    joining_fee_display: str
    annual_fee_display: str
    annual_fee_waiver_spend: Optional[float]
    domestic_lounge_visits: Optional[int]
    lounge_spend_requirement: Optional[float]
    lounge_spend_period: Optional[str]
    categories: Dict[str, str] = {}  # category_name -> reward_display
    merchants: Dict[str, str] = {}  # merchant_name -> reward_display
    additional_info: str = ""

    class Config:
        from_attributes = True 