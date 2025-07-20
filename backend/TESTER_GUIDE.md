# 🧪 Tester Guide - Database Management

Welcome! This guide will help you refresh the database for testing the SmartCards AI application.

## 🚀 Quick Start (Most Common)

### For Windows Users:
1. Open Command Prompt or PowerShell
2. Navigate to the `backend` folder
3. Double-click `refresh_db.bat` OR run:
   ```cmd
   refresh_db.bat
   ```

### For All Platforms:
1. Navigate to the `backend` folder
2. Run:
   ```bash
   python refresh_db.py
   ```

## 📋 What This Does

The refresh script will:
- ✅ **Drop all existing tables** (clean slate)
- ✅ **Create fresh database schema**
- ✅ **Seed with 5 sample credit cards**:
  - SBI Cashback Card
  - HDFC Swiggy Card
  - Axis Ace Card
  - HDFC Millennia Card
  - ICICI Amazon Pay Card
- ✅ **Verify everything is working**

## ⚡ Quick Options

### 🔄 Full Database Refresh (Recommended)
**When to use:** Starting fresh testing session

**Windows:**
```cmd
refresh_db.bat
```

**All platforms:**
```bash
python refresh_db.py
```

### ⚡ Quick Data Refresh (Faster)
**When to use:** Keep database structure, just refresh data

**Windows:**
```cmd
quick_refresh.bat
```

**All platforms:**
```bash
python quick_refresh.py
```

## 🔧 After Running the Script

1. **Start the backend server:**
   ```bash
   python main.py
   ```

2. **Start the frontend (in separate terminal):**
   ```bash
   cd ../frontend
   npm start
   ```

3. **Begin testing!** 🎉

## ✅ Testing Features

After refresh, you can test:

### 🏠 **Dashboard**
- View total cards count
- Click on "Total Cards" to navigate to cards page

### 💳 **Cards Page**
- Browse 5 sample credit cards
- View card details, rewards, and benefits

### 🔍 **Card Comparison**
- Compare multiple cards side by side
- Filter by bank, card tier, etc.

### 🤖 **AI Chatbot**
- Ask questions about cards
- Get personalized recommendations

## 🚨 Troubleshooting

### Script Won't Run?
```bash
# Make sure you're in the backend directory
cd backend

# Check if Python is installed
python --version

# Install dependencies if needed
pip install -r requirements.txt
```

### Database Locked Error?
- Stop the backend server (`Ctrl+C`)
- Close any database browser tools
- Run the script again

### Import Errors?
```bash
# Make sure you're in the backend folder
cd backend
python refresh_db.py
```

## 📞 Need Help?

If you encounter issues:
1. Check that you're in the `backend` directory
2. Ensure Python is installed and working
3. Make sure no other processes are using the database
4. Try the full refresh instead of quick refresh

## 📝 Script Details

| Script | Speed | Use Case |
|--------|-------|----------|
| `refresh_db.py` | Slower | Complete fresh start |
| `quick_refresh.py` | Faster | Data refresh only |
| `refresh_db.bat` | Windows | Easy double-click option |
| `quick_refresh.bat` | Windows | Fast data refresh |

---
**Happy Testing! 🧪✨** 