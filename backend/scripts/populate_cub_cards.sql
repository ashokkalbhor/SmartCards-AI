-- City Union Bank Credit Cards Population Script
-- Private sector bank with strong South Indian presence
-- Total: 8 cards focusing on retail and SME segments

DELETE FROM card_master_data WHERE bank_name = 'City Union Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Private Banking Cards
('City Union Bank', 'CUB Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 750, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with essential benefits for retail customers', TRUE),

('City Union Bank', 'CUB Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1500, 450000, 21, 70,
1, 0, TRUE, 45000, 750000,
3.5, 'Mid-tier credit card with enhanced benefits and reward earning', TRUE),

('City Union Bank', 'CUB Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 3500, 650000, 21, 70,
2, 2, TRUE, 65000, 1200000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

-- RuPay Card
('City Union Bank', 'CUB RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 600000,
1.0, 'Premium RuPay card with domestic focus and enhanced benefits', TRUE),

-- Specialized Cards
('City Union Bank', 'CUB Business Credit Card', 'Business', 'Visa', 'Business',
3000, 5000, 600000, 25, 70,
3, 3, TRUE, 100000, 1500000,
3.5, 'Business credit card designed for SMEs and entrepreneurs', TRUE),

('City Union Bank', 'CUB Women Credit Card', 'Women Special', 'Visa', 'Standard',
500, 500, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
3.5, 'Special credit card for women with exclusive benefits and offers', TRUE),

-- Co-branded Card
('City Union Bank', 'CUB Shopping Credit Card', 'Shopping Focused', 'Visa', 'Standard',
750, 1250, 400000, 21, 70,
1, 1, TRUE, 40000, 700000,
3.5, 'Shopping-focused card with enhanced rewards on retail purchases', TRUE),

-- Premium Card
('City Union Bank', 'CUB Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
4, 6, TRUE, 150000, 2500000,
3.5, 'Premium signature card with exclusive privileges for high-net-worth customers', TRUE);