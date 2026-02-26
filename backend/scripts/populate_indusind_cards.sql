-- IndusInd Bank Credit Cards Population Script
-- Comprehensive script for populating 11 IndusInd Bank credit cards

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    annual_fee, joining_fee, minimum_age, maximum_age, minimum_salary,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, domestic_lounge_visits,
    international_lounge_visits, welcome_bonus_points,
    minimum_credit_limit, maximum_credit_limit, insurance_benefits,
    concierge_service
) VALUES
('IndusInd Bank', 'Platinum RuPay Credit Card', 'Entry-Level', 'RuPay', 'Standard', 0.0, 0.0, 18, 65, 200000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 1000.0, 50000.0, 500000.0, '{"type": "Basic", "coverage": "Air accident Rs. 25 lakh"}', 0),

('IndusInd Bank', 'Legend Credit Card', 'Entry-Level', 'Visa', 'Standard', 0.0, 0.0, 21, 65, 250000.0, 1, 1.8, 500.0, 1, 1, 2, 0, 2000.0, 75000.0, 800000.0, '{"type": "Travel", "coverage": "Lost baggage, travel assistance"}', 1),

('IndusInd Bank', 'EazyDiner Platinum Credit Card', 'Dining-Focused', 'Visa', 'Standard', 0.0, 0.0, 21, 65, 300000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 500.0, 100000.0, 1000000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0),

('IndusInd Bank', 'Platinum Aura Edge Credit Card', 'Lifestyle', 'Visa', 'Standard', 0.0, 0.0, 21, 65, 250000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 1500.0, 75000.0, 800000.0, '{"type": "Comprehensive", "coverage": "Air accident Rs. 25 lakh, travel insurance"}', 0),

('IndusInd Bank', 'Platinum Visa Credit Card', 'Basic', 'Visa', 'Standard', 0.0, 0.0, 18, 65, 200000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 750.0, 50000.0, 500000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0),

('IndusInd Bank', 'Tiger Credit Card', 'Premium-Lifestyle', 'Visa', 'Premium', 0.0, 0.0, 21, 60, 500000.0, 1, 1.5, 750.0, 1, 1, 8, 8, 5000.0, 200000.0, 2000000.0, '{"type": "Premium", "coverage": "Air accident Rs. 1 crore, travel insurance"}', 1),

('IndusInd Bank', 'Samman RuPay Credit Card', 'Government-Employee', 'RuPay', 'Standard', 199.0, 0.0, 21, 65, 250000.0, 0, 3.5, 450.0, 1, 1, 0, 0, 1000.0, 100000.0, 800000.0, '{"type": "Basic", "coverage": "Air accident Rs. 10 lakh"}', 0),

('IndusInd Bank', 'Pinnacle Credit Card', 'Premium', 'Mastercard', 'Premium', 0.0, 14999.0, 25, 60, 800000.0, 0, 3.5, 750.0, 1, 1, 4, 0, 10000.0, 300000.0, 3000000.0, '{"type": "Premium", "coverage": "Air accident Rs. 1 crore, travel insurance"}', 1),

('IndusInd Bank', 'Nexxt Credit Card', 'Interactive-Premium', 'Visa', 'Premium', 0.0, 10000.0, 23, 60, 600000.0, 0, 3.5, 750.0, 1, 1, 2, 0, 5000.0, 250000.0, 2500000.0, '{"type": "Premium", "coverage": "Air accident Rs. 50 lakh, travel insurance"}', 1),

('IndusInd Bank', 'EazyDiner Credit Card', 'Premium-Dining', 'Visa', 'Premium', 2999.0, 2999.0, 25, 60, 1000000.0, 0, 3.5, 1000.0, 1, 1, 8, 0, 10000.0, 400000.0, 4000000.0, '{"type": "Premium", "coverage": "Air accident Rs. 1 crore, comprehensive travel insurance"}', 1),

('IndusInd Bank', 'Avios Visa Infinite Credit Card', 'Super-Premium-Travel', 'Visa', 'Super-Premium', 5000.0, 10000.0, 25, 60, 3600000.0, 0, 1.5, 1500.0, 1, 1, 8, 8, 25000.0, 500000.0, 10000000.0, '{"type": "Premium", "coverage": "Air accident Rs. 60 lakh, comprehensive travel insurance"}', 1); 