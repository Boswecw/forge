# Forge Production Verification System (FPVS) - Implementation Context

**Document Version:** 1.0.0  
**Created:** 2025-12-27  
**Purpose:** Provide complete context for VS Code Claude Code to implement Phase 1 of FPVS

---

## Project Overview

**Company:** Boswell Digital Solutions LLC  
**CEO/Founder:** Charles Boswell  
**Ecosystem:** Forge - Suite of AI-powered backend services and desktop applications

### Core Philosophy

- **README-driven development** - Documentation as source of truth
- **Signal Over Noise** - Minimal, purposeful implementations
- **Determinism > Magic** - Explicit over implicit
- **Left → Right cognitive flow** - Code reads like prose
- **Evidence-based operations** - Proof over assumptions

---

## Current Production Services

All services deployed on **Render.com** (free tier):

### 1. NeuroForge (LLM Orchestration)
- **Production URL:** `https://neuroforge-9lxc.onrender.com`
- **Local Port:** 8000
- **Repository:** `~/Forge/NeuroForge/neuroforge_backend/`
- **Status:** Production (v1.2.3+)
- **Language:** Python 3.11+, FastAPI
- **Purpose:** Multi-provider LLM routing with cost optimization
- **Key Features:** 
  - OpenAI, Anthropic, Google, xAI, Ollama support
  - MAPO (Multi-AI Parallel Orchestration)
  - MAID (Managed AI Decisioning)
  - Circuit breaker pattern
  - Redis caching

**Current Endpoints:**
- `GET /health` - Basic health check (exists)
- Various execution endpoints (`/api/v1/execute`, `/api/v1/mapo`, `/api/v1/maid`)

**Known Issues:**
- No `/ready` endpoint for dependency validation
- No `/version` endpoint for build metadata
- No correlation ID middleware
- Logging does not include correlation IDs

---

### 2. DataForge (Vector Memory Engine)
- **Production URL:** `https://dataforge-pzmo.onrender.com`
- **Local Port:** 8001
- **Repository:** `~/Forge/DataForge/app/`
- **Status:** Production (v5.2.0, 296 tests passing)
- **Language:** Python 3.11+, FastAPI, SQLAlchemy 2.0
- **Purpose:** Persistent vector storage with semantic search
- **Key Features:**
  - PostgreSQL + pgvector
  - Multiple embedding models (OpenAI ada-002, local ONNX)
  - Metadata filtering
  - Batch document ingestion

**Current Endpoints:**
- `GET /health` - Basic health check (exists)
- `POST /api/v1/artifacts` - Store documents
- `POST /api/v1/search` - Semantic search
- Various CRUD endpoints

**Known Issues:**
- No `/ready` endpoint for dependency validation
- No `/version` endpoint for build metadata
- No correlation ID middleware
- Logging does not include correlation IDs

---

### 3. Rake (Data Ingestion Pipeline)
- **Production URL:** `https://rake-zp35.onrender.com`
- **Local Port:** 8002
- **Repository:** `~/Forge/rake/app/`
- **Status:** Production (v1.0, 77 tests passing)
- **Language:** Python 3.11+, FastAPI
- **Purpose:** Automated data ingestion from external sources
- **Key Features:**
  - Web URL ingestion (HTML, PDF, DOCX)
  - Pipeline: FETCH → CLEAN → CHUNK → EMBED → STORE
  - Job queue management
  - Retry logic with exponential backoff

**Current Endpoints:**
- `GET /health` - Basic health check (exists)
- `POST /api/v1/ingest` - Submit ingestion job
- `GET /api/v1/jobs/{job_id}` - Poll job status

**Known Issues:**
- No `/ready` endpoint for dependency validation
- No `/version` endpoint for build metadata
- No correlation ID middleware
- Logging does not include correlation IDs

---

### 4. ForgeAgents (Agent Orchestration)
- **Production URL:** `https://forgeagents.onrender.com`
- **Local Port:** 8787
- **Repository:** `~/Forge/ForgeAgents/app/`
- **Status:** Beta (85% complete, 14,313 LOC)
- **Language:** Python 3.11+, FastAPI
- **Purpose:** Autonomous AI agents with tools, policies, memory
- **Key Features:**
  - 23 tools across Rake, NeuroForge, DataForge, filesystem
  - 11 policies (safety, domain, resource)
  - 5 reference agents (assistant, developer, analyst, research, coordinator)
  - Three-tier memory (short-term, long-term, episodic)

**Current Endpoints:**
- `GET /api/health` - Basic health check (exists)
- `POST /api/v1/agents` - Create agent
- `POST /api/v1/agents/{id}/execute` - Execute task

**Known Issues:**
- No `/ready` endpoint for dependency validation
- No `/version` endpoint for build metadata
- No correlation ID middleware
- Logging does not include correlation IDs

---

## Shared Infrastructure

### Database: PostgreSQL (Render)
- **URL:** Set via `DATABASE_URL` environment variable
- **Extensions:** pgvector (for DataForge)
- **Connections:** Connection pooling via SQLAlchemy
- **Access Pattern:** Each service has its own connection pool

### Cache: Redis Cloud
- **URL:** Set via `REDIS_URL` environment variable
- **Usage:** 
  - NeuroForge: Prompt/output caching, rate limiting
  - DataForge: Embedding cache
  - Rake: Job state caching
- **TTL Defaults:** Configurable per service

---

## Common Technology Stack

All services share:

```python
# Core dependencies
fastapi >= 0.104.0
uvicorn[standard] >= 0.24.0
pydantic >= 2.5.0
pydantic-settings >= 2.1.0
python-dotenv >= 1.0.0

# Database
sqlalchemy >= 2.0.23
psycopg2-binary >= 2.9.9
alembic >= 1.12.1

# Async HTTP
httpx >= 0.25.2
aiohttp >= 3.9.1

# Caching
redis >= 5.0.1
hiredis >= 2.2.3

# Logging
structlog >= 23.2.0

# Testing
pytest >= 7.4.3
pytest-asyncio >= 0.21.1
pytest-cov >= 4.1.0
```

### Common Patterns

**FastAPI Application Structure:**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ServiceName", version="x.y.z")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include routers
from app.routers import some_router
app.include_router(some_router.router, prefix="/api/v1")
```

**Configuration Pattern:**
```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Service metadata
    service_name: str = "servicename"
    version: str = "1.0.0"
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # API Keys
    api_key: str | None = None

settings = Settings()
```

**Logging Pattern:**
```python
import structlog

logger = structlog.get_logger()

# Usage
logger.info(
    "request_processed",
    service="neuroforge",
    route="/api/v1/execute",
    status_code=200,
    duration_ms=142.5
)
```

---

## FPVS Implementation Goals

### Phase 1 Objectives (This Implementation)

**Add three standardized endpoints to each service:**

1. **`GET /health`** (enhance existing)
   - Lightweight liveness check
   - Returns 200 if process is alive
   - No dependency checks
   - Response time < 500ms

2. **`GET /ready`** (new)
   - Comprehensive readiness validation
   - Checks all critical dependencies
   - Returns 200 only if service can fulfill contracts
   - Includes dependency latency metrics

3. **`GET /version`** (new)
   - Service metadata
   - Build SHA from environment
   - Deployment timestamp
   - Service name

**Add correlation ID middleware to each service:**

4. **Correlation ID Middleware**
   - Accept `X-Correlation-ID` header
   - Generate UUID if not provided
   - Add to request state
   - Echo back in response header
   - Include in all log entries

**Enhance logging to include correlation IDs:**

5. **Structured Logging Enhancement**
   - All log entries include correlation_id
   - All log entries include service name
   - All log entries include route path
   - All log entries include status code
   - All log entries include duration (where applicable)

---

## Expected File Locations

### NeuroForge
```
~/Forge/NeuroForge/neuroforge_backend/
├── main.py                  # FastAPI app - MODIFY for middleware
├── config.py                # Settings - may need version addition
├── routers/
│   └── health.py            # CREATE/MODIFY - add ready/version endpoints
└── middleware/
    └── correlation.py       # CREATE - correlation ID middleware
```

### DataForge
```
~/Forge/DataForge/app/
├── main.py                  # FastAPI app - MODIFY for middleware
├── config.py                # Settings - may need version addition
├── routers/
│   └── health.py            # CREATE/MODIFY - add ready/version endpoints
└── middleware/
    └── correlation.py       # CREATE - correlation ID middleware
```

### Rake
```
~/Forge/rake/app/
├── main.py                  # FastAPI app - MODIFY for middleware
├── config.py                # Settings - may need version addition
├── routers/
│   └── health.py            # CREATE/MODIFY - add ready/version endpoints
└── middleware/
    └── correlation.py       # CREATE - correlation ID middleware
```

### ForgeAgents
```
~/Forge/ForgeAgents/app/
├── main.py                  # FastAPI app - MODIFY for middleware
├── core/
│   └── config.py            # Settings - may need version addition
├── api/
│   └── health.py            # MODIFY - add ready/version endpoints
└── middleware/
    └── correlation.py       # CREATE - correlation ID middleware
```

---

## Standardized Endpoint Specifications

### `/health` Endpoint

**Purpose:** Liveness check only - is the process alive?

**Method:** GET

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-27T14:32:11Z"
}
```

**Requirements:**
- Always returns 200 (unless process crashed)
- No external dependency checks
- Response time < 500ms
- Safe to call frequently (every 10s)

**Example Implementation:**
```python
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Level 0: Liveness check (lightweight, always safe)"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

---

### `/ready` Endpoint

**Purpose:** Readiness check - can the service fulfill its contract?

**Method:** GET

**Headers:** 
- `X-Correlation-ID` (optional) - for request tracing

**Response (Healthy):**
```json
{
  "status": "ready",
  "timestamp": "2025-12-27T14:32:11Z",
  "version": "5.2.0",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "dependencies": {
    "database": {
      "status": "ok",
      "latency_ms": 12
    },
    "redis": {
      "status": "ok",
      "latency_ms": 3
    },
    "neuroforge": {
      "status": "ok",
      "latency_ms": 45
    }
  }
}
```

**Response (Degraded):**
```json
{
  "status": "degraded",
  "timestamp": "2025-12-27T14:32:11Z",
  "version": "5.2.0",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "dependencies": {
    "database": {
      "status": "ok",
      "latency_ms": 12
    },
    "redis": {
      "status": "degraded",
      "latency_ms": 250,
      "error": "High latency detected"
    }
  }
}
```

**Response (Unavailable):**
```json
{
  "status": "unavailable",
  "timestamp": "2025-12-27T14:32:11Z",
  "version": "5.2.0",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "dependencies": {
    "database": {
      "status": "error",
      "error": "Connection refused"
    },
    "redis": {
      "status": "ok",
      "latency_ms": 3
    }
  }
}
```

**Status Determination:**
- `ready`: All critical dependencies healthy
- `degraded`: Optional dependencies unhealthy or high latency
- `unavailable`: Critical dependencies unavailable

**Service-Specific Dependency Checks:**

**NeuroForge:**
- Database: `SELECT 1` query
- Redis: `PING` command
- Optional: Check at least one provider API is reachable

**DataForge:**
- Database: `SELECT 1` query
- Redis: `PING` command
- pgvector extension: `SELECT extversion FROM pg_extension WHERE extname = 'vector'`

**Rake:**
- Database: `SELECT 1` query
- Redis: `PING` command
- DataForge: `GET /health` check

**ForgeAgents:**
- Database: `SELECT 1` query (if used)
- Redis: `PING` command (if used)
- NeuroForge: `GET /health` check
- DataForge: `GET /health` check
- Rake: `GET /health` check

**Example Implementation:**
```python
from fastapi import APIRouter, Header
from datetime import datetime
import uuid
import asyncio

router = APIRouter()

async def check_database() -> dict:
    """Check database connectivity"""
    try:
        start = asyncio.get_event_loop().time()
        # Execute trivial query
        async with get_db() as db:
            await db.execute(text("SELECT 1"))
        latency_ms = int((asyncio.get_event_loop().time() - start) * 1000)
        return {"status": "ok", "latency_ms": latency_ms}
    except Exception as e:
        return {"status": "error", "error": str(e)}

async def check_redis() -> dict:
    """Check Redis connectivity"""
    try:
        start = asyncio.get_event_loop().time()
        redis_client = get_redis_client()
        await redis_client.ping()
        latency_ms = int((asyncio.get_event_loop().time() - start) * 1000)
        return {"status": "ok", "latency_ms": latency_ms}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.get("/ready")
async def readiness_check(
    x_correlation_id: str | None = Header(None, alias="X-Correlation-ID")
):
    """Level 1: Readiness check (validates dependencies)"""
    correlation_id = x_correlation_id or str(uuid.uuid4())
    
    # Run all checks concurrently
    db_check, redis_check = await asyncio.gather(
        check_database(),
        check_redis()
    )
    
    checks = {
        "database": db_check,
        "redis": redis_check
    }
    
    # Determine overall status
    critical_checks = ["database"]  # Adjust per service
    
    has_errors = any(
        checks[name]["status"] == "error" 
        for name in critical_checks
    )
    has_degraded = any(
        check.get("latency_ms", 0) > 200 
        for check in checks.values()
    )
    
    if has_errors:
        status = "unavailable"
    elif has_degraded:
        status = "degraded"
    else:
        status = "ready"
    
    return {
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.version,
        "correlation_id": correlation_id,
        "dependencies": checks
    }
```

---

### `/version` Endpoint

**Purpose:** Service metadata and build information

**Method:** GET

**Response:**
```json
{
  "service_name": "neuroforge",
  "version": "1.2.3",
  "build_sha": "a1b2c3d4e5f6",
  "deployed_at": "2025-12-27T10:15:30Z"
}
```

**Environment Variable Sources:**
- `build_sha`: From `RENDER_GIT_COMMIT` (Render sets this automatically)
- `deployed_at`: From `RENDER_DEPLOY_TIME` (Render sets this automatically)

**Example Implementation:**
```python
import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/version")
async def version_info():
    """Service version and build metadata"""
    return {
        "service_name": settings.service_name,
        "version": settings.version,
        "build_sha": os.getenv("RENDER_GIT_COMMIT", "unknown"),
        "deployed_at": os.getenv("RENDER_DEPLOY_TIME", "unknown")
    }
```

---

## Correlation ID Middleware Specification

**Purpose:** Enable request tracing across services

**Behavior:**
1. Check for `X-Correlation-ID` header in incoming request
2. If present, use that value
3. If absent, generate new UUIDv4
4. Add correlation_id to request.state (accessible in handlers)
5. Echo correlation_id back in response header
6. Include in all log entries for this request

**Implementation:**
```python
# middleware/correlation.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid
import structlog

logger = structlog.get_logger()

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle correlation IDs for request tracing.
    
    - Accepts X-Correlation-ID header from client
    - Generates UUID if not provided
    - Adds to request.state for handler access
    - Echoes back in response header
    - Includes in structured logs
    """
    
    async def dispatch(self, request: Request, call_next):
        # Extract or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # Add to request state for access in handlers
        request.state.correlation_id = correlation_id
        
        # Log request received
        logger.info(
            "request_received",
            correlation_id=correlation_id,
            service=request.app.title,  # e.g. "NeuroForge"
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None
        )
        
        # Process request
        response: Response = await call_next(request)
        
        # Echo correlation ID in response
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
```

**Integration in main.py:**
```python
from app.middleware.correlation import CorrelationIDMiddleware

app = FastAPI(title="ServiceName")

# Add correlation ID middleware
app.add_middleware(CorrelationIDMiddleware)
```

---

## Logging Enhancement Specification

**Current State:** Most services use print statements or basic logging

**Target State:** Structured logging with correlation IDs

**Required Fields in Every Log Entry:**
- `correlation_id`: Request correlation ID (from middleware)
- `service`: Service name (e.g., "neuroforge")
- `timestamp`: ISO 8601 format with timezone
- `level`: info, warning, error, debug
- `message`: Human-readable description
- `route`: API route path (if applicable)
- `status_code`: HTTP status (if applicable)
- `duration_ms`: Request duration (if applicable)

**Example Enhanced Logging:**
```python
import structlog
from fastapi import Request

logger = structlog.get_logger()

@router.post("/api/v1/execute")
async def execute_prompt(request: Request, payload: ExecuteRequest):
    start_time = time.time()
    correlation_id = request.state.correlation_id
    
    logger.info(
        "execution_started",
        correlation_id=correlation_id,
        service="neuroforge",
        route="/api/v1/execute",
        model=payload.model
    )
    
    try:
        result = await process_execution(payload)
        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.info(
            "execution_completed",
            correlation_id=correlation_id,
            service="neuroforge",
            route="/api/v1/execute",
            status_code=200,
            duration_ms=duration_ms,
            model=result.model_used,
            tokens=result.total_tokens
        )
        
        return result
        
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        
        logger.error(
            "execution_failed",
            correlation_id=correlation_id,
            service="neuroforge",
            route="/api/v1/execute",
            status_code=500,
            duration_ms=duration_ms,
            error=str(e),
            error_type=type(e).__name__
        )
        
        raise
```

---

## Testing Requirements

Each new endpoint and middleware must have tests:

### Health Endpoint Tests
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient):
    """Health check should always return 200 OK"""
    response = await client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_health_is_fast(client: AsyncClient):
    """Health check should respond in < 500ms"""
    import time
    start = time.time()
    response = await client.get("/health")
    duration_ms = (time.time() - start) * 1000
    
    assert response.status_code == 200
    assert duration_ms < 500
```

### Ready Endpoint Tests
```python
@pytest.mark.asyncio
async def test_ready_returns_status(client: AsyncClient):
    """Ready check should return status and dependencies"""
    response = await client.get("/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] in ["ready", "degraded", "unavailable"]
    assert "dependencies" in data
    assert "correlation_id" in data

@pytest.mark.asyncio
async def test_ready_accepts_correlation_id(client: AsyncClient):
    """Ready check should use provided correlation ID"""
    test_id = "test-correlation-12345"
    response = await client.get(
        "/ready",
        headers={"X-Correlation-ID": test_id}
    )
    
    data = response.json()
    assert data["correlation_id"] == test_id

@pytest.mark.asyncio
async def test_ready_generates_correlation_id(client: AsyncClient):
    """Ready check should generate correlation ID if not provided"""
    response = await client.get("/ready")
    
    data = response.json()
    assert "correlation_id" in data
    assert len(data["correlation_id"]) == 36  # UUID format
```

### Version Endpoint Tests
```python
@pytest.mark.asyncio
async def test_version_returns_metadata(client: AsyncClient):
    """Version endpoint should return service metadata"""
    response = await client.get("/version")
    assert response.status_code == 200
    
    data = response.json()
    assert "service_name" in data
    assert "version" in data
    assert "build_sha" in data
    assert "deployed_at" in data
```

### Correlation Middleware Tests
```python
@pytest.mark.asyncio
async def test_middleware_echoes_correlation_id(client: AsyncClient):
    """Middleware should echo correlation ID in response header"""
    test_id = "test-12345"
    response = await client.get(
        "/health",
        headers={"X-Correlation-ID": test_id}
    )
    
    assert response.headers["X-Correlation-ID"] == test_id

@pytest.mark.asyncio
async def test_middleware_generates_correlation_id(client: AsyncClient):
    """Middleware should generate correlation ID if not provided"""
    response = await client.get("/health")
    
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    assert len(correlation_id) == 36  # UUID format
```

---

## Deployment Considerations

### Render Environment Variables

Services will automatically receive:
- `RENDER_GIT_COMMIT`: Git SHA of deployed commit
- `RENDER_DEPLOY_TIME`: ISO 8601 timestamp of deployment

No additional configuration needed for `/version` endpoint.

### Health Check Configuration

Update Render health check settings:
- **Path:** `/health` (not `/ready` - ready is too heavy)
- **Interval:** 30 seconds
- **Timeout:** 5 seconds
- **Unhealthy threshold:** 3 consecutive failures

### Testing After Deployment

After deploying changes to production:

```bash
# Test each service
for service in neuroforge dataforge rake forgeagents; do
    echo "Testing $service..."
    
    # Health check
    curl https://${service}-api.onrender.com/health
    
    # Ready check with correlation ID
    curl -H "X-Correlation-ID: test-$(uuidgen)" \
         https://${service}-api.onrender.com/ready
    
    # Version info
    curl https://${service}-api.onrender.com/version
    
    echo ""
done
```

---

## Success Criteria for Phase 1

Phase 1 is complete when:

- [ ] All 4 services have `/health`, `/ready`, `/version` endpoints
- [ ] All endpoints respond correctly with proper schemas
- [ ] Correlation ID middleware is implemented in all services
- [ ] All log entries include correlation_id and service name
- [ ] All new code has 100% test coverage
- [ ] Services deployed to Render successfully
- [ ] Manual verification tests pass for all services
- [ ] Render logs show correlation IDs in entries

---

## Additional Notes

### Code Style Preferences

- Type hints on all function signatures
- Docstrings on all public functions
- Async/await for I/O operations
- Pydantic models for request/response validation
- Structured logging over print statements
- Explicit error handling (no silent failures)

### Git Workflow

Each service should have:
1. Feature branch: `feature/fpvs-phase1-standardization`
2. Incremental commits with clear messages
3. All tests passing before commit
4. PR created with summary of changes

Example commit messages:
- `feat(health): Add /ready endpoint with dependency checks`
- `feat(middleware): Add correlation ID middleware`
- `feat(version): Add /version endpoint with build metadata`
- `test(health): Add comprehensive tests for new endpoints`
- `docs(readme): Update README with new endpoints`

---

## Questions/Clarifications

If you encounter any of these situations during implementation:

1. **Service has custom authentication**: Check if `/health`, `/ready`, `/version` should be public or authenticated
   - **Answer:** All three endpoints should be PUBLIC (no auth required) for monitoring purposes

2. **Database connection pattern differs**: Some services may use different DB clients
   - **Adapt:** Modify check_database() to match the service's existing pattern

3. **Service has no Redis**: Some services may not use caching
   - **Adapt:** Remove redis check from that service's `/ready` endpoint

4. **Service has additional dependencies**: Some services may depend on other Forge services
   - **Add:** Include those dependency checks in `/ready` endpoint

5. **Existing middleware conflicts**: Some services may have other middleware
   - **Solution:** Add CorrelationIDMiddleware FIRST in middleware chain

---

## Reference Implementation Order

Recommended implementation order:

1. **Start with NeuroForge** (most complex, good reference)
2. **Then DataForge** (similar patterns)
3. **Then Rake** (simpler, fewer dependencies)
4. **Finally ForgeAgents** (different structure, may require adaptation)

---

## End of Context Document

This document provides all necessary context for implementing Phase 1 of the Forge Production Verification System. Proceed with systematic implementation following the patterns and specifications outlined above.

**Next Steps:** See `FPVS_Implementation_Prompt.md` for detailed implementation instructions.
