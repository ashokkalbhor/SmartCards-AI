-- Kotak Mahindra Bank Credit Cards Population Script
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
('Kotak Mahindra Bank', '811 Credit Card', 'Digital-First', 'Mastercard', 'Standard', 500.0, 0.0, 21, 65, 200000.0, 0, 3.25, 450.0, 1, 1, 0, 0, 1000.0, 50000.0, 500000.0, '{"type": "Basic", "coverage": "Rs. 5 lakh personal accident"}', 0),
('Kotak Mahindra Bank', 'Zen Credit Card', 'Lifestyle', 'Visa', 'Premium', 1000.0, 1000.0, 21, 65, 350000.0, 0, 3.0, 550.0, 1, 1, 4, 0, 5000.0, 100000.0, 800000.0, '{"type": "Health & Wellness", "coverage": "Health and wellness insurance"}', 0),
('Kotak Mahindra Bank', 'White Credit Card', 'Premium', 'Visa', 'Premium', 2500.0, 2500.0, 21, 65, 600000.0, 0, 2.25, 700.0, 1, 1, 8, 2, 25000.0, 200000.0, 2000000.0, '{"type": "Premium", "coverage": "Premium travel and lifestyle insurance"}', 1),
('Kotak Mahindra Bank', 'League Credit Card', 'Sports-Lifestyle', 'Mastercard', 'Premium', 1500.0, 1500.0, 21, 65, 450000.0, 0, 3.0, 600.0, 1, 1, 6, 0, 8000.0, 150000.0, 1200000.0, '{"type": "Sports", "coverage": "Sports accident and fitness injury coverage"}', 0),
('Kotak Mahindra Bank', 'Platinum Credit Card', 'Standard', 'Visa', 'Standard', 750.0, 750.0, 21, 65, 300000.0, 0, 3.5, 500.0, 1, 1, 3, 0, 2000.0, 75000.0, 600000.0, '{"type": "Basic", "coverage": "Basic personal accident and purchase protection"}', 0),
('Kotak Mahindra Bank', 'Royale Credit Card', 'Super-Premium', 'Visa', 'Super-Premium', 10000.0, 10000.0, 25, 65, 2000000.0, 0, 1.75, 1000.0, 1, 1, 999, 999, 150000.0, 1000000.0, 10000000.0, '{"type": "Ultra-Premium", "coverage": "Travel Rs. 75 lakh, medical Rs. 25 lakh"}', 1),
('Kotak Mahindra Bank', 'Privy Credit Card', 'Invitation-Only', 'Mastercard', 'Super-Premium', 25000.0, 25000.0, 30, 65, 5000000.0, 0, 1.5, 1500.0, 1, 1, 999, 999, 500000.0, 2000000.0, 50000000.0, '{"type": "Invitation-Only", "coverage": "Comprehensive luxury coverage"}', 1),
('Kotak Mahindra Bank', 'Urbane Credit Card', 'Urban-Lifestyle', 'Visa', 'Premium', 1200.0, 1200.0, 21, 65, 400000.0, 0, 2.75, 550.0, 1, 1, 5, 1, 6000.0, 120000.0, 1000000.0, '{"type": "Urban Lifestyle", "coverage": "Urban lifestyle and travel insurance"}', 0),
('Kotak Mahindra Bank', 'Essentials Credit Card', 'Basic', 'RuPay', 'Basic', 199.0, 199.0, 18, 65, 150000.0, 0, 3.75, 350.0, 1, 1, 0, 0, 500.0, 25000.0, 200000.0, '{"type": "Basic", "coverage": "Basic purchase protection"}', 0),
('Kotak Mahindra Bank', 'Business Credit Card', 'Business', 'Visa', 'Business', 2000.0, 2000.0, 21, 70, 500000.0, 0, 2.5, 750.0, 1, 1, 4, 2, 10000.0, 200000.0, 5000000.0, '{"type": "Business", "coverage": "Business insurance and fraud protection"}', 0);