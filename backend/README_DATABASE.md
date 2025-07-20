# Database Management Scripts

This directory contains scripts to manage and refresh the SmartCards AI database for testing purposes.

## 🔄 Database Refresh Scripts

### 1. Full Database Refresh (`refresh_db.py`)

**Use this when:** You need a completely clean database from scratch.

```bash
python refresh_db.py
```

**What it does:**
- ✅ Drops all existing tables
- ✅ Creates fresh database schema
- ✅ Seeds with sample card data
- ✅ Verifies database integrity

**⚠️ WARNING:** This will **DELETE ALL DATA** including users, transactions, conversations, etc.

### 2. Quick Data Refresh (`quick_refresh.py`)

**Use this when:** You want to reset data but keep the database structure.

```bash
python quick_refresh.py
```

**What it does:**
- ✅ Clears all existing data
- ✅ Keeps database tables intact
- ✅ Re-seeds with fresh sample data
- ✅ Much faster than full refresh

**⚠️ WARNING:** This will **DELETE ALL DATA** but preserves table structure.

## 📊 Sample Data Included

After running either script, your database will contain:

### Credit Card Master Data
- **5 sample credit cards** with realistic data:
  - SBI Cashback Card
  - HDFC Swiggy Card  
  - Axis Ace Card
  - HDFC Millennia Card
  - ICICI Amazon Pay Card

### Card Features
- ✅ Reward rates for different categories
- ✅ Merchant-specific bonuses
- ✅ Annual fees and joining fees
- ✅ Lounge access benefits
- ✅ Reward program details

## 🛠️ Manual Database Operations

### Initialize Database (First Time)
```bash
python init_db.py
```

### Seed Only Card Data
```bash
python app/scripts/seed_card_master_data.py
```

### Run Migrations
```bash
python migrations/add_card_master_data.py
```

## 🧪 Testing Workflow

### For Complete Fresh Start:
1. `python refresh_db.py` - Full database refresh
2. `python main.py` - Start backend server
3. Open frontend and begin testing

### For Quick Testing Iterations:
1. `python quick_refresh.py` - Quick data refresh
2. Continue testing with fresh data

## 🔍 Verification

Both scripts include verification steps that will show:
- Number of tables created/maintained
- Record counts for each table
- Success/failure status

## ⚠️ Important Notes

1. **Backup Important Data:** These scripts will delete all existing data
2. **Test Environment:** Use these scripts in development/testing only
3. **Dependencies:** Ensure all Python dependencies are installed
4. **Database Connection:** Scripts use the same database configuration as the main application

## 🐛 Troubleshooting

### Common Issues:

**Import Errors:**
```bash
# Make sure you're in the backend directory
cd backend
python refresh_db.py
```

**Permission Errors:**
```bash
# On Unix systems, make scripts executable
chmod +x refresh_db.py quick_refresh.py
```

**Database Lock Errors:**
- Stop the backend server before running scripts
- Close any database browser connections

### Getting Help:

If scripts fail, check:
1. Backend server is stopped
2. No database connections are open
3. All dependencies are installed: `pip install -r requirements.txt`
4. You're running from the `backend` directory

## 📝 Adding More Sample Data

To add more sample data, edit the seeding functions in:
- `app/scripts/seed_card_master_data.py` - For card data
- Create new scripts for users, transactions, etc.

Then update the refresh scripts to call your new seeding functions. 