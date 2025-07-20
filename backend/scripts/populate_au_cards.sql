-- AU Small Finance Bank Credit Cards Population Script
-- Growing small finance bank with modern credit card offerings
-- Total: 9 cards focusing on underserved segments and innovation

DELETE FROM card_master_data WHERE bank_name = 'AU Small Finance Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Entry Level Cards
('AU Small Finance Bank', 'AU Bank Altura Credit Card', 'Altura', 'Visa', 'Standard',
500, 500, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with basic benefits and reward earning', TRUE),

('AU Small Finance Bank', 'AU Bank Altura Plus Credit Card', 'Altura Plus', 'Visa', 'Standard',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 700000,
3.5, 'Enhanced entry-level card with additional benefits and lounge access', TRUE),

-- Mid-Tier Cards
('AU Small Finance Bank', 'AU Bank Zenith Credit Card', 'Zenith', 'Visa', 'Premium',
4999, 4999, 800000, 21, 70,
4, 4, TRUE, 80000, 1500000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

('AU Small Finance Bank', 'AU Bank Vetta Credit Card', 'Vetta', 'Visa', 'Premium',
7500, 7500, 1200000, 25, 70,
6, 8, TRUE, 150000, 2500000,
3.5, 'High-end premium card with exclusive privileges and concierge services', TRUE),

-- Co-branded Cards
('AU Small Finance Bank', 'AU Bank Airtel Credit Card', 'Co-branded Telecom', 'Visa', 'Standard',
500, 500, 350000, 21, 70,
1, 0, TRUE, 35000, 600000,
3.5, 'Telecom co-branded card with Airtel specific benefits and rewards', TRUE),

('AU Small Finance Bank', 'AU Bank Snapdeal Credit Card', 'Co-branded Shopping', 'Visa', 'Standard',
750, 750, 400000, 21, 70,
1, 0, TRUE, 40000, 700000,
3.5, 'E-commerce focused co-branded card with Snapdeal shopping benefits', TRUE),

-- Specialized Cards
('AU Small Finance Bank', 'AU Bank Business Credit Card', 'Business', 'Visa', 'Business',
2500, 2500, 600000, 25, 70,
2, 2, TRUE, 100000, 1000000,
3.5, 'Business credit card designed for small business owners and entrepreneurs', TRUE),

('AU Small Finance Bank', 'AU Bank Easy Credit Card', 'Easy Access', 'RuPay', 'Standard',
NULL, 199, 200000, 21, 70,
0, 0, TRUE, 20000, 300000,
1.0, 'Affordable credit card with low fees targeting underserved segments', TRUE),

-- Digital Innovation
('AU Small Finance Bank', 'AU Bank Digital Credit Card', 'Digital First', 'Visa', 'Standard',
NULL, 299, 250000, 21, 45,
1, 0, TRUE, 25000, 400000,
3.5, 'Digital-native credit card with instant approval and mobile-first features', TRUE);