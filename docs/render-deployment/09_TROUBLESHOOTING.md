# Forge Ecosystem - Troubleshooting Guide

**Document Version:** 1.0.0
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Common Issues

### Service Unavailable (503)

**Symptom**: Service returns 503 or doesn't respond

**Causes & Solutions**:

1. **Cold Start (Free Tier)**
   - **Cause**: Service spins down after 15 minutes inactivity
   - **Solution**: Wait 60-90 seconds for spin-up, or use Forge Command "Wake All"
   - **Prevention**: Upgrade to Render Starter plan ($7/month, no spin-down)

2. **Database Connection Failed**
   - **Cause**: PostgreSQL not running or DATABASE_URL incorrect
   - **Check**: Render Dashboard → Database status
   - **Solution**: Verify DATABASE_URL in service environment variables

3. **Deployment Failed**
   - **Cause**: Build error or health check timeout
   - **Check**: Render Dashboard → Logs tab
   - **Solution**: Fix build errors and redeploy

---

### Slow Response Times

**Symptom**: API requests take > 5 seconds

**Causes & Solutions**:

1. **Cold Start Delay**
   - **Cause**: First request after spin-down
   - **Solution**: Use "Wake All" in Forge Command before critical operations

2. **Database Query Slow**
   - **Cause**: Missing index or N+1 queries
   - **Check**: Enable query logging, use EXPLAIN ANALYZE
   - **Solution**: Add database indexes:
     ```sql
     CREATE INDEX idx_name ON table(column);
     ```

3. **Redis Cache Miss**
   - **Cause**: Redis not configured or cache cleared
   - **Check**: Verify REDIS_URL environment variable
   - **Solution**: Configure Redis Cloud (free tier available)

4. **LLM Provider Timeout**
   - **Cause**: OpenAI/Anthropic API slow or rate limited
   - **Check**: NeuroForge logs for "timeout" errors
   - **Solution**: Increase timeout, implement retry logic

---

### Authentication Errors (401)

**Symptom**: "Unauthorized" or "Invalid token"

**Causes & Solutions**:

1. **Token Expired**
   - **Cause**: JWT token older than 24 hours
   - **Solution**: Refresh token via `/api/v1/auth/refresh`

2. **Invalid JWT Secret**
   - **Cause**: JWT_SECRET_KEY mismatch between services
   - **Solution**: Ensure all services use same JWT_SECRET_KEY

3. **Missing Authorization Header**
   - **Cause**: Client not sending `Authorization: Bearer <token>`
   - **Solution**: Add header to all authenticated requests

---

### Database Issues

#### Connection Pool Exhausted

**Symptom**: "QueuePool limit exceeded"

**Solution**:
```python
# Increase pool size in database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Up from 10
    max_overflow=40  # Up from 20
)
```

#### Migration Failed

**Symptom**: Alembic error during deployment

**Solution**:
```bash
# Rollback migration
alembic downgrade -1

# Fix migration file
# Edit alembic/versions/xxx.py

# Reapply
alembic upgrade head
```

#### Database Full (Free Tier Limit)

**Symptom**: "disk full" error

**Check**:
```sql
SELECT pg_size_pretty(pg_database_size('dataforge'));
```

**Solution**:
1. Delete old data:
   ```sql
   DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '90 days';
   VACUUM FULL;
   ```
2. Upgrade to paid plan (10GB+ storage)

---

### Service-Specific Issues

#### DataForge

**pgvector Extension Not Found**

**Symptom**: "type 'vector' does not exist"

**Solution**:
```sql
-- Connect to database
psql <DATABASE_URL>

-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;
```

**Embedding Generation Failed**

**Symptom**: "VoyageAI API key invalid"

**Solution**:
- Verify `VOYAGE_API_KEY` in environment variables
- Test API key: `curl https://api.voyageai.com/v1/embeddings -H "Authorization: Bearer $VOYAGE_API_KEY"`

#### NeuroForge

**Model Not Available**

**Symptom**: "Model 'gpt-4' not found"

**Solution**:
- Check `OPENAI_API_KEY` is valid
- Verify model name is correct (e.g., `gpt-4-turbo-preview`)
- Check OpenAI account has access to model

**Context Retrieval Failed**

**Symptom**: "DataForge unreachable"

**Solution**:
- Verify `DATAFORGE_BASE_URL` points to correct service
- Check DataForge health: `curl https://dataforge.onrender.com/health`

#### ForgeAgents

**Agent Execution Timeout**

**Symptom**: Agent stops responding after 5 minutes

**Solution**:
- Increase `DEFAULT_EXECUTION_TIMEOUT` in environment variables
- Check for infinite loops in agent logic

**Tool Adapter Failed**

**Symptom**: "Rake adapter connection refused"

**Solution**:
- Verify `RAKE_URL`, `NEUROFORGE_URL`, `DATAFORGE_URL` are correct
- Check target service health

#### Rake

**Job Stuck in 'pending'**

**Symptom**: Job never starts processing

**Solution**:
- Check worker processes are running
- Verify Redis connection (if using Celery)
- Restart Rake service

**Embedding Generation Failed**

**Symptom**: "OpenAI API rate limit exceeded"

**Solution**:
- Reduce `MAX_WORKERS` to slow down requests
- Implement exponential backoff
- Upgrade OpenAI tier for higher rate limits

---

## Error Code Reference

### 4xx Client Errors

| Code | Error | Solution |
|------|-------|----------|
| `400` | Bad Request | Check request body format |
| `401` | Unauthorized | Refresh JWT token |
| `403` | Forbidden | Check user permissions |
| `404` | Not Found | Verify resource ID exists |
| `409` | Conflict | Resource already exists |
| `422` | Validation Error | Fix input data |
| `429` | Rate Limit | Wait or upgrade tier |

### 5xx Server Errors

| Code | Error | Solution |
|------|-------|----------|
| `500` | Internal Server Error | Check logs, report bug |
| `502` | Bad Gateway | External API down |
| `503` | Service Unavailable | Cold start or maintenance |
| `504` | Gateway Timeout | Increase timeout |

---

## Emergency Procedures

### Service Completely Down

1. **Check Render Status**
   - Navigate to Render Dashboard
   - Verify service is "Live" (green)

2. **Check Logs**
   - Click on service → Logs tab
   - Look for startup errors

3. **Rollback if Needed**
   - Click Deploys tab
   - Find last working deployment
   - Click "Redeploy"

4. **Manual Restart**
   - Click Manual Deploy → Clear build cache & deploy

### Database Corruption

1. **Stop All Services**
   - Temporarily disable in Render Dashboard

2. **Restore from Backup**
   - Database → Backups tab
   - Select backup from before corruption
   - Click Restore (CAUTION: overwrites data)

3. **Restart Services**
   - Re-enable services

4. **Verify Data Integrity**
   - Run data validation queries

### Total Ecosystem Failure

1. **Create Incident Channel**
   - Slack/Discord for coordination

2. **Check External Dependencies**
   - Render status page
   - OpenAI status page
   - Database provider status

3. **Parallel Debugging**
   - DataForge team checks database
   - NeuroForge team checks LLM connections
   - ForgeAgents team checks agent logic

4. **Rollback to Last Known Good**
   - Identify last working deployment across all services
   - Rollback all services to those versions

---

## Performance Debugging

### High CPU Usage

```bash
# Check PostgreSQL CPU
SELECT query, state, query_start
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

# Kill long-running query
SELECT pg_terminate_backend(pid);
```

### High Memory Usage

```bash
# Check memory per service (Render Dashboard)
# Upgrade plan if consistently at limit

# Optimize Python memory
import gc
gc.collect()  # Force garbage collection
```

### Slow Queries

```sql
-- Enable slow query log
ALTER DATABASE dataforge SET log_min_duration_statement = 1000;  -- Log queries > 1s

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## Getting Help

### Self-Service

1. **Check this guide** for common issues
2. **Review logs** in Render Dashboard
3. **Test health endpoints** for all services
4. **Check Forge Command dashboard** for metrics

### Support Channels

- **Email**: charlesboswell@boswelldigitalsolutions.com
- **GitHub Issues**: For bugs in specific repos
- **Documentation**: `/home/charlie/Forge/ecosystem/docs/`

### Reporting Bugs

Include:
- Service name and version
- Steps to reproduce
- Error messages (full stack trace)
- Environment (local, staging, production)
- Relevant logs (last 50 lines)

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
