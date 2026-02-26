-- Central Bank of India Credit Cards Population Script
-- Public sector bank with strong presence in western and central India
-- Total: 9 cards focusing on retail and agricultural banking

DELETE FROM card_master_data WHERE bank_name = 'Central Bank of India';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Portfolio
('Central Bank of India', 'Central Bank Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 750, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with essential benefits for retail customers', TRUE),

('Central Bank of India', 'Central Bank Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1500, 450000, 21, 70,
1, 0, TRUE, 45000, 750000,
3.5, 'Mid-tier credit card with enhanced benefits and reward programs', TRUE),

('Central Bank of India', 'Central Bank Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 3500, 650000, 21, 70,
2, 2, TRUE, 65000, 1200000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

-- RuPay Cards
('Central Bank of India', 'Central Bank RuPay Classic', 'RuPay Classic', 'RuPay', 'Standard',
NULL, NULL, 200000, 21, 70,
0, 0, TRUE, 20000, 300000,
1.0, 'Lifetime free RuPay card with domestic focus and basic benefits', TRUE),

('Central Bank of India', 'Central Bank RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
750, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 600000,
1.0, 'Premium RuPay card with lounge access and enhanced benefits', TRUE),

-- Specialized Cards
('Central Bank of India', 'Central Bank Business Credit Card', 'Business', 'Visa', 'Business',
3000, 5000, 600000, 25, 70,
3, 3, TRUE, 100000, 1500000,
3.5, 'Business credit card for commercial and agricultural enterprises', TRUE),

('Central Bank of India', 'Central Bank Kisan Credit Card', 'Agricultural', 'RuPay', 'Standard',
NULL, NULL, 150000, 18, 70,
0, 0, TRUE, 15000, 200000,
1.0, 'Specialized agricultural credit card for farmers and rural customers', TRUE),

-- Co-branded Cards
('Central Bank of India', 'Central Bank Fuel Credit Card', 'Fuel Co-branded', 'RuPay', 'Standard',
500, 750, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
1.0, 'Fuel-focused card with enhanced benefits at petrol outlets', TRUE),

-- Premium Card
('Central Bank of India', 'Central Bank Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
4, 6, TRUE, 150000, 2500000,
3.5, 'Premium signature card with exclusive privileges for high-income customers', TRUE);