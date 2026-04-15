# 04 — Registries and Role Matrix

## Files

| File | Purpose |
|---|---|
| `registry/artifact_family_registry.json` | Admitted families, their versions, producers, consumers |
| `registry/version_registry.json` | Version status per family (active/deprecated/sunset) |
| `registry/deprecation_registry.json` | Deprecated version records |
| `registry/repo_role_matrix.json` | Per-repo role class, emit/consume permissions, gate profiles |

## Repo role matrix

The role matrix is the authoritative source for what each ecosystem repo may do.

### Direct proving-slice participants

| Repo | Role Class | Emits | Consumes | Promotes | Review Surface |
|---|---|---|---|---|---|
| `forge-contract-core` | contract_core | — | — | no | no |
| `dataforge-Local` | producer_promoter | source_drift_finding, promotion_envelope | promotion_receipt | yes | no |
| `DataForge` | shared_truth_consumer, shared_truth_owner | promotion_receipt | source_drift_finding, promotion_envelope | no | no |
| `Forge_Command` | review_surface | — | source_drift_finding, promotion_receipt | no | yes |

### Execution bridge v1 participants

| Repo | Role Class | Emits | Consumes | Gate Profile |
|---|---|---|---|---|
| `fa-local` | execution_consumer | execution_request, execution_status_event | approval_artifact | contract_core_gate + cargo_test |
| `Forge_Command` | review_surface, approval_authority | approval_artifact | source_drift_finding, promotion_receipt, execution_request, execution_status_event | (proving slice gates) |

### Indirect / future participants

| Repo | Role Class | Notes |
|---|---|---|
| `forge-eval` | evaluation_producer | Indirect first-wave participant |
| `ForgeMath` | evaluation_producer | Indirect first-wave participant |
| `forgeHQ` | producer_only | Excluded from proving slice 01 |

## Forbidden payload classes

The role matrix records what each repo must never emit:
- `forge-contract-core` — forbidden from all runtime artifacts
- `dataforge-Local` — forbidden from emitting execution_request, approval_artifact
- `DataForge` — forbidden from emitting execution_request, approval_artifact
- `Forge_Command` — may emit approval_artifact only; forbidden from emitting execution_request or lifecycle truth
- `fa-local` — forbidden from emitting source_drift_finding, promotion_envelope, promotion_receipt

## Required gate profiles

Each direct participant carries a required gate profile in the role matrix. These gate profiles must pass in CI for the repo to be considered proving-slice ready.
