-- Update Offline Spends reward rate to 0.0 for all cards to match the template

BEGIN TRANSACTION;

-- Update all existing Offline Spends entries to have 0.0 reward rate
UPDATE card_spending_categories 
SET reward_rate = 0.0 
WHERE category_name = 'offline_spends';

COMMIT;

-- Verify the changes
SELECT 
    'Offline Spends reward rates after update:' as description,
    reward_rate,
    COUNT(*) as count
FROM card_spending_categories 
WHERE category_name = 'offline_spends' 
GROUP BY reward_rate;
