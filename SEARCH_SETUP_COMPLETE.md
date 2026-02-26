# 🔍 Search API Setup Guide

## ✅ Installation Complete!

Multi-provider search with automatic fallback has been installed. You now have access to:
- **Tavily AI Search** (1,000 free searches/month)
- **Serper/Google Search** (2,500 free searches/month)  
- **DuckDuckGo** (Unlimited free fallback)

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Free API Keys

#### Option A: Tavily (Recommended - AI Optimized)
1. Go to https://tavily.com
2. Click "Get API Key" or "Sign Up"
3. Sign up with email (no credit card required)
4. Copy your API key (starts with `tvly-`)

#### Option B: Serper (Google Quality Results)
1. Go to https://serper.dev
2. Click "Sign Up" 
3. Sign up with Google/email (no credit card required)
4. Copy your API key from dashboard

**Recommended**: Get both for maximum reliability!

---

### Step 2: Add API Keys to `.env`

Open `/Users/ashokkumarkalbhor/SmartCards-AI/backend/.env` and add:

```bash
# Search API Keys
TAVILY_API_KEY=tvly-YOUR_KEY_HERE
SERPER_API_KEY=YOUR_SERPER_KEY_HERE
```

---

### Step 3: Test Your Setup

Run the test script:

```bash
cd /Users/ashokkumarkalbhor/SmartCards-AI/backend
python test_search_apis.py
```

You should see:
```
✅ Search Result:
[Source: Tavily AI Search]

Title: HDFC Regalia Credit Card
URL: https://www.hdfcbank.com/...
Content: ...
```

---

## 📊 What You Get

### Free Tier Limits:
| Provider | Monthly Limit | Quality | Speed |
|----------|---------------|---------|-------|
| Tavily | 1,000 | ⭐⭐⭐⭐⭐ | Fast |
| Serper | 2,500 | ⭐⭐⭐⭐⭐ | Fast |
| DuckDuckGo | Unlimited | ⭐⭐⭐ | Slow |

**Total: 3,500+ premium searches/month FREE!**

### Usage Estimate:
- Automated card updates (292 cards): ~600 searches/month
- User chat queries: ~200-500 searches/month
- **Total**: ~800-1,100 searches/month ✅ Well within limits!

---

## 🔧 How It Works

The search tool automatically tries providers in order:

```
1. Try Tavily (best for AI)
   ↓ (if fails or no key)
2. Try Serper (Google quality)
   ↓ (if fails or no key)
3. Use DuckDuckGo (free fallback)
```

No code changes needed - just add API keys and it works!

---

## 🧪 Testing Different Scenarios

### Test with Tavily only:
```bash
# In .env, only set:
TAVILY_API_KEY=tvly-your-key
# Leave SERPER_API_KEY empty
```

### Test with Serper only:
```bash
# In .env, only set:
SERPER_API_KEY=your-key
# Leave TAVILY_API_KEY empty
```

### Test fallback to DuckDuckGo:
```bash
# In .env, comment out both:
# TAVILY_API_KEY=
# SERPER_API_KEY=
```

---

## 📈 Monitoring Usage

### Tavily Dashboard:
- Login to https://tavily.com/dashboard
- View: API calls used, remaining quota, response times

### Serper Dashboard:
- Login to https://serper.dev/dashboard
- View: Credits used, API logs, usage statistics

---

## 🆘 Troubleshooting

### "All search providers failed"
**Solution**: 
1. Check API keys are correctly set in `.env`
2. Restart your FastAPI server to load new env vars
3. Verify API keys are valid (login to provider dashboards)

### "Rate limit exceeded" 
**Solution**:
- This means you've used your monthly quota
- Either wait for next month or add another provider
- DuckDuckGo fallback should still work

### "Import tavily could not be resolved"
**Solution**:
```bash
cd /Users/ashokkumarkalbhor/SmartCards-AI/backend
pip install tavily-python google-search-results
```

---

## 🎯 Next Steps

1. **Get API keys** from Tavily and/or Serper (5 min)
2. **Add to `.env`** file (1 min)
3. **Test** with `python test_search_apis.py` (1 min)
4. **Restart backend** to load new config
5. **Done!** Your search is now production-ready 🎉

---

## 💡 Pro Tips

- **Tavily** is best for AI-specific research (reward rates, features)
- **Serper** is best for general web search (official pages, news)
- **DuckDuckGo** works without API key but can be rate-limited
- Get **both Tavily + Serper** for 3,500 free searches/month!

---

## 📚 Documentation

- Tavily Docs: https://docs.tavily.com
- Serper Docs: https://serper.dev/docs
- LangChain Integration: Already configured in `agent_tools.py`

---

**Need help?** Open an issue or check the logs in `backend_run.log`
