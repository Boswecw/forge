# Forge Ecosystem — Dictionary Compression Integration Plan

**Version:** 0.2.1  
**Date:** 2026-02-24  
**Status:** PROPOSED — Awaiting Roadmap Slot  
**Priority:** P2 (Scalability Hardening)  
**Protocol:** `BDS_DOCUMENTATION_PROTOCOL_v1.md` §2.2 (Module Specs)  
**Reference:** [Dictionary Compression is finally here](https://httptoolkit.com/blog/dictionary-compression-performance-zstd-brotli/) — Tim Perry, February 2026  
**RFC:** [RFC 9842](https://www.rfc-editor.org/rfc/rfc9842) — Compression Dictionary Transport  

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| 0.1 | 2026-02-24 | Initial plan metadata |
| 0.2 | 2026-02-24 | Added dictionary scope boundaries (§5.1), canonical cache-key design (§5.4), transport/archive program separation (§6.0), COVER/FastCover training guidance (§6.2), streaming decompression abort (§3 invariant #8), minimum payload threshold (§3 invariant #7), observability moved into Phase 3, schema-drift invalidation trigger (§5.2), training_params registry field (§5.1) |
| 0.2.1 | 2026-02-24 | Added deployment context note (§1) acknowledging archive-first leverage in standalone Tauri desktop; XDG path compliance in Phase 4 |

---

## 1. Problem Statement

The Forge Ecosystem generates high volumes of structurally repetitive inter-service JSON traffic: inference payloads, agent execution records, governance artifacts, and data pipeline messages. Current compression (if any) uses generic gzip with no domain-specific optimization. As execution volume scales — particularly with the Agentic Reasoning extensions — this becomes a compounding cost in bandwidth, latency, and storage.

Dictionary compression (Zstandard with trained dictionaries) exploits the structural regularity of Forge's internal payloads to achieve 50–90% size reductions beyond standard compression, at lower CPU cost than alternatives like Brotli.

This plan governs two distinct sub-programs — **transport compression** (ephemeral, performance-oriented, gracefully degradable) and **archive compression** (durable, version-stable, must support decompression years after creation). These share tooling and governance but have different durability requirements and are phased accordingly.

**Deployment context:** In the current standalone Tauri 2 Debian deployment, all inter-service traffic occurs over localhost loopback between ForgeCommand-managed processes. This makes transport bandwidth savings marginal — the transport program's value on desktop is CPU/serialization efficiency, not network reduction. Archive compression is the higher-leverage program in this deployment model, as evidence bundles, knowledge archives, and governance artifacts reside on the user's local filesystem where storage reduction directly improves the desktop experience. The plan's architecture is designed to serve both the current standalone desktop deployment and future distributed deployments without structural changes.

---

## 2. Scope

### In Scope

**Transport compression (inter-service):**
- FastAPI middleware layer for inter-service HTTP payloads
- Rake pipeline stage transit payloads
- ForgeAgents Experience Store retrieval payloads (planned)
- Governed Broadcast envelope compression (planned)
- DataForge search response payloads

**Archive compression (long-term storage):**
- Governance evidence bundle archival
- Historical evidence export packages
- Long-term audit artifact storage

**Shared infrastructure:**
- Dictionary training, versioning, and distribution governance
- Forge-Smithy static asset delivery (browser-facing, Brotli path)

### Out of Scope

- pgvector ANN indices and raw embedding vectors (dense floats — no meaningful gain)
- Redis in-memory cache entry compression (CPU tradeoff negative on hot-path reads)
- Streaming SSE token delivery (incompatible with dictionary framing)
- WebSocket compression (complexity overhead outweighs benefit per Discord's findings)
- Compression of pre-hash canonical forms (governance constraint — see §7)
- Inference request/response prompt text (high-entropy natural language — poor dictionary target)
- Payloads below minimum compressible size threshold (see §3 invariant #7)

---

## 3. Architecture Invariants

These are non-negotiable. Any implementation that conflicts must be escalated.

1. **Hash before compress, never compress before hash.** SHA-256 artifact hashing operates on pre-compression canonical form. Compression is a transport/storage optimization only. Violating this breaks deterministic evidence verification.
2. **ForgeCommand governs dictionary distribution.** Active dictionary versions are registered and distributed through ForgeCommand as the root of trust. Services do not negotiate dictionaries peer-to-peer.
3. **Integration Law #1 applies.** ForgeCommand orchestrates which dictionary version is active per service pair. Services consume dictionaries; they do not self-select.
4. **Compression is opt-in and gracefully degradable.** If a service cannot decompress (missing dictionary, version mismatch, unsupported encoding), it falls back to uncompressed or standard gzip. No fail-open on missing dictionaries — fail to uncompressed.
5. **Dictionary-compressed responses must never be cached without dictionary-version keying.** Any response cache must use the canonical cache key structure defined in §5.4.
6. **Zstandard for inter-service transport; Brotli for browser-facing static assets.** Zstd wins on speed for hot-path internal calls. Brotli wins on ratio for pre-compressed static delivery.
7. **Minimum payload size threshold.** Payloads below `MIN_COMPRESSIBLE_SIZE_BYTES` (default: 1024 bytes) are never dictionary-compressed. This includes health checks, status pings, and small acknowledgment responses. Dictionary framing overhead on small payloads can produce negative compression ratios.
8. **Streaming decompression abort.** Decompression must abort if the output buffer exceeds an absolute ceiling (`MAX_DECOMPRESSED_BYTES`, default: 50MB) *before* the proportional ratio limit is evaluated. This is a streaming check — evaluated during decompression, not after. Prevents memory exhaustion from adversarial payloads that stay within the proportional limit but expand to extreme absolute sizes.
9. **Same-origin restriction for browser-facing paths.** Dictionaries cannot cross origins per RFC 9842. Forge-Smithy dictionaries are scoped to their serving origin only.

---

## 4. Target Applications (Ranked by Impact)

### Tier 1 — High Value

| Target | Service Pair | Payload Profile | Expected Gain | Dependency |
|--------|-------------|-----------------|---------------|------------|
| Experience Store retrieval | ForgeAgents → DataForge | Top-K execution summaries, identical schema, same gate names/archetypes | 60–80% beyond gzip | Agentic Reasoning Session 3+ |
| Evidence bundle archival | All services → DataForge/export | JSON-heavy audit artifacts, schema-consistent across runs | 50–70% storage reduction | None (current system) |
| Governed Broadcast envelope | ForgeAgents → ForgeCommand → targets | Fixed schema (`source_agent_id`, `target_scope`, `knowledge_type`, etc.) | 70–85% envelope compression | Agentic Reasoning Session 8 |

### Tier 2 — Medium Value

| Target | Service Pair | Payload Profile | Expected Gain | Dependency |
|--------|-------------|-----------------|---------------|------------|
| Rake pipeline transit | Rake stages (FETCH→CLEAN→CHUNK→EMBED→STORE) | Chunk metadata wrappers, repeated schema across thousands of records | 40–60% transit reduction | None (current system) |
| DataForge search responses | DataForge → requesting service | Scored results with metadata blobs, repeated response envelopes | 30–50% response reduction | None (current system) |
| ForgeCommand orchestration messages | ForgeCommand ↔ all services | Health checks, trust tokens, governance event chain entries | 30–40% reduction | None (current system) |

### Tier 3 — Low Value / Deferred

| Target | Reason for Deferral |
|--------|-------------------|
| NeuroForge prompt cache (Redis L1) | CPU overhead on every cache read negates storage savings unless memory-bound |
| Inference request/response body | Prompt text is high-entropy natural language — poor dictionary target |
| Forge-Smithy Svelte components | Already handled by standard Brotli; dictionary transport for browser assets is Chrome-only (~70% coverage) until Safari/Firefox ship support |

---

## 5. Dictionary Governance Model

### 5.1 Dictionary Registry

Dictionaries are named, versioned, and stored in DataForge as governance artifacts. Each dictionary is scoped to a specific service pair, payload class, and schema version range — ensuring that schema evolution triggers dictionary revalidation rather than silent degradation.

```
Table: compression_dictionaries [PLANNED]
─────────────────────────────────────────
dictionary_id         UUID          PK
name                  TEXT          NOT NULL    -- e.g. "forge-agents-experience-v1"
version               INTEGER       NOT NULL    -- monotonically increasing
service_pair          TEXT          NOT NULL    -- e.g. "forgeagents-dataforge"
payload_class         TEXT          NOT NULL    -- e.g. "experience-retrieval"
schema_version_min    TEXT          NOT NULL    -- minimum payload schema version covered
schema_version_max    TEXT          NOT NULL    -- maximum payload schema version covered
algorithm             TEXT          NOT NULL    -- "zstd" | "brotli"
dictionary_size_bytes INTEGER       NOT NULL    -- size of trained dictionary
dictionary_blob       BYTEA         NOT NULL    -- trained dictionary binary
sha256_hash           TEXT          NOT NULL    -- hash of dictionary_blob
training_sample_n     INTEGER       NOT NULL    -- number of samples used for training
training_params       TEXT          NOT NULL    -- reproducibility record
                                                -- e.g. "zstd --train --cover=k=1024,d=8 --maxdict=65536"
compression_ratio     FLOAT         NULL        -- measured ratio on held-out test set
program               TEXT          NOT NULL    -- "transport" | "archive"
created_at            TIMESTAMPTZ   DEFAULT NOW()
retired_at            TIMESTAMPTZ   NULL        -- set when superseded
```

**Unique constraint:** `(service_pair, payload_class, schema_version_max, program)` — at most one ACTIVE dictionary per scope per program.

### 5.2 Dictionary Lifecycle

```
TRAINING → CANDIDATE → ACTIVE → RETIRED

TRAINING:    Dictionary being built from sample payloads.
CANDIDATE:   Trained, pending validation on 20% held-out test set.
             Rejected if < 40% gain over gzip.
ACTIVE:      Distributed to services via ForgeCommand, in use.
RETIRED:     Superseded by newer version; retained for decompression of archived data.
```

**Retention rule:** RETIRED dictionaries are never deleted. Archived evidence compressed with dictionary version N must always be decompressible.

**Invalidation triggers — any of the following forces a dictionary back to TRAINING:**

- Payload schema version exceeds `schema_version_max` (schema evolution)
- Payload envelope structure changes (field additions, removals, or renames)
- Measured compression ratio degrades >10% from `compression_ratio` at registration
- Manual invalidation via ForgeCommand governance action

When a dictionary is invalidated, the system does not stop compressing — it falls back to the previous ACTIVE version (if one exists within the schema range) or to uncompressed. The invalidated dictionary enters TRAINING for its new schema range.

### 5.3 Distribution Flow

```
DataForge (stores dictionary blob)
    │
    ▼
ForgeCommand (distributes active version via /config/compression endpoint)
    │
    ├──► NeuroForge   (receives + caches locally)
    ├──► ForgeAgents   (receives + caches locally)
    ├──► Rake          (receives + caches locally)
    └──► DataForge     (already has it — self-reference)
```

Services poll ForgeCommand for dictionary updates on startup and at configurable intervals. Dictionary version mismatch triggers graceful fallback to uncompressed.

On receipt, each service verifies the SHA-256 hash of the dictionary blob against the hash provided by ForgeCommand. Hash mismatch is a hard failure — the dictionary is rejected and the service falls back to uncompressed, logging a governance warning event. Distribution occurs only over TLS.

### 5.4 Canonical Cache Key Structure

Any cache layer that stores dictionary-compressed responses must use the following key structure to prevent cross-dictionary collisions:

```
cache_key = sha256(
    route_path
    + "|" + dictionary_id
    + "|" + content_encoding     -- "dcz" | "dcb" | "identity"
)
```

HTTP-layer caches (reverse proxies, CDN) must set:

```
Vary: Accept-Encoding, Available-Dictionary
```

Internal application-layer caches must include `dictionary_id` as a first-class cache key component. Responses cached without dictionary-version keying are considered corrupted and must be evicted.

---

## 6. Technical Implementation Outline

### 6.0 Transport vs. Archive — Operational Differences

This plan governs two sub-programs with shared tooling but distinct operational requirements.

| Concern | Transport Compression | Archive Compression |
|---------|----------------------|-------------------|
| **Purpose** | Reduce inter-service bandwidth and latency | Reduce long-term storage cost |
| **Durability** | Ephemeral — decompressed on receipt | Must support decompression 5–10+ years later |
| **Fallback** | Graceful → uncompressed or gzip | No fallback — must succeed or block export |
| **Dictionary retention** | RETIRED dictionaries may be evicted from local service cache after grace period | RETIRED dictionaries must be retained indefinitely in DataForge |
| **Compression level** | Zstd level 3 (speed priority) | Zstd level 9+ (ratio priority) |
| **Dictionary size** | 64KB target (minimize load overhead) | Up to 128KB (ratio priority) |
| **Failure mode** | Warning event, continue uncompressed | Error event, halt export pipeline |
| **Phase** | Phase 3 | Phase 4 |

### 6.1 Compression Middleware (FastAPI) — Transport Program

Shared middleware installed per-service. Not a global swap — per-route opt-in.

```python
# PLANNED — illustrative structure only
class ZstdDictionaryMiddleware:
    """
    FastAPI middleware for Zstandard dictionary compression.
    
    - Reads Accept-Encoding from request
    - Checks response payload size >= MIN_COMPRESSIBLE_SIZE_BYTES (1024)
    - If dcz supported AND active dictionary available for this route:
        - Compress response with dictionary at Zstd level 3
        - Set Content-Encoding: dcz
        - Set Vary: Accept-Encoding, Available-Dictionary
        - Set Dictionary-ID header with active dictionary identifier
    - Otherwise: fall through to standard compression or uncompressed
    
    Per-route observability emitted on every compressed response:
        original_size_bytes, compressed_size_bytes, ratio,
        compression_cpu_time_us, dictionary_id, dictionary_version
    
    Fallback events logged with reason:
        dictionary_missing, dictionary_hash_mismatch,
        payload_below_threshold, encoding_not_supported
    """
```

**Header contract for inter-service communication:**

| Header | Direction | Value | Purpose |
|--------|-----------|-------|---------|
| `Accept-Encoding` | Request | `dcz, zstd, gzip, identity` | Client declares supported encodings |
| `Available-Dictionary` | Request | `:base64(sha256(dict)):` | Client declares available dictionary (RFC 9842 structured field) |
| `Dictionary-ID` | Request | Dictionary name + version | Optional explicit dictionary identifier |
| `Content-Encoding` | Response | `dcz` or `zstd` or `gzip` | Server declares encoding used |
| `Vary` | Response | `Accept-Encoding, Available-Dictionary` | Cache variance declaration |
| `Use-As-Dictionary` | Response | `match="/path/*"` | Browser-facing only — instructs client to cache response as dictionary |

### 6.2 Dictionary Training Pipeline

```
1. Collect representative payloads (5k–50k samples per payload class)
     - Stratify samples across schema versions and agent archetypes
     - Ensure coverage of edge cases (empty arrays, null fields, max-length values)

2. Train using COVER algorithm for structured JSON:

     Transport dictionaries:
       zstd --train --cover=k=1024,d=8 --maxdict=65536 samples/* -o candidate.dict

     Archive dictionaries:
       zstd --train --cover=k=1024,d=8 --maxdict=131072 samples/* -o candidate-archive.dict

     COVER uses cost-model optimization for fragment selection, producing
     higher-quality dictionaries for structured JSON than default training.

3. Validate on 20% held-out test set:
     - Measure ratio at target Zstd level (3 for transport, 9 for archive)
     - Reject if < 40% improvement over standard gzip on the same test set
     - Record ratio, training params, and sample count in registry

4. Register CANDIDATE in DataForge compression_dictionaries table
     - training_params field records exact CLI invocation for reproducibility

5. Promote to ACTIVE via ForgeCommand governance endpoint

6. Services pick up new dictionary on next poll cycle
```

### 6.3 Technology Stack

| Component | Technology | Version Requirement |
|-----------|-----------|-------------------|
| Python compression | `compression.zstd` (stdlib) | Python 3.14+ |
| Python fallback | `zstandard` (PyPI, C-binding) | Any current (if < 3.14) |
| Rust compression (Tauri) | `zstd` crate | Latest stable |
| Node.js (if applicable) | `zlib.zstdCompress` | Node 24.6+ / 22.19+ |
| Dictionary training | `zstd` CLI (COVER algorithm) | Latest stable |
| Browser static assets | Brotli (existing) | Already deployed |

---

## 7. Governance Constraints

### 7.1 Evidence Integrity Rule

```
CANONICAL FORM (JSON, deterministic key order)
    │
    ├──► SHA-256 hash (governance artifact identity)
    │
    └──► Zstd compress (transport/storage optimization)
         │
         └──► Store/transmit compressed form + dictionary_id reference
              │
              └──► Retrieve → load correct dictionary → decompress → verify hash
```

The hash is computed on the canonical pre-compression form. Compression is applied after hashing. Decompression reproduces the exact canonical form. This is a hard invariant — compression must be lossless and deterministic for the same input + dictionary pair.

**Archive-specific constraint:** Every archived evidence bundle stores its `dictionary_id` alongside the compressed blob. The archive retrieval path must load the correct dictionary version before decompression. If the dictionary is unavailable (should never happen given the retention rule), decompression fails loudly rather than returning corrupted data.

### 7.2 Audit Trail

Dictionary usage is logged in the governance event chain:

- Dictionary version activated (ForgeCommand event)
- Dictionary version retired (ForgeCommand event)
- Dictionary invalidated by schema drift (ForgeCommand event)
- Fallback to uncompressed triggered (service-level warning event)
- Archive decompression with non-current dictionary (informational event)

### 7.3 Security

- Dictionary content is not secret but is integrity-sensitive. Dictionary blobs are SHA-256 hashed at registration; services verify hash on receipt. Distribution occurs only over TLS.
- **Proportional decompression limit:** Max decompressed size = 10× compressed size or configurable cap per route.
- **Absolute decompression limit:** Decompression aborts immediately if output buffer exceeds `MAX_DECOMPRESSED_BYTES` (default: 50MB), regardless of proportional ratio. This is a streaming check — evaluated during decompression, not after. Prevents memory exhaustion from adversarial payloads.
- User-supplied dictionary hashes (in `Available-Dictionary` header for browser-facing paths) are validated against known dictionaries only — never used as filesystem or storage keys directly.

---

## 8. Implementation Phases

### Phase 1 — Measurement Baseline (Pre-requisite)

**Effort:** 1 session  
**Goal:** Instrument current inter-service payload sizes to establish baseline metrics.

- Add response size logging middleware to NeuroForge, DataForge, ForgeAgents, Rake
- Capture payload class, size, endpoint, service pair for 1 week of representative traffic
- Produce baseline report: median/p95/p99 payload sizes per service pair and payload class
- Identify payloads below 1KB threshold (excluded from future phases)
- **Exit gate:** Baseline report reviewed, high-value targets confirmed with real data

### Phase 2 — Dictionary Training & Validation

**Effort:** 1–2 sessions  
**Goal:** Train and validate dictionaries for Tier 1 targets.

- Export representative payload samples from baseline collection
- Train Zstd dictionaries per payload class using COVER algorithm
- Train separate dictionaries for transport (64KB, level 3) and archive (128KB, level 9) programs
- Validate compression ratios against 20% held-out test sets
- Implement `compression_dictionaries` table in DataForge
- Register CANDIDATE dictionaries with full `training_params` recorded
- **Exit gate:** ≥40% improvement over standard gzip for all Tier 1 payload classes in both transport and archive configurations

### Phase 3 — Middleware, Distribution & Observability

**Effort:** 2–3 sessions  
**Goal:** Deploy compression middleware, ForgeCommand dictionary distribution, and per-route observability from day one.

- Implement `ZstdDictionaryMiddleware` as shared FastAPI middleware
- Implement minimum payload size threshold check (`MIN_COMPRESSIBLE_SIZE_BYTES = 1024`)
- Implement both proportional (10×) and absolute (50MB) decompression limits as streaming checks
- Implement ForgeCommand `/config/compression` distribution endpoint with SHA-256 hash verification
- Implement canonical cache key structure (§5.4)
- Install middleware on Tier 1 service routes (opt-in, not global)
- Implement graceful fallback (dictionary missing → uncompressed)
- Deploy per-route compression observability:
  - Original payload size (bytes)
  - Compressed payload size (bytes)
  - Compression ratio
  - Compression CPU time (microseconds)
  - Dictionary ID and version
  - Fallback events (count + reason)
- **Exit gate:** Tier 1 routes compressing with dictionary, fallback verified, no governance hash breakage, observability dashboard showing per-route metrics

### Phase 4 — Evidence Archive Compression

**Effort:** 1 session  
**Goal:** Apply archive-program dictionary compression to governance evidence bundle export/archival.

- Train evidence-specific archive dictionary (128KB, level 9) from historical evidence bundles
- Integrate compression into evidence export pipeline (post-hash, storing `dictionary_id` alongside blob)
- Implement archive retrieval path: load correct dictionary version → decompress → verify hash
- Ensure archive storage paths are XDG-compliant on Linux/Debian (e.g. `~/.local/share/forge-smithy/` for data, `~/.config/forge-smithy/` for configuration) for seamless desktop packaging
- Verify round-trip: compress → store → retrieve → decompress → hash-verify
- Verify cross-version: compress with dictionary v1 → retire v1 → promote v2 → retrieve v1-compressed bundle → decompress with v1 dictionary
- **Exit gate:** Evidence bundles compress ≥50%, hash verification passes on all test bundles including cross-version retrieval

### Phase 5 — Tier 2 Rollout & Browser Path

**Effort:** 2 sessions  
**Goal:** Extend to medium-value targets; evaluate browser-facing dictionary transport.

- Deploy middleware to Tier 2 service routes
- Evaluate Compression Dictionary Transport (RFC 9842) for Forge-Smithy static assets
- If browser support ≥85%: implement `Use-As-Dictionary` headers for JS/WASM bundles
- If browser support <85%: defer, continue with standard Brotli
- **Exit gate:** Tier 2 routes live, browser path decision documented with CanIUse data

### Phase 6 — Staleness Detection & Dictionary Refresh

**Effort:** 1 session  
**Goal:** Production staleness detection and dictionary refresh automation.

- Implement dictionary staleness detection: periodic ratio measurement on production samples against current ACTIVE dictionary
- Implement automatic invalidation trigger when ratio degrades >10% from registered baseline
- Implement schema-drift detection: payload schema version exceeds dictionary's `schema_version_max` → automatic invalidation → fallback to previous ACTIVE or uncompressed
- Document dictionary retraining SOP
- **Exit gate:** Staleness detection live, schema-drift trigger active, retraining SOP reviewed

---

## 9. Dependencies & Blockers

| Dependency | Status | Blocks |
|-----------|--------|--------|
| Python 3.14 (`compression.zstd` stdlib) | Released | Phase 3 (or use `zstandard` PyPI as bridge) |
| Agentic Reasoning Experience Store | PLANNED (Session 3+) | Phase 2 Tier 1 dictionary for experience retrieval |
| Governed Broadcast (Tool #36) | PLANNED (Session 8) | Phase 2 Tier 1 dictionary for broadcast envelopes |
| ForgeCommand `/config/*` endpoint pattern | Exists | Phase 3 distribution |
| DataForge schema migration capability | Exists | Phase 2 table creation |
| Browser dictionary transport (Safari/Firefox) | In Progress (not shipped) | Phase 5 browser path decision |

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Actual compression gains below projections | Medium | Low | Phase 1 baseline measurement before any implementation investment |
| Dictionary version mismatch causes decompression failure | Medium | High | Graceful fallback to uncompressed; dictionary hash verification on receipt |
| Compression breaks evidence hash verification | Low | Critical | Invariant #1 enforced — hash before compress; round-trip tests in Phase 4 exit gate |
| Dictionary retraining neglected, ratio degrades | Medium | Low | Phase 6 staleness monitoring with automated alerts |
| Python 3.14 not yet deployed in Forge services | Medium | Low | `zstandard` PyPI package as drop-in bridge until stdlib available |
| Schema evolution silently degrades dictionary effectiveness | Medium | Medium | Schema version range in registry; automatic invalidation on version breach (§5.2) |
| Compression overhead on small payloads produces negative ratios | Medium | Low | `MIN_COMPRESSIBLE_SIZE_BYTES` threshold enforced in middleware (invariant #7) |
| Adversarial payload causes memory exhaustion during decompression | Low | High | Dual limits: proportional (10×) and absolute (50MB) streaming abort (invariant #8) |
| Archive dictionary unavailable for historical decompression | Very Low | Critical | RETIRED dictionaries never deleted; archive blobs store `dictionary_id`; retrieval path loads correct version |

---

## 11. Success Metrics

| Metric | Target | Measured At |
|--------|--------|-------------|
| Tier 1 inter-service payload reduction (transport) | ≥50% beyond current compression | Phase 3 exit |
| Evidence bundle archive size reduction (archive) | ≥50% | Phase 4 exit |
| Compression/decompression latency overhead | <5ms p99 per request | Phase 3 exit (observability from day one) |
| Governance hash verification pass rate | 100% (zero breakage) | All phases |
| Dictionary fallback rate (missing/mismatch) | <1% of requests after Phase 3 stabilization | Phase 3 observability |
| Cross-version archive decompression success | 100% | Phase 4 exit |
| Dictionary retraining frequency | Quarterly or on >10% ratio degradation | Phase 6 SOP |
| Schema-drift invalidation response time | <1 poll cycle after schema version bump | Phase 6 |

---

## 12. Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-24 | Plan created at P2 priority | Not a current bottleneck; becomes high-leverage at scale |
| 2026-02-24 | Zstd for inter-service, Brotli for browser | Zstd speed advantage on hot paths; Brotli ratio advantage for static pre-compressed assets |
| 2026-02-24 | Redis L1 cache compression deferred | CPU overhead per read negates storage savings unless memory-bound |
| 2026-02-24 | WebSocket compression excluded | Per Discord's production findings — complexity outweighs benefit |
| 2026-02-24 | Dictionary distribution via ForgeCommand | Respects Integration Law #1; prevents ad-hoc peer negotiation |
| 2026-02-24 | v0.2: Transport/archive separated as distinct sub-programs | Different durability, fallback, and retention requirements |
| 2026-02-24 | v0.2: Dictionary scoped to schema version range | Prevents silent degradation when payload schemas evolve; schema breach triggers automatic invalidation |
| 2026-02-24 | v0.2: COVER algorithm for dictionary training | Cost-model fragment selection produces higher-quality dictionaries for structured JSON than default training |
| 2026-02-24 | v0.2: Observability moved from Phase 6 to Phase 3 | Compression metrics must be available from first deployment; debugging without measurement data is unacceptable |
| 2026-02-24 | v0.2: Dual decompression limits (proportional + absolute) | Proportional limit alone insufficient for adversarial payloads; streaming abort prevents memory exhaustion |
| 2026-02-24 | v0.2: training_params field added to registry | Exact CLI invocation recorded for dictionary reproducibility |
| 2026-02-24 | v0.2.1: Deployment context documented — archive is higher-leverage on desktop | Standalone Tauri deployment has localhost-only transport (marginal bandwidth savings); local disk storage is the user-visible constraint |
| 2026-02-24 | v0.2.1: XDG path compliance required for archive storage | Seamless Debian packaging requires standard Linux data/config paths |

---

*This plan is a living document. Update the decision log as architectural choices are made or revised.*
