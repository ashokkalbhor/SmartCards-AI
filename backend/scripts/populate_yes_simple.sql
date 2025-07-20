-- YES Bank Credit Cards Population Script
-- Simplified version matching database schema

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    annual_fee, joining_fee, minimum_age, maximum_age, minimum_salary,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, domestic_lounge_visits,
    international_lounge_visits, welcome_bonus_points,
    minimum_credit_limit, maximum_credit_limit, insurance_benefits,
    concierge_service
) VALUES
('YES Bank', 'Marquee Credit Card', 'Super-Premium', 'Visa', 'Super-Premium', 4999.0, 9999.0, 21, 60, 3600000.0, 0, 1.0, 1350.0, 1, 1, 24, 999, 40000.0, 500000.0, 5000000.0, '{"type": "Premium", "coverage": "Credit shield Rs. 15 lakh, purchase protection Rs. 50,000"}', 1),
('YES Bank', 'Prosperity Credit Card', 'Premium', 'Visa', 'Premium', 2999.0, 2999.0, 21, 60, 1200000.0, 0, 2.5, 750.0, 1, 1, 12, 0, 15000.0, 200000.0, 2000000.0, '{"type": "Premium", "coverage": "Travel insurance Rs. 25 lakh, personal accident Rs. 10 lakh"}', 1),
('YES Bank', 'Wellness Credit Card', 'Lifestyle-Health', 'Mastercard', 'Premium', 1999.0, 1999.0, 21, 60, 600000.0, 0, 2.75, 650.0, 1, 1, 6, 0, 8000.0, 150000.0, 1200000.0, '{"type": "Health & Wellness", "coverage": "Health insurance top-up Rs. 5 lakh"}', 0),
('YES Bank', 'First Exclusive Credit Card', 'Premium-Exclusive', 'Visa', 'Super-Premium', 5999.0, 5999.0, 25, 65, 1800000.0, 0, 1.5, 900.0, 1, 1, 16, 8, 50000.0, 300000.0, 3000000.0, '{"type": "Exclusive", "coverage": "Travel insurance Rs. 50 lakh, luxury lifestyle protection"}', 1),
('YES Bank', 'Premia Credit Card', 'Mid-Premium', 'Visa', 'Premium', 1499.0, 1499.0, 21, 60, 500000.0, 0, 2.75, 650.0, 1, 1, 8, 0, 8000.0, 120000.0, 1000000.0, '{"type": "Premium", "coverage": "Travel insurance Rs. 15 lakh, personal accident Rs. 8 lakh"}', 0),
('YES Bank', 'Kisan Credit Card', 'Agricultural', 'RuPay', 'Basic', 500.0, 0.0, 21, 70, 100000.0, 0, 3.5, 400.0, 1, 1, 0, 0, 3000.0, 25000.0, 300000.0, '{"type": "Agricultural", "coverage": "Crop insurance and agricultural accident coverage"}', 0),
('YES Bank', 'Business Credit Card', 'Business', 'Visa', 'Business', 2500.0, 2500.0, 21, 70, 800000.0, 0, 2.25, 800.0, 1, 1, 6, 2, 12000.0, 250000.0, 8000000.0, '{"type": "Business", "coverage": "Business insurance and comprehensive fraud protection"}', 1),
('YES Bank', 'Ace Credit Card', 'Cashback', 'Mastercard', 'Standard', 999.0, 999.0, 21, 65, 300000.0, 0, 3.0, 500.0, 1, 1, 2, 0, 5000.0, 80000.0, 800000.0, '{"type": "Cashback", "coverage": "Basic personal accident and purchase protection"}', 0); 