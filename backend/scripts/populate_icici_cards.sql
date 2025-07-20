-- ICICI Bank Credit Cards Population Script
-- Generated: December 2024
-- Total Cards: 5 (Simplified Version)

BEGIN;

-- 1. ICICI Bank Amazon Pay Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, reward_program_name, reward_expiry_period,
    minimum_redemption_points, is_active, is_available_online,
    description, additional_features
) VALUES (
    'ICICI Bank', 'Amazon Pay Credit Card', 'Co-branded', 'Mastercard', 'basic',
    499, 499, false, 50000,
    3.5, 500, 3.5,
    0, 0,
    2000, 300000, 21, 65,
    true, true,
    '{"personal_accident": 200000}',
    'Amazon Pay Rewards', 24, 1000,
    true, true,
    'Co-branded credit card offering enhanced rewards on Amazon purchases',
    '{"amazon_cashback": "5%", "fuel_surcharge_waiver": true}'
);

-- 2. ICICI Bank Sapphiro Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service, reward_program_name,
    reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description, additional_features
) VALUES (
    'ICICI Bank', 'Sapphiro Credit Card', 'Premium', 'Visa', 'premium',
    3500, 3500, false, 400000,
    2.5, 750, 3.0,
    12, 0,
    15000, 800000, 21, 65,
    true, true,
    '{"travel_insurance": 5000000}',
    true, 'Reward Points', 36, 1000,
    true, true,
    'Premium lifestyle credit card with lounge access',
    '{"golf_benefits": true, "dining_discounts": "25%"}'
);

-- 3. ICICI Bank Coral Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, reward_program_name, reward_expiry_period,
    minimum_redemption_points, is_active, is_available_online,
    description, additional_features
) VALUES (
    'ICICI Bank', 'Coral Credit Card', 'Mid-Premium', 'Visa', 'mid_premium',
    1500, 1500, false, 200000,
    3.0, 600, 3.25,
    6, 0,
    5000, 500000, 21, 65,
    true, true,
    '{"air_accident": 1000000}',
    'Reward Points', 36, 1000,
    true, true,
    'Balanced premium card with travel benefits',
    '{"fuel_surcharge_waiver": "2.5%", "movie_discounts": true}'
);

-- 4. ICICI Bank Emeralde Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service, reward_program_name,
    reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description, additional_features
) VALUES (
    'ICICI Bank', 'Emeralde Credit Card', 'Super Premium', 'Visa Infinite', 'super_premium',
    12000, 12000, false, 1000000,
    1.5, 1000, 2.5,
    999, 999,
    100000, 2500000, 25, 65,
    true, true,
    '{"travel_insurance": 10000000}',
    true, 'Reward Points', 36, 1000,
    true, true,
    'Ultra-premium card with unlimited lounge access',
    '{"unlimited_lounge": true, "priority_services": true}'
);

-- 5. ICICI Bank Platinum Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, reward_program_name, reward_expiry_period,
    minimum_redemption_points, is_active, is_available_online,
    description, additional_features
) VALUES (
    'ICICI Bank', 'Platinum Credit Card', 'Standard', 'Visa', 'basic',
    750, 750, false, 100000,
    3.5, 500, 3.5,
    2, 0,
    2500, 400000, 21, 65,
    true, true,
    '{"personal_accident": 500000}',
    'Reward Points', 36, 1000,
    true, true,
    'Everyday rewards card with basic benefits',
    '{"fuel_surcharge_waiver": true, "weekend_bonuses": true}'
);

-- Note: spending_categories and merchant_rewards tables will be added later if needed

COMMIT;