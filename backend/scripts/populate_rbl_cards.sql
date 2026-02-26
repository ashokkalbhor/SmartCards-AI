-- RBL Bank Credit Cards Population Script
-- Comprehensive script for populating 12 RBL Bank credit cards

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier,
    annual_fee, joining_fee, minimum_age, maximum_age, minimum_salary,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, domestic_lounge_visits,
    international_lounge_visits, welcome_bonus_points,
    minimum_credit_limit, maximum_credit_limit, insurance_benefits,
    concierge_service
) VALUES
('RBL Bank', 'World Safari Credit Card', 'Premium Travel', 'Visa', 'Premium', 3000.0, 3000.0, 21, 65, 300000.0, 0, 0.0, 750.0, 1, 1, 8, 999, 3000.0, 100000.0, 1000000.0, '{"type": "Comprehensive", "coverage": "Travel insurance, personal liability, trip delays, baggage loss"}', 1),
('RBL Bank', 'Icon Credit Card', 'Premium Lifestyle', 'Mastercard', 'Premium', 2500.0, 2500.0, 21, 65, 300000.0, 0, 3.5, 700.0, 1, 1, 4, 0, 10000.0, 75000.0, 800000.0, '{"type": "Premium", "coverage": "Purchase protection, travel insurance"}', 1),
('RBL Bank', 'Platinum Maxima Plus Credit Card', 'Premium', 'Visa', 'Premium', 2000.0, 2500.0, 21, 65, 250000.0, 0, 3.5, 650.0, 1, 1, 8, 0, 10000.0, 60000.0, 750000.0, '{"type": "Basic", "coverage": "Personal accident insurance"}', 0),
('RBL Bank', 'Platinum Delight Credit Card', 'Mid-Range', 'Mastercard', 'Premium', 2500.0, 500.0, 21, 65, 200000.0, 0, 3.5, 600.0, 1, 1, 0, 0, 4000.0, 50000.0, 600000.0, '{"type": "Basic", "coverage": "Personal accident insurance"}', 0),
('RBL Bank', 'Cookies Credit Card', 'Digital Lifestyle', 'Visa', 'Standard', 500.0, 500.0, 21, 65, 200000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 2000.0, 40000.0, 500000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0),
('RBL Bank', 'ShopRite Credit Card', 'Cashback', 'Mastercard', 'Standard', 500.0, 0.0, 21, 65, 200000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 2000.0, 40000.0, 500000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0),
('RBL Bank', 'IRCTC RBL Bank Credit Card', 'Co-branded Travel', 'RuPay', 'Standard', 500.0, 500.0, 21, 65, 200000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 2000.0, 40000.0, 500000.0, '{"type": "Basic", "coverage": "Travel insurance"}', 0),
('RBL Bank', 'IndianOil RBL Bank XTRA Credit Card', 'Co-branded Fuel', 'Visa', 'Standard', 1000.0, 1000.0, 21, 65, 200000.0, 0, 3.5, 550.0, 1, 1, 0, 0, 1500.0, 50000.0, 600000.0, '{"type": "Basic", "coverage": "Personal accident insurance"}', 0),
('RBL Bank', 'Insignia Preferred Banking Card', 'Super-Premium', 'Visa', 'Super-Premium', 10000.0, 10000.0, 21, 65, 1000000.0, 0, 1.5, 1000.0, 1, 1, 12, 999, 25000.0, 200000.0, 2000000.0, '{"type": "Premium", "coverage": "Comprehensive travel and lifestyle insurance"}', 1),
('RBL Bank', 'Play Credit Card', 'Entertainment', 'Mastercard', 'Standard', 750.0, 750.0, 21, 65, 200000.0, 0, 3.5, 500.0, 1, 1, 0, 0, 1000.0, 40000.0, 500000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0),
('RBL Bank', 'SalarySe UP Credit Card', 'Digital UPI', 'RuPay', 'Standard', 0.0, 0.0, 21, 65, 150000.0, 1, 3.5, 450.0, 1, 1, 0, 0, 500.0, 30000.0, 300000.0, '{"type": "Basic", "coverage": "Digital transaction protection"}', 0),
('RBL Bank', 'BankBazaar SaveMax Credit Card', 'Cashback', 'Visa', 'Standard', 0.0, 500.0, 21, 65, 200000.0, 1, 3.5, 500.0, 1, 1, 0, 0, 1000.0, 40000.0, 500000.0, '{"type": "Basic", "coverage": "Purchase protection"}', 0); 