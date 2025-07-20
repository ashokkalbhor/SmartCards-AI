-- Saraswat Bank Credit Cards Population Script
-- Cooperative bank with strong presence in Maharashtra and Goa
-- Total: 7 cards focusing on community-focused services

DELETE FROM card_master_data WHERE bank_name = 'Saraswat Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Cooperative Banking Cards
('Saraswat Bank', 'Saraswat Classic Credit Card', 'Classic', 'Visa', 'Standard',
500, 750, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level credit card with community banking benefits', TRUE),

('Saraswat Bank', 'Saraswat Gold Credit Card', 'Gold', 'Visa', 'Standard',
1000, 1500, 450000, 21, 70,
1, 0, TRUE, 45000, 750000,
3.5, 'Mid-tier credit card with enhanced benefits for cooperative members', TRUE),

('Saraswat Bank', 'Saraswat Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2500, 3500, 650000, 21, 70,
2, 2, TRUE, 65000, 1200000,
3.5, 'Premium credit card with comprehensive travel and lifestyle benefits', TRUE),

-- RuPay Card
('Saraswat Bank', 'Saraswat RuPay Platinum', 'RuPay Platinum', 'RuPay', 'Premium',
1000, 1000, 400000, 21, 70,
2, 1, TRUE, 40000, 600000,
1.0, 'Premium RuPay card with cooperative banking advantages', TRUE),

-- Specialized Cards
('Saraswat Bank', 'Saraswat Business Credit Card', 'Business', 'Visa', 'Business',
2500, 4000, 500000, 25, 70,
2, 2, TRUE, 100000, 1200000,
3.5, 'Business credit card for cooperative society members and SMEs', TRUE),

('Saraswat Bank', 'Saraswat Community Credit Card', 'Community Special', 'RuPay', 'Standard',
NULL, 300, 250000, 21, 70,
1, 0, TRUE, 25000, 400000,
1.0, 'Special credit card for cooperative community members with preferential rates', TRUE),

-- Premium Card
('Saraswat Bank', 'Saraswat Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
3, 4, TRUE, 150000, 2000000,
3.5, 'Premium signature card for high-net-worth cooperative members', TRUE);