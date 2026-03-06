# Forge Ecosystem - Data Flow & Architecture

**Document Version:** 1.0.0
**Last Updated:** February 5, 2026
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Database Overview](#database-overview)
2. [Core Tables](#core-tables)
3. [Data Flow Patterns](#data-flow-patterns)
4. [Vector Embeddings](#vector-embeddings)
5. [Redis Caching](#redis-caching)
6. [Migration Strategy](#migration-strategy)

---

## Database Overview

### Shared PostgreSQL Architecture

All Forge services share a single PostgreSQL database (`dataforge-db`) on Render Free Tier.

**Database Configuration**:
- **Name**: `dataforge`
- **Owner**: DataForge service (runs all migrations)
- **Extensions**: `pgvector`, `pg_trgm` (trigram indexing), `uuid-ossp`
- **Version**: PostgreSQL 13+
- **Size Limit**: 1GB (Free Tier)

###Table Ownership

| Service | Tables | Role |
|---------|--------|------|
| **DataForge** | `users`, `documents`, `chunks`, `domains`, `tags`, `runs`, `projects`, `audit_logs`, `telemetry_events`, `secrets`, `execution_index` | Owner (runs migrations) |
| **NeuroForge** | `inference_logs`, `model_performance`, `prompt_cache_entries` | Consumer (DataForge creates tables) |
| **ForgeAgents** | `agents`, `executions`, `memory`, `bugcheck_runs`, `findings` | Consumer (DataForge creates tables) |
| **Rake** | `jobs`, `job_status` | Consumer (DataForge creates tables) |

**Key Principle**: DataForge owns the schema. Other services only read/write data.

---

## Core Tables

### Users & Authentication

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

### Domains & Documents

```sql
CREATE TABLE domains (
    id VARCHAR(100) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    description TEXT,
    parent_id VARCHAR(100) REFERENCES domains(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    domain_id VARCHAR(100) NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    doc_type VARCHAR(50) NOT NULL,  -- guide, pattern, example, reference
    content TEXT NOT NULL,
    doc_metadata TEXT,  -- JSON string
    is_published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_documents_domain ON documents(domain_id);
CREATE INDEX idx_documents_type ON documents(doc_type);
CREATE INDEX idx_documents_published ON documents(is_published);
```

### Chunks & Embeddings (pgvector)

```sql
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding vector(1536),  -- pgvector type (Voyage-2 / OpenAI ada-002)
    search_vector tsvector,  -- Full-text search
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chunks_document ON chunks(document_id);
CREATE INDEX idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_chunks_search ON chunks USING gin(search_vector);
```

### Runs (NeuroForge Provenance)

```sql
CREATE TABLE runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER REFERENCES users(id),
    model VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    output TEXT,
    context_ids INTEGER[],
    parameters JSONB,
    tokens_used INTEGER,
    cost_usd NUMERIC(10, 6),
    latency_ms INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_runs_user ON runs(user_id);
CREATE INDEX idx_runs_model ON runs(model);
CREATE INDEX idx_runs_created ON runs(created_at DESC);
```

### Projects (VibeForge Integration)

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50),
    project_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE project_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    message_count INTEGER DEFAULT 0,
    tokens_used INTEGER DEFAULT 0
);
```

### Audit Logs (Immutable)

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    action VARCHAR(50) NOT NULL,
    payload JSONB,
    signature VARCHAR(255),  -- HMAC-SHA256
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_event ON audit_logs(event_type);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
```

### Execution Index (ForgeAgents)

```sql
CREATE TABLE execution_index (
    run_id VARCHAR(64) PRIMARY KEY,
    trace_id VARCHAR(64) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB,
    metadata JSONB
);

CREATE INDEX idx_exec_trace ON execution_index(trace_id);
CREATE INDEX idx_exec_agent ON execution_index(agent_type);
CREATE INDEX idx_exec_status ON execution_index(status);
```

### BugCheck Runs & Findings

```sql
CREATE TABLE bugcheck_runs (
    run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    targets TEXT[] NOT NULL,
    mode VARCHAR(20) NOT NULL,  -- quick, standard, deep
    scope VARCHAR(50) NOT NULL,  -- changed_files, package, full_repo
    commit_sha VARCHAR(64) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    severity_counts JSONB,
    gating_result VARCHAR(10),  -- pass, block
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE findings (
    finding_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID NOT NULL REFERENCES bugcheck_runs(run_id),
    fingerprint VARCHAR(255) NOT NULL,
    severity VARCHAR(10) NOT NULL,  -- S0, S1, S2, S3, S4
    category VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    location JSONB,
    lifecycle_state VARCHAR(20) DEFAULT 'NEW',
    autofix_available BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_findings_run ON findings(run_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_fingerprint ON findings(fingerprint);
```

### Rake Jobs

```sql
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_type VARCHAR(50) NOT NULL,  -- url, file, text
    source_url TEXT,
    domain_id VARCHAR(100) REFERENCES domains(id),
    status VARCHAR(20) DEFAULT 'pending',
    progress JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(created_at DESC);
```

---

## Data Flow Patterns

### Pattern 1: Document Ingestion

```
┌─────────┐
│  User   │
└────┬────┘
     │ POST /api/v1/jobs
     ▼
┌─────────┐
│  Rake   │ 1. Fetch URL/file
│  :8002  │ 2. Clean content
└────┬────┘ 3. Chunk (500 tokens)
     │ 4. Generate embeddings
     │ POST /admin/documents
     ▼
┌──────────┐
│DataForge │ 5. Store document
│  :8001   │ 6. Store chunks
└────┬─────┘ 7. Store embeddings
     │
     ▼
┌──────────┐
│PostgreSQL│ documents → chunks → embeddings (pgvector)
└──────────┘
```

### Pattern 2: Semantic Search

```
┌─────────┐
│  User   │
└────┬────┘
     │ POST /api/v1/search/semantic
     │ {"query": "How to authenticate?"}
     ▼
┌──────────┐
│DataForge │ 1. Generate query embedding (Voyage AI)
│  :8001   │ 2. Vector similarity search (pgvector)
└────┬─────┘ 3. Rank results by cosine similarity
     │
     ▼
┌──────────┐
│PostgreSQL│ SELECT * FROM chunks
│          │ ORDER BY embedding <=> query_embedding
└────┬─────┘ LIMIT 10
     │
     ▼
┌─────────┐
│ Results │ [{"chunk_id": 1, "similarity": 0.89, ...}]
└─────────┘
```

### Pattern 3: LLM Execution with Provenance

```
┌─────────┐
│  User   │
└────┬────┘
     │ POST /process
     ▼
┌───────────┐
│NeuroForge │ 1. Query DataForge for context
│   :8000   │ 2. Build prompt with context
└────┬──────┘ 3. Route to best model (champion tracking)
     │ 4. Execute LLM call
     │ 5. Evaluate response
     │ POST /api/v1/runs (provenance)
     ▼
┌──────────┐
│DataForge │ 6. Store run record
│  :8001   │    - Model, provider
└────┬─────┘    - Tokens, cost, latency
     │          - Context IDs used
     ▼
┌──────────┐
│PostgreSQL│ INSERT INTO runs (...)
└──────────┘
```

### Pattern 4: Agent Execution

```
┌─────────┐
│  User   │
└────┬────┘
     │ POST /api/v1/agents/{id}/execute
     ▼
┌─────────────┐
│ForgeAgents  │ 1. Load agent from registry
│   :8010     │ 2. Execute task loop
└──────┬──────┘    - Query DataForge (data)
       │           - Call NeuroForge (AI)
       │           - Call Rake (ingestion)
       │ 3. Write to execution_index
       ▼
┌──────────┐
│DataForge │ 4. Persist execution record
│  :8001   │ 5. Store memory updates
└────┬─────┘ 6. Log tool calls
     │
     ▼
┌──────────┐
│PostgreSQL│ execution_index → memory → audit_logs
└──────────┘
```

---

## Vector Embeddings

### pgvector Extension

**Enabled by**:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

**Vector Operations**:
```sql
-- Cosine similarity (most common)
SELECT embedding <=> query_embedding AS distance
FROM chunks
ORDER BY distance
LIMIT 10;

-- Euclidean distance
SELECT embedding <-> query_embedding AS distance
FROM chunks;

-- Inner product
SELECT embedding <#> query_embedding AS distance
FROM chunks;
```

### Index Types

**IVFFlat (Approximate)**:
```sql
CREATE INDEX idx_chunks_embedding
ON chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**HNSW (Higher accuracy, slower)**:
```sql
CREATE INDEX idx_chunks_embedding_hnsw
ON chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Embedding Providers

| Provider | Model | Dimensions | Cost per 1M tokens |
|----------|-------|------------|---------------------|
| **Voyage AI** | `voyage-2` | 1536 | $0.10 |
| **OpenAI** | `text-embedding-3-small` | 1536 | $0.02 |
| **OpenAI** | `text-embedding-3-large` | 3072 | $0.13 |
| **Cohere** | `embed-english-v3.0` | 1024 | $0.10 |

---

## Redis Caching

### Cache Architecture

```
┌──────────────────────────────────┐
│       Application Layer           │
│  NeuroForge, DataForge, etc.     │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│         Redis Cluster             │
│  - Query cache (TTL: 1 hour)     │
│  - Prompt cache (TTL: 24 hours)  │
│  - Session store (TTL: 7 days)   │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│        PostgreSQL                 │
│  (Source of truth - cache miss)  │
└──────────────────────────────────┘
```

### Cache Strategies

**Query Cache (DataForge)**:
```python
# Key: hash(query, domain_id, limit)
# TTL: 1 hour
cache_key = f"search:{hash(query)}:{domain_id}:{limit}"
```

**Prompt Cache (NeuroForge)**:
```python
# Key: MinHash signature of prompt
# TTL: 24 hours
cache_key = f"prompt:{minhash_signature}"
```

**Session Cache (All services)**:
```python
# Key: user_id:session_id
# TTL: 7 days
cache_key = f"session:{user_id}:{session_id}"
```

### Cache Invalidation

**Write-through**:
```python
# On document update
redis.delete(f"search:*:{document.domain_id}:*")
db.update(document)
```

**Time-based**:
```python
# Automatic expiration via TTL
redis.setex(key, ttl_seconds, value)
```

---

## Migration Strategy

### Alembic Configuration

**DataForge owns all migrations**:
```bash
# alembic.ini
script_location = alembic
sqlalchemy.url = ${DATABASE_URL}
```

### Migration Workflow

1. **Create Migration** (local):
   ```bash
   cd DataForge
   alembic revision --autogenerate -m "add_new_table"
   ```

2. **Review Generated SQL**:
   ```python
   # alembic/versions/xxx_add_new_table.py
   def upgrade():
       op.create_table('new_table', ...)

   def downgrade():
       op.drop_table('new_table')
   ```

3. **Test Locally**:
   ```bash
   alembic upgrade head
   alembic downgrade -1
   ```

4. **Deploy** (push to master):
   - Render auto-deploys DataForge
   - Migrations run on startup
   - Other services inherit new schema

### Zero-Downtime Migrations

**Add Column (safe)**:
```python
op.add_column('users', sa.Column('new_field', sa.String(), nullable=True))
```

**Drop Column (requires care)**:
```python
# Step 1: Deploy code that doesn't use column
# Step 2: Wait 24 hours
# Step 3: Drop column
op.drop_column('users', 'old_field')
```

**Rename Column (multi-step)**:
```python
# Step 1: Add new column
op.add_column('users', sa.Column('new_name', sa.String()))

# Step 2: Backfill data
op.execute('UPDATE users SET new_name = old_name')

# Step 3: Drop old column (after deploy)
op.drop_column('users', 'old_name')
```

---

## Performance Optimization

### Indexing Strategy

```sql
-- High-cardinality columns
CREATE INDEX idx_users_email ON users(email);  -- Unique lookups

-- Frequent WHERE clauses
CREATE INDEX idx_documents_domain ON documents(domain_id);  -- Filtering

-- Sorting columns
CREATE INDEX idx_runs_created ON runs(created_at DESC);  -- ORDER BY

-- Composite indexes
CREATE INDEX idx_chunks_doc_idx ON chunks(document_id, chunk_index);  -- Multi-column
```

### Query Optimization

**Use EXPLAIN ANALYZE**:
```sql
EXPLAIN ANALYZE
SELECT * FROM chunks
WHERE document_id = 123
ORDER BY chunk_index;
```

**Avoid N+1 Queries**:
```python
# Bad (N+1)
for doc in documents:
    chunks = db.query(Chunk).filter_by(document_id=doc.id).all()

# Good (eager loading)
documents = db.query(Document).options(joinedload(Document.chunks)).all()
```

### Connection Pooling

```python
# SQLAlchemy configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Max connections
    max_overflow=20,       # Extra connections if needed
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600      # Recycle connections every hour
)
```

---

**Document maintained by:** Boswell Digital Solutions LLC
**Last reviewed:** February 5, 2026
**Next review:** March 2026
