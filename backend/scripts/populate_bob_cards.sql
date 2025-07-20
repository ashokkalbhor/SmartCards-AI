-- Bank of Baroda (BOBCARD) Credit Cards Population Script
-- Comprehensive portfolio: Entry-level to Super-premium cards
-- 23+ cards covering all segments including professional, defense, and co-branded cards

INSERT INTO card_master_data (
    bank_name, card_name, card_variant, card_network, card_tier, 
    joining_fee, annual_fee, is_lifetime_free,
    minimum_age, maximum_age, 
    domestic_lounge_visits, international_lounge_visits,
    reward_program_name, description, additional_features,
    created_at, updated_at
) VALUES

-- Premium Lifestyle Cards
('Bank of Baroda', 'BOBCARD ETERNA', 'Premium Lifestyle', 'Mastercard', 'Premium', 
 2499, 2499, 0, 21, 65, -1, 0, 'BOB Rewards',
 '15 RP per ₹100 on Travel, Dining, International & Online Shopping; 3 RP per ₹100 on other spends',
 '{"key_benefits": "Unlimited domestic lounge access, 6-month FitPass Pro membership, ₹1 crore air accident cover, BOGO movie tickets", "spending_categories": "Travel,Dining,Online Shopping,Entertainment", "merchant_rewards": "MasterCard Priceless offers,District app movie benefits,FitPass Pro fitness network"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'BOBCARD TIARA', 'Women''s Premium', 'Mastercard', 'Premium', 
 2499, 2499, 0, 21, 65, -1, 0, 'BOB Rewards',
 'Accelerated rewards on health, beauty & shopping; Health packages included',
 '{"key_benefits": "Amazon Prime/Disney Hotstar membership, Myntra & Flipkart vouchers, Lakme Salon benefits, Women-centric health insurance", "spending_categories": "Health & Beauty,Shopping,Entertainment,Wellness", "merchant_rewards": "Myntra,Flipkart,Nykaa,BigBasket,Lakme Salon,Swiggy One"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Travel & Experience Cards  
('Bank of Baroda', 'BOBCARD PREMIER', 'Travel Premium', 'Visa', 'Premium',
 1000, 1000, 0, 21, 65, 2, 0, 'BOB Rewards',
 '10 RP per ₹100 on Travel, Dining & International spends; 2 RP per ₹100 on other spends',
 '{"key_benefits": "Quarterly airport lounge access, travel deals & benefits, 24x7 concierge services", "spending_categories": "Travel,Dining,International", "merchant_rewards": "Travel booking portals,Hotel bookings,Restaurant partnerships"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Everyday Rewards Cards
('Bank of Baroda', 'BOBCARD SELECT', 'Online Shopping', 'Mastercard', 'Standard',
 750, 750, 0, 18, 65, 0, 0, 'BOB Rewards',
 '5 RP per ₹100 on Dining, Online Shopping & Utility bills; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Cashback redemption options, fuel surcharge waiver, online shopping acceleration", "spending_categories": "Online Shopping,Dining,Utilities", "merchant_rewards": "E-commerce platforms,Online bill payment,Digital wallets"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'BOBCARD EASY', 'Everyday Rewards', 'Mastercard', 'Standard',
 0, 0, 1, 18, 65, 0, 0, 'BOB Rewards',
 '5 RP per ₹100 on Department Stores, Groceries & Movies; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free, fuel surcharge waiver, easy EMI conversion, reward redemption flexibility", "spending_categories": "Grocery,Movies,Department Stores", "merchant_rewards": "Supermarkets,Cinema chains,Retail stores"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'BOBCARD PRIME', 'Secured Basic', 'Mastercard', 'Basic',
 0, 0, 1, 18, 65, 0, 0, 'BOB Rewards',
 '4 RP per ₹100 on all spends; FD-backed card',
 '{"key_benefits": "Lifetime free, secured against FD, guaranteed issuance, reward points on spend", "spending_categories": "All Categories", "merchant_rewards": "Universal acceptance,All merchant categories"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Co-branded Cards
('Bank of Baroda', 'HPCL BOBCARD ENERGIE', 'Fuel Co-branded', 'Mastercard', 'Standard',
 499, 499, 0, 18, 65, 4, 0, 'BOB Rewards',
 '24 RP per ₹150 on HPCL fuel; 4 RP per ₹150 on Grocery; 2 RP per ₹150 on other spends',
 '{"key_benefits": "Up to 80 liters free fuel annually, 25% discount on movie tickets, domestic lounge access", "spending_categories": "Fuel,Grocery,Movies", "merchant_rewards": "HPCL pumps,BookMyShow,Grocery stores"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'IRCTC BOBCARD', 'Railway Travel', 'RuPay', 'Standard',
 500, 350, 0, 18, 65, 4, 0, 'BOB Rewards',
 'Up to 40 RP per ₹100 on IRCTC bookings; 4 RP per ₹100 on Grocery; 2 RP per ₹100 on other spends',
 '{"key_benefits": "Up to 10% savings on train tickets, railway lounge access, travel convenience", "spending_categories": "Railway Travel,Grocery,Travel", "merchant_rewards": "IRCTC website & app,Railway lounges,Travel bookings"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'SNAPDEAL BOBCARD', 'E-commerce', 'RuPay', 'Standard',
 249, 249, 0, 18, 65, 0, 0, 'BOB Rewards',
 '5% unlimited cashback on Snapdeal; 10 RP per ₹100 on Online Shopping; 4 RP per ₹100 on other spends',
 '{"key_benefits": "Shopping vouchers worth ₹500, everyday shopping rewards, auto-credited cashback", "spending_categories": "E-commerce,Online Shopping", "merchant_rewards": "Snapdeal platform,Online retailers,Digital shopping"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Digital & Fintech Cards
('Bank of Baroda', 'One BOBCARD', 'Metal Digital', 'Visa', 'Premium',
 0, 0, 1, 18, 65, 0, 0, 'OneCard Rewards',
 '1% unlimited shopping rewards; 1% forex markup; Metal card with app control',
 '{"key_benefits": "India''s best metal credit card, dedicated OneCard app, full-stack tech, user control", "spending_categories": "All Categories,International", "merchant_rewards": "Universal merchant acceptance,International usage"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'Uni GoldX BOBCARD', 'Digital Gold', 'Mastercard', 'Premium',
 0, 0, 1, 18, 65, 0, 0, 'Uni Gold Rewards',
 '1% Gold rewards on all spends; Up to 5% Gold on Uni Store; 0% forex markup',
 '{"key_benefits": "Earn 24K digital gold, appreciate over time, Uni Store benefits, zero forex", "spending_categories": "All Categories,International,Gold Investment", "merchant_rewards": "Uni Store,Gold accumulation,International merchants"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Professional Cards
('Bank of Baroda', 'ICAI EXCLUSIVE BOBCARD', 'Professional CA', 'Mastercard', 'Premium',
 0, 0, 1, 21, 65, 12, 0, 'BOB Rewards',
 '5 RP per ₹100 on Dining, Utility & Online; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free for ICAI members, airport lounge access, FitPass Pro membership, professional insurance", "spending_categories": "Professional Services,Dining,Utilities", "merchant_rewards": "Professional platforms,Accounting software,Business services"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'ICSI DIAMOND BOBCARD', 'Professional CS', 'Mastercard', 'Premium',
 0, 0, 1, 21, 65, 12, 0, 'BOB Rewards',
 '5 RP per ₹100 on Dining, Utility & Online; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free for ICSI members, airport lounge access, FitPass Pro membership, professional benefits", "spending_categories": "Professional Services,Dining,Utilities", "merchant_rewards": "Company secretary services,Professional development,Business platforms"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'CMA ONE BOBCARD', 'Professional CMA', 'Mastercard', 'Premium',
 1, 0, 0, 21, 65, 12, 0, 'BOB Rewards',
 '5 RP per ₹100 on Dining, Utility & Online; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Exclusive for ICMAI members, FitPass Pro membership, professional indemnity insurance, airport lounge access", "spending_categories": "Professional Services,Dining,Utilities", "merchant_rewards": "Cost accounting services,Professional training,Business consulting"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Defense & Government Cards
('Bank of Baroda', 'Indian Army YODDHA BOBCARD', 'Defense Army', 'Mastercard', 'Premium',
 0, 0, 1, 18, 65, 8, 0, 'BOB Rewards',
 '10 RP per ₹100 on Grocery & Department Stores; 2 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free for Army personnel, Amazon Prime membership, airport lounge access, FitPass Pro membership", "spending_categories": "Grocery,Department Stores,Defense Services", "merchant_rewards": "Military canteens,Defense establishments,Grocery chains"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'Indian Navy VARUNAH BOBCARD', 'Defense Navy', 'Mastercard', 'Premium',
 0, 0, 1, 18, 65, 8, 0, 'BOB Rewards',
 'Up to 15 RP per ₹100 on Premium variant; Up to 10 RP per ₹100 on Plus variant; Up to 5 RP per ₹100 on Base variant',
 '{"key_benefits": "Multiple variants, Amazon Prime membership, FitPass Pro membership, airport lounge access, exclusive benefits", "spending_categories": "Defense Services,General Spending", "merchant_rewards": "Naval establishments,Defense services,General merchants"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'Indian Coast Guard RAKSHAMAH BOBCARD', 'Defense Coast Guard', 'Mastercard', 'Premium',
 0, 0, 1, 18, 65, 8, 0, 'BOB Rewards',
 '5 RP per ₹100 on Grocery & Department Stores; 2 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free for Coast Guard personnel, airport lounge access, exclusive memberships, FitPass Pro", "spending_categories": "Defense Services,Grocery,Department Stores", "merchant_rewards": "Coast Guard facilities,Maritime services,Defense establishments"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'Assam Rifles The SENTINEL BOBCARD', 'Defense Assam Rifles', 'Mastercard', 'Premium',
 0, 0, 1, 18, 65, 8, 0, 'BOB Rewards',
 '5 RP per ₹100 on Grocery & Department Stores; 2 RP per ₹100 on other spends',
 '{"key_benefits": "First credit card for Assam Rifles, lifetime free, airport lounge access, Amazon Prime membership", "spending_categories": "Defense Services,Grocery,Department Stores", "merchant_rewards": "Assam Rifles establishments,Defense services,Border area merchants"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'VIKRAM BOBCARD', 'Defense General', 'Mastercard', 'Standard',
 0, 0, 1, 18, 65, 0, 0, 'BOB Rewards',
 '5 RP per ₹100 on Grocery, Movies & Department Stores; 1 RP per ₹100 on other spends',
 '{"key_benefits": "Lifetime free for all defense personnel, Disney Hotstar subscription, value-for-money perks", "spending_categories": "Defense Services,Grocery,Movies", "merchant_rewards": "Defense establishments,Entertainment platforms,Grocery stores"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Business Cards
('Bank of Baroda', 'BOBCARD CORPORATE', 'Business Premium', 'Mastercard', 'Business',
 0, 0, 1, 21, 65, 8, 0, 'BOB Business Rewards',
 '1 RP per ₹100 on other categories; 0.5 RP per ₹100 on selected MCCs',
 '{"key_benefits": "Business operations support, 50 days interest-free credit, airport lounge access, 24x7 support", "spending_categories": "Business Expenses,Corporate Travel,Office Supplies", "merchant_rewards": "B2B platforms,Corporate travel,Business services"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'BOBCARD EMPOWER', 'Business SME', 'Mastercard', 'Business',
 0, 500, 0, 21, 65, 0, 0, 'BOB Business Rewards',
 'Spend-based rewards for proprietors and self-employed; Cashless convenience',
 '{"key_benefits": "Business empowerment, expense management, cashless transactions, spend-based rewards", "spending_categories": "Business Expenses,Professional Services", "merchant_rewards": "SME services,Professional tools,Business platforms"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Regional Bank Cards
('Bank of Baroda', 'BUPB/BGGB/BRKGB PRAGATI BOBCARD', 'Regional Rural Bank', 'RuPay', 'Basic',
 0, 0, 1, 18, 65, 0, 0, 'BOB Rewards',
 'Everyday shopping rewards with Smart EMI options',
 '{"key_benefits": "Lifetime free for regional rural bank customers, growth-focused benefits, Smart EMI facility", "spending_categories": "Rural Banking,Everyday Spending", "merchant_rewards": "Rural merchants,Agricultural services,Local businesses"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

('Bank of Baroda', 'Nainital Bank RENAISSANCE BOBCARD', 'Regional Bank', 'Mastercard', 'Standard',
 0, 250, 0, 18, 65, 0, 0, 'BOB Rewards',
 '5X Rewards on purchases; Fuel surcharge waiver; Smart EMI option',
 '{"key_benefits": "Nainital Bank customer benefits, everyday purchase rewards, fuel benefits", "spending_categories": "Everyday Spending,Fuel", "merchant_rewards": "Regional merchants,Fuel stations,Local businesses"}',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP); 