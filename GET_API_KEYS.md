# 🔑 Quick API Key Setup Guide

## Get Your Free API Keys (5 minutes)

### 🎯 Tavily API Key (Recommended - 1,000 free searches/month)

1. **Visit**: https://tavily.com
2. **Click**: "Get API Key" or "Start Free"
3. **Sign Up**: Use your email (NO credit card required)
4. **Copy Key**: Will look like `tvly-xxxxxxxxxxxxxxxxxxxxx`
5. **Paste in `.env`**:
   ```bash
   TAVILY_API_KEY=tvly-your-actual-key-here
   ```

---

### 🎯 Serper API Key (Optional - 2,500 free searches/month)

1. **Visit**: https://serper.dev
2. **Click**: "Sign Up" 
3. **Sign Up**: With Google or email (NO credit card required)
4. **Dashboard**: Go to https://serper.dev/dashboard
5. **Copy Key**: Click "Show API Key"
6. **Paste in `.env`**:
   ```bash
   SERPER_API_KEY=your-actual-key-here
   ```

---

## 📝 Your .env File Location

```
/Users/ashokkumarkalbhor/SmartCards-AI/backend/.env
```

---

## ✅ After Adding Keys

1. **Save** the `.env` file
2. **Test** with:
   ```bash
   cd /Users/ashokkumarkalbhor/SmartCards-AI/backend
   python test_search_apis.py
   ```
3. **Restart** your backend server (if running)

---

## 🎯 Recommended Setup

**Minimum**: Get Tavily key (1,000 searches/month - enough for your needs)

**Optimal**: Get both Tavily + Serper (3,500 searches/month - excellent redundancy)

---

## 💡 Pro Tip

You can start with just **Tavily** - it's AI-optimized and perfect for credit card research. Add Serper later if you need more capacity.

---

**Ready?** Get your keys and I'll help you test! 🚀
