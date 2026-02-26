-- HDFC Bank Credit Cards Master Data Population Script
-- Generated with comprehensive details from official sources and research

BEGIN;

-- Insert HDFC Bank Credit Cards into card_master_data table

-- 1. HDFC Bank Millennia Credit Card
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
    'HDFC Bank', 'Millennia Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    1000, 1000, false, 100000,
    3.5, 500, 2.5,
    4, 0,
    1000, 0,
    35000, 21, 65,
    true, true,
    '{}', false,
    'CashPoints', 24, 500,
    true, true, 'Best cashback credit card with 5% cashback on popular brands and 1% on all other spends',
    '{"fuel_surcharge_waiver": true, "emi_conversion": true, "milestone_benefits": true, "good_food_trail": true}'
);

-- 2. HDFC Bank MoneyBack+ Credit Card
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
    'HDFC Bank', 'MoneyBack+ Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 21, 60,
    true, true,
    'CashPoints', 24, 500,
    true, true, 'Entry-level cashback credit card with rewards on online spends and utility payments',
    '{"fuel_surcharge_waiver": true, "emi_conversion": true, "contactless_payments": true}'
);

-- 3. HDFC Bank Freedom Credit Card
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
    'HDFC Bank', 'Freedom Credit Card', 'Standard', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 21, 60,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Lifestyle-focused credit card with rewards on entertainment and dining',
    '{"fuel_surcharge_waiver": true, "emi_conversion": true, "lifestyle_benefits": true}'
);

-- 4. HDFC Bank Regalia Gold Credit Card
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
    'HDFC Bank', 'Regalia Gold Credit Card', 'Gold', 'Visa/Mastercard', 'premium',
    2500, 2500, false, 400000,
    2.0, 750, 2.5,
    12, 6,
    2500, 100000,
    75000, 21, 65,
    true, true,
    '{"accidental_death_cover": 10000000, "emergency_hospitalization": 1500000, "credit_liability_cover": 900000}', true,
    '{"quarterly_vouchers": 1500, "annual_flight_vouchers": 5000, "additional_flight_vouchers": 5000}',
    'Reward Points', 36, 1000,
    true, true, 'Premium travel and rewards credit card with exclusive memberships and lounge access',
    '{"club_vistara_silver": true, "mmt_black_elite": true, "priority_pass": true, "concierge_24x7": true}'
);

-- 5. HDFC Bank Regalia Credit Card
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
    'HDFC Bank', 'Regalia Credit Card', 'Standard', 'Visa/Mastercard', 'premium',
    2500, 2500, false, 300000,
    2.0, 750, 2.5,
    12, 6,
    0, 50000, 21, 65,
    true, true,
    '{"accidental_death_cover": 10000000, "emergency_hospitalization": 1500000, "credit_liability_cover": 900000}', false,
    '{"milestone_10k_points": 500000, "additional_5k_points": 800000}',
    'Reward Points', 36, 1000,
    true, true, 'Premium rewards credit card with excellent lounge access and dining benefits',
    '{"dineout_passport": true, "priority_pass": true, "good_food_trail": true}'
);

-- 6. HDFC Bank Infinia Credit Card
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
    'HDFC Bank', 'Infinia Credit Card', 'Metal Edition', 'Visa/Mastercard', 'super_premium',
    12500, 12500, false, 1000000,
    2.0, 1000, 2.5,
    999, 999,
    12500, 0,
    300000, 21, 65,
    true, true,
    '{"accidental_death_cover": 30000000, "emergency_hospitalization": 5000000, "credit_liability_cover": 900000}', true,
    '{"renewal_waiver": 1000000, "club_marriott": true, "itc_benefits": true}',
    'Reward Points', 36, 1000,
    true, true, 'Ultra-premium by-invitation-only metallic credit card with unlimited lounge access and concierge services',
    '{"metallic_card": true, "unlimited_lounge": true, "golf_privileges": true, "global_concierge": true, "club_marriott": true, "itc_hotels": true}'
);

-- 7. HDFC Bank Diners Club Privilege Credit Card
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
    'HDFC Bank', 'Diners Club Privilege Credit Card', 'Standard', 'Diners Club', 'premium',
    1000, 1000, false, 300000,
    3.5, 750, 2.5,
    8, 8,
    0, 50000, 21, 65,
    true, true,
    '{"accidental_death_cover": 5000000, "emergency_hospitalization": 1000000}', false,
    '{"quarterly_vouchers": 1500, "swiggy_one": true, "times_prime": true}',
    'Reward Points', 36, 1000,
    true, true, 'Premium Diners Club card with excellent dining rewards and lounge access',
    '{"bookmyshow_bogo": true, "swiggy_benefits": true, "smartbuy_rewards": true, "airmiles_transfer": true}'
);

-- 8. HDFC Bank Diners Club Black Credit Card
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
    'HDFC Bank', 'Diners Club Black Credit Card', 'Standard', 'Diners Club', 'super_premium',
    10000, 10000, false, 500000,
    2.0, 1000, 2.5,
    999, 999,
    10000, 0,
    200000, 21, 65,
    true, true,
    '{"accidental_death_cover": 20000000, "emergency_hospitalization": 3000000, "purchase_protection": 500000}', true,
    '{"club_marriott": true, "amazon_prime": true, "swiggy_one": true}',
    'Reward Points', 36, 1000,
    true, true, 'Super-premium Diners Club card with unlimited lounge access and premium benefits',
    '{"unlimited_lounge": true, "golf_privileges": true, "weekend_dining_2x": true, "smartbuy_10x": true}'
);

-- 9. HDFC Bank Diners Club Black Metal Edition
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
    'HDFC Bank', 'Diners Club Black Metal Edition', 'Metal', 'Diners Club', 'elite',
    10000, 10000, false, 800000,
    2.0, 1000, 2.5,
    999, 999,
    10000, 0,
    300000, 21, 65,
    true, true,
    '{"accidental_death_cover": 30000000, "emergency_hospitalization": 5000000, "purchase_protection": 1000000}', true,
    '{"metal_card": true, "club_marriott": true, "amazon_prime": true, "swiggy_one": true}',
    'Reward Points', 36, 1000,
    true, true, 'Elite metallic Diners Club card with premium privileges and unlimited access',
    '{"metallic_card": true, "unlimited_lounge": true, "golf_privileges": true, "concierge_24x7": true}'
);

-- 10. HDFC Bank PixEL Play Credit Card
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
    'HDFC Bank', 'PixEL Play Credit Card', 'Standard', 'RuPay', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 25000, 18, 35,
    true, true,
    'CashPoints', 24, 500,
    true, true, 'Digital-first RuPay credit card for young professionals with gaming and entertainment benefits',
    '{"digital_cashback": true, "gaming_benefits": true, "rupay_benefits": true, "young_professional": true}'
);

-- 11. HDFC Bank PixEL Go Credit Card
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
    'HDFC Bank', 'PixEL Go Credit Card', 'Standard', 'RuPay', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 20000, 18, 35,
    true, true,
    'CashPoints', 24, 500,
    true, true, 'Entry-level digital RuPay credit card with cashback on digital transactions',
    '{"digital_cashback": true, "rupay_benefits": true, "first_card": true, "mobile_first": true}'
);

-- 12. HDFC Bank IndianOil Credit Card
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
    'HDFC Bank', 'IndianOil HDFC Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded fuel credit card with special benefits at IndianOil petrol pumps',
    '{"fuel_benefits": true, "indianoil_rewards": true, "fuel_surcharge_waiver": true}'
);

-- 13. HDFC Bank Swiggy Credit Card
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
    'HDFC Bank', 'Swiggy HDFC Bank Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 21, 65,
    true, true,
    'CashPoints', 24, 500,
    true, true, 'Co-branded cashback credit card with special benefits on Swiggy orders and dining',
    '{"swiggy_benefits": true, "dining_cashback": true, "swiggy_one": true, "food_delivery": true}'
);

-- 14. HDFC Bank Tata Neu Infinity Credit Card
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
    'HDFC Bank', 'Tata Neu Infinity Credit Card', 'Co-branded', 'Visa/Mastercard/RuPay', 'premium',
    1500, 1500, false, 150000,
    3.5, 750, 2.5,
    6, 0,
    1500, 50000, 21, 65,
    true, true,
    'NeuCoins', 36, 1000,
    true, true, 'Co-branded rewards credit card with benefits across Tata ecosystem',
    '{"tata_neu_benefits": true, "ecosystem_rewards": true, "multi_network": true, "neucoins": true}'
);

-- 15. HDFC Bank IRCTC Credit Card
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
    'HDFC Bank', 'IRCTC HDFC Bank Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    4, 0,
    500, 30000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded travel credit card with special benefits for railway bookings',
    '{"irctc_benefits": true, "railway_booking": true, "travel_insurance": true, "lounge_access": true}'
);

-- 16. HDFC Bank RuPay Credit Card
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
    'HDFC Bank', 'HDFC RuPay Credit Card', 'Basic', 'RuPay', 'basic',
    0, 500, true, 25000,
    3.5, 400, 2.5,
    0, 0,
    0, 25000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Basic RuPay credit card with domestic benefits and government transaction advantages',
    '{"rupay_benefits": true, "government_payments": true, "domestic_focus": true, "ltf_available": true}'
);

-- 17. HDFC Bank Marriott Bonvoy Credit Card
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
    'HDFC Bank', 'Marriott Bonvoy HDFC Credit Card', 'Co-branded', 'Visa/Mastercard', 'premium',
    5000, 5000, false, 500000,
    2.0, 750, 2.5,
    6, 6,
    5000, 100000,
    100000, 21, 65,
    true, true,
    '{"travel_insurance": true, "purchase_protection": true}', false,
    'Marriott Bonvoy Points', 0, 3000,
    true, true, 'Co-branded travel credit card with Marriott hotel benefits and points',
    '{"marriott_bonvoy": true, "hotel_benefits": true, "travel_focused": true, "elite_status": true}'
);

-- 18. HDFC Bank Shoppers Stop Credit Card
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
    'HDFC Bank', 'Shoppers Stop HDFC Bank Credit Card', 'Co-branded', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded shopping credit card with special benefits at Shoppers Stop stores',
    '{"shoppers_stop_benefits": true, "shopping_rewards": true, "retail_focused": true, "fashion_benefits": true}'
);

-- 19. HDFC Bank Harley-Davidson Diners Club Card
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
    'HDFC Bank', 'HDFC Harley-Davidson Diners Club Card', 'Co-branded', 'Diners Club', 'premium',
    2500, 2500, false, 300000,
    3.5, 750, 2.5,
    8, 8,
    2500, 75000, 21, 65,
    true, true,
    'Reward Points', 36, 1000,
    true, true, 'Co-branded lifestyle credit card for Harley-Davidson enthusiasts with exclusive benefits',
    '{"harley_davidson_benefits": true, "lifestyle_focused": true, "biking_community": true, "exclusive_events": true}'
);

-- 20. HDFC Bank Doctor's Regalia Credit Card
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, is_lifetime_free, annual_fee_waiver_spend,
    foreign_transaction_fee, late_payment_fee, cash_advance_fee,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_salary, minimum_age, maximum_age,
    contactless_enabled, chip_enabled,
    insurance_benefits, concierge_service,
    reward_program_name, reward_expiry_period, minimum_redemption_points,
    is_active, is_available_online, description,
    additional_features
) VALUES (
    'HDFC Bank', 'Doctor''s Regalia Credit Card', 'Professional', 'Visa/Mastercard', 'premium',
    2500, 2500, false, 300000,
    2.0, 750, 2.5,
    12, 6,
    2500, 75000, 25, 65,
    true, true,
    '{"accidental_death_cover": 10000000, "emergency_hospitalization": 1500000, "professional_liability": 500000}', true,
    'Reward Points', 36, 1000,
    true, true, 'Professional credit card exclusively for medical practitioners with specialized benefits',
    '{"medical_professionals": true, "professional_liability": true, "healthcare_benefits": true, "priority_service": true}'
);

-- 21. HDFC Bank PIXEL Play Credit Card (Digital Card)
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
    'HDFC Bank', 'PIXEL Play Credit Card', 'Digital', 'Visa/Mastercard', 'basic',
    500, 500, false, 50000,
    3.5, 500, 2.5,
    0, 0,
    500, 30000, 18, 35,
    true, true,
    'Reward Points', 36, 500,
    true, true, 'Digital-first credit card with app-based management and customizable benefits for Gen Z',
    '{"digital_card": true, "app_based": true, "customizable_benefits": true, "gen_z_focused": true, "instant_digital_card": true}'
);

-- 22. HDFC Bank PIXEL Go Credit Card (Digital Card)
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
    'HDFC Bank', 'PIXEL Go Credit Card', 'Digital', 'Visa/Mastercard', 'basic',
    0, 0, true, 0,
    3.5, 500, 2.5,
    0, 0,
    0, 20000, 18, 30,
    true, true,
    'Reward Points', 36, 500,
    true, true, 'Lifetime free digital credit card for students and young professionals with instant approval',
    '{"lifetime_free": true, "digital_card": true, "student_friendly": true, "instant_approval": true, "zero_fees": true}'
);

-- 23. HDFC Bank Tata Neu Infinity Credit Card (Co-branded Premium)
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
    'HDFC Bank', 'Tata Neu Infinity Credit Card', 'Co-branded', 'Mastercard', 'super_premium',
    3500, 3500, false, 300000,
    2.0, 750, 2.5,
    6, 3,
    5000, 75000,
    75000, 21, 65,
    true, true,
    '{"travel_insurance": true, "purchase_protection": true, "emergency_assistance": true}', false,
    '{"tata_neu_coins": 5000, "quarterly_benefits": 3000, "milestone_rewards": 7500}',
    'Tata NeuCoins', 24, 100,
    true, true, 'Premium co-branded credit card with Tata ecosystem benefits and NeuCoins rewards',
    '{"tata_ecosystem": true, "neu_coins": true, "co_branded": true, "tata_brands": true, "lifestyle_benefits": true, "premium_rewards": true}'
);

COMMIT;

-- Insert spending categories for key cards
BEGIN;

-- Millennia Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'groceries', 'Groceries', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'travel', 'Travel', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'fuel', 'Fuel', 0.0, 'cashback', 0, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'entertainment', 'Entertainment', 1.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

-- Infinia Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'groceries', 'Groceries', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'travel', 'Travel', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'fuel', 'Fuel', 0.0, 'points', 0, 'monthly', true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'entertainment', 'Entertainment', 3.33, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Infinia Credit Card' AND bank_name = 'HDFC Bank';

-- PIXEL Play Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'entertainment', 'Entertainment & Streaming', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

-- PIXEL Go Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.0, 'points', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'PIXEL Go Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'online_shopping', 'Online Shopping', 1.5, 'points', 250, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Go Credit Card' AND bank_name = 'HDFC Bank';

-- Tata Neu Infinity Credit Card Categories
INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'general', 'General Spends', 1.5, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'tata_brands', 'Tata Brand Spends', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'dining', 'Dining', 2.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_spending_categories (card_master_id, category_name, category_display_name, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'travel', 'Travel', 2.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

COMMIT;

-- Insert merchant-specific rewards
BEGIN;

-- Millennia Credit Card Merchants (5% cashback)
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'amazon', 'Amazon', 'e-commerce', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'flipkart', 'Flipkart', 'e-commerce', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'swiggy', 'Swiggy', 'food-delivery', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'zomato', 'Zomato', 'food-delivery', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'myntra', 'Myntra', 'fashion', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'bookmyshow', 'BookMyShow', 'entertainment', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'uber', 'Uber', 'transportation', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'cult_fit', 'Cult.fit', 'fitness', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'sony_liv', 'Sony LIV', 'entertainment', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'tata_cliq', 'Tata CLiQ', 'e-commerce', 5.0, 'cashback', 1000, 'monthly', true 
FROM card_master_data WHERE card_name = 'Millennia Credit Card' AND bank_name = 'HDFC Bank';

-- PIXEL Play Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'netflix', 'Netflix', 'streaming', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'spotify', 'Spotify', 'streaming', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'zomato', 'Zomato', 'food-delivery', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'gaming_platforms', 'Gaming Platforms', 'gaming', 2.0, 'points', 500, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Play Credit Card' AND bank_name = 'HDFC Bank';

-- PIXEL Go Credit Card Merchants
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'amazon', 'Amazon', 'e-commerce', 1.5, 'points', 250, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Go Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'flipkart', 'Flipkart', 'e-commerce', 1.5, 'points', 250, 'monthly', true 
FROM card_master_data WHERE card_name = 'PIXEL Go Credit Card' AND bank_name = 'HDFC Bank';

-- Tata Neu Infinity Credit Card Merchants (Tata ecosystem)
INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'tata_cliq', 'Tata CLiQ', 'e-commerce', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'bigbasket', 'BigBasket', 'groceries', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'croma', 'Croma', 'electronics', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'westside', 'Westside', 'fashion', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'taj_hotels', 'Taj Hotels', 'travel', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'air_india', 'Air India', 'travel', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

INSERT INTO card_merchant_rewards (card_master_id, merchant_name, merchant_display_name, merchant_category, reward_rate, reward_type, reward_cap, reward_cap_period, is_active) 
SELECT id, 'tata_motors', 'Tata Motors', 'automotive', 5.0, 'neucoins', NULL, NULL, true 
FROM card_master_data WHERE card_name = 'Tata Neu Infinity Credit Card' AND bank_name = 'HDFC Bank';

COMMIT; 