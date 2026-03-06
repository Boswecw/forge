# Forge Documentation Protocol v1

**Status:** Canonical
**Effective date:** 2026-03-06
**Owner:** Charlie
**Scope:** Forge ecosystem repositories with `doc/system/`, `docs/`, or top-level `README.md` entrypoint surfaces

## Purpose

Forge repositories use documentation for doctrine, architecture, runbooks, and operator entrypoints. This protocol defines one shared contract so repository documentation remains auditable, deterministic to build, and explicit about the difference between stable architecture facts and audit-derived snapshot observations.

This protocol governs:

- repository `doc/system/` trees
- assembled `*SYSTEM.md` artifacts
- top-level `README.md` entrypoints
- truth classification for canonical versus snapshot facts
- deterministic `BUILD.sh` assembly behavior
- repo-specific deviation handling
- documentation updates after code-to-doc audits

## Truth Classes

### Canonical Fact

A canonical fact is stable, normative, and architecture-defining. Canonical facts include:

- subsystem role and boundary
- authority ownership
- durable truth ownership
- service port or operating mode
- CLI versus HTTP boundary
- stage ordering
- lifecycle invariants
- failure doctrine
- authentication semantics
- governance ownership

Canonical facts must read as doctrine or invariant statements.

Examples:

- "DataForge is the durable truth store."
- "Forge Eval is a standalone CLI subsystem."
- "ForgeAgents runs on port 8010."

### Snapshot Fact

A snapshot fact is audit-derived and time-sensitive. Snapshot facts include:

- router totals
- endpoint totals
- file counts
- line counts
- component counts
- command counts
- schema or table tallies
- test totals
- coverage percentages
- current implementation surface metrics

Snapshot facts must be labeled visibly. Approved labels include:

- "Current audited snapshot"
- "Current code snapshot"
- "Audit-derived count"
- "As of this document version"

Snapshot facts must never be phrased as timeless doctrine.

### Planned / Not Implemented

If behavior is planned but not implemented, documentation must say so directly.

Approved wording:

- "Planned, not yet implemented"
- "Contract defined; runtime not implemented"
- "Out of scope in current runtime"

### Representative Breakdown

Breakdown tables that illustrate a larger system without guaranteeing a full sum must say so explicitly.

Approved wording:

- "Representative snapshot breakdown"
- "Representative domain breakdown"
- "Illustrative breakdown; top-line total appears above"

## Required `doc/system/` Structure

Each protocol-compliant repository `doc/system/` tree must include:

- `_index.md`
- `BUILD.sh`
- zero or more numbered chapter files named `NN-*.md`

Preferred chapter semantics:

1. Overview / Philosophy
2. Architecture
3. Tech Stack
4. Project Structure
5. Config / Env / CLI
6+. Repo-specific operational chapters
final major chapter: Handover / Runbook / Constraints
optional last chapter: Documentation Truth Policy

This ordering is guidance, not forced identity. Repo-specific architecture may justify different later chapters.

## `_index.md` Contract

Each `_index.md` must state:

- document title
- protocol version reference
- short truth-class summary
- table of parts or equivalent index
- assembly command
- assembled output artifact path/name
- last updated date

If the repo has important deviations from the resident-service model, `_index.md` should say so near the top.

Examples:

- Forge Eval is CLI-oriented and emits local artifacts.
- forge-smithy is Tauri/IPC centered rather than a resident HTTP service.
- ecosystem-level docs aggregate cross-repo truth instead of documenting one local runtime.

## Naming Conventions

### Files

- `_index.md` for the index
- `NN-*.md` for numbered chapters
- assembled artifact name in the form `<prefix>SYSTEM.md` when the repo convention already uses a prefix
- `SYSTEM.md` for the ecosystem-level aggregate unless a repo-specific prefix is already canonical

### Narrative Names vs Code IDs

If a system uses both human-readable narrative names and code-facing identifiers, documentation must distinguish them clearly.

Example:

- narrative stage: `reviewer findings`
- stage/artifact ID: `review_findings`
- internal implementation name, if different: `reviewer_execution`

Do not silently mix these names.

## BUILD.sh Contract

Each compliant `doc/system/BUILD.sh` must:

- use `#!/usr/bin/env bash`
- use `set -euo pipefail`
- derive `SCRIPT_DIR` from `${BASH_SOURCE[0]}`
- write exactly one assembled output artifact
- assemble `_index.md` first
- append numbered `NN-*.md` files in lexical order
- insert deterministic separators between sections
- skip missing numbered files safely
- print a final summary with the output artifact path or line count
- avoid side effects unrelated to assembly

Default assembly logic:

1. resolve `SCRIPT_DIR`
2. define `OUTPUT`
3. discover numbered parts with lexical ordering
4. write `_index.md`
5. append `---` separator
6. append each numbered part with deterministic separators
7. print completion summary

Builder scripts must remain simple and boring. No content rewriting, filtering, or repo-specific transformations unless there is a documented deviation.

## Canonical README Contract

When a top-level `README.md` exists, it must act as the repository entrypoint and state:

- repo identity
- repo type: service, desktop app, CLI subsystem, library, or internal tooling
- authority boundary or ownership boundary
- whether the README is overview-only, operational entrypoint guidance, or deeper local reference
- where `doc/system/` lives when present
- which document is authoritative for deeper reference
- truth-class guidance for metrics in the README

Minimum approved README contract block:

- role
- boundary
- doc authority
- truth-class note

Example:

- "This README is the repository entrypoint overview. `doc/system/_index.md` and the assembled system reference are the authoritative deep references."
- "Counts and status badges in this README are snapshot facts unless explicitly marked as targets or invariants."

## Snapshot Labeling Rules

When numeric counts appear:

- label them as snapshot values
- keep them close to the metric they qualify
- avoid repeating the same total in multiple sections unless each repetition is clearly scoped

If one section presents a top-line total and another section presents a breakdown:

- make the top line the audited total
- make the breakdown explicitly representative unless it is guaranteed to reconcile

## Repo Deviation Rules

Repository differences are allowed when they reflect real architecture.

Accepted deviation examples:

- Forge Eval has no resident HTTP API in the current Pack J runtime
- forge-smithy is centered on Tauri IPC, frontend routes, and governance runtime
- `smithy` is a vendored library, not a service
- ecosystem-level docs aggregate cross-repo doctrine

Deviations must be:

- explicit
- justified by code or established doctrine
- documented in `_index.md`, README, or the compliance report

Do not flatten meaningful differences just to force symmetry.

## Handover / Runbook Requirements

Each mature `doc/system/` tree should include a final handover or runbook chapter that documents:

- critical invariants
- operator warnings
- build or startup sequence
- migration or maintenance cautions
- known limitations

If a repo is not mature enough for a full runbook, the compliance report must say so.

## Maintenance Rules After Audits

After any code-to-doc audit:

1. verify canonical facts from code or canonical doctrine before editing them
2. relabel measured counts as snapshot facts
3. update `_index.md` last-updated date when the doc set changes materially
4. rebuild the assembled artifact with `BUILD.sh`
5. record unresolved contradictions in the current audit report

Do not guess at unresolved facts. Fail closed and record them.

## Canonical Documentation Registry

The canonical inventory for governed documentation surfaces is:

- `docs/canonical/documentation_registry_v1.json`

The registry is the source of truth for:

- which repos or surfaces are governed
- whether a surface is mature, partial, deferred, or historical
- which policy class applies
- whether README contract checks are required
- whether a full `doc/system/` tree is required
- which assembled `*SYSTEM.md` artifact belongs to the surface

New governed surfaces must be added to the registry before they are treated as compliant. Do not duplicate repo inventory in multiple scripts once the registry exists.

## Documentation Policy Classes

Registry entries must map each governed surface onto one policy class. Policy class defines the default documentation obligation; the registry may promote a surface beyond the class baseline when that deviation is intentional and recorded.

### Runtime Subsystem

Examples:

- `NeuroForge`
- `DataForge`
- `ForgeAgents`
- `rake`

Default requirements:

- canonical `README.md` required
- full `doc/system/` required
- deterministic `BUILD.sh` required
- assembled `*SYSTEM.md` required
- full protocol gate enforced

### Desktop Authority / Operator Application

Examples:

- `forge-smithy`
- `Forge_Command`

Default requirements:

- canonical `README.md` required
- full `doc/system/` required
- deterministic `BUILD.sh` required
- assembled `*SYSTEM.md` required
- UI / IPC / integration chapters included as the local architecture requires

### Standalone Governed CLI / Subsystem

Examples:

- `forge-eval/repo`

Default requirements:

- canonical `README.md` required
- full `doc/system/` required
- deterministic `BUILD.sh` required
- assembled `*SYSTEM.md` required
- CLI, stage, artifact, and interface boundary chapters included where applicable

### Support Surface

Examples:

- `checkly`
- promoted support/tooling repos such as `forge-telemetry`, `ForgeImages`, or `smithy` when the registry explicitly requires more than README-only coverage

Default requirements:

- canonical `README.md` required
- full `doc/system/` not required unless the registry explicitly promotes the surface
- deterministic builder and assembled artifact required only when the registry explicitly requires `doc/system/`
- limited protocol gate by default; full protocol gate only when promoted by registry

### Canonical Doctrine / Cross-Cutting Docs Surface

Examples:

- ecosystem root aggregate docs
- canonical doctrine directories when explicitly governed as standalone surfaces

Default requirements:

- canonical entrypoint documentation required
- full `doc/system/` required when the surface owns an assembled system reference
- no fake service/runtime chapters should be invented
- boundaries must state that the surface governs doctrine rather than serving runtime traffic

### Historical / Archived Surface

Default requirements:

- historical labeling required
- active compliance checks are limited to labeling and boundary sanity
- legacy values may remain only when clearly marked historical or snapshot

### Deferred Surface

Examples:

- `contracts`
- `doctrine`
- `fixtures`
- `forge-brand`

Default requirements:

- registry entry required
- doc expectation explicitly marked deferred
- checker and `doc-audit` must not falsely report the surface as compliant
- follow-up status should appear in the active audit report

## Compliance Gate

Forge documentation is enforced through a registry-driven two-layer gate:

1. `scripts/check-documentation-protocol.py` for protocol-bearing surface checks
2. `scripts/doc-audit` for registry inventory, discovery, stale-output detection, and CI-facing enforcement

Recommended front door:

```bash
bash scripts/doc-audit
```

Strict CI / merge-gate mode:

```bash
bash scripts/doc-audit --strict --run-builds
```

Optional scoped mode for local review or changed-surface pipelines:

```bash
bash scripts/doc-audit --changed-only
bash scripts/doc-audit --changed-only --changed-path <path> [--changed-path <path> ...]
bash scripts/doc-audit --changed-only --changed-paths-file /tmp/doc-audit-paths.txt
```

Changed-only mode may auto-discover changes from nested git repos. Workspace-root surfaces that are not git repos should pass explicit changed paths when scoped auditing is required.

CI systems should prefer an explicit changed-path file produced from the repository diff rather than relying on local dirty-state discovery. The default workflow entrypoint is:

```bash
bash scripts/collect-doc-audit-paths.sh --base <sha> --head <sha> --output /tmp/doc-audit-paths.txt
bash scripts/doc-audit --strict --run-builds --changed-only --changed-paths-file /tmp/doc-audit-paths.txt
```

CI should also emit machine-readable and human-readable audit artifacts:

```bash
bash scripts/doc-audit --strict --run-builds \
  --changed-only \
  --changed-paths-file /tmp/doc-audit-paths.txt \
  --report-out /tmp/doc-audit-report.md \
  --json-out /tmp/doc-audit-report.json
```

Those outputs should be uploaded as CI artifacts even when the audit fails so stale-doc hints and scoped-surface decisions remain inspectable after the run.

CI should also translate the JSON output into inline annotations and a run summary. Recommended pattern:

```bash
python3 scripts/emit-doc-audit-annotations.py --json /tmp/doc-audit-report.json
```

When `GITHUB_STEP_SUMMARY` is present, the annotation emitter should append:

- scoped-surface summary
- stale or missing assembled-doc hints
- high-signal warnings and errors

For pull requests, CI should also render and upsert a single sticky comment from the same JSON payload:

```bash
python3 scripts/render-doc-audit-comment.py \
  --json /tmp/doc-audit-report.json \
  --out /tmp/doc-audit-comment.md
```

The PR comment should:

- summarize pass/warn/fail status
- list the scoped surfaces
- include changed-path context when the scoped path list is short enough to stay readable
- surface stale or missing assembled-doc hints
- avoid duplicate comment spam by updating one stable marker comment

Lower-level checker entrypoint:

```bash
python3 scripts/check-documentation-protocol.py
python3 scripts/check-documentation-protocol.py --expected-report-date YYYY-MM-DD --run-builds
```

The registry-driven gate verifies:

- canonical protocol spec exists
- canonical documentation registry exists and is valid
- latest or explicitly required audit report exists
- audit report covers tracked compliant, partial, and deferred surfaces
- required protocol-bearing READMEs contain the canonical `Documentation Contract` fields
- surfaces whose registry policy requires `doc/system/` contain protocol-aware `_index.md`
- required `doc/system/BUILD.sh` scripts match the deterministic contract
- required assembled `*SYSTEM.md` artifacts exist and can be rebuilt deterministically
- newly discovered nested repos and submodules are visible relative to the registry
- stale assembled artifacts are surfaced to operators and CI
- maintained protocol surfaces do not reintroduce forbidden legacy markers such as old protocol naming or retired canonical ports

This gate is intentionally conservative. If a new mature repo, support surface, nested repo, or deferred surface is added, update the registry first, then refresh the audit report.

## Submodule And Newly Discovered Repo Intake Rules

When a new sibling repo, submodule, or attached tooling repo is discovered:

1. determine whether it is a real repo or only a workspace directory
2. check for `doc/system/`, `docs/`, and a top-level `README.md`
3. add or update the registry entry before changing checker logic
4. classify it by policy class, maturity class, doc class, and status
5. if mature enough, apply the protocol
6. if not mature enough, add at least:
   - a README entrypoint note if one exists
   - compliance report entry with follow-up status

Do not fabricate a deep system manual for immature repos.
