-- Punjab & Maharashtra Co-op Bank Credit Cards Population Script
-- Multi-state cooperative bank serving Punjab and Maharashtra
-- Total: 5 cards focusing on cooperative banking with multi-state operations

DELETE FROM card_master_data WHERE bank_name = 'Punjab & Maharashtra Co-op Bank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Cooperative Banking Cards
('Punjab & Maharashtra Co-op Bank', 'PMC Classic Credit Card', 'Classic', 'RuPay', 'Standard',
NULL, 500, 250000, 21, 70,
0, 0, TRUE, 25000, 400000,
1.0, 'Entry-level cooperative credit card with basic benefits', TRUE),

('Punjab & Maharashtra Co-op Bank', 'PMC Gold Credit Card', 'Gold', 'Visa', 'Standard',
750, 1000, 400000, 21, 70,
1, 0, TRUE, 40000, 600000,
3.5, 'Mid-tier credit card for cooperative bank members', TRUE),

('Punjab & Maharashtra Co-op Bank', 'PMC Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2000, 3000, 600000, 21, 70,
2, 1, TRUE, 60000, 1000000,
3.5, 'Premium credit card with enhanced benefits for high-income members', TRUE),

-- Specialized Cards
('Punjab & Maharashtra Co-op Bank', 'PMC Business Credit Card', 'Business', 'Visa', 'Business',
2500, 4000, 500000, 25, 70,
2, 2, TRUE, 100000, 1200000,
3.5, 'Business credit card for cooperative society business members', TRUE),

-- Premium Card
('Punjab & Maharashtra Co-op Bank', 'PMC Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
3, 3, TRUE, 150000, 2000000,
3.5, 'Premium signature card for affluent cooperative bank members', TRUE);