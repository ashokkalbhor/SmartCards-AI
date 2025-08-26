-- Add Offline Spends category to all cards that are missing it
-- With reward rate 0.0 to match the template

BEGIN TRANSACTION;

-- Insert Offline Spends category for all cards that don't have it
INSERT INTO card_spending_categories (
    card_master_id, 
    category_name, 
    category_display_name, 
    reward_rate, 
    reward_type, 
    reward_cap, 
    reward_cap_period, 
    is_active
)
SELECT 
    c.id as card_master_id,
    'offline_spends' as category_name,
    'Offline Spends' as category_display_name,
    0.0 as reward_rate,
    'points' as reward_type,
    NULL as reward_cap,
    NULL as reward_cap_period,
    1 as is_active
FROM card_master_data c
WHERE c.is_active = 1 
AND c.id NOT IN (
    SELECT DISTINCT card_master_id 
    FROM card_spending_categories 
    WHERE category_name = 'offline_spends'
);

COMMIT;

-- Verify the changes
SELECT 
    'Total cards with Offline Spends after update:' as description,
    COUNT(DISTINCT card_master_id) as count
FROM card_spending_categories 
WHERE category_name = 'offline_spends';
