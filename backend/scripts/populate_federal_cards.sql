-- Federal Bank Credit Cards Population Script
-- Well-established private bank with South Indian roots and modern approach
-- Total: 8 cards covering traditional and modern banking needs

DELETE FROM card_master_data WHERE bank_name = 'Federal Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Portfolio
('Federal Bank', 'Federal Bank Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 750, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with essential benefits and global acceptance', TRUE),

('Federal Bank', 'Federal Bank Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1500, 450000, 21, 70,
1, 0, TRUE, 45000, 750000,
3.5, 'Mid-tier credit card with enhanced benefits and reward earning', TRUE),

('Federal Bank', 'Federal Bank Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 3500, 700000, 21, 70,
2, 2, TRUE, 70000, 1200000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

-- RuPay Cards
('Federal Bank', 'Federal Bank RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 600000,
1.0, 'Premium RuPay card with domestic focus and lounge access', TRUE),

-- Specialized Cards
('Federal Bank', 'Federal Bank Business Credit Card', 'Business', 'Visa', 'Business',
3000, 5000, 600000, 25, 70,
3, 3, TRUE, 100000, 1500000,
3.5, 'Business credit card tailored for entrepreneurs and SMEs', TRUE),

('Federal Bank', 'Federal Bank Women Credit Card', 'Women Special', 'Visa', 'Standard',
500, 500, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
3.5, 'Special credit card for women with exclusive benefits and offers', TRUE),

-- Co-branded Card
('Federal Bank', 'Federal Bank Celesta Credit Card', 'Premium Lifestyle', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
4, 6, TRUE, 150000, 2000000,
3.5, 'Premium lifestyle card with exclusive privileges and concierge services', TRUE),

-- Digital Card
('Federal Bank', 'Federal Bank Easy Credit Card', 'Digital Focus', 'RuPay', 'Standard',
NULL, 399, 250000, 21, 50,
1, 0, TRUE, 25000, 400000,
1.0, 'Digital-first credit card with simplified application and instant approval', TRUE);