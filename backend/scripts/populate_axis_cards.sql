-- Axis Bank Credit Cards Master Data Population Script
-- Generated with comprehensive details from official sources and research
-- Axis Bank offers a wide range from entry-level to ultra-premium cards

BEGIN;

-- Insert Axis Bank Credit Cards into card_master_data table

-- 1. Axis Bank NEO Credit Card (Entry Level)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'NEO Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    250, 250, false, 25000,
    3.5, 500, 2.5,
    0, 0,
    250, 25000, 18, 65,
    true, true,
    'EDGE Reward Points', 36, 500,
    true, true, 'Entry-level credit card with contactless payments and digital-first approach',
    '{"contactless_payments": true, "digital_first": true, "budget_friendly": true, "instant_approval": true}'
);

-- 2. Axis Bank My Zone Credit Card (Youth Focused)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'My Zone Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 18, 35,
    true, true,
    'EDGE Reward Points', 36, 500,
    true, true, 'Youth-oriented credit card with dining and shopping benefits',
    '{"youth_benefits": true, "dining_rewards": true, "shopping_benefits": true, "lifestyle_focused": true}'
);

-- 3. Axis Bank ACE Credit Card (Cashback Focus)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'ACE Credit Card', 'Standard', 'Visa/Mastercard', 'premium',
    500, 500, false, 200000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 18, 65,
    true, true,
    'Cashback', 12, 100,
    true, true, 'Cashback credit card with high rewards on bill payments and e-commerce',
    '{"cashback_focus": true, "bill_payments": true, "ecommerce_rewards": true, "utility_benefits": true}'
);

-- 4. Axis Bank Flipkart Credit Card (E-commerce)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Flipkart Credit Card', 'Co-branded', 'Mastercard', 'premium',
    500, 500, false, 200000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 18, 65,
    true, true,
    'EDGE Reward Points', 36, 500,
    true, true, 'Co-branded e-commerce credit card with Flipkart shopping benefits',
    '{"flipkart_benefits": true, "ecommerce_rewards": true, "co_branded": true, "shopping_focused": true}'
);

-- 5. Axis Bank Airtel Credit Card (Telecom Benefits)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Airtel Credit Card', 'Co-branded', 'Mastercard', 'premium',
    500, 500, false, 200000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 18, 65,
    true, true,
    'EDGE Reward Points', 36, 500,
    true, true, 'Co-branded telecom credit card with Airtel recharge and bill payment benefits',
    '{"airtel_benefits": true, "telecom_rewards": true, "utility_payments": true, "co_branded": true}'
);

-- 6. Axis Bank Select Credit Card (Mid-Premium)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Select Credit Card', 'Premium', 'Visa/Mastercard', 'premium',
    1500, 1500, false, 250000,
    3.5, 500, 2.5,
    4, 2,
    1500, 50000, 21, 65,
    true, true,
    '{"purchase_protection": true, "zero_lost_card_liability": true}',
    'EDGE Reward Points', 36, 500,
    true, true, 'Mid-premium credit card with lounge access and comprehensive rewards',
    '{"lounge_access": true, "premium_benefits": true, "travel_benefits": true, "dining_privileges": true}'
);

-- 7. Axis Bank Privilege Credit Card (Premium)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service,
    milestone_benefits,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Privilege Credit Card', 'Premium', 'Visa/Mastercard', 'premium',
    3500, 3500, false, 350000,
    2.0, 750, 2.5,
    8, 4,
    3500, 75000, 21, 65,
    true, true,
    '{"travel_insurance": true, "purchase_protection": true, "emergency_assistance": true}', true,
    '{"milestone_rewards": 5000, "quarterly_benefits": 2000}',
    'EDGE Reward Points', 36, 500,
    true, true, 'Premium credit card with enhanced travel benefits and concierge services',
    '{"premium_travel": true, "concierge_service": true, "golf_privileges": true, "priority_customer_service": true}'
);

-- 8. Axis Bank Magnus Credit Card (Super Premium)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, welcome_bonus_spend_requirement,
    minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service,
    milestone_benefits,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Magnus Credit Card', 'Metal', 'Mastercard', 'super_premium',
    12500, 12500, false, 1500000,
    2.0, 1000, 2.5,
    999, 999,
    25000, 100000,
    150000, 21, 65,
    true, true,
    '{"travel_insurance": 50000000, "purchase_protection": true, "emergency_assistance": true, "golf_insurance": true}', true,
    '{"annual_fee_waiver": 1500000, "monthly_milestone": 25000, "quarterly_benefits": 10000}',
    'EDGE Reward Points', 36, 500,
    true, true, 'Ultra-premium metallic credit card with unlimited lounge access and luxury benefits',
    '{"metallic_card": true, "unlimited_lounge": true, "luxury_benefits": true, "concierge_24x7": true, "golf_privileges": true, "transfer_partners": true}'
);

-- 9. Axis Bank Reserve Credit Card (Ultra Premium)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, welcome_bonus_spend_requirement,
    minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service,
    milestone_benefits,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'Reserve Credit Card', 'Metal', 'Mastercard', 'super_premium',
    50000, 50000, false, 2500000,
    2.0, 1500, 2.5,
    999, 999,
    100000, 200000,
    300000, 25, 65,
    true, true,
    '{"travel_insurance": 100000000, "purchase_protection": true, "emergency_assistance": true, "personal_accident": 50000000}', true,
    '{"annual_benefits": 50000, "quarterly_vouchers": 15000, "luxury_experiences": true}',
    'EDGE Reward Points', 36, 500,
    false, true, 'Invitation-only ultra-premium metallic card with exclusive luxury benefits and experiences',
    '{"invitation_only": true, "ultra_premium": true, "luxury_experiences": true, "personal_relationship_manager": true, "exclusive_events": true}'
);

-- 10. Axis Bank IOCL Credit Card (Fuel Focus)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'Axis Bank', 'IOCL Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 18, 65,
    true, true,
    'EDGE Reward Points', 36, 500,
    true, true, 'Co-branded fuel credit card with IOCL petrol pump benefits and fuel rewards',
    '{"fuel_rewards": true, "iocl_benefits": true, "fuel_surcharge_waiver": true, "co_branded": true}'
);

COMMIT;

-- Insert spending categories for key Axis Bank cards
BEGIN;

-- Axis Bank ACE Credit Card Categories (Cashback focus)
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'bill_payments', 'Bill Payments & Utilities', 5.0, 'cashback', 200, 'monthly', true 
FROM card_master_data WHERE card_name = 'ACE Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 4.0, 'cashback', 200, 'monthly', true 
FROM card_master_data WHERE card_name = 'ACE Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.5, 'cashback', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ACE Credit Card' AND bank_name = 'Axis Bank';

-- Axis Bank Magnus Credit Card Categories (High reward)
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 6.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'travel', 'Travel', 6.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 6.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'international', 'International Spends', 6.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

-- Axis Bank NEO Credit Card Categories (Entry level)
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining & Restaurants', 2.0, 'points', 100, 'monthly', true 
FROM card_master_data WHERE card_name = 'NEO Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'NEO Credit Card' AND bank_name = 'Axis Bank';

COMMIT;

-- Insert merchant-specific rewards
BEGIN;

-- Axis Bank Flipkart Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'flipkart', 'Flipkart', 'e-commerce', 5.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Flipkart Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'myntra', 'Myntra', 'fashion', 4.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Flipkart Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'cleartrip', 'Cleartrip', 'travel', 4.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Flipkart Credit Card' AND bank_name = 'Axis Bank';

-- Axis Bank Airtel Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'airtel', 'Airtel', 'telecom', 25.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Airtel Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'airtel_digital_tv', 'Airtel Digital TV', 'entertainment', 25.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Airtel Credit Card' AND bank_name = 'Axis Bank';

-- Axis Bank IOCL Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'iocl', 'Indian Oil Petrol Pumps', 'fuel', 7.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'IOCL Credit Card' AND bank_name = 'Axis Bank';

-- Axis Bank Magnus Credit Card Premium Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'gyftr', 'Gyftr Gift Vouchers', 'gift-vouchers', 25.0, 'points', 50000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'grabdeals', 'GrabDeals', 'travel', 25.0, 'points', 50000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Magnus Credit Card' AND bank_name = 'Axis Bank';

COMMIT; 