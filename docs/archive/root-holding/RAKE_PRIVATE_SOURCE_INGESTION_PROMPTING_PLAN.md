# Rake — Private Source Ingestion Prompting Plan

**Reference:** `ForgeCommand_Rake_Private_Source_Ingestion_Plan_v1.md` (Option A)  
**External Review:** Independent security & architecture review (Feb 2026)  
**Protocol:** `BDS_DOCUMENTATION_PROTOCOL_v1.md` §8 (Prompting Plans)  
**Date:** February 25, 2026  
**Status:** PLAN METADATA — Awaiting spec amendments before session authoring  
**Sessions:** 8 (documentation-first, then code, ordered by dependency)  
**Estimated total effort:** 4–5 focused sessions for P0/P1, 2–3 sessions for P2  
**Services touched:** DataForge, ForgeCommand, Rake  
**Complexity class:** Large (3 services, 8 sessions → Prompting Plan with dependency graph)

---

## 1. Feature Summary

Enable operator-curated, authenticated ("private source") crawling via ForgeCommand as Root of Trust, with every crawl represented as a RunIntent.v1-governed Private Source Ingestion Mission (PSIM). Secrets live in the OS keyring and never cross the UI boundary. Rake executes missions under scoped run_tokens; all outputs persist to DataForge with full evidence chains.

---

## 2. Spec Review Findings — Required Amendments Before Implementation

Two independent reviews (internal + external) converged on six issues that must be resolved in the spec before session authoring begins. These are ordered by governance severity.

### Amendment A-001: tenant_id Omission (Governance Violation)

**Severity:** V0 — Critical (bypasses multi-tenancy invariant)  
**Finding:** The PrivateSourceProfile model, RunIntent extension fields, and the mission start payload all omit `tenant_id`. Rake is multi-tenant by default — every DataForge write requires tenant context.  
**Required change:**
- Add `tenant_id` to `PrivateSourceProfile` schema (§3.1)
- Add `tenant_id` to RunIntent.v1 extension fields (§3.3)
- Add `tenant_id` to mission start payload (§5.2)
- Rake must propagate tenant_id through all pipeline stages for private source documents

### Amendment A-002: Rake API Path Design (Architecture Decision)

**Severity:** V1 — Structural  
**Finding:** Spec proposes `POST /api/v1/missions/private/start`, but Rake already has `POST /api/v1/missions` for research missions with a fundamentally different lifecycle (strategize → approve → execute). Parallel mission types sharing the `/missions` namespace without explicit discrimination creates routing ambiguity.  
**Decision required (pick one):**
- **Option 1:** Unified namespace — `POST /api/v1/missions` with `mission_type` discriminator in request body. Middleware routes to appropriate handler based on type.
- **Option 2:** Separate namespace — `POST /api/v1/private-ingestion` as a top-level resource. Clean separation, no interference with existing mission lifecycle.
- **Recommendation:** Option 1 (unified) aligns better with existing Rake conventions and makes future mission types easier. Add `mission_type` enum: `research` | `private_source`.

### Amendment A-003: auth_blob Transport Threat Model (Security Honesty)

**Severity:** V2 — Convention  
**Finding:** Spec claims "credentials never cross IPC boundary" and secrets are passed "in-memory only." The auth_blob field in the HTTP POST body to Rake traverses the network stack, even on localhost. This is not truly in-memory — it's an HTTP payload.  
**Required change:**
- Document the threat model explicitly in §2.2: "Secure for localhost loopback. If Rake is ever deployed off-box, require mTLS or switch to credential-fetch-by-reference pattern."
- Add a deployment constraint to §10 acceptance criteria: "Rake must be colocated with ForgeCommand (same host) for auth_blob transport security."

### Amendment A-004: Keyring Abstraction Alignment (Cross-Platform)

**Severity:** V2 — Convention  
**Finding:** Spec hardcodes "GNOME Keyring" throughout. ForgeCommand's canonical SYSTEM.md already uses the `keyring` crate, which abstracts across macOS Keychain, Windows Credential Manager, and Linux Secret Service (GNOME Keyring is one backend).  
**Required change:**
- Replace all references to "GNOME Keyring" with "OS keyring (via `keyring` crate)"
- Reference ForgeCommand SYSTEM.md §9 (Keyring Credentials) as the canonical pattern
- KeychainRef model (§3.2) `keychain_service` default remains `forge-command` per existing convention

### Amendment A-005: PSP Versioning and In-Flight Scope Behavior (Governance Gap)

**Severity:** V1 — Structural  
**Finding:** Spec doesn't address what happens when a PSP is edited while a mission is in flight. The run_token binds `allowed_scopes_hash`, which implies the answer is "running missions use creation-time scopes" — but this must be stated explicitly.  
**Required change:**
- Add to §4.1 (Token Binding Contract): "The run_token binds the PSP state at mission creation time. Subsequent PSP edits do not affect in-flight missions. The `allowed_scopes_hash` serves as the immutability proof."
- Add to §10 acceptance criteria: "PSP edits during an active mission do not alter that mission's scope enforcement."

### Amendment A-006: Quality Gate Deduplication (Rake Pipeline Conflict)

**Severity:** V2 — Convention  
**Finding:** Rake's built-in pipeline already has quality gates in the CLEAN stage (boilerplate detection, text length filtering). The PSP adds a separate `quality_gates` object. Two quality gate systems evaluating the same content could silently conflict or duplicate work.  
**Required change:**
- Add to §6.1: "PSP quality_gates are passed to Rake as pipeline configuration overrides. They replace (not supplement) Rake's default CLEAN stage thresholds for the duration of the private source mission. If a PSP field is null, Rake's built-in default applies."
- This follows the same override pattern Rake uses for research mission configuration.

---

## 3. Dependency Graph

```
Session 1 (Doc: SYSTEM.md updates — Rake + ForgeCommand + DataForge)
    │
    ├──► Session 2 (Code: DataForge schema — PrivateSourceProfile table + migration)
    │        │
    │        ├──► Session 3 (Code: ForgeCommand keychain adapter + PSP CRUD + IPC commands)
    │        │        │
    │        │        ├──► Session 4 (Code: Rake mission endpoint + scope enforcement middleware)
    │        │        │        │
    │        │        │        └──► Session 5 (Code: Evidence bundle creation + DataForge writes)
    │        │        │
    │        │        └──► Session 6 (Code: ForgeCommand UI — Private Sources page + Run Viewer)
    │        │
    │        └──► Session 7 (Code: RunIntent.v1 extension + run_token scope binding)
    │
    └──► Session 8 (Code: Circuit breakers + degradation flags + resilience)
```

---

## 4. Architecture Invariants (Apply to ALL Sessions)

These are non-negotiable. Every session must respect them. If a design conflicts, stop and escalate.

1. **ForgeCommand is Root of Trust.** All credential access, run lifecycle transitions, and mission authorization originate from ForgeCommand. No service self-authorizes.
2. **DataForge is the single source of truth.** All durable state (PSPs, mission records, documents, embeddings, evidence) is persisted via DataForge. ForgeCommand local state (KeychainRef) is metadata only.
3. **Intent → Execution → Evidence is mandatory.** Every private source crawl is a RunIntent.v1 mission. No crawl executes without a signed intent and issued run_token.
4. **Credentials never reach the UI.** The Svelte frontend declares intent; ForgeCommand Rust broker handles all secret material. IPC payloads carry profile IDs, never secrets.
5. **Silent fallbacks are banned.** All degradation is explicit, flagged, and surfaced. Auth expiry, keyring lock, site blocks — all produce named degradation events.
6. **Rake is write-only to DataForge.** Rake stores documents, embeddings, and evidence. It never reads its own prior outputs.
7. **Every DataForge write carries tenant_id.** No exceptions. (Amendment A-001)
8. **run_token binds PSP state at creation time.** In-flight missions are immutable to PSP edits. (Amendment A-005)

---

## 5. Session Summary Table

| Session | Title | Priority | Services | Phase |
|---------|-------|----------|----------|-------|
| 1 | Documentation: SYSTEM.md updates | P0 | Docs only | Documentation |
| 2 | DataForge schema: PrivateSourceProfile | P0 | DataForge | Schema & Data |
| 3 | ForgeCommand: keychain adapter + PSP CRUD | P0 | ForgeCommand | Service Backend |
| 4 | Rake: mission endpoint + scope enforcement | P0 | Rake | Service Backend |
| 5 | Evidence bundle creation + DataForge writes | P1 | Rake, DataForge | Service Backend |
| 6 | ForgeCommand UI: Private Sources + Run Viewer | P1 | ForgeCommand | UI Layer |
| 7 | RunIntent.v1 extension + token scope binding | P0 | ForgeCommand | Orchestration |
| 8 | Circuit breakers + degradation flags | P2 | ForgeCommand, Rake | Resilience |

**Note:** Sessions 3 and 7 are tightly coupled (keychain adapter produces the secrets that token binding consumes). Session 7 could be merged into Session 3 if velocity warrants a hybrid approach per BDS SOP §7.7.

---

## 6. Implementation Phase Mapping

Per BDS SOP §7.3 implementation ordering:

| BDS Phase | Sessions | Produces |
|-----------|----------|----------|
| Phase 1: Schema & Data | Session 2 | `private_source_profiles` table, migration, DataForge API endpoints |
| Phase 2: Service Backend | Sessions 3, 4, 5 | Keychain adapter, PSP CRUD, mission endpoint, evidence writes |
| Phase 4: Orchestration | Session 7 | RunIntent.v1 extension, run_token scope binding, IPC wrappers |
| Phase 5: UI | Session 6 | Private Sources page, Run Viewer extensions |
| Phase 6: Integration Verification | Completion Gate | End-to-end mission lifecycle test |

Phase 3 (Agent & Tool Layer) is not needed — private source ingestion does not introduce new ForgeAgents capabilities.

---

## 7. External Review Dispositions

Items from the independent security review, with dispositions based on ecosystem context.

| Review Item | Disposition | Rationale |
|-------------|-------------|-----------|
| GNOME Keyring CVE-2018-19358 / D-Bus filtering | **Acknowledged, deferred** | Single-operator desktop app. D-Bus sandboxing adds complexity for minimal threat reduction in this context. Revisit if multi-user deployment ever considered. |
| robots.txt compliance | **Rejected** | Private source ingestion crawls operator's own authenticated accounts. robots.txt applies to public crawling, which Rake handles via Firecrawl/Tavily. |
| GDPR/HIPAA/PII concerns | **Rejected** | Single-tenant, single-operator system. Operator ingests their own data into their own knowledge base. No third-party PII processing. |
| mTLS for internal APIs | **Rejected** | Services run on localhost or Render internal network. run_token HMAC-SHA256 provides sufficient auth for this deployment model. |
| Multi-instance Rake / Kubernetes | **Rejected** | Enterprise ceremony. Rake is stateless; horizontal scale can be added later if needed. Zero current demand. |
| Scheduling / batching for recurring missions | **Accepted as P2** | Useful for recurring crawls. Add to Session 8 or as follow-up feature. APScheduler infrastructure exists in Rake (disabled by default). |
| Circuit breaker thresholds for auth failures | **Accepted, Session 8** | Specific thresholds (e.g., 3 auth failures → trip breaker) should be defined during resilience implementation. |
| Auto-locking keyring on idle | **Deferred** | OS-level concern. ForgeCommand already handles keyring-locked gracefully (feature degrades, warning logged). |

---

## 8. Completion Gate

After all sessions are complete, verify:

```bash
# 1. Schema verification — PrivateSourceProfile table exists with tenant_id
psql $DATABASE_URL -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'private_source_profiles';"

# 2. Keychain round-trip — store and retrieve a test secret
# (manual verification via ForgeCommand debug UI or Rust test)

# 3. Mission lifecycle — create PSP → attach secret → create RunIntent → start mission → verify evidence
# (end-to-end integration test script)

# 4. Scope enforcement — attempt out-of-scope URL fetch → expect 409
curl -X POST http://localhost:8002/api/v1/missions \
  -H "Authorization: Bearer $RUN_TOKEN" \
  -d '{"url": "https://example.com/billing/invoices"}' \
  # Expected: 409 Conflict + security event logged

# 5. Degradation visibility — lock keyring → verify DEGRADED_KEYRING_LOCKED flag surfaces
# (manual verification)

# 6. PSP immutability — edit PSP during active mission → verify running mission unaffected
# (integration test)

# 7. Acceptance criteria from spec §10 — all must pass:
#    ✓ UI never receives secret material
#    ✓ Secrets stored only in OS keyring
#    ✓ Every private crawl is a RunIntent mission
#    ✓ run_token bound to scope; out-of-scope fetch rejected
#    ✓ All durable outputs written to DataForge with tenant_id
#    ✓ Evidence exists for every fetched page
#    ✓ Degraded states are explicit and surfaced
#    ✓ After FINALIZED, no further mutations accepted
```

---

## 9. Blockers & Prerequisites

| Prerequisite | Status | Blocks |
|-------------|--------|--------|
| Spec amendments A-001 through A-006 resolved | **PENDING** | All sessions |
| API path decision (A-002) finalized | **PENDING** | Sessions 4, 5, 7 |
| ForgeCommand keyring crate functional | Exists | Session 3 |
| RunIntent.v1 / RunManager operational | Exists | Session 7 |
| DataForge migration capability | Exists | Session 2 |
| Rake research mission infrastructure | Exists | Session 4 (reuse patterns) |

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Browser-mode crawling (Playwright/Firecrawl) adds significant complexity | Medium | Medium | MVP with HTTP-only; browser mode as P2 enhancement |
| Cookie jars expire frequently, degrading mission success rate | High | Low | DEGRADED_AUTH_EXPIRED flag + operator notification; UX for quick re-auth |
| Keyring daemon unavailable in headless CI/test environments | Medium | Low | Existing ForgeCommand pattern: feature degrades gracefully, tests mock keyring |
| Private source sites change structure, breaking extraction | Medium | Low | Quality gates catch low-quality extractions; operator reviews evidence diffs |

---

*Per BDS_DOCUMENTATION_PROTOCOL_v1.md §7.1 — this prompting plan is a session-level tactical guide. It does not supersede SYSTEM.md or Architecture Specs. All changes made during these sessions must be reflected back into the relevant SYSTEM.md part files and rebuilt.*

*Next step: Resolve spec amendments A-001–A-006, finalize API path decision (A-002), then author full session prompts with context bundles and acceptance criteria.*
