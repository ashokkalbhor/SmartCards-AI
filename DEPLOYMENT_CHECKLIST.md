# Deployment Checklist: Admin Card Update System

## Pre-Deployment Checks

### ✅ Dependencies
- [ ] `beautifulsoup4==4.14.2` installed
- [ ] `aiohttp==3.12.15` installed
- [ ] `apscheduler==3.11.0` installed
- [ ] OpenAI API key configured in environment
- [ ] `OPENAI_MODEL=gpt-5` set in config

### ✅ Database
- [ ] Tables exist:
  - [ ] `card_master_data`
  - [ ] `card_spending_categories`
  - [ ] `card_merchant_rewards`
  - [ ] `edit_suggestions`
  - [ ] `community_posts`
  - [ ] `user_roles`
- [ ] At least one admin user exists
- [ ] Admin user has active role in `user_roles`

### ✅ Configuration
- [ ] `terms_and_conditions_url` populated for cards to be updated
- [ ] Trusted bank domains list reviewed
- [ ] Scheduler cron timing configured (default: 1st of month at midnight)
- [ ] Rate limiting configured (default: 5 cards per batch)

### ✅ Security
- [ ] JWT authentication working
- [ ] Admin role verification tested
- [ ] CORS settings allow frontend domain
- [ ] Rate limiting enabled on API
- [ ] Trusted domain whitelist verified

---

## Testing Checklist

### Unit Tests
```bash
cd backend
source venv311/bin/activate
pytest tests/test_card_update_service.py -v
pytest tests/test_web_scraping_service.py -v
```

- [ ] All card update service tests pass
- [ ] All web scraping service tests pass
- [ ] Mock responses working correctly

### Integration Tests

#### 1. Status Endpoint
```bash
curl -X GET "http://localhost:8000/api/v1/card-updates/status" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```
- [ ] Returns 200 OK
- [ ] Returns correct JSON structure
- [ ] Shows `scheduler_running: true`
- [ ] Non-admin gets 403 Forbidden

#### 2. Extraction Test
```bash
python backend/test_admin_card_updates.py \
  --token YOUR_TOKEN \
  --test extract \
  --url "https://www.hdfcbank.com/personal/pay/cards/credit-cards/regalia" \
  --card-name "Regalia" \
  --bank-name "HDFC Bank"
```
- [ ] Successfully fetches content
- [ ] AI extraction completes
- [ ] Returns structured JSON
- [ ] Untrusted domain returns 400

#### 3. Single Card Update
```bash
python backend/test_admin_card_updates.py \
  --token YOUR_TOKEN \
  --test card \
  --card-id 1
```
- [ ] Card update completes
- [ ] Edit suggestions created
- [ ] No database errors
- [ ] Invalid card ID returns 404

#### 4. Bulk Update (Optional - use with caution)
```bash
python backend/test_admin_card_updates.py \
  --token YOUR_TOKEN \
  --test all
```
- [ ] Process starts in background
- [ ] Status shows `is_running: true`
- [ ] Multiple edit suggestions created
- [ ] Status returns to `is_running: false` after completion

---

## Post-Deployment Validation

### Day 1: Immediate Checks
- [ ] Application starts without errors
- [ ] Scheduler initializes successfully
- [ ] Check logs for startup messages:
  ```
  ✅ Card Update Scheduler initialized successfully
  ```
- [ ] API documentation accessible at `/docs`
- [ ] Admin can access card-updates endpoints

### Week 1: Monitoring
- [ ] No errors in application logs
- [ ] Status endpoint responds correctly
- [ ] Manual trigger tested successfully
- [ ] Edit suggestions appear in admin dashboard
- [ ] Community posts generated on approval

### Month 1: First Automated Run
- [ ] Scheduler runs on 1st of month at midnight
- [ ] Check logs for execution:
  ```
  Starting monthly card update process
  Processing {N} active cards
  Monthly card update process completed
  ```
- [ ] Edit suggestions created for changed data
- [ ] No critical errors during run
- [ ] Processing time reasonable (< 30 min for 100 cards)

---

## Rollback Plan

If issues occur, rollback steps:

### 1. Disable Scheduler
```python
# In backend/app/main.py, comment out:
# card_update_scheduler.start()
```

### 2. Disable Router
```python
# In backend/app/main.py, comment out:
# app.include_router(card_updates_router, ...)
```

### 3. Restart Application
```bash
# Reload app
# The system will run without card update features
```

### 4. Database Cleanup (if needed)
```sql
-- Delete test edit suggestions
DELETE FROM edit_suggestions 
WHERE user_id = (SELECT id FROM users WHERE email = 'system-updater@smartcards.ai');

-- Delete test community posts
DELETE FROM community_posts 
WHERE user_id = (SELECT id FROM users WHERE email = 'system-updater@smartcards.ai');
```

---

## Monitoring Setup

### Application Logs
```bash
# Watch card update logs
tail -f /var/log/smartcards/app.log | grep "Card Update"

# Watch error logs
tail -f /var/log/smartcards/app.log | grep "ERROR"
```

### Key Metrics to Track
- **Success Rate**: % of cards successfully processed
- **Processing Time**: Time to complete all cards
- **Error Rate**: Failed extractions per run
- **Approval Rate**: % of suggestions approved by admins
- **Data Quality**: Accuracy of extracted data

### Alerts to Set Up
- [ ] Alert if scheduler fails to start
- [ ] Alert if update process runs > 60 minutes
- [ ] Alert if error rate > 20%
- [ ] Alert if extraction fails for multiple cards
- [ ] Daily summary email of edit suggestions

---

## Documentation Verification

### For Admins
- [ ] [ADMIN_CARD_UPDATES.md](ADMIN_CARD_UPDATES.md) accessible
- [ ] [ADMIN_QUICK_REFERENCE.md](ADMIN_QUICK_REFERENCE.md) accessible
- [ ] [ADMIN_VISUAL_GUIDE.md](ADMIN_VISUAL_GUIDE.md) accessible
- [ ] Test script (`test_admin_card_updates.py`) documented
- [ ] Admin training completed

### For Developers
- [ ] [ADMIN_IMPLEMENTATION_SUMMARY.md](ADMIN_IMPLEMENTATION_SUMMARY.md) reviewed
- [ ] [copilot-instructions.md](.github/copilot-instructions.md) updated
- [ ] README.md mentions admin features
- [ ] API docs (`/docs`) include card-updates section

---

## Performance Optimization

### Before Production
- [ ] Database indexes on frequently queried fields:
  ```sql
  CREATE INDEX idx_card_master_active ON card_master_data(is_active);
  CREATE INDEX idx_card_master_url ON card_master_data(terms_and_conditions_url);
  CREATE INDEX idx_edit_suggestions_status ON edit_suggestions(status);
  CREATE INDEX idx_edit_suggestions_user ON edit_suggestions(user_id);
  ```
- [ ] Connection pooling configured
- [ ] Redis caching enabled (if applicable)
- [ ] APScheduler job store optimized

### During Production
- [ ] Monitor database query performance
- [ ] Monitor API response times
- [ ] Monitor OpenAI API rate limits
- [ ] Adjust batch size if needed
- [ ] Tune delays between batches

---

## Security Hardening

### Pre-Production
- [ ] API keys stored in environment variables (not code)
- [ ] Admin endpoints require authentication + authorization
- [ ] SQL injection protection verified (using ORM)
- [ ] Rate limiting configured
- [ ] HTTPS enabled in production
- [ ] Trusted domain list minimal and verified

### Production
- [ ] Review admin user list
- [ ] Audit logs enabled for all admin actions
- [ ] Monitor for suspicious activity
- [ ] Regular security updates applied
- [ ] Backup strategy in place

---

## Disaster Recovery

### Backup Strategy
- [ ] Database backups configured (daily)
- [ ] Configuration backups stored securely
- [ ] Backup restoration tested

### Recovery Procedures
1. **Scheduler Won't Start**
   - Check logs for specific error
   - Verify APScheduler installation
   - Restart application

2. **Extractions Failing**
   - Check OpenAI API key validity
   - Verify API rate limits not exceeded
   - Check bank website accessibility
   - Review AI prompt if needed

3. **Edit Suggestions Not Created**
   - Check system user exists
   - Verify database permissions
   - Review comparison logic
   - Check logs for exceptions

4. **Database Corruption**
   - Restore from latest backup
   - Rerun failed updates
   - Verify data integrity

---

## Success Criteria

System is considered successfully deployed when:

- ✅ All tests pass
- ✅ Scheduler starts automatically on app launch
- ✅ Admin can manually trigger updates
- ✅ Edit suggestions are created for changes
- ✅ Approval workflow functions correctly
- ✅ Community posts are generated
- ✅ No critical errors in logs for 7 days
- ✅ First automated run completes successfully
- ✅ Admin team trained and comfortable using system

---

## Support Contacts

### Technical Issues
- **Backend Team**: backend@smartcards.ai
- **DevOps Team**: devops@smartcards.ai
- **On-Call**: [Phone/Slack]

### Business Issues
- **Product Manager**: pm@smartcards.ai
- **Admin Team Lead**: admin@smartcards.ai

---

## Appendix: Environment Variables

Required environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5

# Database (if not using defaults)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Application
SECRET_KEY=your-secret-key-here
API_V1_STR=/api/v1
ALLOWED_ORIGINS=https://yourdomain.com

# Optional: Custom Scheduler Settings
CARD_UPDATE_DAY=1
CARD_UPDATE_HOUR=0
CARD_UPDATE_MINUTE=0
```

---

**Deployment Date**: _____________  
**Deployed By**: _____________  
**Verified By**: _____________  
**Sign-off**: _____________

---

**Status**: Ready for deployment ✅
