# Forge Ecosystem - Development Guide

**Document Version:** 1.0.0
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Local Development Setup

### Prerequisites

```bash
# Python 3.11+
python3 --version  # Should be 3.11 or higher

# PostgreSQL 13+
psql --version

# Redis 6+ (optional but recommended)
redis-cli --version

# Git
git --version
```

### 1. Clone Repositories

```bash
# Create workspace
mkdir ~/Forge && cd ~/Forge

# Clone services
git clone https://github.com/Boswecw/DataForge.git
git clone https://github.com/Boswecw/NeuroForge.git
git clone https://github.com/Boswecw/Forge-Agents.git
git clone https://github.com/Boswecw/rake.git
```

### 2. Setup PostgreSQL

```bash
# Create database
createdb dataforge

# Enable pgvector extension
psql dataforge -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 3. Setup Redis (Optional)

```bash
# Start Redis
redis-server

# OR use Redis Cloud (free tier)
# https://app.redislabs.com
```

### 4. Configure Environment Variables

**DataForge**:
```bash
cd DataForge
cp .env.example .env

# Edit .env:
DATABASE_URL=postgresql://localhost:5432/dataforge
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
VOYAGE_API_KEY=<your-key>
```

**NeuroForge**:
```bash
cd NeuroForge/neuroforge_backend
cp .env.example .env

# Edit .env:
DATABASE_URL=postgresql+asyncpg://localhost:5432/dataforge
DATAFORGE_BASE_URL=http://localhost:8001
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
```

**ForgeAgents**:
```bash
cd ForgeAgents
cp .env.example .env

# Edit .env:
DATABASE_URL=postgresql://localhost:5432/dataforge
DATAFORGE_URL=http://localhost:8001
NEUROFORGE_URL=http://localhost:8000
RAKE_URL=http://localhost:8002
OPENAI_API_KEY=<your-key>
```

**Rake**:
```bash
cd rake
cp .env.example .env

# Edit .env:
DATABASE_URL=postgresql+asyncpg://localhost:5432/dataforge
DATAFORGE_BASE_URL=http://localhost:8001
OPENAI_API_KEY=<your-key>
```

### 5. Install Dependencies

```bash
# DataForge
cd DataForge
python3 -m venv venv
source venv/bin/activate
pip install -e ./forge-telemetry
pip install -r requirements.txt

# NeuroForge
cd NeuroForge/neuroforge_backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# ForgeAgents
cd ForgeAgents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Rake
cd rake
python3 -m venv venv
source venv/bin/activate
pip install -e ./forge-telemetry
pip install -r requirements.txt
```

### 6. Run Database Migrations

```bash
# DataForge owns migrations
cd DataForge
source venv/bin/activate
alembic upgrade head
```

### 7. Start Services

**Terminal 1 - DataForge**:
```bash
cd DataForge
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - NeuroForge**:
```bash
cd NeuroForge/neuroforge_backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - ForgeAgents**:
```bash
cd ForgeAgents
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```

**Terminal 4 - Rake**:
```bash
cd rake
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### 8. Verify Services

```bash
# Health checks
curl http://localhost:8001/health  # DataForge
curl http://localhost:8000/health  # NeuroForge
curl http://localhost:8010/health  # ForgeAgents
curl http://localhost:8002/health  # Rake

# Swagger docs
open http://localhost:8001/docs  # DataForge
open http://localhost:8000/docs  # NeuroForge
```

---

## Testing

### Unit Tests

```bash
# DataForge
cd DataForge
pytest tests/ -v

# NeuroForge
cd NeuroForge/neuroforge_backend
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html
```

### Integration Tests

```bash
# Test full workflow
pytest tests/integration/ -v --integration
```

### Load Tests (k6)

```bash
# Install k6: https://k6.io/docs/get-started/installation/

# Run load test
k6 run tests/load/api_test.js
```

---

## Code Standards

### Linting

```bash
# Ruff (Python linter)
ruff check .

# Auto-fix
ruff check . --fix

# Format
ruff format .
```

### Type Checking

```bash
# mypy
mypy app/
```

### Pre-Commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Git Workflow

### Branch Strategy

- **master**: Production-ready code (auto-deploys to Render)
- **feature/***: New features
- **fix/***: Bug fixes
- **hotfix/***: Emergency production fixes

### Commit Messages

```
feat: Add semantic search endpoint
fix: Correct JWT expiration validation
docs: Update API documentation
chore: Upgrade dependencies
test: Add tests for user auth
```

### Pull Request Process

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit frequently
3. Run tests: `pytest tests/ -v`
4. Push to GitHub: `git push origin feature/new-feature`
5. Create Pull Request on GitHub
6. Request review from team
7. Address feedback
8. Merge to master (auto-deploys)

---

## Debugging

### Database Inspection

```bash
# Connect to database
psql dataforge

# List tables
\dt

# Describe table
\d users

# Run query
SELECT * FROM users LIMIT 10;
```

### Redis Inspection

```bash
# Connect to Redis
redis-cli

# List keys
KEYS *

# Get value
GET key

# Monitor commands
MONITOR
```

### Application Logs

```bash
# Structured logging
tail -f logs/app.log | jq

# Follow logs in real-time
uvicorn ... --log-level debug
```

---

## Common Tasks

### Add New API Endpoint

```python
# 1. Create router function
@router.post("/api/v1/resource")
async def create_resource(data: ResourceCreate):
    # Implementation
    pass

# 2. Register router in app/main.py
app.include_router(resource_router)

# 3. Add tests
def test_create_resource():
    response = client.post("/api/v1/resource", json={...})
    assert response.status_code == 201

# 4. Update API docs
# Auto-generated by FastAPI/Swagger
```

### Add Database Table

```bash
# 1. Update models in app/models/models.py
class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    # ...

# 2. Generate migration
alembic revision --autogenerate -m "add_new_table"

# 3. Review migration file
# Edit if needed

# 4. Apply migration
alembic upgrade head

# 5. Commit migration file
git add alembic/versions/*.py
git commit -m "Add new_table migration"
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8001

# Kill process
kill -9 <PID>
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
pg_isready

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify virtual environment
which python  # Should be in venv/
```

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
