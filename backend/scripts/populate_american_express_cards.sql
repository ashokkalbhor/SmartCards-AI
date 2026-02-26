-- American Express India Credit Cards and Charge Cards Population Script
-- Comprehensive script for populating 5 American Express cards (4 credit + 1 charge)

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    annual_fee, joining_fee, minimum_age, maximum_age, minimum_salary,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, domestic_lounge_visits,
    international_lounge_visits, welcome_bonus_points,
    minimum_credit_limit, maximum_credit_limit, insurance_benefits,
    concierge_service
) VALUES
('American Express', 'SmartEarn Credit Card', 'Entry-Level-Rewards', 'American Express', 'Standard', 495.0, 0.0, 18, 65, 450000.0, 0, 3.5, 600.0, 1, 1, 0, 0, 500.0, 50000.0, 800000.0, '{"type": "Basic", "coverage": "Zero lost card liability, purchase protection"}', 0),
('American Express', 'Membership Rewards Credit Card', 'Mid-Tier-Rewards', 'American Express', 'Premium', 1000.0, 1000.0, 18, 65, 600000.0, 0, 3.5, 750.0, 1, 1, 0, 0, 4000.0, 100000.0, 1500000.0, '{"type": "Enhanced", "coverage": "Zero lost card liability, purchase protection, extended warranty"}', 0),
('American Express', 'Platinum Travel Credit Card', 'Premium-Travel', 'American Express', 'Premium', 5000.0, 5000.0, 18, 65, 600000.0, 0, 3.5, 900.0, 1, 1, 8, 0, 10000.0, 200000.0, 3000000.0, '{"type": "Comprehensive", "coverage": "Travel insurance, zero lost card liability, purchase protection, extended warranty"}', 0),
('American Express', 'Platinum Reserve Credit Card', 'Super-Premium', 'American Express', 'Super-Premium', 10000.0, 10000.0, 18, 65, 600000.0, 0, 3.5, 1200.0, 1, 1, 999, 999, 11000.0, 500000.0, 5000000.0, '{"type": "Ultra-Premium", "coverage": "Comprehensive travel insurance, personal accident, purchase protection, extended warranty, concierge protection"}', 1),
('American Express', 'Centurion Charge Card', 'Invitation-Only-Charge', 'American Express', 'Ultra-Premium', 0.0, 0.0, 21, 70, 2500000.0, 0, 0.0, 0.0, 1, 1, 999, 999, 50000.0, 999999.0, 999999999.0, '{"type": "Ultimate", "coverage": "Comprehensive global coverage, personal concierge protection, emergency assistance worldwide"}', 1); 