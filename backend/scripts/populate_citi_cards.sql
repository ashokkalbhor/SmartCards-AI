-- Citibank Credit Cards Population Script
-- International bank with premium banking services in India
-- Total: 12 cards focusing on international premium banking and wealth management

DELETE FROM card_master_data WHERE bank_name = 'Citibank';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Entry Premium Cards
('Citibank', 'Citi Rewards Credit Card', 'Rewards', 'Mastercard', 'Standard',
1000, 1000, 500000, 21, 70,
2, 4, TRUE, 50000, 800000,
3.5, 'Rewards-focused credit card with international banking benefits', TRUE),

('Citibank', 'Citi Cash Back Credit Card', 'Cashback', 'Visa', 'Standard',
1000, 1000, 500000, 21, 70,
1, 2, TRUE, 50000, 800000,
3.5, 'Straightforward cashback card with premium international features', TRUE),

-- Mid-Tier Premium Cards
('Citibank', 'Citi Select Credit Card', 'Select', 'Mastercard', 'Premium',
2500, 2500, 800000, 21, 70,
4, 8, TRUE, 100000, 1500000,
3.5, 'Premium credit card with comprehensive international travel benefits', TRUE),

('Citibank', 'Citi Premier Miles Credit Card', 'Premier Miles', 'Visa', 'Premium',
3000, 3000, 800000, 21, 70,
4, 12, TRUE, 100000, 1500000,
3.5, 'Travel-focused premium card with extensive airline miles benefits', TRUE),

-- High-End Premium Cards
('Citibank', 'Citi Prestige Credit Card', 'Prestige', 'Mastercard', 'Ultra-Premium',
20000, 20000, 2500000, 25, 70,
12, 24, TRUE, 500000, 5000000,
3.5, 'Ultra-premium card with exclusive global privileges and concierge services', TRUE),

('Citibank', 'Citi Private Client Credit Card', 'Private Client', 'Visa', 'Ultra-Premium',
50000, 50000, 5000000, 25, 70,
24, 48, TRUE, 1000000, 10000000,
3.5, 'Exclusive private banking card for ultra-high-net-worth individuals', TRUE),

-- Business Cards
('Citibank', 'Citi Business Credit Card', 'Business', 'Mastercard', 'Business',
5000, 5000, 1000000, 25, 70,
6, 12, TRUE, 200000, 2000000,
3.5, 'International business card with comprehensive corporate benefits', TRUE),

('Citibank', 'Citi Corporate Credit Card', 'Corporate', 'Visa', 'Business',
10000, 10000, 1500000, 25, 70,
8, 16, TRUE, 500000, 5000000,
3.5, 'Corporate credit card for large enterprises with global operations', TRUE),

-- Co-branded Premium Cards
('Citibank', 'Citi Indian Oil Credit Card', 'Co-branded Fuel', 'Mastercard', 'Standard',
1500, 1500, 600000, 21, 70,
2, 4, TRUE, 60000, 1000000,
3.5, 'Premium fuel co-branded card with Indian Oil benefits', TRUE),

('Citibank', 'Citi Flipkart Credit Card', 'Co-branded Shopping', 'Mastercard', 'Standard',
500, 500, 400000, 21, 70,
1, 2, TRUE, 40000, 800000,
3.5, 'E-commerce focused co-branded card with Flipkart benefits', TRUE),

-- Specialized Premium Cards
('Citibank', 'Citi PremierMiles Executive Credit Card', 'Executive Miles', 'Visa', 'Premium',
7500, 7500, 1200000, 25, 70,
6, 18, TRUE, 200000, 3000000,
3.5, 'Executive travel card with premium airline and hotel benefits', TRUE),

-- Ultra-Premium Invitation Only
('Citibank', 'Citi Chairman Credit Card', 'Chairman', 'Mastercard', 'Ultra-Premium',
100000, 100000, 10000000, 30, 70,
48, 96, TRUE, 2000000, 25000000,
3.5, 'Invitation-only ultra-premium card for the most affluent customers', TRUE);