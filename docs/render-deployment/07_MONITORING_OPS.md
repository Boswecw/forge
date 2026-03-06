# Forge Ecosystem - Monitoring & Operations

**Document Version:** 1.0.0
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Monitoring Tools

### 1. Forge Command (Primary)

**Real-Time Dashboard** (Tauri Desktop App):
- Service health status (DataForge, NeuroForge, ForgeAgents, Rake)
- API latency tracking (P50/P90/P99)
- Token usage and costs
- Error rates and alerts
- "Wake All" feature (prevent cold starts)

### 2. Render Dashboard

**Infrastructure Monitoring**:
- Service logs (real-time streaming)
- Deployment history
- Database metrics (connections, storage, queries/sec)
- Health check status

### 3. Prometheus + Grafana

**Metrics Collection**:
- Request throughput (RPS)
- Response times (histograms)
- Error rates (4xx/5xx)
- Database connection pool
- Cache hit rates

---

## Health Checks

### Endpoints

| Service | Endpoint | Timeout |
|---------|----------|---------|
| **DataForge** | `GET /health` | 60s |
| **NeuroForge** | `GET /health` | 60s |
| **ForgeAgents** | `GET /health/render` | 60s |
| **Rake** | `GET /health/render` | 60s |

### Health Response

```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T12:00:00Z",
  "service": "DataForge",
  "version": "5.2.0",
  "dependencies": {
    "database": "connected",
    "redis": "connected"
  },
  "metrics": {
    "uptime_seconds": 3600,
    "requests_total": 1523,
    "errors_total": 2
  }
}
```

---

## Incident Response Runbook

### P0: Service Down (Critical)

**Detection**:
- Health check fails
- 100% error rate in Forge Command

**Response**:
1. Check Render dashboard for service status
2. Check deployment logs for errors
3. Verify database connectivity
4. Rollback to last working deployment if needed
5. Notify stakeholders

**SLA**: 15 minutes to resolution

### P1: Performance Degradation (High)

**Detection**:
- P95 latency > 5 seconds
- Error rate > 5%

**Response**:
1. Check database slow queries
2. Verify Redis cache hit rate
3. Check for cold starts (spin-up delays)
4. Scale up if needed (upgrade Render plan)

**SLA**: 1 hour to resolution

### P2: Isolated Issues (Medium)

**Detection**:
- Single endpoint failing
- Specific user affected

**Response**:
1. Review logs for specific error
2. Check for data corruption
3. Fix bug and deploy
4. Notify affected users

**SLA**: 4 hours to resolution

---

## Performance Optimization

### Database Optimization

```sql
-- Add index for slow query
CREATE INDEX idx_name ON table(column);

-- Analyze query performance
EXPLAIN ANALYZE SELECT ...;

-- Vacuum database (reclaim space)
VACUUM ANALYZE;
```

### Cache Optimization

```python
# Increase cache hit rate
redis.setex(key, ttl=3600, value)  # Longer TTL

# Monitor cache metrics
cache_hit_rate = hits / (hits + misses)
```

### Connection Pooling

```python
# Increase pool size if connections exhausted
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Up from 10
    max_overflow=40  # Up from 20
)
```

---

## Backup & Recovery

### Automated Backups (Render)

- **Frequency**: Daily
- **Retention**: 7 days (Free Tier), 30 days (Paid)
- **Storage**: Render-managed

### Manual Backup

```bash
# Backup database
pg_dump <DATABASE_URL> > backup_$(date +%Y%m%d).sql

# Restore database (CAUTION: overwrites data)
psql <DATABASE_URL> < backup_20260205.sql
```

### Point-in-Time Recovery

Not available on Free Tier. Upgrade to Starter plan for PITR.

---

## Alerting

### Alert Channels

- Forge Command desktop notifications
- Email (via SMTP)
- Slack/Discord webhooks (optional)
- PagerDuty (optional)

### Alert Thresholds

| Alert | Condition | Severity |
|-------|-----------|----------|
| **Service Down** | Health check fails | P0 |
| **High Error Rate** | Error rate > 10% | P1 |
| **High Latency** | P95 > 5s | P1 |
| **Database Full** | Storage > 900MB | P1 |
| **Cost Spike** | Daily cost > $10 | P2 |

---

## Common Operations

### Wake Services (Prevent Cold Starts)

```bash
# Using Forge Command "Wake All" button
# OR manually:
curl https://dataforge.onrender.com/health
curl https://neuroforge.onrender.com/health
curl https://forgeagents.onrender.com/health
curl https://rake.onrender.com/health
```

### View Logs

```bash
# Via Render Dashboard: Logs tab
# OR via Render CLI:
render logs --service=dataforge --tail
```

### Restart Service

```bash
# Via Render Dashboard: Manual Deploy → Clear build cache & deploy
# OR via Render CLI:
render deploy --service=dataforge
```

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
