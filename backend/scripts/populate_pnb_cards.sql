-- Punjab National Bank (PNB) Credit Cards Population Script
-- Comprehensive portfolio covering RuPay, Visa, Co-branded, and Specialized cards
-- Total: 15 cards covering entry-level to premium segments

-- Clear any existing PNB data
DELETE FROM card_master_data WHERE bank_name = 'Punjab National Bank';

-- Insert PNB Credit Cards matching actual database schema
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    joining_fee, annual_fee, minimum_salary, minimum_age, maximum_age,
    domestic_lounge_visits, international_lounge_visits,
    contactless_enabled, minimum_credit_limit, maximum_credit_limit,
    foreign_transaction_fee, description, is_active
) VALUES

-- 1. PNB RuPay Platinum Card
('Punjab National Bank', 'PNB RuPay Platinum', 'Platinum', 'RuPay', 'Premium',
NULL, NULL, 250000, 21, 70,
2, 4, TRUE, 25000, 500000,
1.0, 'Feature-rich RuPay card with comprehensive benefits, lounge access, and no annual fee with minimal usage', TRUE),

-- 2. PNB RuPay Select Card
('Punjab National Bank', 'PNB RuPay Select', 'Select', 'RuPay', 'Premium',
500, 750, 500000, 21, 70,
4, 8, TRUE, 50000, 1000000,
1.0, 'Premium RuPay card with enhanced rewards on retail spending and comprehensive travel benefits', TRUE),

-- 3. PNB RuPay Millennial Card
('Punjab National Bank', 'PNB RuPay Millennial', 'Millennial', 'RuPay', 'Standard',
399, 999, 500000, 21, 35,
1, 2, TRUE, 50000, 1000000,
1.0, 'Youth-focused card with health, fitness benefits and accelerated rewards for millennials', TRUE),

-- 4. PNB Rakshak RuPay Platinum Card
('Punjab National Bank', 'PNB Rakshak RuPay Platinum', 'Rakshak Platinum', 'RuPay', 'Premium',
NULL, NULL, 250000, 21, 70,
2, 4, TRUE, 25000, 500000,
1.0, 'Exclusive card for defense personnel with enhanced insurance and family benefits', TRUE),

-- 5. PNB Rakshak RuPay Select Card
('Punjab National Bank', 'PNB Rakshak RuPay Select', 'Rakshak Select', 'RuPay', 'Premium',
NULL, NULL, 500000, 21, 70,
4, 8, TRUE, 50000, 1000000,
1.0, 'Premium defense personnel card with enhanced rewards and comprehensive family benefits', TRUE),

-- 6. PNB Visa Classic Card
('Punjab National Bank', 'PNB Visa Classic', 'Classic', 'Visa', 'Standard',
NULL, 300, 300000, 21, 70,
0, 0, TRUE, 30000, 500000,
3.5, 'Entry-level Visa card with global acceptance and basic benefits for international transactions', TRUE),

-- 7. PNB Visa Gold Card
('Punjab National Bank', 'PNB Visa Gold', 'Gold', 'Visa', 'Standard',
NULL, 500, 400000, 21, 70,
1, 0, TRUE, 40000, 800000,
3.5, 'Mid-tier Visa card with enhanced travel benefits and comprehensive purchase protection', TRUE),

-- 8. PNB Visa Platinum Card
('Punjab National Bank', 'PNB Visa Platinum', 'Platinum', 'Visa', 'Premium',
NULL, 750, 500000, 21, 70,
2, 2, TRUE, 50000, 1000000,
3.5, 'Premium Visa card with comprehensive travel benefits and enhanced global acceptance', TRUE),

-- 9. PNB Visa Signature Card
('Punjab National Bank', 'PNB Visa Signature', 'Signature', 'Visa', 'Premium',
NULL, 1500, 750000, 21, 70,
4, 6, TRUE, 125000, 1500000,
3.5, 'Super-premium Visa card for HNI customers with exclusive privileges and comprehensive benefits', TRUE),

-- 10. PNB Wave & Pay Credit Card
('Punjab National Bank', 'PNB Wave & Pay', 'Contactless', 'Visa', 'Standard',
NULL, 400, 350000, 21, 70,
0, 0, TRUE, 35000, 600000,
3.5, 'Innovation-focused contactless card with advanced payment technology and digital integration', TRUE),

-- 11. PNB Patanjali RuPay Select Card
('Punjab National Bank', 'PNB Patanjali RuPay Select', 'Co-branded Select', 'RuPay', 'Premium',
500, 750, 400000, 21, 70,
2, 4, TRUE, 40000, 800000,
1.0, 'Co-branded card with Patanjali offering exclusive benefits on health, wellness, and Ayurvedic products', TRUE),

-- 12. PNB Patanjali RuPay Platinum Card
('Punjab National Bank', 'PNB Patanjali RuPay Platinum', 'Co-branded Platinum', 'RuPay', 'Standard',
NULL, 500, 300000, 21, 70,
1, 2, TRUE, 30000, 600000,
1.0, 'Co-branded Patanjali card focusing on health, wellness, and Ayurvedic lifestyle benefits', TRUE),

-- 13. PNB EMT RuPay Card
('Punjab National Bank', 'PNB EMT RuPay', 'EMT Special', 'RuPay', 'Premium',
2000, 2000, 400000, 21, 70,
2, 4, TRUE, 50000, 1000000,
1.0, 'Specialized card for healthcare professionals with medical emergency benefits and travel vouchers', TRUE),

-- 14. PNB Global Classic Credit Card
('Punjab National Bank', 'PNB Global Classic', 'Global Classic', 'Visa', 'Standard',
NULL, NULL, 250000, 21, 70,
0, 0, TRUE, 25000, 400000,
3.5, 'Lifetime free entry-level card ideal for beginners with global Visa acceptance', TRUE),

-- 15. PNB Global Gold Credit Card
('Punjab National Bank', 'PNB Global Gold', 'Global Gold', 'Visa', 'Standard',
NULL, 300, 300000, 21, 70,
1, 1, TRUE, 30000, 600000,
3.5, 'Mid-tier global card with enhanced benefits and international acceptance for regular travelers', TRUE);

-- Verify the population
SELECT 
    COUNT(*) as total_cards,
    COUNT(CASE WHEN card_tier = 'Standard' THEN 1 END) as standard,
    COUNT(CASE WHEN card_tier = 'Premium' THEN 1 END) as premium
FROM card_master_data 
WHERE bank_name = 'Punjab National Bank';

-- Display summary by network
SELECT 
    card_network,
    COUNT(*) as card_count
FROM card_master_data 
WHERE bank_name = 'Punjab National Bank'
GROUP BY card_network
ORDER BY card_count DESC; 