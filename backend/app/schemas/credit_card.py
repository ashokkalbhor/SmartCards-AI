from typing import Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime


class CreditCardBase(BaseModel):
    card_name: str
    card_type: str
    card_network: str
    card_number_last4: str
    card_holder_name: str
    expiry_month: int
    expiry_year: int
    
    @validator('card_number_last4')
    def validate_card_number_last4(cls, v):
        if not v.isdigit() or len(v) != 4:
            raise ValueError('Card number last 4 digits must be 4 digits')
        return v
    
    @validator('expiry_month')
    def validate_expiry_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('Expiry month must be between 1 and 12')
        return v
    
    @validator('expiry_year')
    def validate_expiry_year(cls, v):
        current_year = datetime.now().year
        if v < current_year or v > current_year + 20:
            raise ValueError('Expiry year must be between current year and current year + 20')
        return v


class CreditCardCreate(CreditCardBase):
    card_master_data_id: Optional[int] = None
    credit_limit: Optional[float] = None
    available_credit: Optional[float] = None
    current_balance: float = 0.0
    due_date: Optional[datetime] = None
    minimum_payment: Optional[float] = None
    reward_rate_general: float = 1.0
    reward_rate_dining: Optional[float] = None
    reward_rate_groceries: Optional[float] = None
    reward_rate_travel: Optional[float] = None
    reward_rate_online_shopping: Optional[float] = None
    reward_rate_fuel: Optional[float] = None
    reward_rate_entertainment: Optional[float] = None
    welcome_benefits: Optional[str] = None
    annual_fee: float = 0.0
    foreign_transaction_fee: float = 0.0
    late_payment_fee: Optional[float] = None
    is_default: bool = False
    is_primary: bool = False
    features: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class CreditCardUpdate(BaseModel):
    card_name: Optional[str] = None
    credit_limit: Optional[float] = None
    available_credit: Optional[float] = None
    current_balance: Optional[float] = None
    due_date: Optional[datetime] = None
    minimum_payment: Optional[float] = None
    reward_rate_general: Optional[float] = None
    reward_rate_dining: Optional[float] = None
    reward_rate_groceries: Optional[float] = None
    reward_rate_travel: Optional[float] = None
    reward_rate_online_shopping: Optional[float] = None
    reward_rate_fuel: Optional[float] = None
    reward_rate_entertainment: Optional[float] = None
    welcome_benefits: Optional[str] = None
    annual_fee: Optional[float] = None
    foreign_transaction_fee: Optional[float] = None
    late_payment_fee: Optional[float] = None
    is_default: Optional[bool] = None
    is_primary: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class CreditCardResponse(CreditCardBase):
    id: int
    user_id: int
    card_master_data_id: Optional[int] = None
    masked_number: str
    expiry_date: str
    credit_limit: Optional[float] = None
    available_credit: Optional[float] = None
    current_balance: float
    utilization_rate: float
    due_date: Optional[datetime] = None
    minimum_payment: Optional[float] = None
    reward_rate_general: float
    reward_rate_dining: Optional[float] = None
    reward_rate_groceries: Optional[float] = None
    reward_rate_travel: Optional[float] = None
    reward_rate_online_shopping: Optional[float] = None
    reward_rate_fuel: Optional[float] = None
    reward_rate_entertainment: Optional[float] = None
    welcome_benefits: Optional[str] = None
    annual_fee: float
    foreign_transaction_fee: float
    late_payment_fee: Optional[float] = None
    is_active: bool
    is_default: bool
    is_primary: bool
    features: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CreditCardSummary(BaseModel):
    """Summary of credit card for dashboard"""
    id: int
    card_name: str
    card_network: str
    masked_number: str
    current_balance: float
    credit_limit: Optional[float] = None
    utilization_rate: float
    reward_rate_general: float
    is_default: bool
    is_primary: bool
    due_date: Optional[datetime] = None
    minimum_payment: Optional[float] = None


class CardRecommendation(BaseModel):
    """Credit card recommendation for a specific merchant/category"""
    card_id: int
    card_name: str
    card_network: str
    reward_rate: float
    reward_amount: float
    reason: str
    special_offers: Optional[list] = None
    is_best_choice: bool = False


class CardComparison(BaseModel):
    """Comparison between multiple cards"""
    cards: list[CreditCardResponse]
    best_card_id: int
    comparison_reasons: Dict[str, str] 