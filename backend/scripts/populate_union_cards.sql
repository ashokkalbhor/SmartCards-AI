-- Union Bank of India Credit Cards Population Script
-- One of India's largest public sector banks with comprehensive portfolio
-- Total: 12 cards covering traditional and modern banking needs

DELETE FROM card_master_data WHERE bank_name = 'Union Bank of India';

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- Traditional Public Sector Offerings
('Union Bank of India', 'Union Bank RuPay Classic', 'Classic', 'RuPay', 'Standard',
NULL, NULL, 200000, 21, 70,
0, 0, TRUE, 20000, 300000,
1.0, 'Entry-level RuPay card with basic benefits and no annual fee', TRUE),

('Union Bank of India', 'Union Bank RuPay Platinum', 'Platinum', 'RuPay', 'Premium',
NULL, 500, 300000, 21, 70,
2, 1, TRUE, 30000, 500000,
1.0, 'Premium RuPay card with lounge access and comprehensive benefits', TRUE),

('Union Bank of India', 'Union Bank Visa Gold', 'Gold', 'Visa', 'Standard',
500, 750, 350000, 21, 70,
1, 0, TRUE, 35000, 600000,
3.5, 'Mid-tier Visa card with enhanced global acceptance', TRUE),

('Union Bank of India', 'Union Bank Visa Platinum', 'Platinum', 'Visa', 'Premium',
1000, 1500, 500000, 21, 70,
2, 2, TRUE, 50000, 800000,
3.5, 'Premium Visa card with comprehensive travel benefits', TRUE),

-- Specialized Segment Cards
('Union Bank of India', 'Union Bank Kisan Credit Card', 'Agricultural', 'RuPay', 'Standard',
NULL, NULL, 150000, 18, 70,
0, 0, TRUE, 15000, 200000,
1.0, 'Agricultural credit card for farmers with specialized benefits', TRUE),

('Union Bank of India', 'Union Bank Women Empowerment Card', 'Women Special', 'RuPay', 'Standard',
NULL, 250, 250000, 21, 70,
1, 0, TRUE, 25000, 400000,
1.0, 'Special credit card for women with exclusive benefits and offers', TRUE),

('Union Bank of India', 'Union Bank Business Card', 'Business', 'Visa', 'Business',
2000, 3000, 500000, 25, 70,
3, 2, TRUE, 100000, 1500000,
3.5, 'Business credit card for entrepreneurs and SMEs', TRUE),

-- Co-branded and Specialty Cards
('Union Bank of India', 'Union Bank HPCL Credit Card', 'Fuel Co-branded', 'RuPay', 'Standard',
500, 750, 300000, 21, 70,
1, 0, TRUE, 30000, 500000,
1.0, 'Fuel co-branded card with special benefits at HPCL outlets', TRUE),

('Union Bank of India', 'Union Bank Shopping Credit Card', 'Retail Focused', 'Visa', 'Standard',
750, 1000, 400000, 21, 70,
1, 1, TRUE, 40000, 700000,
3.5, 'Retail-focused card with enhanced rewards on shopping', TRUE),

-- Digital and Modern Offerings
('Union Bank of India', 'Union Bank Digital Credit Card', 'Digital First', 'RuPay', 'Standard',
NULL, 299, 300000, 21, 45,
1, 0, TRUE, 30000, 500000,
1.0, 'Digital-first credit card for tech-savvy customers', TRUE),

('Union Bank of India', 'Union Bank Contactless Credit Card', 'Contactless', 'Visa', 'Standard',
500, 500, 350000, 21, 70,
0, 0, TRUE, 35000, 600000,
3.5, 'Contactless payment focused card with modern features', TRUE),

-- Premium Offering
('Union Bank of India', 'Union Bank Signature Credit Card', 'Signature', 'Visa', 'Premium',
2500, 5000, 750000, 25, 70,
4, 6, TRUE, 100000, 2000000,
3.5, 'Premium signature card for high-income customers with exclusive privileges', TRUE);