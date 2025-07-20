-- Canara Bank Credit Cards Population Script
-- Major public sector bank with wide geographical reach
-- Total: 10 cards covering traditional banking with modern approach

DELETE FROM card_master_data WHERE bank_name = 'Canara Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Banking Cards
('Canara Bank', 'Canara Bank Classic Credit Card', 'Classic', 'Visa', 'Standard',
NULL, 500, 250000, 21, 70,
0, 0, TRUE, 25000, 400000,
3.5, 'Entry-level credit card with basic benefits and global acceptance', TRUE),

('Canara Bank', 'Canara Bank Gold Credit Card', 'Gold', 'Visa', 'Standard',
750, 1000, 400000, 21, 70,
1, 0, TRUE, 40000, 600000,
3.5, 'Mid-tier credit card with enhanced benefits and rewards', TRUE),

('Canara Bank', 'Canara Bank Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
1500, 2500, 600000, 21, 70,
2, 2, TRUE, 60000, 1000000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

-- RuPay Portfolio
('Canara Bank', 'Canara Bank RuPay Classic', 'RuPay Classic', 'RuPay', 'Standard',
NULL, NULL, 200000, 21, 70,
0, 0, TRUE, 20000, 300000,
1.0, 'Lifetime free RuPay card with domestic focus and basic benefits', TRUE),

('Canara Bank', 'Canara Bank RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
500, 750, 350000, 21, 70,
2, 1, TRUE, 35000, 500000,
1.0, 'Premium RuPay card with lounge access and enhanced benefits', TRUE),

-- Specialized Cards
('Canara Bank', 'Canara Bank Business Credit Card', 'Business', 'Visa', 'Business',
2000, 3500, 500000, 25, 70,
3, 2, TRUE, 100000, 1500000,
3.5, 'Business credit card for entrepreneurs with business-specific benefits', TRUE),

('Canara Bank', 'Canara Bank Women Credit Card', 'Women Special', 'RuPay', 'Standard',
NULL, 300, 250000, 21, 70,
1, 0, TRUE, 25000, 400000,
1.0, 'Special credit card for women with exclusive offers and benefits', TRUE),

-- Co-branded Cards
('Canara Bank', 'Canara Bank IOCL Credit Card', 'Fuel Co-branded', 'RuPay', 'Standard',
500, 750, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
1.0, 'Fuel co-branded card with special benefits at IOCL outlets', TRUE),

('Canara Bank', 'Canara Bank Shopping Credit Card', 'Shopping Focused', 'Visa', 'Standard',
750, 1250, 400000, 21, 70,
1, 1, TRUE, 40000, 700000,
3.5, 'Shopping-focused card with enhanced rewards on retail purchases', TRUE),

-- Premium Signature Card
('Canara Bank', 'Canara Bank Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
6, 8, TRUE, 150000, 2500000,
3.5, 'Ultra-premium signature card with exclusive privileges and concierge services', TRUE);