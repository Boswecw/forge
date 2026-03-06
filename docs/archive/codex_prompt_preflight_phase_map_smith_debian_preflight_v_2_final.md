# Codex Prompt — Preflight Phase Map (SMITH Debian Preflight v2 FINAL)

**Role:** You are Codex running inside VS Code on the SMITH repo.

**Mission:** Implement the Debian Preflight v2 FINAL plan in **phases** with clean commits, deterministic behavior, stable evidence JSON output, and CI gating. Maintain a **Phase Map doc** as you go. When all phases are complete, generate/update a **SMITH changelog** entry from the Phase Map.

**Authoritative reference plan:** `smith_debian_preflight_plan_v2_final.md`

---

## Global constraints (non-negotiable)

1. **Determinism**: Output ordering must be stable across runs (sorted keys / ordered checks list).
2. **Fail-closed**: Missing/invalid policy/config should fail with explicit exit codes.
3. **Stable contracts**: Evidence JSON schema must be versioned and backward-compatible within v2.
4. **No surprise behavior**: Phases must not introduce unrelated refactors.
5. **Traceability**: Each phase must update the Phase Map doc with files changed + behavior deltas.

---

## Deliverables

### A) Implementation
- A Node-based CLI preflight script (Phase 0 → 3)
- Policy file + JSON schema
- Docs for usage + CI
- GitHub workflow(s) for gating and artifacts

### B) Documentation
- `docs/change_maps/deb_preflight_phase_map.md` (updated each phase)
- `CHANGELOG_SMITH.md` (updated at the end)

---

## Evidence JSON contract (v2)

Ensure a **single** JSON object is emitted in `--json` mode.

Minimum fields:
- `schema_version`: string (e.g., `"2.0"`)
- `correlation_id`: uuid-like string (or deterministic short id if plan specifies)
- `policy_hash`: sha256 hex (computed from canonical JSON)
- `target`: string (`debian`/`rpm`/`appimage`/`flatpak`)
- `repo_root`: absolute path
- `checks`: ordered list of check results (stable order)
  - each check: `{ id, status, severity, reason, details? }`
- `summary`: `{ ok, warnings, errors, exit_code }`

Rules:
- Always sort object keys where practical (or use canonical stringify for hashes).
- Always output checks in a deterministic order.

---

## Exit code contract (per plan)

Implement the plan’s exit codes **exactly**. If the plan lists:
- `0` pass
- `1` check failed
- `2` invalid config
- `3` invalid policy
- `4` fix applied
- `5` watch terminated

…then mirror that. If the plan differs, follow the plan.

---

## Phase Map doc format

Create (Phase 0) and update each phase:

`docs/change_maps/deb_preflight_phase_map.md`

For each phase include:
- Goal
- Files added
- Files modified
- Commands added/changed
- Behavior deltas (what’s now enforced)
- Evidence contract changes
- CI changes
- Risks/rollback notes

---

## Git discipline

Commit after each phase using these prefixes:
- `preflight(p0): ...`
- `preflight(p1): ...`
- `preflight(p1.5): ...`
- `preflight(p2): ...`
- `preflight(p3): ...`

Each commit must include:
- implementation for that phase
- Phase Map updates for that phase

---

# PHASE 0 — Scaffolding (no behavior change)

### Goal
Lay down the rails: script stub, minimal policy + schema, docs, phase map doc.

### Steps
1. Add `scripts/deb-preflight.mjs` stub:
   - supports `--help`, `--json`, `--ci`, `--target`
   - outputs a valid JSON object in `--json` mode
   - DOES NOT enforce real checks yet; can emit `NOT_IMPLEMENTED` status entries
2. Add minimal `forge.policy.json` targeting Debian only.
3. Add `schemas/forge-policy.schema.json` minimal schema.
4. Add docs: `docs/buildguard/DEB_PREFLIGHT.md` with how to run.
5. Create `docs/change_maps/deb_preflight_phase_map.md` and write Phase 0 entry.

### Acceptance
- `node scripts/deb-preflight.mjs --help` prints usage.
- `node scripts/deb-preflight.mjs --json` prints valid JSON.

### Commit
`preflight(p0): scaffold deb preflight + policy schema + docs`

---

# PHASE 1 — Deterministic Debian preflight (fail-closed)

### Goal
Implement full Debian checks and deterministic evidence JSON.

### Steps
1. Implement repo root discovery (walk up until `package.json`).
2. Read/validate `forge.policy.json` using the JSON schema.
3. Read `src-tauri/tauri.conf.json`.
4. Implement checks in deterministic order (as specified in plan), e.g.:
   - productName present
   - identifier present + reverse-DNS format
   - version semver format
   - Debian depends includes required entries from policy
   - required assets exist
   - icon size warnings (become errors under `--ci` if plan says)
5. Implement exit codes exactly.
6. Implement stable evidence JSON:
   - `schema_version`, `correlation_id`, `policy_hash`, ordered `checks`, `summary`
7. Add package scripts:
   - `preflight:deb`
   - `preflight:deb:ci`
8. Update Phase Map doc with Phase 1 changes.

### Acceptance
- Misconfigured identifier fails with the correct exit code and reason.
- Missing policy triggers `POLICY_INVALID` code.
- `--ci` strict behavior matches plan.
- Output is stable across runs.

### Commit
`preflight(p1): implement deterministic deb preflight + evidence json`

---

# PHASE 1.5 — Wire preflight into Debian packaging (stop-ship)

### Goal
Debian packaging cannot proceed unless preflight passes.

### Steps
1. Update build pipeline entrypoint (package.json scripts and/or CI) so `pnpm tauri build --bundles deb` is gated by `pnpm preflight:deb:ci`.
2. Ensure failures stop the build early.
3. Update docs and Phase Map.

### Acceptance
- Broken depends list blocks `.deb` builds.

### Commit
`preflight(p1.5): gate deb packaging on preflight`

---

# PHASE 2 — BuildGuard integration + CI artifacts

### Goal
Policy-driven enforcement, CI gating, and evidence artifact upload.

### Steps
1. Make policy authoritative (config-over-code): checks pull requirements from `forge.policy.json`.
2. Ensure `policy_hash` uses canonical JSON stringify.
3. Add GitHub workflow (e.g., `.github/workflows/deb-preflight.yml`):
   - triggers on PRs that touch `src-tauri/**`, `forge.policy.json`, packaging scripts
   - runs `pnpm preflight:deb:ci -- --json > evidence.json`
   - uploads `evidence.json` as artifact
4. Update docs for CI and artifacts.
5. Update Phase Map.

### Acceptance
- Workflow runs on packaging/config changes.
- Evidence artifact is attached to the run.

### Commit
`preflight(p2): add CI gate + evidence artifacts`

---

# PHASE 3 — Multi-target + quality-of-life flags

### Goal
Extend to other packaging targets + add `--dry-run`, `--fix`, `--watch` as specified.

### Steps
1. Implement `--target` with `debian|rpm|appimage|flatpak`.
2. Expand `forge.policy.json` to include target blocks.
3. Expand schema to validate target blocks.
4. Implement:
   - `--dry-run` (validate policy/config only)
   - `--fix` (safe bounded remediations; exit code `FIX_APPLIED` when changes occur)
   - `--watch` (rerun on changes; exit code `WATCH_TERMINATED` on shutdown)
5. Update docs + Phase Map.

### Acceptance
- Target switching changes which checks run.
- `--fix` only makes safe changes and logs them.
- `--watch` doesn’t produce nondeterministic output.

### Commit
`preflight(p3): add multi-target + dry-run/fix/watch`

---

# FINALIZATION — SMITH changelog

### Goal
Generate a changelog entry from the Phase Map.

### Steps
1. Create or update `CHANGELOG_SMITH.md`.
2. Add an entry summarizing:
   - Added preflight CLI, policy + schema, evidence JSON
   - Debian packaging gated
   - CI workflow gate + evidence artifacts
   - Multi-target support + flags
3. Ensure the changelog is consistent with Phase Map file lists.

### Final Commit
`docs: update SMITH changelog for preflight phases`

---

## Output expectations

When you finish each phase:
- Ensure tests/lint (if present) still pass
- Show the diff summary
- Confirm acceptance criteria
- Make the commit

If anything in the repo differs from plan assumptions (file locations, tauri config shape, package manager), adapt **minimally** and record it in Phase Map under “Notes/Deviations.”

