-- IDFC FIRST Bank Credit Cards Population Script
-- Modern digital-first private bank with innovative credit cards
-- Total: 14 cards covering digital innovation and modern banking

DELETE FROM card_master_data WHERE bank_name = 'IDFC FIRST Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Entry Level Cards
('IDFC FIRST Bank', 'FIRST Freedom Credit Card', 'Freedom', 'Visa', 'Standard',
NULL, NULL, 200000, 21, 70,
0, 0, TRUE, 20000, 500000,
3.5, 'Lifetime free credit card with no annual fee and basic benefits', TRUE),

('IDFC FIRST Bank', 'FIRST Classic Credit Card', 'Classic', 'Visa', 'Standard',
499, 499, 300000, 21, 70,
1, 0, TRUE, 30000, 600000,
3.5, 'Entry-level credit card with essential benefits and rewards', TRUE),

-- Mid-Tier Cards
('IDFC FIRST Bank', 'FIRST Millenia Credit Card', 'Millenia', 'Visa', 'Premium',
1000, 1000, 400000, 21, 70,
1, 2, TRUE, 40000, 800000,
3.5, 'Millennial-focused card with digital lifestyle benefits', TRUE),

('IDFC FIRST Bank', 'FIRST Select Credit Card', 'Select', 'Visa', 'Premium',
2500, 2500, 600000, 21, 70,
2, 4, TRUE, 60000, 1000000,
3.5, 'Premium credit card with enhanced travel and dining benefits', TRUE),

-- Premium Cards
('IDFC FIRST Bank', 'FIRST Wealth Credit Card', 'Wealth', 'Visa', 'Premium',
10000, 10000, 1500000, 25, 70,
6, 12, TRUE, 200000, 3000000,
3.5, 'High-net-worth individuals card with exclusive wealth management benefits', TRUE),

('IDFC FIRST Bank', 'FIRST Private Credit Card', 'Private', 'Visa', 'Ultra-Premium',
50000, 50000, 3000000, 25, 70,
12, 24, TRUE, 500000, 10000000,
3.5, 'Ultra-premium private banking card with unlimited privileges', TRUE),

-- Specialized Cards
('IDFC FIRST Bank', 'FIRST Business Credit Card', 'Business', 'Visa', 'Business',
5000, 5000, 800000, 25, 70,
4, 6, TRUE, 150000, 2000000,
3.5, 'Business credit card with comprehensive corporate benefits', TRUE),

('IDFC FIRST Bank', 'FIRST Student Credit Card', 'Student', 'Visa', 'Standard',
NULL, 199, 150000, 18, 30,
0, 0, TRUE, 15000, 200000,
3.5, 'Student credit card with educational benefits and low fees', TRUE),

-- Co-branded Cards
('IDFC FIRST Bank', 'FIRST Club Vistara Credit Card', 'Co-branded Travel', 'Visa', 'Premium',
2500, 2500, 600000, 21, 70,
2, 4, TRUE, 60000, 1000000,
3.5, 'Co-branded travel card with Vistara airline benefits and miles', TRUE),

('IDFC FIRST Bank', 'FIRST Swiggy Credit Card', 'Co-branded Food', 'Visa', 'Standard',
500, 500, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Food delivery focused co-branded card with Swiggy benefits', TRUE),

-- Digital Innovation Cards
('IDFC FIRST Bank', 'FIRST Digital Credit Card', 'Digital', 'Visa', 'Standard',
NULL, 299, 250000, 21, 45,
1, 0, TRUE, 25000, 500000,
3.5, 'Digital-first card with instant approval and virtual card features', TRUE),

('IDFC FIRST Bank', 'FIRST Contactless Credit Card', 'Contactless', 'Visa', 'Standard',
299, 299, 300000, 21, 70,
0, 0, TRUE, 30000, 600000,
3.5, 'Contactless payment focused card with NFC technology', TRUE),

-- Cashback Cards
('IDFC FIRST Bank', 'FIRST Cashback Credit Card', 'Cashback', 'Visa', 'Standard',
500, 500, 350000, 21, 70,
0, 0, TRUE, 35000, 700000,
3.5, 'Cashback focused card with straightforward rewards program', TRUE),

-- Fuel Card
('IDFC FIRST Bank', 'FIRST Fuel Credit Card', 'Fuel Focused', 'Visa', 'Standard',
750, 750, 400000, 21, 70,
1, 0, TRUE, 40000, 800000,
3.5, 'Fuel-focused card with enhanced benefits at petrol pumps', TRUE);