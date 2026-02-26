-- SBI Card Credit Cards Master Data Population Script
-- Generated with comprehensive details from official sources and research
-- SBI Card is India's second-largest credit card issuer with 20+ million cards

BEGIN;

-- Insert SBI Credit Cards into card_master_data table

-- 1. SBI ELITE Credit Card (Flagship Premium Card)
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
    'SBI Card', 'ELITE Credit Card', 'Premium', 'Visa/Mastercard', 'super_premium',
    4999, 4999, false, 500000,
    3.5, 500, 2.5,
    12, 8,
    5000, 100000,
    100000, 21, 65,
    true, true,
    '{"accidental_death_cover": 5000000, "emergency_hospitalization": 1000000, "credit_liability_cover": 500000}', true,
    '{"movie_vouchers": 2000, "dining_vouchers": 2000, "wellness_vouchers": 2000}',
    'Reward Points', 36, 1000,
    true, true, 'Premium lifestyle credit card with comprehensive movie, dining and wellness benefits',
    '{"movie_benefits": true, "dining_discounts": true, "wellness_benefits": true, "concierge_24x7": true, "golf_privileges": true}'
);

-- 2. SBI PULSE Credit Card (Lifestyle Focus)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    milestone_benefits,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'SBI Card', 'PULSE Credit Card', 'Standard', 'Visa/Mastercard', 'premium',
    1499, 1499, false, 200000,
    3.5, 500, 2.5,
    4, 2,
    1000, 40000, 21, 65,
    true, true,
    '{"movie_vouchers": 1000, "dining_benefits": true}',
    'Reward Points', 36, 1000,
    true, true, 'Lifestyle credit card with movie and dining benefits for young professionals',
    '{"movie_benefits": true, "dining_rewards": true, "entertainment_focused": true, "youth_oriented": true}'
);

-- 3. SBI PRIME Credit Card (High Reward Rate)
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
    'SBI Card', 'PRIME Credit Card', 'Standard', 'Visa/Mastercard', 'premium',
    2999, 2999, false, 300000,
    3.5, 500, 2.5,
    8, 4,
    3000, 50000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'High reward rate credit card with accelerated points on all spends',
    '{"high_reward_rate": true, "accelerated_points": true, "lounge_access": true, "fuel_surcharge_waiver": true}'
);

-- 4. SBI Cashback Credit Card (Cashback Focus)
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
    'SBI Card', 'Cashback Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    999, 999, false, 100000,
    3.5, 500, 2.5,
    0, 0,
    500, 35000, 21, 65,
    true, true,
    'Cashback', 12, 500,
    true, true, 'Straightforward cashback credit card with rewards on online spends',
    '{"cashback_rewards": true, "online_shopping": true, "fuel_surcharge_waiver": true, "emi_conversion": true}'
);

-- 5. SBI SimplyCLICK Credit Card (Online Shopping)
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
    'SBI Card', 'SimplyCLICK Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    499, 499, false, 100000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Online shopping focused credit card with accelerated rewards on e-commerce',
    '{"online_shopping": true, "ecommerce_rewards": true, "digital_focused": true, "entry_level": true}'
);

-- 6. SBI SimplySAVE Credit Card (Savings & Rewards)
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
    'SBI Card', 'SimplySAVE Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    499, 499, false, 100000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Value-oriented credit card with rewards on groceries, dining and fuel',
    '{"grocery_rewards": true, "dining_rewards": true, "fuel_rewards": true, "everyday_savings": true}'
);

-- 7. SBI BPCL Credit Card (Fuel Focused)
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
    'SBI Card', 'BPCL Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    499, 499, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded fuel credit card with high rewards on BPCL fuel stations',
    '{"fuel_rewards": true, "bpcl_benefits": true, "fuel_surcharge_waiver": true, "co_branded": true}'
);

-- 8. SBI IRCTC Credit Card (Railway Travel)
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
    'SBI Card', 'IRCTC SBI Card', 'Co-branded', 'Mastercard', 'basic',
    499, 499, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded railway travel credit card with IRCTC booking benefits',
    '{"railway_benefits": true, "irctc_rewards": true, "travel_insurance": true, "booking_convenience": true}'
);

-- 9. SBI Miles Elite Credit Card (Travel Rewards)
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, welcome_bonus_spend_requirement,
    minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'SBI Card', 'Miles Elite Credit Card', 'Premium', 'Visa/Mastercard', 'premium',
    2999, 2999, false, 300000,
    3.5, 500, 2.5,
    8, 4,
    3000, 100000,
    75000, 21, 65,
    true, true,
    '{"travel_insurance": true, "purchase_protection": true}', false,
    'Miles', 36, 1000,
    true, true, 'Travel-focused premium credit card with airline miles and travel benefits',
    '{"airline_miles": true, "travel_benefits": true, "lounge_access": true, "travel_insurance": true}'
);

-- 10. SBI Apollo Credit Card (Healthcare Focus)
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
    'SBI Card', 'Apollo SBI Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    999, 999, false, 100000,
    3.5, 500, 2.5,
    0, 0,
    1000, 35000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Healthcare-focused co-branded credit card with Apollo Hospitals benefits',
    '{"healthcare_benefits": true, "apollo_rewards": true, "medical_discounts": true, "health_checkups": true}'
);

-- 11. SBI Reliance Credit Card (Retail Shopping)
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
    'SBI Card', 'Reliance SBI Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    499, 499, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded retail shopping credit card with Reliance store benefits',
    '{"retail_benefits": true, "reliance_rewards": true, "shopping_discounts": true, "grocery_benefits": true}'
);

-- 12. SBI MAX Credit Card (Premium Lifestyle)
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
    'SBI Card', 'MAX Credit Card', 'Premium', 'Visa/Mastercard', 'premium',
    3999, 3999, false, 400000,
    3.5, 500, 2.5,
    6, 3,
    4000, 75000, 21, 65,
    true, true,
    '{"accidental_death_cover": 2000000, "emergency_hospitalization": 500000}',
    'Reward Points', 36, 1000,
    true, true, 'Premium lifestyle credit card with comprehensive rewards and insurance benefits',
    '{"premium_lifestyle": true, "comprehensive_insurance": true, "lounge_access": true, "concierge_service": true}'
);

COMMIT;

-- Insert spending categories for key SBI cards
BEGIN;

-- SBI ELITE Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 2.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'entertainment', 'Entertainment & Movies', 5.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'groceries', 'Groceries', 2.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

-- SBI PRIME Credit Card Categories (High reward rate)
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 3.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'PRIME Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 3.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'PRIME Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'fuel', 'Fuel', 3.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'PRIME Credit Card' AND bank_name = 'SBI Card';

-- SBI SimplyCLICK Categories (Online focused)
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 5.0, 'points', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'SimplyCLICK Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'SimplyCLICK Credit Card' AND bank_name = 'SBI Card';

COMMIT;

-- Insert merchant-specific rewards
BEGIN;

-- SBI ELITE Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'bookmyshow', 'BookMyShow', 'entertainment', 10.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'pvr_cinemas', 'PVR Cinemas', 'entertainment', 10.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'inox', 'INOX', 'entertainment', 10.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'ELITE Credit Card' AND bank_name = 'SBI Card';

-- SBI SimplyCLICK Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'amazon', 'Amazon', 'e-commerce', 5.0, 'points', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'SimplyCLICK Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'flipkart', 'Flipkart', 'e-commerce', 5.0, 'points', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'SimplyCLICK Credit Card' AND bank_name = 'SBI Card';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'myntra', 'Myntra', 'fashion', 5.0, 'points', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'SimplyCLICK Credit Card' AND bank_name = 'SBI Card';

-- SBI BPCL Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'bpcl', 'BPCL Fuel Stations', 'fuel', 13.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'BPCL Credit Card' AND bank_name = 'SBI Card';

COMMIT; 