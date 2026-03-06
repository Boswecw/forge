# Forge Ecosystem - API Contracts

**Document Version:** 1.0.1
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [DataForge APIs](#dataforge-apis)
4. [NeuroForge APIs](#neuroforge-apis)
5. [ForgeAgents APIs](#forgeagents-apis)
6. [Rake APIs](#rake-apis)
7. [Error Codes](#error-codes)
8. [Rate Limiting](#rate-limiting)

---

## API Overview

### Base URLs

| Service | Production URL | Swagger Docs |
|---------|----------------|--------------|
| **DataForge** | `https://dataforge.onrender.com` | `/docs` |
| **NeuroForge** | `https://neuroforge.onrender.com` | `/docs` |
| **ForgeAgents** | `https://forgeagents.onrender.com` | `/docs` |
| **Rake** | `https://rake.onrender.com` | `/docs` |

### API Versioning

All APIs use URL-based versioning:
```
https://dataforge.onrender.com/api/v1/...
```

### Request Format

```http
Content-Type: application/json
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>  # Optional but recommended
```

### Response Format

```json
{
  "status": "success|error",
  "data": {...},
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {...}
  },
  "meta": {
    "timestamp": "2026-02-05T12:00:00Z",
    "request_id": "uuid"
  }
}
```

---

## Authentication

### Login

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "username": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "refresh_token": "optional_refresh_token"
}
```

### Register

**Endpoint**: `POST /api/v1/auth/register`

**Request**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

### Token Refresh

**Endpoint**: `POST /api/v1/auth/refresh`

**Request**:
```json
{
  "refresh_token": "refresh_token_string"
}
```

### Using Tokens

Include in all authenticated requests:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## DataForge APIs

### Search APIs

#### Semantic Search
**Endpoint**: `POST /api/v1/search/semantic`

**Request**:
```json
{
  "query": "How do I implement authentication?",
  "domain_id": "writing_craft",
  "limit": 10,
  "similarity_threshold": 0.7
}
```

**Response**:
```json
{
  "results": [
    {
      "chunk_id": 123,
      "document_id": 45,
      "title": "Authentication Guide",
      "content": "To implement authentication...",
      "similarity": 0.89,
      "metadata": {...}
    }
  ],
  "total": 15,
  "query_embedding_time_ms": 120,
  "search_time_ms": 45
}
```

#### Full-Text Search
**Endpoint**: `GET /api/v1/search/fulltext`

**Query Params**:
- `q` (required): Search query
- `domain_id` (optional): Filter by domain
- `limit` (optional, default=10): Results limit

**Response**:
```json
{
  "results": [
    {
      "document_id": 45,
      "title": "Authentication Guide",
      "snippet": "...highlighted <mark>authentication</mark> text...",
      "rank": 0.95
    }
  ]
}
```

### Projects API (VibeForge Integration)

#### Create Project
**Endpoint**: `POST /api/v1/projects`

**Request**:
```json
{
  "title": "My Novel Project",
  "description": "A fantasy adventure",
  "project_type": "novel",
  "metadata": {
    "genre": "fantasy",
    "word_count_goal": 80000
  }
}
```

#### Get Project Sessions
**Endpoint**: `GET /api/v1/projects/{project_id}/sessions`

**Response**:
```json
{
  "sessions": [
    {
      "session_id": "uuid",
      "started_at": "2026-02-05T10:00:00Z",
      "ended_at": "2026-02-05T12:30:00Z",
      "message_count": 45,
      "tokens_used": 12000
    }
  ]
}
```

### Runs API (NeuroForge Provenance)

#### Create Run
**Endpoint**: `POST /api/v1/runs`

**Request**:
```json
{
  "model": "gpt-4-turbo-preview",
  "provider": "openai",
  "prompt": "Write a story about...",
  "context_ids": [1, 2, 3],
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

**Response**:
```json
{
  "run_id": "uuid",
  "status": "completed",
  "output": "Once upon a time...",
  "tokens_used": 1523,
  "cost_usd": 0.0456,
  "latency_ms": 2340
}
```

### Admin APIs

#### Create Domain
**Endpoint**: `POST /admin/domains`

**Request**:
```json
{
  "id": "my_domain",
  "label": "My Domain",
  "description": "Domain for...",
  "parent_id": null
}
```

#### Ingest Document
**Endpoint**: `POST /admin/documents`

**Request**:
```json
{
  "domain_id": "my_domain",
  "title": "Guide Title",
  "doc_type": "guide",
  "content": "Full content here...",
  "tags": ["tag1", "tag2"]
}
```

### Secrets API (LLM Key Management)

#### Set Secret
**Endpoint**: `POST /api/v1/secrets/{provider}`

**Request**:
```json
{
  "api_key": "sk-...",
  "enabled": true
}
```

**Response**:
```json
{
  "provider": "openai",
  "encrypted": true,
  "updated_at": "2026-02-05T12:00:00Z"
}
```

### ForgeRun API (Agent Execution Persistence)

#### Create Execution Index
**Endpoint**: `POST /api/v1/forge-run/execution-index`

**Request**:
```json
{
  "run_id": "uuid",
  "trace_id": "uuid",
  "agent_type": "researcher",
  "status": "running",
  "metadata": {...}
}
```

---

## NeuroForge APIs

### Inference APIs

#### Process Request
**Endpoint**: `POST /process`

**Request**:
```json
{
  "prompt": "Explain quantum computing",
  "model": "claude-3-5-sonnet-20241022",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 1.0
  },
  "context": {
    "domain": "science",
    "user_id": "uuid"
  }
}
```

**Response**:
```json
{
  "output": "Quantum computing is...",
  "model": "claude-3-5-sonnet-20241022",
  "provider": "anthropic",
  "tokens": {
    "prompt": 15,
    "completion": 250,
    "total": 265
  },
  "cost_usd": 0.0079,
  "latency_ms": 1840,
  "cache_hit": false
}
```

#### Streaming Request
**Endpoint**: `POST /stream`

**Response**: Server-Sent Events (SSE)
```
event: token
data: {"text": "Quantum", "index": 0}

event: token
data: {"text": " computing", "index": 1}

event: done
data: {"tokens": 250, "cost": 0.0079}
```

### Model Router APIs

#### Get Available Models
**Endpoint**: `GET /models/available`

**Response**:
```json
{
  "models": [
    {
      "id": "gpt-4-turbo-preview",
      "provider": "openai",
      "context_window": 128000,
      "cost_per_1k_tokens": 0.01,
      "enabled": true
    },
    {
      "id": "claude-3-5-sonnet-20241022",
      "provider": "anthropic",
      "context_window": 200000,
      "cost_per_1k_tokens": 0.003,
      "enabled": true
    }
  ]
}
```

#### Get Champion Model
**Endpoint**: `GET /models/champion`

**Query Params**:
- `task_type`: Task type (e.g., "coding", "writing", "analysis")

**Response**:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "provider": "anthropic",
  "reason": "Best cost/performance ratio for task type",
  "performance_score": 0.92,
  "cost_efficiency": 0.88
}
```

### MAID APIs (Multi-Agent Consensus)

#### Validate with MAID
**Endpoint**: `POST /maid/validate`

**Request**:
```json
{
  "prompt": "Review this code for bugs...",
  "code": "def function():\n    ...",
  "models": ["gpt-4", "claude-3-5-sonnet", "gemini-pro"],
  "consensus_threshold": 0.7
}
```

**Response**:
```json
{
  "consensus": 0.85,
  "agreement": true,
  "responses": [
    {
      "model": "gpt-4",
      "output": "Bug found in line 5...",
      "confidence": 0.9
    }
  ],
  "recommendation": "Apply fix from gpt-4"
}
```

### RTCFX APIs (Evidence System)

#### Create Evidence Packet
**Endpoint**: `POST /rtcfx/evidence`

**Request**:
```json
{
  "run_id": "uuid",
  "agent_id": "uuid",
  "action": "code_generation",
  "payload": {...},
  "signature": "ed25519_signature"
}
```

---

## ForgeAgents APIs

### Agent Management

#### List Agents
**Endpoint**: `GET /api/v1/agents`

**Response**:
```json
{
  "agents": [
    {
      "agent_id": "uuid",
      "name": "Research Assistant",
      "type": "researcher",
      "status": "idle",
      "created_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

#### Create Agent
**Endpoint**: `POST /api/v1/agents`

**Request**:
```json
{
  "name": "Code Reviewer",
  "type": "coder",
  "config": {
    "model": "claude-3-5-sonnet",
    "max_iterations": 10,
    "timeout_seconds": 300
  }
}
```

#### Execute Agent
**Endpoint**: `POST /api/v1/agents/{agent_id}/execute`

**Request**:
```json
{
  "task": "Review this pull request",
  "context": {
    "repo": "owner/repo",
    "pr_number": 123
  },
  "tools": ["github", "neuroforge", "dataforge"]
}
```

**Response**:
```json
{
  "execution_id": "uuid",
  "status": "running",
  "started_at": "2026-02-05T12:00:00Z",
  "estimated_duration_seconds": 60
}
```

### Memory APIs

#### Query Long-Term Memory
**Endpoint**: `GET /api/v1/memory/long-term`

**Query Params**:
- `agent_id`: Agent UUID
- `query`: Semantic search query
- `limit`: Result limit

**Response**:
```json
{
  "memories": [
    {
      "memory_id": "uuid",
      "content": "Learned that...",
      "embedding": [0.1, 0.2, ...],
      "created_at": "2026-02-03T10:00:00Z"
    }
  ]
}
```

### BugCheck APIs

#### Start BugCheck Run
**Endpoint**: `POST /api/v1/bugcheck/runs`

**Request**:
```json
{
  "targets": ["neuroforge", "dataforge"],
  "mode": "standard",
  "scope": "full_repo",
  "commit_sha": "abc123"
}
```

**Response**:
```json
{
  "run_id": "uuid",
  "status": "running",
  "started_at": "2026-02-05T12:00:00Z"
}
```

#### WebSocket Stream
**Endpoint**: `WS /api/v1/bugcheck/ws/{run_id}`

**Messages**:
```json
{
  "event": "finding",
  "data": {
    "severity": "S1",
    "category": "security",
    "title": "SQL injection vulnerability",
    "location": "file.py:45"
  }
}
```

---

## Rake APIs

### Job Management

#### Create Ingestion Job
**Endpoint**: `POST /api/v1/jobs`

**Request**:
```json
{
  "source_type": "url",
  "source_url": "https://example.com/article",
  "domain_id": "my_domain",
  "chunking": {
    "chunk_size": 500,
    "overlap": 50
  }
}
```

**Response**:
```json
{
  "job_id": "uuid",
  "status": "pending",
  "created_at": "2026-02-05T12:00:00Z"
}
```

#### Get Job Status
**Endpoint**: `GET /api/v1/jobs/{job_id}`

**Response**:
```json
{
  "job_id": "uuid",
  "status": "completed",
  "progress": {
    "stage": "embedding",
    "percent": 100,
    "documents_processed": 1,
    "chunks_created": 15,
    "embeddings_generated": 15
  },
  "started_at": "2026-02-05T12:00:00Z",
  "completed_at": "2026-02-05T12:02:30Z"
}
```

### Discovery APIs (Phase 1)

#### Submit Discovery Job
**Endpoint**: `POST /api/v1/discover`

**Description**: Submit an async web discovery job with one or more search queries. Returns immediately with a job ID for polling.

**Request**:
```json
{
  "queries": [
    {
      "query": "CMMC Level 2 requirements 2025",
      "max_results": 10,
      "provider": "tavily",
      "search_depth": "advanced",
      "domain_filter": ["nist.gov", "dod.mil"],
      "recency_filter": "year"
    }
  ],
  "tenant_id": "tenant-123",
  "correlation_id": "optional-correlation-id",
  "mission_id": "optional-parent-mission-id"
}
```

**Response** (202 Accepted):
```json
{
  "discovery_id": "disc-abc123def456",
  "status": "processing",
  "poll_url": "/api/v1/discover/disc-abc123def456",
  "submitted_at": "2026-02-05T12:00:00Z"
}
```

#### Get Discovery Results
**Endpoint**: `GET /api/v1/discover/{discovery_id}`

**Description**: Poll for discovery job status and results.

**Response** (Status: processing):
```json
{
  "discovery_id": "disc-abc123def456",
  "correlation_id": "abc-123",
  "status": "processing",
  "queries_executed": 0,
  "total_urls_found": 0,
  "urls": [],
  "errors": [],
  "duration_ms": 0,
  "cost_credits": 0.0,
  "created_at": "2026-02-05T12:00:00Z"
}
```

**Response** (Status: completed):
```json
{
  "discovery_id": "disc-abc123def456",
  "correlation_id": "abc-123",
  "status": "completed",
  "queries_executed": 1,
  "total_urls_found": 10,
  "urls": [
    {
      "url": "https://nist.gov/cmmc",
      "title": "CMMC Level 2 Requirements",
      "snippet": "Comprehensive guide to CMMC Level 2...",
      "domain": "nist.gov",
      "position": 1,
      "relevance_score": 0.95,
      "search_query": "CMMC Level 2 requirements 2025",
      "provider": "tavily",
      "search_depth": "advanced",
      "discovered_at": "2026-02-05T12:00:15Z"
    }
  ],
  "errors": [],
  "duration_ms": 2500,
  "cost_credits": 2.0,
  "created_at": "2026-02-05T12:00:00Z"
}
```

**Response** (Status: failed):
```json
{
  "discovery_id": "disc-abc123def456",
  "correlation_id": "abc-123",
  "status": "failed",
  "queries_executed": 0,
  "total_urls_found": 0,
  "urls": [],
  "errors": [
    {
      "query": "CMMC Level 2 requirements 2025",
      "provider": "tavily",
      "error_code": "execution_failed",
      "error_message": "API key invalid",
      "retryable": false
    }
  ],
  "duration_ms": 100,
  "cost_credits": 0.0,
  "created_at": "2026-02-05T12:00:00Z"
}
```

### Research APIs (Phase 2 - Not Yet Implemented)

#### Create Research Mission

**Endpoint**: `POST /api/v1/research/missions`

**Status**: ⚠️ **Phase 2 - Coming Soon**

**Request**:
```json
{
  "query": "Latest trends in AI",
  "max_sources": 20,
  "cost_cap_usd": 2.0,
  "providers": ["tavily", "serper"]
}
```

**Response**:
```json
{
  "mission_id": "uuid",
  "status": "running",
  "sources_found": 0,
  "cost_so_far": 0.0
}
```

---

## Error Codes

### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200 OK` | Success | Request succeeded |
| `201 Created` | Resource created | POST requests |
| `400 Bad Request` | Invalid input | Validation failed |
| `401 Unauthorized` | Missing/invalid token | Authentication required |
| `403 Forbidden` | Insufficient permissions | Authorization failed |
| `404 Not Found` | Resource not found | ID doesn't exist |
| `409 Conflict` | State conflict | Duplicate resource |
| `422 Unprocessable Entity` | Semantic error | Business logic violation |
| `429 Too Many Requests` | Rate limit exceeded | Slow down |
| `500 Internal Server Error` | Server error | Bug or infrastructure issue |
| `503 Service Unavailable` | Service down | Cold start or maintenance |

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Username or password is incorrect",
    "details": {
      "field": "password",
      "constraint": "must be at least 8 characters"
    },
    "trace_id": "uuid"
  }
}
```

### Common Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `INVALID_CREDENTIALS` | 401 | Login failed |
| `TOKEN_EXPIRED` | 401 | JWT token expired |
| `INSUFFICIENT_PERMISSIONS` | 403 | Lacks required role |
| `RESOURCE_NOT_FOUND` | 404 | ID not in database |
| `DUPLICATE_RESOURCE` | 409 | Already exists |
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `EXTERNAL_API_ERROR` | 502 | LLM provider failed |
| `DATABASE_ERROR` | 503 | Database unavailable |

---

## Rate Limiting

### Default Limits

| Service | Endpoint | Limit | Window |
|---------|----------|-------|--------|
| **DataForge** | All endpoints | 1000 req | 1 hour |
| **NeuroForge** | `/process` | 60 req | 1 minute |
| **ForgeAgents** | `/agents/*/execute` | 100 req | 1 hour |
| **Rake** | `/jobs` | 50 req | 1 hour |

### Rate Limit Headers

Responses include:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1707136800
```

### Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit of 60 requests per minute exceeded",
    "retry_after": 30
  }
}
```

### Bypassing Rate Limits

Use API keys with elevated limits:
```http
X-API-Key: your-elevated-api-key
```

---

## Best Practices

### Idempotency

Use idempotency keys for critical operations:
```http
POST /api/v1/documents
Idempotency-Key: uuid
```

### Pagination

Large result sets use cursor-based pagination:
```http
GET /api/v1/documents?cursor=abc123&limit=50
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "def456",
    "has_more": true
  }
}
```

### Versioning

Specify API version in Accept header:
```http
Accept: application/vnd.forge.v1+json
```

### Correlation IDs

Always include for distributed tracing:
```http
X-Correlation-ID: uuid
```

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
