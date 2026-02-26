# 🚀 Render Deployment - Environment Variables Setup

## ✅ Local Setup (COMPLETED)

Your local environment is now properly configured:
- ✅ `.env` file has `TAVILY_API_KEY` 
- ✅ `.env` is in `.gitignore` (won't be committed)
- ✅ `config.py` reads from environment variables
- ✅ Tavily search is working!

---

## 🌐 Render Deployment Setup

### Step 1: Login to Render Dashboard

1. Go to https://dashboard.render.com
2. Select your **SmartCards-AI backend service**

---

### Step 2: Add Environment Variables

1. In your service dashboard, click on **"Environment"** tab (left sidebar)
2. Scroll to **"Environment Variables"** section
3. Click **"Add Environment Variable"**

---

### Step 3: Add Tavily API Key

Add the following:

| Key | Value |
|-----|-------|
| `TAVILY_API_KEY` | `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` |

**Important**: Click **"Save Changes"** after adding!

---

### Step 4: Optional - Add Serper (if you get it later)

| Key | Value |
|-----|-------|
| `SERPER_API_KEY` | `your-serper-key-here` |

---

### Step 5: Verify Other Required Variables

Make sure these are also set on Render:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DATABASE_URL` | Your database URL |
| `SECRET_KEY` | Your secret key |

---

## 🔄 After Adding Variables

Render will automatically:
1. **Reload environment variables**
2. **Restart your service**
3. Your app will now use Tavily search!

**Note**: No code deployment needed - just adding env vars triggers a restart.

---

## 🧪 Testing on Render

After deployment, test with:

```bash
# From your terminal
curl -X POST https://your-render-app.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "HDFC Regalia rewards rate"}'
```

You should see responses using Tavily search results!

---

## 🔒 Security Best Practices

✅ **DO:**
- Store API keys in Render's Environment Variables
- Keep `.env` in `.gitignore`
- Use different keys for dev/staging/prod if needed

❌ **DON'T:**
- Hardcode API keys in `config.py`
- Commit `.env` file to git
- Share API keys in public repos

---

## 📊 Monitoring

### Check API Usage:
- **Tavily Dashboard**: https://tavily.com/dashboard
- **Serper Dashboard**: https://serper.dev/dashboard

### Check Render Logs:
1. Render Dashboard → Your Service → **"Logs"** tab
2. Look for: `"Attempting search with Tavily..."`
3. Should see: `"Tavily search successful"`

---

## 🆘 Troubleshooting

### "All search providers failed" on Render
**Solution**:
1. Check Render Environment Variables are set correctly
2. Verify no typos in `TAVILY_API_KEY`
3. Check Render logs for specific error messages
4. Restart service manually if needed

### "Module not found: tavily"
**Solution**:
- Ensure `tavily-python==0.7.21` is in `requirements.txt` ✅ (Already added)
- Render will auto-install on next deployment

---

## ✅ Current Status

**Local Development**:
- ✅ Tavily API key configured in `.env`
- ✅ Search working with Tavily
- ✅ Falls back to DuckDuckGo if needed

**Render Deployment**:
- ⏳ Pending: Add `TAVILY_API_KEY` to Render Environment Variables
- ⏳ Pending: Deploy and test

---

## 🎯 Next Steps

1. **Add `TAVILY_API_KEY` to Render** (5 minutes)
2. **Wait for auto-restart** (1-2 minutes)
3. **Test search on production** (1 minute)
4. **Done!** 🎉

Your multi-provider search is now production-ready with:
- 1,000 free Tavily searches/month
- Automatic fallback to DuckDuckGo
- Option to add Serper for 2,500 more searches/month
