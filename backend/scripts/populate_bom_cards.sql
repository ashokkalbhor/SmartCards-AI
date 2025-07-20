-- Bank of Maharashtra Credit Cards Population Script
-- Regional public sector bank with strong Maharashtra presence
-- Total: 6 cards focusing on regional and agricultural banking

DELETE FROM card_master_data WHERE bank_name = 'Bank of Maharashtra';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Core Regional Banking Cards
('Bank of Maharashtra', 'Mahabank Classic Credit Card', 'Classic', 'RuPay', 'Standard',
NULL, 500, 250000, 21, 70,
0, 0, TRUE, 25000, 400000,
1.0, 'Entry-level credit card with regional focus and basic benefits', TRUE),

('Bank of Maharashtra', 'Mahabank Gold Credit Card', 'Gold', 'Visa', 'Standard',
750, 1000, 400000, 21, 70,
1, 0, TRUE, 40000, 600000,
3.5, 'Mid-tier credit card with enhanced benefits for regional customers', TRUE),

('Bank of Maharashtra', 'Mahabank Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
2000, 3000, 600000, 21, 70,
2, 2, TRUE, 60000, 1000000,
3.5, 'Premium credit card with comprehensive benefits for high-income customers', TRUE),

-- Specialized Cards
('Bank of Maharashtra', 'Mahabank Business Credit Card', 'Business', 'Visa', 'Business',
2500, 4000, 500000, 25, 70,
2, 2, TRUE, 100000, 1200000,
3.5, 'Business credit card for regional entrepreneurs and SMEs', TRUE),

('Bank of Maharashtra', 'Mahabank Kisan Credit Card', 'Agricultural', 'RuPay', 'Standard',
NULL, NULL, 150000, 18, 70,
0, 0, TRUE, 15000, 200000,
1.0, 'Agricultural credit card for farmers in Maharashtra region', TRUE),

-- Premium Card
('Bank of Maharashtra', 'Mahabank Signature Credit Card', 'Signature', 'Visa', 'Premium',
5000, 7500, 1000000, 25, 70,
3, 4, TRUE, 150000, 2000000,
3.5, 'Premium signature card for affluent customers in Maharashtra', TRUE);