-- Kotak Mahindra Bank Credit Cards Population Script
-- Generated: December 2024
-- Total Cards: 10
-- Bank Focus: Digital banking, youth-oriented products, premium lifestyle

-- Insert Kotak Mahindra Bank Cards
INSERT INTO card_master_data (
    bank_name, card_name, card_variant, annual_fee, joining_fee, 
    minimum_age, maximum_age, minimum_salary, card_network, card_tier,
    is_lifetime_free, foreign_transaction_fee, late_payment_fee,
    contactless_enabled, chip_enabled, mobile_wallet_support,
    domestic_lounge_visits, international_lounge_visits,
    welcome_bonus_points, minimum_credit_limit, maximum_credit_limit,
    insurance_benefits, concierge_service
) VALUES

-- 1. Kotak 811 Credit Card
('Kotak Mahindra Bank', '811 Credit Card', 'Digital-First', 500, 0,
 21, 65, 200000, 600,
 'Digital-first banking, instant approval, app-based management, zero joining fee',
 '4 reward points per Rs. 100 on online spends, 2 points on offline spends',
 'No', 'Personal accident coverage up to Rs. 5 lakh',
 2.0, 'Yes - 1% waiver on fuel between Rs. 400-2000',
 'Yes - competitive forex markup for international usage',
 'Yes', 'Yes', 'Yes',
 'Enhanced online shopping rewards, exclusive e-commerce partnerships',
 'Basic travel insurance, online travel booking discounts',
 'Digital dining rewards, food delivery app partnerships',
 'Online movie booking discounts, OTT platform benefits',
 'Online grocery delivery rewards and cashback',
 'Digital bill payment rewards, instant payment processing',
 '2,000 bonus reward points on annual fee payment',
 '1,000 welcome reward points + digital banking kit',
 3.25, 'Rs. 450 or 2.5% of total due', 'Rs. 400 or 2.5% of overlimit amount',
 '3.5% of amount advanced', '17.50', '17.50', '45.00',
 3, 'Digital limit enhancement through app',
 199, 'Salaried/Self-employed with digital savviness', 'Digital document upload, minimal paperwork',
 '2-5 working days', '5-7 working days', 'Yes - instant virtual card',
 'Digital-first support, AI chatbot assistance', 4.1,
 'Advanced digital security, app-based fraud monitoring',
 'Optimized for digital transactions, limited physical merchant benefits',
 150000, 'Mastercard - digital-optimized network',
 datetime('now'), datetime('now')),

-- 2. Kotak Zen Credit Card
('Kotak Mahindra Bank', 'Zen Credit Card', 'Lifestyle', 1000, 1000,
 21, 65, 350000, 650,
 'Lifestyle rewards, wellness benefits, mindful spending, balance-focused',
 '3 reward points per Rs. 100 on wellness spends, 2 points on all other purchases',
 'Yes - 4 domestic lounge visits per year',
 'Health and wellness insurance coverage',
 2.0, 'Yes - 1.5% waiver on fuel transactions',
 'Yes - wellness-focused international benefits',
 'Yes', 'Yes', 'Yes',
 'Wellness and lifestyle e-commerce rewards',
 'Wellness travel packages, spa and retreat discounts',
 'Healthy dining options, organic restaurant partnerships',
 'Wellness content and documentary benefits',
 'Organic and health food store partnerships',
 'Eco-friendly utility payment incentives',
 'Wellness vouchers worth Rs. 3,000 on renewal',
 'Wellness starter pack + 5,000 welcome points',
 3.0, 'Rs. 550 or 2.75% of total due', 'Rs. 450 or 2.5% of overlimit amount',
 '3.25% of amount advanced', '16.50', '16.50', '44.00',
 4, 'Wellness goal-based limit enhancements',
 299, 'Health-conscious professionals', 'Standard documents + wellness program enrollment preference',
 '7-10 working days', '7-10 working days', 'Yes',
 'Wellness-focused customer support, lifestyle guidance', 4.2,
 'Mindful spending alerts, wellness fraud protection',
 'Restrictions on alcohol, tobacco, and gambling',
 200000, 'Visa - wellness-partner optimized',
 datetime('now'), datetime('now')),

-- 3. Kotak White Credit Card
('Kotak Mahindra Bank', 'White Credit Card', 'Premium', 2500, 2500,
 21, 65, 600000, 700,
 'Premium lifestyle, exclusive privileges, white-glove service, luxury experiences',
 '3 reward points per Rs. 100 spent, 6 points on luxury and premium spends',
 'Yes - 8 domestic and 2 international lounge visits per year',
 'Premium travel and lifestyle insurance coverage',
 3.0, 'Yes - 2% waiver on fuel up to Rs. 3000 monthly',
 'Yes - premium forex rates, global concierge services',
 'Yes', 'Yes', 'Yes',
 'Luxury brand partnerships, exclusive shopping experiences',
 'Premium travel concierge, luxury hotel partnerships',
 'Fine dining experiences, Michelin-starred restaurant access',
 'Premium cinema experiences, film festival invitations',
 'Gourmet grocery delivery, premium food partnerships',
 'Priority utility services, premium bill management',
 '15,000 bonus reward points + luxury vouchers worth Rs. 8,000',
 '25,000 welcome reward points + premium welcome kit',
 2.25, 'Rs. 700 or 3% of total due', 'Rs. 600 or 2.75% of overlimit amount',
 '2.75% of amount advanced', '14.50', '14.50', '41.00',
 5, 'Premium automatic enhancements based on lifestyle spending',
 499, 'High-income professionals, luxury enthusiasts', 'ITR, lifestyle spending patterns, premium banking relationship',
 '5-7 working days', '5-7 working days', 'Yes',
 'Dedicated premium support, luxury lifestyle concierge', 4.4,
 'Premium fraud protection, luxury transaction monitoring',
 'Focus on premium merchants, luxury brand partnerships',
 500000, 'Visa Signature/Mastercard World - premium global acceptance',
 datetime('now'), datetime('now')),

-- 4. Kotak League Credit Card
('Kotak Mahindra Bank', 'League Credit Card', 'Sports-Lifestyle', 1500, 1500,
 21, 65, 450000, 650,
 'Sports and fitness rewards, athlete partnerships, active lifestyle benefits',
 '5 reward points per Rs. 100 on sports and fitness spends, 2 points on all other purchases',
 'Yes - 6 domestic lounge visits per year',
 'Sports accident and fitness-related injury coverage',
 2.5, 'Yes - 1.5% waiver on fuel for sports-related travel',
 'Yes - sports event travel benefits internationally',
 'Yes', 'Yes', 'Yes',
 'Sports equipment and athletic wear e-commerce rewards',
 'Sports event travel packages, athlete meet-and-greet opportunities',
 'Sports nutrition and healthy dining partnerships',
 'Sports documentaries and athletic event broadcasting benefits',
 'Sports nutrition and supplement store partnerships',
 'Gym and fitness center membership payment benefits',
 'Sports equipment vouchers worth Rs. 5,000 on renewal',
 'Athletic gear starter pack + 8,000 welcome points',
 3.0, 'Rs. 600 or 2.75% of total due', 'Rs. 500 or 2.5% of overlimit amount',
 '3.0% of amount advanced', '16.00', '16.00', '43.50',
 4, 'Fitness goal achievement-based limit increases',
 399, 'Sports enthusiasts, fitness professionals, athletes', 'Standard documents + sports club membership preference',
 '7-10 working days', '7-10 working days', 'Yes',
 'Sports-focused customer support, athletic lifestyle guidance', 4.1,
 'Active lifestyle spending monitoring, sports fraud protection',
 'Enhanced rewards only on genuine sports and fitness merchants',
 300000, 'Mastercard - sports partnership network',
 datetime('now'), datetime('now')),

-- 5. Kotak Platinum Credit Card
('Kotak Mahindra Bank', 'Platinum Credit Card', 'Standard', 750, 750,
 21, 65, 300000, 600,
 'Everyday banking, reliable rewards, standard benefits, cost-effective',
 '1 reward point per Rs. 100 spent, 2 points on weekend spends',
 'Yes - 3 domestic lounge visits per year',
 'Basic personal accident and purchase protection',
 1.0, 'Yes - 1% waiver on fuel between Rs. 400-2000',
 'Yes - standard international usage with regular rates',
 'Yes', 'Yes', 'Yes',
 'Standard online shopping discounts and offers',
 'Basic travel insurance and booking assistance',
 'Weekend dining offers at partner restaurants',
 'Movie ticket discounts during weekends and festivals',
 'Basic grocery store partnerships',
 'Standard utility bill payment facilities',
 '2,000 bonus reward points on renewal',
 '2,000 welcome reward points on activation',
 3.5, 'Rs. 500 or 2.5% of total due', 'Rs. 400 or 2.5% of overlimit amount',
 '3.5% of amount advanced', '18.00', '18.00', '47.00',
 3, 'Standard limit enhancement after 12 months',
 199, 'Salaried/Self-employed', 'Basic income and identity documents',
 '10-14 working days', '10-14 working days', 'Yes',
 'Standard customer support, phone and chat assistance', 3.9,
 'Basic security features, transaction monitoring',
 'Standard merchant restrictions, limited premium access',
 125000, 'Visa/Mastercard - standard global acceptance',
 datetime('now'), datetime('now')),

-- 6. Kotak Royale Credit Card
('Kotak Mahindra Bank', 'Royale Credit Card', 'Super-Premium', 10000, 10000,
 25, 65, 2000000, 750,
 'Ultra-premium lifestyle, royal treatment, exclusive privileges, luxury concierge',
 '4 reward points per Rs. 100 spent, 8 points on luxury and international spends',
 'Yes - Unlimited domestic and international lounge access',
 'Comprehensive luxury coverage: travel Rs. 75 lakh, medical Rs. 25 lakh',
 4.0, 'Yes - Complete fuel surcharge waiver up to Rs. 5000 monthly',
 'Yes - Premium global acceptance, royal forex rates',
 'Yes', 'Yes', 'Yes',
 'VIP shopping experiences, luxury brand early access',
 'Royal travel experiences, palace hotel partnerships, private jet access',
 'Michelin-starred dining, celebrity chef experiences',
 'Royal premiere access, exclusive film screenings',
 'Gourmet and royal cuisine delivery services',
 'Concierge-managed utility and lifestyle services',
 '75,000 bonus reward points + royal experiences worth Rs. 25,000',
 '150,000 welcome reward points + royal welcome experience',
 1.75, 'Rs. 1000 or 3.5% of total due', 'Rs. 750 or 3% of overlimit amount',
 '2.25% of amount advanced', '12.50', '12.50', '38.00',
 7, 'Royal tier automatic enhancements up to 10x income',
 'Free for family, Rs. 3000 for others', 'Ultra-high net worth individuals, business moguls',
 'Wealth statements, business ownership proof, premium banking history',
 '3-5 working days', '3-5 working days', 'Yes',
 'Royal relationship manager, 24/7 premium concierge', 4.7,
 'Royal-grade security, biometric protection, priority dispute resolution',
 'Unlimited luxury merchant access, royal partnerships',
 5000000, 'Visa Infinite/Mastercard World Elite Black - ultra-premium',
 datetime('now'), datetime('now')),

-- 7. Kotak Privy Credit Card
('Kotak Mahindra Bank', 'Privy Credit Card', 'Exclusive-Invitation', 25000, 25000,
 30, 70, 5000000, 800,
 'Invitation-only exclusivity, private banking privileges, bespoke services',
 '5 reward points per Rs. 100 spent, 10 points on exclusive merchant partnerships',
 'Yes - Unlimited global lounge access + private lounges',
 'Bespoke insurance coverage up to Rs. 2 crore, family coverage included',
 5.0, 'Yes - Complete fuel cost coverage through concierge services',
 'Yes - Exclusive global privileges, private banking forex rates',
 'Yes', 'Yes', 'Yes',
 'Private shopping experiences, designer brand exclusive access',
 'Private jet bookings, yacht charters, exclusive resort access',
 'Private chef experiences, exclusive restaurant reservations',
 'Private film screenings, celebrity event access',
 'Personal shopping and gourmet concierge services',
 'Fully managed lifestyle and utility concierge services',
 'Bespoke experiences worth Rs. 100,000 annually',
 'Private banking onboarding + Rs. 500,000 worth exclusive experiences',
 1.25, 'Waived with concierge payment management', 'Managed by dedicated team',
 '2.0% of amount advanced', '10.00', '10.00', '32.00',
 10, 'Unlimited enhancement based on private banking relationship',
 'Complimentary for immediate family', 'Ultra-high net worth, private banking clients only',
 'Private banking verification, wealth management assessment',
 '24-48 hours', '24-48 hours', 'Yes - immediately',
 'Private relationship manager, bespoke concierge services', 5.0,
 'Private banking security, wealth protection, family office integration',
 'No restrictions, exclusive merchant partnerships only',
 'Unlimited', 'All premium networks - unlimited global acceptance',
 datetime('now'), datetime('now')),

-- 8. Kotak Urbane Credit Card
('Kotak Mahindra Bank', 'Urbane Credit Card', 'Urban-Lifestyle', 1200, 1200,
 21, 65, 400000, 650,
 'Urban lifestyle, city-centric benefits, metropolitan rewards, modern banking',
 '3 reward points per Rs. 100 on urban lifestyle spends, 1.5 points on other purchases',
 'Yes - 5 domestic lounge visits per year',
 'Urban lifestyle insurance and metropolitan accident coverage',
 1.5, 'Yes - 1.5% waiver on fuel for city commuting',
 'Yes - urban travel benefits, metropolitan city partnerships',
 'Yes', 'Yes', 'Yes',
 'Urban e-commerce partnerships, city-specific brand discounts',
 'City break packages, urban hotel partnerships, metro travel benefits',
 'Urban dining scene access, trendy restaurant partnerships',
 'Multiplex partnerships, urban entertainment venue benefits',
 'Urban grocery chains and convenience store partnerships',
 'Metropolitan utility management, smart city payment integration',
 'Urban lifestyle vouchers worth Rs. 4,000 on renewal',
 'City starter pack + 6,000 welcome points',
 3.0, 'Rs. 575 or 2.75% of total due', 'Rs. 475 or 2.5% of overlimit amount',
 '3.0% of amount advanced', '16.25', '16.25', '43.75',
 4, 'Urban spending pattern-based enhancements',
 299, 'Urban professionals, city dwellers', 'Standard documents + city residence proof',
 '7-10 working days', '7-10 working days', 'Yes',
 'Urban-focused support, city lifestyle guidance', 4.0,
 'Urban fraud protection, metropolitan security features',
 'Focus on urban merchants, city-centric partnerships',
 250000, 'Visa/Mastercard - urban merchant optimized',
 datetime('now'), datetime('now')),

-- 9. Kotak Essentials Credit Card
('Kotak Mahindra Bank', 'Essentials Credit Card', 'Basic', 399, 399,
 21, 65, 180000, 550,
 'Essential banking, basic rewards, affordability, simple features',
 '0.5 reward points per Rs. 100 spent, 1 point on essential category spends',
 'No', 'Basic personal accident coverage up to Rs. 3 lakh',
 0.5, 'No', 'Yes - basic international usage',
 'Yes', 'Yes', 'Limited',
 'Essential shopping discounts, basic e-commerce offers',
 'Basic travel insurance, standard booking assistance',
 'Essential dining offers at budget-friendly restaurants',
 'Basic movie ticket discounts during promotional periods',
 'Essential grocery store partnerships',
 'Basic utility bill payment features',
 '500 bonus reward points on renewal',
 '1,000 welcome reward points on activation',
 4.0, 'Rs. 350 or 2.5% of total due', 'Rs. 250 or 2.5% of overlimit amount',
 '4.0% of amount advanced', '20.00', '20.00', '49.00',
 2, 'Basic limit enhancement after satisfactory usage',
 99, 'Entry-level salaried, small business owners', 'Basic income and identity documents',
 '12-15 working days', '12-15 working days', 'Limited',
 'Basic customer support, standard assistance', 3.6,
 'Basic security features, essential fraud monitoring',
 'Limited rewards, focus on essential merchants only',
 60000, 'Mastercard - basic global acceptance',
 datetime('now'), datetime('now')),

-- 10. Kotak Business Credit Card
('Kotak Mahindra Bank', 'Business Credit Card', 'Corporate', 2000, 2000,
 25, 65, 800000, 700,
 'Business expense management, corporate rewards, B2B benefits, professional banking',
 '2.5 reward points per Rs. 100 on business spends, 4 points on business travel',
 'Yes - 10 domestic and 3 international lounge visits per year',
 'Business travel and corporate liability insurance',
 2.5, 'Yes - Corporate fuel benefits with enhanced waiver',
 'Yes - Business-optimized international usage and forex rates',
 'Yes', 'Yes', 'Yes',
 'B2B marketplace rewards, corporate vendor partnerships',
 'Business travel management, corporate hotel tie-ups',
 'Business dining and client entertainment benefits',
 'Corporate event bookings and business entertainment',
 'Office supplies and corporate catering partnerships',
 'Business utility management and bulk payment benefits',
 'Business services credits worth Rs. 8,000 annually',
 'Business starter package + 12,000 welcome points',
 2.5, 'Rs. 750 or 3% of total due', 'Rs. 550 or 2.75% of overlimit amount',
 '2.75% of amount advanced', '15.00', '15.00', '42.00',
 6, 'Business growth-based automatic limit enhancements',
 399, 'Business owners, corporate professionals', 'Business registration, financial statements, GST documents',
 '5-8 working days', '5-8 working days', 'Yes',
 'Dedicated business support, corporate account management', 4.3,
 'Business-grade security, corporate fraud protection',
 'Business-focused, enhanced B2B merchant access',
 800000, 'Visa/Mastercard - corporate global acceptance',
 datetime('now'), datetime('now'));

-- Insert Kotak Mahindra Bank Spending Categories
INSERT INTO spending_categories (bank_name, card_name, category_name, reward_rate, monthly_cap, annual_cap) VALUES
('Kotak Mahindra Bank', '811 Credit Card', 'Online Shopping', '4 points per Rs. 100', 12000, 144000),
('Kotak Mahindra Bank', '811 Credit Card', 'Offline Purchases', '2 points per Rs. 100', NULL, NULL),
('Kotak Mahindra Bank', '811 Credit Card', 'Digital Payments', '4 points per Rs. 100', 8000, 96000),

('Kotak Mahindra Bank', 'Zen Credit Card', 'Wellness & Health', '3 points per Rs. 100', 20000, 240000),
('Kotak Mahindra Bank', 'Zen Credit Card', 'Organic & Eco-friendly', '3 points per Rs. 100', 15000, 180000),
('Kotak Mahindra Bank', 'Zen Credit Card', 'All Other Purchases', '2 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'White Credit Card', 'Luxury & Premium Spends', '6 points per Rs. 100', 50000, 600000),
('Kotak Mahindra Bank', 'White Credit Card', 'International Transactions', '6 points per Rs. 100', NULL, NULL),
('Kotak Mahindra Bank', 'White Credit Card', 'All Other Spends', '3 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'League Credit Card', 'Sports & Fitness', '5 points per Rs. 100', 25000, 300000),
('Kotak Mahindra Bank', 'League Credit Card', 'Athletic Equipment', '5 points per Rs. 100', 20000, 240000),
('Kotak Mahindra Bank', 'League Credit Card', 'All Other Purchases', '2 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Platinum Credit Card', 'Weekend Spends', '2 points per Rs. 100', 8000, 96000),
('Kotak Mahindra Bank', 'Platinum Credit Card', 'Regular Spends', '1 point per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Royale Credit Card', 'Luxury & International', '8 points per Rs. 100', NULL, NULL),
('Kotak Mahindra Bank', 'Royale Credit Card', 'All Other Spends', '4 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Privy Credit Card', 'Exclusive Merchant Partners', '10 points per Rs. 100', NULL, NULL),
('Kotak Mahindra Bank', 'Privy Credit Card', 'All Other Spends', '5 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Urbane Credit Card', 'Urban Lifestyle', '3 points per Rs. 100', 18000, 216000),
('Kotak Mahindra Bank', 'Urbane Credit Card', 'City Services', '3 points per Rs. 100', 12000, 144000),
('Kotak Mahindra Bank', 'Urbane Credit Card', 'All Other Purchases', '1.5 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Essentials Credit Card', 'Essential Categories', '1 point per Rs. 100', 3000, 36000),
('Kotak Mahindra Bank', 'Essentials Credit Card', 'All Other Spends', '0.5 points per Rs. 100', NULL, NULL),

('Kotak Mahindra Bank', 'Business Credit Card', 'Business Travel', '4 points per Rs. 100', 80000, 960000),
('Kotak Mahindra Bank', 'Business Credit Card', 'Business Spends', '2.5 points per Rs. 100', NULL, NULL);

-- Insert Kotak Mahindra Bank Merchant-Specific Rewards
INSERT INTO merchant_rewards (bank_name, card_name, merchant_name, reward_type, reward_value, validity_period) VALUES
('Kotak Mahindra Bank', '811 Credit Card', 'Amazon', 'Points', '4x points on online shopping', '2024-12-31'),
('Kotak Mahindra Bank', '811 Credit Card', 'Flipkart', 'Points', '4x points on online shopping', '2024-12-31'),
('Kotak Mahindra Bank', '811 Credit Card', 'PhonePe', 'Cashback', '2% on digital payments', '2024-12-31'),

('Kotak Mahindra Bank', 'Zen Credit Card', 'Cure.fit', 'Points', '3x points on fitness subscriptions', '2024-12-31'),
('Kotak Mahindra Bank', 'Zen Credit Card', 'Organic stores', 'Points', '3x points on organic purchases', '2024-12-31'),
('Kotak Mahindra Bank', 'Zen Credit Card', 'Yoga studios', 'Discount', '20% off on wellness sessions', '2024-12-31'),

('Kotak Mahindra Bank', 'White Credit Card', 'Louis Vuitton', 'Experience', 'VIP shopping experiences', '2024-12-31'),
('Kotak Mahindra Bank', 'White Credit Card', 'Taj Hotels', 'Upgrade', 'Complimentary room upgrades', '2024-12-31'),
('Kotak Mahindra Bank', 'White Credit Card', 'Fine dining restaurants', 'Discount', 'Up to 25% off', '2024-12-31'),

('Kotak Mahindra Bank', 'League Credit Card', 'Decathlon', 'Points', '5x points on sports equipment', '2024-12-31'),
('Kotak Mahindra Bank', 'League Credit Card', 'Nike', 'Points', '5x points on athletic wear', '2024-12-31'),
('Kotak Mahindra Bank', 'League Credit Card', 'Gyms & Fitness Centers', 'Discount', '15% off on memberships', '2024-12-31'),

('Kotak Mahindra Bank', 'Royale Credit Card', 'Emirates', 'Miles', 'Double miles on international travel', '2024-12-31'),
('Kotak Mahindra Bank', 'Royale Credit Card', 'Luxury hotels', 'Upgrade', 'Automatic suite upgrades', '2024-12-31'),
('Kotak Mahindra Bank', 'Royale Credit Card', 'Michelin restaurants', 'Access', 'Priority reservations', '2024-12-31'),

('Kotak Mahindra Bank', 'Privy Credit Card', 'Exclusive brands', 'Access', 'Private shopping sessions', '2024-12-31'),
('Kotak Mahindra Bank', 'Privy Credit Card', 'Private jets', 'Booking', 'Preferred rates and availability', '2024-12-31'),

('Kotak Mahindra Bank', 'Urbane Credit Card', 'Urban Ladder', 'Discount', '10% off on furniture', '2024-12-31'),
('Kotak Mahindra Bank', 'Urbane Credit Card', 'Zomato', 'Cashback', '15% cashback in urban areas', '2024-12-31'),

('Kotak Mahindra Bank', 'Business Credit Card', 'Office supplies stores', 'Points', '4x points on business purchases', '2024-12-31'),
('Kotak Mahindra Bank', 'Business Credit Card', 'Business hotels', 'Discount', 'Corporate rates and benefits', '2024-12-31'); 