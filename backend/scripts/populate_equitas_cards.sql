-- Equitas Small Finance Bank Credit Cards Population Script
-- Small finance bank focusing on underserved segments
-- Total: 8 cards focusing on inclusive financial services

DELETE FROM card_master_data WHERE bank_name = 'Equitas Small Finance Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Entry Level Inclusive Banking Cards
('Equitas Small Finance Bank', 'Equitas Easy Credit Card', 'Easy Access', 'RuPay', 'Standard',
NULL, 199, 200000, 21, 70,
0, 0, TRUE, 20000, 300000,
1.0, 'Affordable credit card targeting underserved segments with low fees', TRUE),

('Equitas Small Finance Bank', 'Equitas Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 500, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with basic benefits for small finance customers', TRUE),

-- Mid-Tier Cards
('Equitas Small Finance Bank', 'Equitas Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 700000,
3.5, 'Enhanced credit card with additional benefits for growing customers', TRUE),

('Equitas Small Finance Bank', 'Equitas Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 2500, 600000, 21, 70,
3, 3, TRUE, 60000, 1000000,
3.5, 'Premium credit card with comprehensive benefits for successful customers', TRUE),

-- Specialized Cards
('Equitas Small Finance Bank', 'Equitas Business Credit Card', 'Business', 'Visa', 'Business',
2000, 2000, 500000, 25, 70,
2, 2, TRUE, 100000, 800000,
3.5, 'Business credit card designed for small business owners and micro-enterprises', TRUE),

('Equitas Small Finance Bank', 'Equitas Women Credit Card', 'Women Empowerment', 'RuPay', 'Standard',
NULL, 299, 250000, 21, 70,
1, 0, TRUE, 25000, 400000,
1.0, 'Special credit card for women empowerment with exclusive benefits', TRUE),

-- Digital Innovation Cards
('Equitas Small Finance Bank', 'Equitas Digital Credit Card', 'Digital First', 'Visa', 'Standard',
NULL, 299, 250000, 21, 45,
1, 0, TRUE, 25000, 400000,
3.5, 'Digital-native credit card with instant approval and mobile-first features', TRUE),

-- Premium Offering
('Equitas Small Finance Bank', 'Equitas Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 5000, 1000000, 25, 70,
4, 6, TRUE, 150000, 2000000,
3.5, 'Premium signature card for high-income customers in small finance segment', TRUE);