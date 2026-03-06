# Forge Ecosystem - Deployment Guide

**Document Version:** 1.0.1
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Prerequisites](#prerequisites)
3. [Render.com Setup](#rendercom-setup)
4. [Database Deployment](#database-deployment)
5. [Service Deployment](#service-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Database Migrations](#database-migrations)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Rollback Procedures](#rollback-procedures)
10. [Deployment Checklist](#deployment-checklist)

---

## Deployment Overview

### Architecture Summary

The Forge ecosystem deploys 4 services to Render.com:
- **DataForge** (port 8001) - Data layer
- **NeuroForge** (port 8000) - AI orchestration
- **ForgeAgents** (port 8010) - Agent coordination
- **Rake** (port 8002) - Data ingestion

All services share a single PostgreSQL database (Render Free Tier limitation) and optional Redis cache.

### Deployment Strategy

```
┌─────────────────────────────────────────────┐
│         Render.com Dashboard                │
│  - Create Database (dataforge-db)           │
│  - Deploy DataForge (runs migrations)       │
│  - Deploy NeuroForge (uses shared DB)       │
│  - Deploy ForgeAgents (uses shared DB)      │
│  - Deploy Rake (uses shared DB)             │
└─────────────────────────────────────────────┘
```

**Key Principles**:
1. Database first - create before deploying services
2. DataForge first - owns database schema and migrations
3. Other services follow - use shared database
4. Environment variables manually configured in Render dashboard

---

## Prerequisites

### Required Accounts

1. **GitHub Account**
   - Purpose: Host service repositories
   - Required for: All services (Render pulls from GitHub)

2. **Render.com Account**
   - Plan: Free Tier (sufficient for development)
   - URL: https://dashboard.render.com
   - Limits:
     - 1 PostgreSQL database (shared)
     - 750 hours/month web service time (shared across all services)
     - Services spin down after 15 minutes inactivity

3. **LLM Provider Accounts** (at least one required)
   - **OpenAI**: https://platform.openai.com/api-keys
   - **Anthropic**: https://console.anthropic.com/settings/keys
   - **Voyage AI**: https://www.voyageai.com/ (recommended for embeddings)
   - **Google AI**: https://aistudio.google.com/app/apikey (optional)
   - **XAI**: https://console.x.ai/ (optional)

4. **Optional Services**
   - **Redis Cloud**: https://app.redislabs.com (free tier available)
   - **Tavily**: https://app.tavily.com/ (web discovery, free tier)
   - **Firecrawl**: https://firecrawl.dev/ (web scraping, free tier)

### Required Tools (Local)

```bash
# Python 3.11+
python3 --version  # Should be 3.11 or higher

# Git
git --version

# Render CLI (optional but recommended)
npm install -g @render.com/cli
render --version
```

### GitHub Repositories

Ensure you have access to these repositories:
- `https://github.com/Boswecw/DataForge.git`
- `https://github.com/Boswecw/NeuroForge.git`
- `https://github.com/Boswecw/Forge-Agents.git`
- `https://github.com/Boswecw/rake.git`

---

## Render.com Setup

### Step 1: Create Render Account

1. Navigate to https://dashboard.render.com
2. Sign up with GitHub (recommended for automatic repo access)
3. Verify email address
4. Complete onboarding wizard

### Step 2: Connect GitHub Repositories

1. Go to **Account Settings** → **Connected Accounts**
2. Click **Connect GitHub**
3. Authorize Render to access your repositories
4. Select the repositories:
   - `DataForge`
   - `NeuroForge`
   - `Forge-Agents`
   - `rake`

### Step 3: Generate API Keys for Later Use

```bash
# Generate a secure JWT secret key (save this!)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate Fernet encryption key for DataForge secrets (save this!)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Database Deployment

### Step 1: Create PostgreSQL Database

**Option A: Via Render Dashboard (Recommended)**

1. Navigate to **Dashboard** → **New** → **PostgreSQL**
2. Configure database:
   - **Name**: `dataforge-db`
   - **Database**: `dataforge`
   - **User**: `dataforge`
   - **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
   - **Plan**: **Free** (256MB RAM, 1GB storage)
3. Click **Create Database**
4. Wait for provisioning (1-2 minutes)
5. **Save the connection details**:
   - Internal Database URL (for services on Render)
   - External Database URL (for local development)

**Option B: Via Render Blueprint**

```bash
# From DataForge repository root
render blueprint apply
```

This creates the database using the `databases` section in `render.yaml`.

### Step 2: Enable pgvector Extension

The pgvector extension is automatically enabled by DataForge on first startup. To verify manually:

```bash
# Connect to database using psql
psql <EXTERNAL_DATABASE_URL>

# Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

# Verify
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Step 3: Verify Database Connectivity

```bash
# Test connection
psql <EXTERNAL_DATABASE_URL> -c "SELECT version();"
```

Expected output:
```
PostgreSQL 13.x on x86_64-pc-linux-gnu, compiled by gcc ...
```

---

## Service Deployment

### Deploy Order

**IMPORTANT**: Deploy services in this order to avoid dependency issues.

1. **DataForge** (owns database, runs migrations)
2. **NeuroForge** (depends on DataForge schema)
3. **Rake** (depends on DataForge schema)
4. **ForgeAgents** (depends on all above)

---

### 1. Deploy DataForge

**Step 1: Create Web Service**

1. Navigate to **Dashboard** → **New** → **Web Service**
2. Configure service:
   - **Repository**: Select `DataForge` from connected repos
   - **Name**: `dataforge`
   - **Region**: Same as database (e.g., `Oregon (US West)`)
   - **Branch**: `master`
   - **Root Directory**: `.` (leave default)
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     python --version
     pip install --upgrade pip
     pip install -e ./forge-telemetry
     pip install --no-cache-dir -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: **Free**

3. Click **Advanced** and configure:
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes (deploy on git push)

**Step 2: Configure Environment Variables**

Click **Environment** tab and add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.10` | Python version |
| `ENVIRONMENT` | `production` | Environment name |
| `DATABASE_URL` | *Copy from dataforge-db Internal URL* | Critical: Use INTERNAL URL |
| `SECRET_KEY` | *Generated JWT secret* | Use `secrets.token_urlsafe(32)` |
| `JWT_SECRET_KEY` | *Same as SECRET_KEY* | For compatibility |
| `SECRETS_ENCRYPTION_KEY` | *Generated Fernet key* | For LLM key encryption |
| `OPENAI_API_KEY` | *Your OpenAI key* | Optional if using Voyage |
| `VOYAGE_API_KEY` | *Your Voyage AI key* | Recommended for embeddings |
| `ANTHROPIC_API_KEY` | *Your Anthropic key* | Optional |
| `ALLOWED_ORIGINS` | `*` | CORS (use specific domains in production) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `EMBEDDING_PROVIDER` | `voyage` | or `openai` or `cohere` |
| `EMBEDDING_MODEL` | `voyage-2` | or `text-embedding-3-small` |

**Step 3: Deploy**

1. Click **Create Web Service**
2. Monitor deployment logs in real-time
3. Wait for "Your service is live" message (5-10 minutes)
4. Test deployment:
   ```bash
   curl https://dataforge.onrender.com/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-02-05T12:00:00Z",
     "service": "DataForge",
     "version": "5.2.0",
     "database": "connected"
   }
   ```

**Step 4: Run Database Migrations**

DataForge automatically runs Alembic migrations on startup. Verify in logs:

```
INFO: Running database migrations...
INFO: Alembic: Running upgrade -> 9fe94997bec5, initial_database_schema
INFO: Alembic: Running upgrade 9fe94997bec5 -> 60a104999620, add_runs_tables
...
INFO: Alembic: Migrations complete
```

---

### 2. Deploy NeuroForge

**Step 1: Create Web Service**

1. Navigate to **Dashboard** → **New** → **Web Service**
2. Configure service:
   - **Repository**: Select `NeuroForge` from connected repos
   - **Name**: `neuroforge`
   - **Region**: Same as DataForge
   - **Branch**: `master`
   - **Root Directory**: `.` (leave default)
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     bash scripts/render_build.sh
     ```
   - **Start Command**:
     ```bash
     uvicorn neuroforge_backend.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: **Free**

3. Click **Advanced** and configure:
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes

**Step 2: Configure Environment Variables**

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.10` | Python version |
| `ENVIRONMENT` | `production` | Environment name |
| `DEBUG` | `false` | Disable debug mode |
| `DATABASE_URL` | *Copy from dataforge-db Internal URL* | **MUST match DataForge** |
| `DATAFORGE_BASE_URL` | `https://dataforge.onrender.com` | Internal service URL |
| `OPENAI_API_KEY` | *Your OpenAI key* | Required if using OpenAI models |
| `ANTHROPIC_API_KEY` | *Your Anthropic key* | Required if using Claude models |
| `GOOGLE_API_KEY` | *Your Google AI key* | Optional |
| `XAI_API_KEY` | *Your XAI key* | Optional |
| `ADMIN_API_KEY` | *Generate with secrets.token_urlsafe(32)* | Admin operations |
| `CORS_ORIGINS` | `*` | CORS (use specific domains in production) |
| `ENABLE_LOCAL_MODELS` | `false` | No Ollama on Render |
| `ENABLE_REMOTE_MODELS` | `true` | Enable cloud LLMs |
| `STRICT_MODE` | `false` | Relaxed validation |
| `MAX_OUTPUT_TOKENS` | `4096` | Max response length |

**Step 3: Deploy and Test**

1. Click **Create Web Service**
2. Wait for deployment (5-10 minutes)
3. Test:
   ```bash
   curl https://neuroforge.onrender.com/health
   ```

---

### 3. Deploy Rake

**Step 1: Create Web Service**

1. Navigate to **Dashboard** → **New** → **Web Service**
2. Configure service:
   - **Repository**: Select `rake` from connected repos
   - **Name**: `rake`
   - **Region**: Same as DataForge
   - **Branch**: `master`
   - **Root Directory**: `.` (leave default)
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -e ./forge-telemetry && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: **Free**

3. Click **Advanced** and configure:
   - **Health Check Path**: `/health/render`
   - **Auto-Deploy**: Yes

**Step 2: Configure Environment Variables**

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.10` | Python version |
| `ENVIRONMENT` | `production` | Environment name |
| `DATABASE_URL` | *Copy from dataforge-db Internal URL* | **MUST match DataForge** |
| `DATAFORGE_BASE_URL` | `https://dataforge.onrender.com` | Internal service URL |
| `OPENAI_API_KEY` | *Your OpenAI key* | For embeddings |
| `TAVILY_API_KEY` | *Your Tavily key* | Optional (Phase 1 primary search) |
| `SERPER_API_KEY` | *Your Serper key* | Optional (Phase 1 fallback search) |
| `FIRECRAWL_API_KEY` | *Your Firecrawl key* | Optional (Phase 1 scraping) |
| `RESEARCH_DEFAULT_PROVIDER` | `tavily` | Default search provider |
| `RESEARCH_MAX_SOURCES_PER_MISSION` | `50` | Max URLs per discovery job |
| `RESEARCH_MISSION_COST_CAP_USD` | `2.00` | Max cost per mission |
| `REDIS_URL` | *Your Redis Cloud URL* | Optional (caching, graceful degradation) |
| `JWT_SECRET_KEY` | *Generate with secrets.token_urlsafe(32)* | Authentication |
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `SCHEDULER_ENABLED` | `false` | Disable cron jobs on Render |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `VERSION` | `1.0.0` | Service version |

**Step 3: Deploy and Test**

1. Click **Create Web Service**
2. Wait for deployment (5-10 minutes)
3. Test:
   ```bash
   curl https://rake.onrender.com/health/render
   ```

---

### 4. Deploy ForgeAgents

**Step 1: Create Web Service**

1. Navigate to **Dashboard** → **New** → **Web Service**
2. Configure service:
   - **Repository**: Select `Forge-Agents` from connected repos
   - **Name**: `forgeagents`
   - **Region**: Same as DataForge
   - **Branch**: `master`
   - **Root Directory**: `.` (leave default)
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     chmod +x render-build.sh && ./render-build.sh
     ```
   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: **Free**

3. Click **Advanced** and configure:
   - **Health Check Path**: `/health/render`
   - **Auto-Deploy**: Yes

**Step 2: Configure Environment Variables**

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.10` | Python version |
| `ENVIRONMENT` | `production` | Environment name |
| `DATABASE_URL` | *Copy from dataforge-db Internal URL* | **MUST match DataForge** |
| `DATAFORGE_URL` | `https://dataforge.onrender.com` | Internal service URL |
| `NEUROFORGE_URL` | `https://neuroforge.onrender.com` | Internal service URL |
| `RAKE_URL` | `https://rake.onrender.com` | Internal service URL |
| `OPENAI_API_KEY` | *Your OpenAI key* | For agent operations |
| `ANTHROPIC_API_KEY` | *Your Anthropic key* | For agent operations |
| `JWT_SECRET_KEY` | *Generate with secrets.token_urlsafe(32)* | Authentication |
| `LLM_PROVIDER` | `anthropic` | Default provider |
| `OPENAI_ENABLED` | `true` | Enable OpenAI |
| `OPENAI_DEFAULT_MODEL` | `gpt-4-turbo-preview` | Default model |
| `ANTHROPIC_ENABLED` | `true` | Enable Anthropic |
| `ANTHROPIC_DEFAULT_MODEL` | `claude-3-sonnet-20240229` | Default model |
| `CORS_ORIGINS` | `["*"]` | CORS (JSON array) |
| `LOG_LEVEL` | `info` | Logging verbosity |

**Step 3: Deploy and Test**

1. Click **Create Web Service**
2. Wait for deployment (5-10 minutes)
3. Test:
   ```bash
   curl https://forgeagents.onrender.com/health/render
   ```

---

## Environment Configuration

### Environment Variable Best Practices

#### Security

```bash
# NEVER commit secrets to git
echo ".env" >> .gitignore

# Generate strong secrets
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Use environment-specific secrets
# - Different JWT_SECRET_KEY for dev/staging/prod
# - Rotate secrets every 90 days
```

#### Database URLs

**Internal URL** (for services on Render):
```
postgresql://user:pass@host.internal:5432/db
```

**External URL** (for local development):
```
postgresql://user:pass@host.aws-us-west-2.render.com:5432/db
```

**CRITICAL**: Always use **Internal URL** for services deployed on Render (faster, no egress costs).

#### CORS Origins

**Development**:
```bash
ALLOWED_ORIGINS=*
```

**Production**:
```bash
ALLOWED_ORIGINS=https://app.boswelldigital.com,https://dashboard.boswelldigital.com
```

### Redis Configuration (Optional)

If using Redis Cloud:

1. Sign up at https://app.redislabs.com
2. Create free database (30MB)
3. Copy connection URL (starts with `redis://` or `rediss://`)
4. Add to each service:
   ```bash
   REDIS_URL=rediss://default:password@host.cloud.redislabs.com:12345/0
   ```

**Note**: Services degrade gracefully without Redis (caching disabled).

---

## Database Migrations

### Migration Strategy

**DataForge owns all schema migrations**. Other services NEVER run migrations.

### Running Migrations

**Automatic (Recommended)**:
Migrations run automatically on DataForge startup via Alembic.

**Manual (If Needed)**:
```bash
# SSH into DataForge service (if supported by Render plan)
# Or run locally against production database

# Install dependencies
pip install alembic sqlalchemy psycopg2-binary

# Run migrations
cd DataForge
export DATABASE_URL="postgresql://..."
alembic upgrade head
```

### Creating New Migrations

```bash
# Local development only
cd DataForge
source venv/bin/activate

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description_of_change"

# Review generated migration in alembic/versions/
# Edit if needed (Alembic isn't perfect)

# Test migration
alembic upgrade head

# Test rollback
alembic downgrade -1

# Commit migration file to git
git add alembic/versions/xxxx_description.py
git commit -m "Add migration: description"
git push origin master

# Deploy to Render (auto-deploy triggers)
# Migration runs automatically on DataForge startup
```

### Migration Verification

```bash
# Check current migration version
psql <DATABASE_URL> -c "SELECT * FROM alembic_version;"

# Check applied migrations
psql <DATABASE_URL> -c "SELECT version_num FROM alembic_version ORDER BY version_num DESC LIMIT 10;"
```

### Rollback Procedure

**CAUTION**: Rolling back migrations can cause data loss.

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <version_hash>

# Rollback all migrations (DANGEROUS)
alembic downgrade base
```

---

## CI/CD Pipeline

### Render Auto-Deploy

Render automatically deploys on git push when **Auto-Deploy** is enabled.

**Workflow**:
1. Developer pushes to `master` branch
2. GitHub webhook triggers Render
3. Render pulls latest code
4. Runs build command
5. Starts new service instance
6. Health check passes
7. Routes traffic to new instance
8. Old instance shut down

**Deployment Time**: 5-10 minutes per service.

### Manual Deploy

**Via Render Dashboard**:
1. Navigate to service
2. Click **Manual Deploy** → **Deploy latest commit**
3. Wait for deployment

**Via Render CLI**:
```bash
# Install Render CLI
npm install -g @render.com/cli

# Authenticate
render login

# Deploy specific service
render deploy --service=dataforge
render deploy --service=neuroforge
render deploy --service=forgeagents
render deploy --service=rake
```

### Pre-Deploy Checklist

Before pushing to `master`:

- [ ] All tests pass locally: `pytest tests/ -v`
- [ ] Linting passes: `ruff check . && mypy .`
- [ ] Environment variables updated in Render dashboard
- [ ] Database migration tested locally
- [ ] No breaking API changes (or versioned correctly)
- [ ] Changelog updated
- [ ] Backup database (if schema changes)

### Post-Deploy Verification

```bash
# Test all health endpoints
curl https://dataforge.onrender.com/health
curl https://neuroforge.onrender.com/health
curl https://forgeagents.onrender.com/health/render
curl https://rake.onrender.com/health/render

# Test critical API endpoints
curl https://dataforge.onrender.com/api/v1/search/health
curl https://neuroforge.onrender.com/models/available

# Check logs for errors
# (via Render Dashboard → Logs tab)

# Monitor latency in Forge Command dashboard
```

---

## Rollback Procedures

### Emergency Rollback

If deployment causes critical issues:

**Option 1: Rollback via Render Dashboard**

1. Navigate to service in Render Dashboard
2. Click **Deploys** tab
3. Find last working deployment
4. Click **⋯** → **Redeploy**
5. Confirm rollback

**Option 2: Revert Git Commit**

```bash
# Identify bad commit
git log --oneline -10

# Revert commit (creates new commit that undoes changes)
git revert <commit_hash>

# Push to trigger auto-deploy
git push origin master
```

**Option 3: Emergency Code Revert**

```bash
# Hard reset to previous commit (CAUTION: loses commits)
git reset --hard <previous_good_commit>

# Force push (requires force push enabled)
git push --force origin master
```

### Database Rollback

If migration causes issues:

**Option 1: Rollback Migration**

```bash
# Connect to database
psql <DATABASE_URL>

# Check current version
SELECT * FROM alembic_version;

# Manually run downgrade (dangerous)
# Better: Redeploy DataForge with migration rollback logic
```

**Option 2: Restore from Backup**

Render automatically backs up PostgreSQL databases daily.

1. Navigate to **Database** → **Backups** in Render Dashboard
2. Select backup from before migration
3. Click **Restore**
4. Confirm (this OVERWRITES current database)

**CRITICAL**: Notify all teams before restoring backup.

### Service Degradation Procedure

If a service is unhealthy but not completely broken:

1. **Identify Issue**:
   - Check Render logs
   - Check Forge Command dashboard
   - Check health endpoint responses

2. **Isolate Impact**:
   - Determine which services are affected
   - Check if issue is service-specific or database-wide

3. **Temporary Mitigation**:
   - If one service is down, others continue working (stateless architecture)
   - Cold start delays increase but system remains functional

4. **Fix and Redeploy**:
   - Fix bug in code
   - Push to master
   - Monitor deployment

---

## Deployment Checklist

### Pre-Deployment

- [ ] **Code Quality**
  - [ ] All tests passing (`pytest`)
  - [ ] Linting clean (`ruff check .`)
  - [ ] Type checking clean (`mypy .`)
  - [ ] No security vulnerabilities (`bandit -r .`)

- [ ] **Configuration**
  - [ ] Environment variables updated in Render
  - [ ] Secrets rotated (if needed)
  - [ ] Database URL correct (Internal URL)
  - [ ] CORS origins configured

- [ ] **Database**
  - [ ] Backup created (automatic daily, verify in dashboard)
  - [ ] Migration tested locally
  - [ ] Migration reversible (downgrade tested)

- [ ] **Documentation**
  - [ ] CHANGELOG.md updated
  - [ ] API docs updated (if breaking changes)
  - [ ] Deployment notes written

### During Deployment

- [ ] Monitor Render deployment logs
- [ ] Watch for build errors
- [ ] Check health endpoint after deployment
- [ ] Verify database connection in logs

### Post-Deployment

- [ ] **Smoke Tests**
  - [ ] All health endpoints respond
  - [ ] Critical API endpoints work
  - [ ] Database queries execute
  - [ ] Redis cache connected (if configured)

- [ ] **Monitoring**
  - [ ] Check Forge Command dashboard
  - [ ] Verify no error spikes in logs
  - [ ] Check latency metrics
  - [ ] Verify cold start times acceptable

- [ ] **Rollback Readiness**
  - [ ] Document last working commit hash
  - [ ] Keep Render dashboard open
  - [ ] Monitor for 15 minutes post-deploy

### Rollback Checklist

- [ ] Issue identified and confirmed
- [ ] Stakeholders notified
- [ ] Last working deployment identified
- [ ] Rollback method chosen (Render UI vs git revert)
- [ ] Rollback executed
- [ ] Health checks passing
- [ ] Incident report created

---

## Troubleshooting Deployments

### Build Failures

**Issue**: `pip install` fails

**Solution**:
```bash
# Check requirements.txt for version conflicts
pip-compile requirements.in --resolver=backtracking

# Test build locally
docker build -t test .
```

**Issue**: Python version mismatch

**Solution**:
Set `PYTHON_VERSION=3.11.10` environment variable in Render.

### Startup Failures

**Issue**: Health check timeout

**Solution**:
- Increase health check timeout in Render (60+ seconds)
- Check logs for startup errors
- Verify DATABASE_URL is correct

**Issue**: Database connection refused

**Solution**:
- Verify using **Internal Database URL** (not External)
- Check database is running in Render dashboard
- Verify database credentials

### Runtime Issues

**Issue**: Service spins down (cold starts)

**Solution**:
- Expected on Free Tier (15 minutes inactivity)
- Use Forge Command "Wake All" feature
- Upgrade to Render Starter plan ($7/month, never spins down)

**Issue**: Out of memory errors

**Solution**:
- Free Tier has 512MB RAM limit
- Optimize code (reduce memory footprint)
- Upgrade to Starter plan (512MB → 2GB)

---

## Summary

**Key Takeaways**:

1. **Database First**: Create PostgreSQL before services
2. **Deploy Order**: DataForge → NeuroForge → Rake → ForgeAgents
3. **Shared Database**: All services use same DATABASE_URL (Internal)
4. **Auto-Deploy**: Push to `master` triggers deployment
5. **Migrations**: DataForge owns schema, runs automatically
6. **Rollback**: Redeploy previous version via Render UI
7. **Cold Starts**: Expected on Free Tier (60-90 seconds)

**Production Recommendations**:

- Use Render Starter plan ($7/month per service) for zero-downtime deploys
- Set up Redis Cloud for improved caching
- Configure specific CORS origins (not `*`)
- Rotate secrets every 90 days
- Monitor with Forge Command dashboard
- Set up Sentry/Datadog for error tracking

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
