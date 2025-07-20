# HDFC Bank Credit Cards Population Guide

This directory contains scripts to populate your master database with comprehensive HDFC Bank credit cards data.

## 📁 Files Included

- `populate_hdfc_cards.sql` - Complete SQL script with 20 HDFC Bank credit cards
- `run_hdfc_population.py` - Python script to execute the SQL population
- `README_HDFC_Population.md` - This documentation file

## 🏦 Credit Cards Included (20 Cards)

### Basic Tier Cards
1. **Millennia Credit Card** - 5% cashback on popular brands
2. **MoneyBack+ Credit Card** - Entry-level cashback rewards
3. **Freedom Credit Card** - Lifestyle and entertainment focused
4. **PixEL Play Credit Card** - Digital RuPay for young professionals
5. **PixEL Go Credit Card** - Entry-level digital RuPay
6. **HDFC RuPay Credit Card** - Basic RuPay with government benefits

### Premium Tier Cards
7. **Regalia Credit Card** - Premium rewards with lounge access
8. **Regalia Gold Credit Card** - Enhanced travel and rewards
9. **Diners Club Privilege Credit Card** - Premium dining rewards
10. **Tata Neu Infinity Credit Card** - Tata ecosystem rewards
11. **Doctor's Regalia Credit Card** - Professional medical practitioners

### Super Premium Tier Cards
12. **Infinia Credit Card** - Ultra-premium metallic by-invitation-only
13. **Diners Club Black Credit Card** - Super-premium unlimited lounge
14. **Diners Club Black Metal Edition** - Elite metallic card

### Co-branded Cards
15. **IndianOil HDFC Credit Card** - Fuel benefits
16. **Swiggy HDFC Bank Credit Card** - Food delivery benefits
17. **IRCTC HDFC Bank Credit Card** - Railway booking benefits
18. **Marriott Bonvoy HDFC Credit Card** - Hotel benefits and points
19. **Shoppers Stop HDFC Bank Credit Card** - Shopping rewards
20. **Harley-Davidson Diners Club Card** - Lifestyle for biking enthusiasts

## 📊 Data Completeness

Each card includes:
- ✅ **Financial Details**: Joining fees, annual fees, waiver conditions
- ✅ **Reward Programs**: Category-wise rates, merchant-specific benefits  
- ✅ **Insurance Coverage**: Accident, hospitalization, liability coverage
- ✅ **Lounge Access**: Domestic and international visits
- ✅ **Eligibility**: Minimum salary, age requirements
- ✅ **Special Benefits**: Concierge, milestone rewards, exclusive memberships
- ✅ **Category Rewards**: Dining, groceries, travel, online shopping, fuel, entertainment
- ✅ **Merchant Rewards**: Amazon, Flipkart, Swiggy, Zomato, BookMyShow, Uber, etc.

## 🚀 How to Execute

### Option 1: Using Python Script (Recommended)
```bash
cd backend/scripts
python run_hdfc_population.py
```

### Option 2: Direct SQL Execution
```bash
psql -d smartcards_ai -f populate_hdfc_cards.sql
```

## ⚙️ Prerequisites

1. **Database Setup**: Ensure your PostgreSQL database is running
2. **Environment Variables**: Set up your `.env` file with database credentials:
   ```
   DB_HOST=localhost
   DB_NAME=smartcards_ai
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```
3. **Python Dependencies**: Install required packages:
   ```bash
   pip install psycopg2-binary python-dotenv
   ```

## 🔍 What Gets Populated

### Main Tables
- `card_master_data` - 20 HDFC Bank credit cards with complete details
- `card_spending_categories` - Category-wise reward rates for key cards
- `card_merchant_rewards` - Merchant-specific benefits (especially for Millennia)

### Sample Data Highlights
- **Millennia Card**: 5% cashback on Amazon, Flipkart, Swiggy, Zomato, etc.
- **Infinia Card**: 3.33% reward rate across all categories, unlimited lounge access
- **Regalia Gold**: Premium travel benefits, Club Vistara Silver membership
- **Diners Club Black**: Unlimited domestic/international lounge access

## 📈 Expected Results

After successful execution:
- ✅ 20 HDFC Bank credit cards in your master database
- ✅ Complete financial and eligibility details
- ✅ Comprehensive reward structure data
- ✅ Ready for comparison engine integration
- ✅ Available in your "Add Card" quick selection

## 🎯 Next Steps

1. **Verify Data**: Check your comparison page to see all HDFC cards
2. **Test Quick Add**: Try adding cards from the master database
3. **Expand Coverage**: Add more banks using similar scripts
4. **Update Regularly**: Keep reward rates and fees current

## 💡 Tips

- **Annual Fee Updates**: Review and update annual fees quarterly
- **Reward Rate Changes**: Banks change reward rates frequently
- **New Card Launches**: Add new cards as HDFC launches them
- **Deactivated Cards**: Mark discontinued cards as `is_active = false`

---

**Generated with comprehensive research from official HDFC Bank sources and industry data.** 