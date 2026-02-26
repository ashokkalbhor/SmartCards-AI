-- Standard Chartered Bank Credit Cards Population Script
-- Comprehensive script for populating 11 Standard Chartered cards

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    annual_fee, joining_fee, minimum_age, maximum_age, minimum_salary,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, domestic_lounge_visits,
    international_lounge_visits, welcome_bonus_points,
    minimum_credit_limit, maximum_credit_limit, insurance_benefits,
    concierge_service
) VALUES
('Standard Chartered Bank', 'Platinum Rewards Credit Card', 'Entry-Level', 'Visa', 'Standard', 0.0, 250.0, 18, 65, 200000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 500.0, 50000.0, 500000.0, '{"type": "Basic", "coverage": "Personal accident insurance"}', 0),

('Standard Chartered Bank', 'Smart Credit Card', 'Digital', 'Mastercard', 'Standard', 499.0, 499.0, 18, 65, 250000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 1000.0, 75000.0, 750000.0, '{"type": "Basic", "coverage": "Zero liability protection"}', 0),

('Standard Chartered Bank', 'Rewards Credit Card', 'Shopping', 'Mastercard', 'Gold', 1000.0, 0.0, 18, 65, 300000.0, 0, 3.5, 700.0, 1, 1, 4, 0, 2000.0, 100000.0, 1000000.0, '{"type": "Enhanced", "coverage": "Purchase protection and zero liability"}', 0),

('Standard Chartered Bank', 'EaseMyTrip Credit Card', 'Travel', 'Mastercard', 'Gold', 350.0, 350.0, 18, 65, 350000.0, 0, 3.5, 500.0, 1, 1, 2, 0, 1500.0, 100000.0, 800000.0, '{"type": "Travel", "coverage": "Travel accident insurance"}', 0),

('Standard Chartered Bank', 'Super Value Titanium Credit Card', 'Cashback', 'Visa', 'Gold', 750.0, 750.0, 18, 65, 400000.0, 0, 3.5, 700.0, 1, 1, 2, 2, 2000.0, 125000.0, 1000000.0, '{"type": "Comprehensive", "coverage": "Zero liability and fraud protection"}', 0),

('Standard Chartered Bank', 'Ultimate Credit Card', 'Premium', 'Visa', 'Platinum', 5000.0, 5000.0, 21, 65, 1200000.0, 0, 2.0, 1200.0, 1, 1, 12, 24, 6000.0, 300000.0, 3000000.0, '{"type": "Premium", "coverage": "Rs. 1 crore air accident, USD 25,000 medical"}', 1),

('Standard Chartered Bank', 'Priority Visa Infinite Credit Card', 'Super-Premium', 'Visa', 'Super-Premium', 0.0, 0.0, 25, 65, 2500000.0, 1, 3.5, 1200.0, 1, 1, 16, 48, 10000.0, 500000.0, 5000000.0, '{"type": "Premium", "coverage": "Rs. 1.2 crore air accident, USD 25,000 medical"}', 1),

('Standard Chartered Bank', 'Manhattan Credit Card', 'Shopping', 'Mastercard', 'Gold', 999.0, 999.0, 18, 65, 500000.0, 0, 3.5, 700.0, 1, 1, 0, 0, 5000.0, 150000.0, 1200000.0, '{"type": "Enhanced", "coverage": "Purchase protection and zero liability"}', 0),

('Standard Chartered Bank', 'Emirates World Credit Card', 'Travel', 'Mastercard', 'Platinum', 3000.0, 3000.0, 21, 65, 800000.0, 0, 3.5, 1000.0, 1, 1, 4, 8, 4000.0, 200000.0, 2000000.0, '{"type": "Travel", "coverage": "Rs. 1 crore air accident insurance"}', 1),

('Standard Chartered Bank', 'DigiSmart Credit Card', 'Digital', 'Mastercard', 'Standard', 588.0, 49.0, 18, 65, 250000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 1000.0, 75000.0, 600000.0, '{"type": "Basic", "coverage": "Online fraud protection"}', 0),

('Standard Chartered Bank', 'Business Credit Card', 'Business', 'Mastercard', 'Gold', 1500.0, 1500.0, 21, 65, 600000.0, 0, 3.5, 800.0, 1, 1, 2, 0, 3000.0, 200000.0, 1500000.0, '{"type": "Business", "coverage": "Business insurance and fraud protection"}', 0); 