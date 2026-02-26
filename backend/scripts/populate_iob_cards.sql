-- Indian Overseas Bank Credit Cards Population Script
-- Public sector bank with significant international presence
-- Total: 7 cards focusing on international banking expertise

DELETE FROM card_master_data WHERE bank_name = 'Indian Overseas Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core International Banking Cards
('Indian Overseas Bank', 'IOB Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 750, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with international banking benefits', TRUE),

('Indian Overseas Bank', 'IOB Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1500, 450000, 21, 70,
1, 1, TRUE, 45000, 750000,
3.5, 'Mid-tier credit card with enhanced international acceptance', TRUE),

('Indian Overseas Bank', 'IOB Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 3500, 650000, 21, 70,
2, 4, TRUE, 65000, 1200000,
3.5, 'Premium credit card with comprehensive international travel benefits', TRUE),

-- RuPay Card
('Indian Overseas Bank', 'IOB RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 600000,
1.0, 'Premium RuPay card with domestic and international benefits', TRUE),

-- Specialized Cards
('Indian Overseas Bank', 'IOB Business Credit Card', 'Business', 'Visa', 'Business',
3000, 5000, 600000, 25, 70,
3, 6, TRUE, 100000, 1500000,
3.5, 'International business credit card for export-import businesses', TRUE),

('Indian Overseas Bank', 'IOB NRI Credit Card', 'NRI Special', 'Visa', 'Premium',
2000, 2500, 500000, 21, 70,
2, 8, TRUE, 50000, 1000000,
3.5, 'Special credit card for Non-Resident Indians with international benefits', TRUE),

-- Premium Card
('Indian Overseas Bank', 'IOB Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
4, 12, TRUE, 150000, 2500000,
3.5, 'Premium signature card with global privileges and concierge services', TRUE);