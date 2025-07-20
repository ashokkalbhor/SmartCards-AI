-- HSBC India Credit Cards Population Script
-- International bank with premium credit card portfolio in India
-- Total: 7 cards focusing on international banking expertise and premium services

DELETE FROM card_master_data WHERE bank_name = 'HSBC India';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Classic International Banking
('HSBC India', 'HSBC Cashback Credit Card', 'Cashback', 'Visa', 'Standard',
1000, 1000, 500000, 21, 70,
1, 2, TRUE, 50000, 800000,
3.5, 'Straightforward cashback card with international banking benefits', TRUE),

('HSBC India', 'HSBC Smart Value Credit Card', 'Smart Value', 'Mastercard', 'Standard',
750, 750, 400000, 21, 70,
1, 1, TRUE, 40000, 600000,
3.5, 'Value-focused card with smart rewards and international acceptance', TRUE),

-- Premium Travel Cards
('HSBC India', 'HSBC Platinum Credit Card', 'Platinum', 'Visa', 'Premium',
3500, 3500, 800000, 21, 70,
4, 6, TRUE, 100000, 1500000,
3.5, 'Premium travel card with comprehensive international benefits', TRUE),

('HSBC India', 'HSBC Premier Credit Card', 'Premier', 'Mastercard', 'Premium',
5000, 5000, 1500000, 25, 70,
6, 12, TRUE, 200000, 3000000,
3.5, 'Premier banking credit card with exclusive wealth management benefits', TRUE),

-- Ultra Premium
('HSBC India', 'HSBC Premier World Credit Card', 'Premier World', 'Mastercard', 'Ultra-Premium',
15000, 15000, 3000000, 25, 70,
12, 24, TRUE, 500000, 10000000,
3.5, 'Ultra-premium card for high-net-worth individuals with global privileges', TRUE),

-- Business Card
('HSBC India', 'HSBC Business Credit Card', 'Business', 'Visa', 'Business',
5000, 5000, 1000000, 25, 70,
4, 8, TRUE, 200000, 2000000,
3.5, 'International business card with global acceptance and corporate benefits', TRUE),

-- Co-branded Premium
('HSBC India', 'HSBC Emirates Skywards Credit Card', 'Co-branded Travel', 'Mastercard', 'Premium',
7500, 7500, 1200000, 25, 70,
4, 8, TRUE, 150000, 2500000,
3.5, 'Premium travel co-branded card with Emirates airline benefits and miles', TRUE);