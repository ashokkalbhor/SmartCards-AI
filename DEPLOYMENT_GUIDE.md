# 🚀 SmartCards AI Deployment Guide

## 🛡️ Safety First - Backward Compatibility

This deployment maintains full backward compatibility with your existing codebase.

## 📋 Pre-Deployment Checklist

### ✅ Current Status
- [x] Using Create React App (stable) instead of Vite
- [x] Backend configured for Railway
- [x] Database initialized and working
- [x] Environment variables configured
- [x] All dependencies installed

### 🔧 Required Setup

#### 1. Environment Variables (Set in Railway Dashboard)
```
OPENAI_API_KEY=your_actual_openai_api_key
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your_production_secret_key
```

#### 2. Database Setup
- SQLite database will be created automatically
- For production, consider PostgreSQL (Railway supports this)

## 🚀 Deployment Options

### Option 1: Railway (Recommended)
**Pros**: Easy, free tier, handles both frontend and backend
**Cons**: Limited free tier usage

#### Steps:
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your repository
4. Set environment variables
5. Deploy

### Option 2: Vercel (Frontend) + Railway (Backend)
**Pros**: Excellent performance, great free tier
**Cons**: Need to deploy separately

#### Frontend (Vercel):
1. Go to [Vercel.com](https://vercel.com)
2. Import your repository
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/build`

#### Backend (Railway):
1. Deploy backend to Railway
2. Update frontend API URL to point to Railway backend

### Option 3: Render
**Pros**: Good free tier, easy deployment
**Cons**: Slower cold starts

## 🔄 Rollback Plan

If anything goes wrong:

1. **Immediate Rollback**: `git checkout main`
2. **Revert Changes**: `git revert deployment-safe`
3. **Restore Local**: `git pull origin main`

## 📊 Monitoring

### Health Checks
- Backend: `https://your-app.railway.app/health`
- Frontend: Check Vercel/Railway dashboard

### Environment Variables
Make sure these are set in production:
- `OPENAI_API_KEY`
- `ENVIRONMENT=production`
- `SECRET_KEY` (generate a strong one)

## 🐛 Troubleshooting

### Common Issues:
1. **Build Failures**: Check `requirements-prod.txt` for missing dependencies
2. **Environment Variables**: Ensure all required vars are set
3. **Database Issues**: Check if SQLite file is being created
4. **CORS Issues**: Update `ALLOWED_ORIGINS` for your domain

### Debug Commands:
```bash
# Check backend logs
railway logs

# Check frontend build
npm run build

# Test locally
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔗 URLs After Deployment

- **Frontend**: `https://your-app.vercel.app` or `https://your-app.railway.app`
- **Backend API**: `https://your-backend.railway.app`
- **API Docs**: `https://your-backend.railway.app/docs`

## 📝 Post-Deployment Checklist

- [ ] Test all API endpoints
- [ ] Verify frontend loads correctly
- [ ] Check database connectivity
- [ ] Test OpenAI integration
- [ ] Monitor error logs
- [ ] Update DNS if using custom domain

## 🆘 Support

If you encounter issues:
1. Check the logs in your deployment platform
2. Verify environment variables are set correctly
3. Test locally first: `npm start` and `python3 -m uvicorn app.main:app`
4. Rollback to previous working version if needed 