# Documentation Protocol Canonicalization Report — 2026-03-06

## Scope

This report records the documentation protocol canonicalization pass across the Forge ecosystem workspace on 2026-03-06.

Primary target surfaces:
- top-level `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- selected `doc/system/` chapters where canonical vs snapshot drift or port/name contradictions were obvious and safely resolvable

Authority for this pass:
- `docs/canonical/documentation_protocol_v1.md`

## Protocol Decisions Applied

1. Canonical facts and snapshot facts are now explicitly separated.
2. `_index.md` files now carry a shared protocol header, truth-class summary, build command, output artifact, and last-updated date.
3. `doc/system/BUILD.sh` scripts were normalized to one deterministic assembly contract:
   - `#!/usr/bin/env bash`
   - `set -euo pipefail`
   - `_index.md` first
   - numbered chapters in lexical order
   - deterministic separators
   - explicit output summary
4. Top-level READMEs now use a shared `Documentation Contract` block that states:
   - repo/surface type
   - authority boundary
   - deep reference
   - README role
   - truth-note behavior for snapshot metrics
5. Repo-specific deviations were preserved and made explicit rather than flattened.
6. Stale canonical port references were corrected in targeted `README` and `doc/system` surfaces.
7. Remaining `BDS Protocol` naming inside maintained `doc/system` sources was replaced with Forge Documentation Protocol naming where the reference described the active documentation standard rather than a historical artifact.
8. Registry-driven governance replaced hardcoded repo inventory in the protocol checker.
9. `doc-audit` became the first-class front door for discovery, stale assembled-doc detection, and CI-facing enforcement.
10. Documentation policy classes are now canonical, and registry entries determine whether a surface is full-system-doc, README-only, deferred, or historical.

## Repos Examined

Primary in-scope repos and surfaces examined:
- ecosystem root
- `NeuroForge`
- `DataForge`
- `ForgeAgents`
- `rake`
- `forge-smithy`
- `forge-eval/repo`
- `Forge_Command`
- `ForgeImages`
- `canebrake_press`
- `cortex_bds`
- `smithy`
- `tarcie`
- `zfss`

Additional discovered ecosystem participants examined:
- nested git repo: `DataForge/forge-telemetry`
- workspace monitoring surface: `checkly`
- workspace support surfaces reviewed for intake status only: `contracts`, `doctrine`, `fixtures`, `forge-brand`

Submodules:
- none found

## Files Changed

### Canonical protocol
- `docs/canonical/documentation_protocol_v1.md` (new)
- `docs/canonical/documentation_registry_v1.json` (new)

### Compliance report
- `docs/audits/documentation_protocol_canonicalization_report_2026-03-06.md` (new)

### Verification gate
- `scripts/check-documentation-protocol.py` (new)
- `scripts/doc-audit` (new)
- `scripts/doc-audit.py` (new)
- `scripts/doc_registry.py` (new)
- `scripts/README.md`

### CI integration
- `.github/workflows/documentation_protocol.yml` (new)

### Ecosystem root
- `README.md`
- `doc/README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/SYSTEM.md` (rebuilt)

### NeuroForge
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/02-architecture.md`
- `doc/system/03-tech-stack.md`
- `doc/system/08-ecosystem-integration.md`
- `doc/nfSYSTEM.md` (rebuilt)

### DataForge
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/02-architecture.md`
- `doc/system/05-config-env.md`
- `doc/system/11-handover.md`
- `doc/dfSYSTEM.md` (rebuilt)

### DataForge/forge-telemetry
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/01-overview-philosophy.md`
- `doc/system/02-architecture.md`
- `doc/system/03-tech-stack.md`
- `doc/system/04-project-structure.md`
- `doc/system/05-config-env.md`
- `doc/system/06-handover.md`
- `doc/ftSYSTEM.md` (rebuilt)

### ForgeAgents
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/01-overview-philosophy.md`
- `doc/system/02-architecture.md`
- `doc/system/03-tech-stack.md`
- `doc/system/04-project-structure.md`
- `doc/system/05-config-env.md`
- `doc/system/07-backend-internals.md`
- `doc/system/08-ecosystem-integration.md`
- `doc/system/11-handover.md`
- `doc/faSYSTEM.md` (rebuilt)

### rake
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/02-architecture.md`
- `doc/raSYSTEM.md` (rebuilt)

### forge-smithy
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/01-overview-philosophy.md`
- `doc/system/02-architecture.md`
- `doc/system/05-config-env.md`
- `doc/system/10-security-compliance.md`
- `doc/system/11-ecosystem-integration.md`
- `doc/system/14-error-handling.md`
- `doc/fsSYSTEM.md` (rebuilt)

### forge-eval/repo
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/feSYSTEM.md` (rebuilt)

### Forge_Command
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/01-overview-philosophy.md`
- `doc/system/02-architecture.md`
- `doc/system/04-project-structure.md`
- `doc/system/08-tauri-command-interface.md`
- `doc/system/12-ecosystem-integration.md`
- `doc/system/16-headless-mode.md`
- `doc/fcSYSTEM.md` (rebuilt)

### ForgeImages
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/fiSYSTEM.md` (rebuilt)

### canebrake_press
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/system/02-architecture.md`
- `doc/system/04-project-structure.md`
- `doc/system/05-config-environment.md`
- `doc/system/08-api-fastify.md`
- `doc/system/09-python-backend.md`
- `doc/system/10-dataforge-crud.md`
- `doc/system/32-forgeagents-integration.md`
- `doc/cpSYSTEM.md` (rebuilt)

### cortex_bds
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/cbSYSTEM.md` (rebuilt)

### smithy
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/spSYSTEM.md` (rebuilt)

### tarcie
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/tcSYSTEM.md` (rebuilt)

### zfss
- `README.md`
- `doc/system/_index.md`
- `doc/system/BUILD.sh`
- `doc/zsSYSTEM.md` (rebuilt)

### Additional discovered surfaces
- `DataForge/forge-telemetry/README.md`
- `checkly/README.md`

## Accepted Repo-Specific Deviations

- `forge-eval/repo`: standalone CLI evaluator, local artifacts, no resident HTTP API in the current Pack J runtime.
- `forge-smithy`: desktop/Tauri + IPC governance workbench, not a resident backend service.
- `Forge_Command`: desktop control plane with a local orchestrator and local API boundary.
- `ForgeImages`: tooling/library-oriented repo, not a resident ecosystem service.
- `smithy`: vendored Rust library, not a service.
- `tarcie`, `cortex_bds`, `zfss`: local-first desktop/tooling repos rather than resident backend services.
- ecosystem root: aggregate cross-repo reference, not a repo-local subsystem manual.
- `checkly`: README-only workspace monitoring surface; no `doc/system/` tree yet.

## Compliance Matrix — Repositories

| Repo / Surface | Discovery | Canonical README | `_index.md` | `BUILD.sh` | Truth Classes Explicit | Snapshot Labeling | Deviations Documented | Status | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| ecosystem root | workspace root | yes | yes | yes | yes | yes | yes | compliant | Aggregate reference rebuilt to `doc/SYSTEM.md`. |
| NeuroForge | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Canonical ForgeCommand port references corrected in targeted chapters. |
| DataForge | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Canonical service port normalized to `8001` in targeted chapters. |
| forge-telemetry | nested git repo | yes | yes | yes | yes | yes | yes | compliant | Shared library deviation explicit; `doc/ftSYSTEM.md` added. |
| ForgeAgents | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Canonical service port normalized to `8010`; README and local system manual now agree. |
| rake | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | README and architecture docs now use canonical DataForge / ForgeCommand references. |
| forge-smithy | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Desktop/Tauri deviation explicit; canonical ForgeAgents/ForgeCommand references corrected. |
| forge-eval/repo | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | CLI-only deviation explicit; Pack J boundary preserved. |
| Forge_Command | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Canonical docs and active runtime/docs now distinguish `8003` orchestrator, `8004` Axum API, and auxiliary token bridge `8790`. |
| ForgeImages | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Tooling repo deviation explicit. |
| canebrake_press | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | App repo deviation explicit; targeted service URLs normalized. |
| cortex_bds | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Local-first desktop/tooling deviation explicit. |
| smithy | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Vendored library deviation explicit. |
| tarcie | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Local capture-tool deviation explicit. |
| zfss | primary workspace repo | yes | yes | yes | yes | yes | yes | compliant | Local authoritative-store deviation explicit. |
## Compliance Matrix — Additional Workspace Surfaces

| Surface | Type | Canonical README | `doc/system/` | Status | Notes |
|---|---|---:|---:|---|---|
| eval-cal-node | standalone CLI subsystem | yes | no | partial | Post-implementation calibration node; README contract present; no `doc/system/` tree yet (deferred to later revision). |
| checkly | workspace monitoring surface | yes | no | partial | README contract added; no repo-local system manual exists. |
| contracts | workspace support surface | no | no | deferred | Useful support surface; no protocol header or `doc/system/` tree yet. |
| doctrine | workspace support surface | no | no | deferred | References canonical docs but does not yet carry a protocol contract. |
| fixtures | workspace support surface | no | no | deferred | Fixture surface; no protocol contract yet. |
| forge-brand | workspace support surface | no | no | deferred | Asset surface; no protocol contract yet. |

## Unresolved Mismatches

1. `checkly`, `contracts`, `doctrine`, `fixtures`, and `forge-brand` are active workspace documentation surfaces without full protocol structures.
   - `checkly` received a README contract because it is an operator-facing surface.
   - The others are deferred pending a decision on whether they should remain lightweight support surfaces or gain formal `doc/system/` trees.

## Follow-Up Recommendations

1. Use `bash scripts/doc-audit --strict --run-builds` as the primary documentation governance command in CI and local release checks.
2. Onboard any newly discovered repo by adding a registry entry before touching checker logic.
3. Keep support, deferred, and historical surfaces explicit in the registry instead of promoting them implicitly through ad hoc script edits.
2. Decide whether `checkly`, `contracts`, `doctrine`, `fixtures`, and `forge-brand` should remain lightweight workspace surfaces or receive minimal protocol headers by default.

## Rebuild Verification

Rebuilt assembled system references during this pass:
- `doc/SYSTEM.md`
- `NeuroForge/doc/nfSYSTEM.md`
- `DataForge/doc/dfSYSTEM.md`
- `ForgeAgents/doc/faSYSTEM.md`
- `rake/doc/raSYSTEM.md`
- `forge-smithy/doc/fsSYSTEM.md`
- `forge-eval/repo/doc/feSYSTEM.md`
- `Forge_Command/doc/fcSYSTEM.md`
- `ForgeImages/doc/fiSYSTEM.md`
- `canebrake_press/doc/cpSYSTEM.md`
- `cortex_bds/doc/cbSYSTEM.md`
- `smithy/doc/spSYSTEM.md`
- `tarcie/doc/tcSYSTEM.md`
- `zfss/doc/zsSYSTEM.md`

All targeted `BUILD.sh` scripts completed successfully after normalization.
