# Plan / Prompt v1.2 — DF Local Foundation Hardening + Seed-App Attachment
**Date:** 2026-03-15
**Revision:** v1.2
**Predecessor:** plan_prompt_v_1.md (v1.1)
**Change Summary:** Addresses six senior-review pressure points from the v1.1 close-out review.
Adds migration concurrency locking, signed export envelopes, CLI surface discipline,
registration compatibility semantics, health-event retention controls, and the AuthorForge
seed-app attachment proof. Adds red-team test clusters for status leakage and restore abuse.

---

# Prompt — Read First

You are hardening **DF Local Foundation v1.2** and delivering the first seed-app attachment.

v1.1 established the architectural skeleton, enforcement surfaces, and first test cluster.
v1.2 proves the system resists adversarial inputs, tightens the remaining weak points identified
in the senior review, and delivers one real app attachment without domain-authority leakage.

## READ FIRST — OPERATOR RULES
- Follow the steps exactly, in order.
- Do not weaken any v1.1 invariant. Only add constraint, never subtract.
- Keep migration locking narrow: one advisory lock, bounded scope, no global state.
- Signed envelopes must not expand visibility — the signature covers metadata only.
- CLI tools must call the same validation core as app code. No shortcuts.
- AuthorForge attachment must prove zero domain-authority leakage into core — that is the acceptance gate.
- Red-team tests must attempt real leakage, not mock it. If the test does not actually try to leak, it proves nothing.
- If any of the six pressure points cannot be resolved as stated, stop and report the conflict.

## GOAL
Harden DF Local Foundation from "architecturally credible" to "resists bad behavior" across
all six identified weak points, and prove the attachment model with one real seed app.

## SCOPE
### In scope
- Migration concurrency lock (advisory, fail-closed)
- Health-event retention discipline
- Signed export envelope (HMAC or asymmetric — chosen below)
- Registration compatibility semantics hardened
- Profile / config bypass prevention
- CLI tool authority surface audit and tightening
- AuthorForge seed-app attachment (schema namespace, migrations, health surface)
- Status red-team test cluster (leakage attempts via status/error surfaces)
- Restore abuse test cluster (hostile fixtures)

### Out of scope
- Multi-app rollout beyond AuthorForge
- Cloud sync or hybrid feature implementation
- Billing/entitlement flows
- NeuroForge Local bounded contract implementation (that is Slice 7)
- Hybrid augmentation contract (that is Slice 8)

---

# Locked Plan — v1.2

## 1. Pressure Point Resolution

### 1.1 Migration Concurrency / Locking

**Problem:** Two processes starting simultaneously could both believe migrations are pending
and attempt to apply them, producing double-application, partial state, or lock contention.

**Solution: PostgreSQL advisory lock on migration.**

```python
# Pattern: acquire advisory lock before migration check/apply
# Lock ID is deterministic per foundation install
MIGRATION_ADVISORY_LOCK_ID = 7261728173  # stable, unique to DF Local Foundation

async with advisory_lock(pool, MIGRATION_ADVISORY_LOCK_ID):
    # check + apply migrations here
    pass
# Lock released on context exit, even on exception
```

**Rules:**
- Advisory lock acquired before any migration check or application.
- If lock cannot be acquired within timeout: report `migrating`, do not proceed.
- Lock is session-scoped and auto-released on connection close.
- No global Python-level locking — PostgreSQL is the authority.
- Timeout on lock acquisition must be explicit (default: 5 seconds).
- Failed lock acquisition is logged and surfaces as `migrating`, never `ready`.
- Stale migration state after crash is resolved by re-acquiring the lock and re-checking.

**Deliverables:**
- `core/lifecycle/migration_lock.py` — advisory lock context manager
- Updated `core/lifecycle/manager.py` — wraps migration path in advisory lock
- Tests: concurrent startup simulation, lock contention, crash recovery posture

---

### 1.2 Health-Event Retention Discipline

**Problem:** `core_health_events` can become a junk drawer, accumulate indefinitely,
or become a side-channel for domain/app information.

**Rules:**
- Retention window: 30 days. Events older than 30 days are prunable (not auto-deleted — operator action or explicit maintenance call).
- Allowed event classes: bounded to the `ErrorClass` vocabulary (migration_failure, connection_failure, integrity_failure, compatibility_failure, startup_failure, restore_blocked).
- No free-form error messages in the event table. `error_class` column only.
- No domain metadata. No app-specific state beyond `app_id` (which is an operational identifier, not customer data).
- `app_id` in health events refers to registered app IDs (e.g., `core`, `authorforge`) — never customer IDs, project IDs, or user IDs.
- A maintenance helper `core/lifecycle/maintenance.py` provides `prune_health_events(older_than_days: int)`.

**Deliverables:**
- SQL: retention TTL comment in `core_health_events` DDL (already exists — add retention documentation)
- `core/lifecycle/maintenance.py` — prune helper
- Tests: event write contains only bounded fields, prune does not touch recent events

---

### 1.3 Export / Backup Envelope Signing

**Problem:** Hash-only envelopes prove integrity but not authenticity. A hostile actor
could generate a fake backup with a matching hash for a different payload.

**Decision: HMAC-SHA256 with a locally-held secret key.**

Rationale:
- Asymmetric signing (RSA/Ed25519) is the gold standard but requires key management
  infrastructure that does not yet exist in this layer.
- HMAC-SHA256 with a per-install secret stored in the local data directory is appropriate
  for a local-first system where the attacker does not have filesystem access.
- If an attacker has filesystem access, they already own the machine — signing does not help.
- The HMAC key is stored at `{df_local_data_dir}/signing.key` (mode 0600).
- The key is generated on first foundation init and never leaves the data directory.

**Envelope fields added:**
```json
{
  "integrity_hash": "sha256:...",
  "envelope_hmac": "hmac-sha256:<hex>",
  "hmac_covers": ["app_id", "foundation_version", "schema_version",
                  "backup_at", "format_version", "integrity_hash",
                  "includes_namespaces"]
}
```

**HMAC canonicalization:**
- Fields are sorted alphabetically before HMAC computation.
- Values are JSON-serialized (compact, no trailing whitespace).
- HMAC is computed over the UTF-8 bytes of the canonical JSON string.
- This makes the HMAC deterministic.

**Restore validation update:**
- After existing checks, also verify `envelope_hmac`.
- If `signing.key` does not exist or HMAC does not match: `RestoreBlockedError(error_class="integrity_failure")`.
- If envelope pre-dates signing support (no `envelope_hmac` field): treat as unsigned.
  Operator must explicitly pass `--allow-unsigned` to accept unsigned envelopes.
  Default is to block unsigned envelopes on restore.

**Deliverables:**
- `core/backup/signing.py` — HMAC key management and signing/verification
- Updated `core/backup/manager.py` — signs envelopes on write, verifies on restore
- Updated `tools/db-restore` — `--allow-unsigned` flag
- Tests: signed envelope verifies, tampered envelope blocked, unsigned blocked by default

---

### 1.4 Registration Compatibility Semantics

**Problem:** "Minimum compatible version" semantics are ambiguous — what does it mean
when app code is newer than foundation metadata? What about downgrade attempts?

**Clarified rules:**

| Scenario | Behavior |
|----------|---------|
| app `foundation_version_required` == running foundation version | Accept |
| app `foundation_version_required` < running foundation version | Accept (app requests older, running is newer — OK) |
| app `foundation_version_required` > running foundation version | Reject — foundation too old for this app |
| app schema version > foundation-known core schema version | Accept (app migration ahead of core is fine) |
| app schema version < app's own `expected_version` | Report `migrating` for that app, block that app's `ready` |
| Re-registration with incompatible version change | Reject if previously registered version was incompatible; require explicit forced re-registration |

**Implementation:**
- `core/lifecycle/compatibility.py` — `check_registration_compatibility(registration, running_foundation_version)` → `CompatibilityResult`
- Returns `compatible: bool`, `reason: str | None`, `error_class: str | None`
- Called by lifecycle manager before accepting a registration.
- Called at startup for all existing registrations — incompatible re-registrations are flagged, not silently accepted.
- Downgrade detection: if the new registration's `foundation_version_required` is higher than a prior registration for the same `app_id`, the change must be explicit (operator flag).

**Deliverables:**
- `core/lifecycle/compatibility.py`
- Updated `core/lifecycle/manager.py` — calls compatibility check on registration
- Tests: all four version scenarios, downgrade blocked, re-registration conflict

---

### 1.5 Profile / Config Bypass Prevention

**Problem:** Config can become a soft bypass layer if profile combinations are not validated
or if `local`/`hybrid`/`cloud-enabled` mode can be silently overridden.

**Hardened rules:**
- Profile is strictly one of `{dev, test, prod-local}`. Already enforced in v1.1. Adding test.
- `app_mode` in settings must match the `app_mode` declared in `core_app_registry`.
  If they diverge (e.g., app registered as `local` but settings say `hybrid`): report `degraded`.
- In `prod-local` profile: any use of `dev`-only behaviors (e.g., skipping migration checks) is
  a startup fault, not a silent noop.
- No fallback to default credentials in `prod-local` profile. Missing required env vars are a
  hard startup failure.
- `test` profile may relax PostgreSQL connection requirements (in-memory or test DB) but must
  still enforce all contract validations.

**Deliverables:**
- Updated `core/config/settings.py` — prod-local strict mode validator
- Updated `core/lifecycle/manager.py` — mode consistency check (settings vs registry)
- Tests: profile mismatch detection, prod-local strict mode, missing required vars in prod-local

---

### 1.6 CLI Tool Authority Surface

**Problem:** Operator tools can become the easiest path for doctrine bypass — they may
call lower-level APIs, emit fields beyond the health contract, or accept namespace arguments
that bypass registration.

**Audit and tightening rules:**
- All CLI tools must call the same core modules as app code. No internal shortcuts.
- `db-status` output is validated against `health.schema.json` before emission. If it fails, the tool exits non-zero with an error — not a raw dump.
- `db-backup` and `db-export` must verify that the target namespace is registered in `core_app_registry` before accepting the operation. Unregistered namespace → blocked.
- `db-restore` must not emit any customer-data fields from the envelope. It may print: app_id, schema_version, foundation_version, backup_at, integrity_hash — nothing else.
- `db-restore --dry-run` added: runs all validation without applying. Useful for CI and operator safety checks.

**Deliverables:**
- Updated `tools/db-status` — validates output against schema before printing
- Updated `tools/db-backup` — namespace registration check
- Updated `tools/db-export` — namespace registration check
- Updated `tools/db-restore` — envelope output filter, `--dry-run` flag
- Tests: CLI emits only bounded fields, unregistered namespace blocked, dry-run validates without applying

---

## 2. Slice 6 — AuthorForge Seed-App Attachment

### 2.1 Goal

Prove the attachment model with one real app. Not a simulation. Not a stub.
AuthorForge attaches, registers, runs its own migrations, and exposes a health surface —
without any AuthorForge domain tables appearing in the foundation core.

### 2.2 What Must Be Created

**In `df-local-foundation/`:**

```
sql/apps/authorforge/
  0001_authorforge_attach.sql    # Creates authorforge schema + registers app
tests/first_integration/
  test_authorforge_attachment.py # Proves the attachment invariants
```

**In AuthorForge (or as a reference implementation note if AuthorForge repo is separate):**
- AuthorForge registers with `app_id: "authorforge"`, `schema_namespace: "authorforge"`, `app_mode: "local"`
- AuthorForge runs its own migrations under `authorforge.*`
- AuthorForge exposes a health endpoint conforming to `contracts/health.schema.json`
- No AuthorForge domain tables exist in `core.*`

### 2.3 Attachment SQL

```sql
-- sql/apps/authorforge/0001_authorforge_attach.sql
-- This file is run by AuthorForge, not by the foundation.
-- It registers the app and creates its namespace.
-- Foundation does not own or inspect this namespace.

BEGIN;

CREATE SCHEMA IF NOT EXISTS authorforge;

INSERT INTO core_app_registry
    (app_id, app_version, foundation_version_required, schema_namespace, app_mode)
VALUES
    ('authorforge', '1.0.0', '1.1.0', 'authorforge', 'local')
ON CONFLICT (app_id) DO UPDATE SET
    app_version = EXCLUDED.app_version,
    updated_at = NOW();

INSERT INTO core_schema_versions
    (target, schema_namespace, current_version, expected_version, status)
VALUES
    ('authorforge', 'authorforge', '0001', '0001', 'current')
ON CONFLICT (target) DO UPDATE SET
    current_version = EXCLUDED.current_version,
    updated_at = NOW();

COMMIT;
```

### 2.4 Attachment Invariants (Tested)

| Invariant | Test |
|-----------|------|
| `authorforge.*` tables do not exist in `core.*` | Query `information_schema.tables WHERE table_schema = 'core'` — must show only `core_*` tables |
| AuthorForge health response conforms to schema | Validate against `health.schema.json` |
| Foundation health reports `ready` only when all registered apps are `ready` | Add second app with `migrating` state, verify foundation-level status is not `ready` |
| App can be deregistered without corrupting foundation core | Deregister AuthorForge, verify `core_*` tables intact |
| App cannot write to `core.*` namespace | Attempt `INSERT INTO core_app_registry` from app migration context — must enforce namespace separation |

### 2.5 Privacy Boundary Verification

The attachment test must confirm:

- ForgeCommand-facing health response for the attached app contains no AuthorForge domain fields
- Foundation status surface still exposes no table contents, record counts, or project names
- `core_health_events` for AuthorForge events contains only `app_id`, `status`, `error_class` — no AuthorForge business context

---

## 3. Red-Team Test Clusters

### 3.1 Status Leakage Red-Team

Location: `tests/visibility_boundary/test_status_redteam.py`

These tests **actively attempt to leak** restricted data through status surfaces.
If the implementation prevents the leak, the test passes. If not, the test exposes a real hole.

| Attack | Expected Outcome |
|--------|----------------|
| Inject `record_counts` into health dict | `PrivacyViolationError` |
| Inject `project_names` into health dict | `PrivacyViolationError` |
| Inject `manuscript_names` into health dict | `PrivacyViolationError` |
| Inject `table_list` into health dict | `PrivacyViolationError` |
| Inject `query_surface` into health dict | `PrivacyViolationError` |
| Inject `customer_data` into health dict | `PrivacyViolationError` |
| Error class contains free-form text | Schema validation rejects |
| `last_error_class` set to non-vocabulary string | Schema validation rejects |
| `status` set to undeclared value (e.g., `"operational"`) | Schema validation rejects |
| Attempt to add extra field to health response | Schema `additionalProperties: false` rejects |
| `db_engine` set to anything other than `"postgresql"` | Schema `const` rejects |
| `ownership` set to anything other than `"app-local"` | Schema `const` rejects |

### 3.2 Restore Abuse Red-Team

Location: `tests/backup_restore/test_restore_redteam.py`

| Hostile Fixture | Expected Outcome |
|----------------|----------------|
| Wrong `app_id` in envelope | `RestoreBlockedError(error_class="compatibility_failure")` |
| Truncated payload (hash mismatch) | `RestoreBlockedError(error_class="integrity_failure")` |
| Envelope HMAC tampered | `RestoreBlockedError(error_class="integrity_failure")` |
| Replayed old export (valid hash, old `backup_at`) | Accepted (timestamp is informational, not a replay guard — document this limit explicitly) |
| Cross-version downgrade (schema_version > current) | `RestoreBlockedError(error_class="compatibility_failure")` |
| Unsigned envelope, default mode | `RestoreBlockedError(error_class="integrity_failure")` |
| Unsigned envelope, `--allow-unsigned` flag | Proceed with warning |
| Missing `envelope_hmac` field | Treated as unsigned → blocked by default |
| `app_id` in envelope is reserved (`core`) | `RestoreBlockedError(error_class="compatibility_failure")` |
| Envelope namespace does not match registered app | `RestoreBlockedError(error_class="compatibility_failure")` |
| Unsupported format version | `RestoreBlockedError(error_class="compatibility_failure")` |
| Missing required envelope field | `RestoreBlockedError(error_class="integrity_failure")` |

---

## 4. Implementation Order

### Step 1 — Migration locking
Lock the concurrency hole before any other change, because everything else builds on lifecycle start.

Files:
- `core/lifecycle/migration_lock.py`
- Updated `core/lifecycle/manager.py`
- Tests: `tests/migration_status/test_migration_lock.py`

### Step 2 — Health-event retention
Small change, high discipline value.

Files:
- `core/lifecycle/maintenance.py`
- Tests: `tests/visibility_boundary/test_health_event_discipline.py`

### Step 3 — Envelope signing
Upgrade existing backup/export path.

Files:
- `core/backup/signing.py`
- Updated `core/backup/manager.py`
- Updated `tools/db-restore`
- Tests: `tests/backup_restore/test_envelope_signing.py`

### Step 4 — Registration compatibility semantics
Tighten registration before attaching a real app.

Files:
- `core/lifecycle/compatibility.py`
- Updated `core/lifecycle/manager.py`
- Tests: `tests/registration/test_compatibility_semantics.py`

### Step 5 — Profile / config bypass prevention
Tighten config before integration tests run.

Files:
- Updated `core/config/settings.py`
- Tests: `tests/registration/test_config_bypass.py` (or `tests/visibility_boundary/`)

### Step 6 — CLI tool authority audit
Tighten tools after core is hardened.

Files:
- Updated `tools/db-status`, `tools/db-backup`, `tools/db-export`, `tools/db-restore`
- Tests: `tests/visibility_boundary/test_cli_authority.py`

### Step 7 — Red-team test clusters
Write adversarial tests against the now-hardened stack.

Files:
- `tests/visibility_boundary/test_status_redteam.py`
- `tests/backup_restore/test_restore_redteam.py`

### Step 8 — AuthorForge seed-app attachment
Prove the model.

Files:
- `sql/apps/authorforge/0001_authorforge_attach.sql`
- `tests/first_integration/test_authorforge_attachment.py`
- `tests/first_integration/__init__.py`

---

## 5. Acceptance Tests

| Test | Expected |
|------|---------|
| Concurrent lifecycle start (2 processes) | Only one proceeds with migration; other waits or reports `migrating` |
| Lock timeout exceeded | Reports `migrating`, not `unavailable`, not silent degradation |
| Health event write — free-form field attempt | Blocked at DB constraint or application layer |
| Health event prune — only old events removed | Recent events survive prune |
| Signed backup round-trip | Backup signs, restore verifies, passes |
| Tampered envelope (any field) | Restore blocked, `integrity_failure` |
| Unsigned backup, default restore | Blocked unless `--allow-unsigned` |
| App `foundation_version_required` > running | Registration rejected, `compatibility_failure` |
| App re-registration downgrade blocked | Hard failure unless operator explicit |
| `prod-local` profile with missing required env | Hard startup failure, not silent default |
| `db-status` output invalid against schema | Tool exits non-zero, no raw dump |
| `db-export` with unregistered namespace | Blocked |
| Status surface — all 11 injection attacks | `PrivacyViolationError` or schema rejection |
| Restore — all 12 hostile fixtures | `RestoreBlockedError` with correct error class |
| AuthorForge attachment | All 5 attachment invariants pass |
| Foundation-level `ready` with app in `migrating` | Foundation reports `degraded`, not `ready` |

---

## 6. Invariants (Unchanged from v1.1 + additions)

All v1.1 invariants hold. Additional v1.2 invariants:

8. Migration state advances only under advisory lock.
9. Export envelopes are HMAC-signed with a locally-held key.
10. Unsigned envelopes are blocked on restore by default.
11. CLI tools cannot emit fields outside the bounded health contract.
12. CLI tools cannot operate on unregistered namespaces.
13. Registration compatibility is checked before any runtime operation proceeds.
14. Incompatible version states fail closed before runtime.
15. AuthorForge domain tables do not exist in `core.*`.
16. Foundation `ready` requires all registered apps to be `ready`.

---

## 7. DONE WHEN

- [ ] Migration advisory lock implemented and tested
- [ ] Health-event retention discipline documented and prune helper exists
- [ ] Export/backup envelopes are HMAC-signed
- [ ] Unsigned envelopes blocked by default on restore
- [ ] Registration compatibility semantics are explicit and enforced
- [ ] `prod-local` profile enforces no-default-credential rule
- [ ] CLI tools validated against health schema before output
- [ ] CLI tools block on unregistered namespace arguments
- [ ] All 11 status-leakage red-team tests pass
- [ ] All 12 restore-abuse red-team tests pass
- [ ] AuthorForge attachment SQL exists and runs cleanly
- [ ] All 5 AuthorForge attachment invariants tested and green
- [ ] Foundation-level `ready` blocked when any registered app is `migrating`
- [ ] No new `[TODO]` or `[PLANNED]` markers anywhere in the codebase
