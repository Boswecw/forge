# Slice 00 Proof Gate Inventory

Generated: `2026-06-19T07:04:12Z`

This inventory records known proving-side gates and the currently visible
target-side gates. Slice 00 does not add or change runtime gates.

## Proving Repos

| Repo | Required gate |
| --- | --- |
| `/home/charlie/Forge/ecosystem/local-systems/forge-local-systems-runtime` | `make validate` |
| `/home/charlie/Forge/ecosystem/local-systems/cortex` | `make validate`; `make test-runtime`; `make test-gnats` when GNAT/local retrieval surfaces are touched |
| `/home/charlie/Forge/ecosystem/local-systems/dataforge-Local` | `bash ci_gate.sh` |
| `/home/charlie/Forge/ecosystem/local-systems/neuronforge-local-operator` | `bash scripts/run-tests.sh`; manual baseline review for model/prompt promotions |
| `/home/charlie/Forge/ecosystem/local-systems/fa-local-operator` | `cargo test`; `bash ci_gate.sh` if the slice touches its contract gate |

## Target Repos

| Target repo | Existing gate evidence | Gap |
| --- | --- | --- |
| `/home/charlie/Forge/apps/public-app-local-support/forge-local-runtime-master-reference` | `Makefile` exposes `make validate`, `make validate-schemas`, `make check-boundaries` | No gap identified for Slice 00 inventory. |
| `/home/charlie/Forge/apps/public-app-local-support/cortex` | `Makefile` exposes `make validate` and `make test-runtime` | No `make test-gnats` target visible in the app-support Cortex copy. |
| `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` | `pyproject.toml` defines pytest settings and dev dependencies | No explicit repo-local Makefile or CI gate visible. Record as a target validation gap. |
| `/home/charlie/Forge/apps/public-app-local-support/neuronforge` | `tests/test-continuity-adjacent-scene.sh` exists | No broad target-side test runner visible. Record as a target validation gap. |
| `/home/charlie/Forge/apps/public-app-local-support/fa-local` | `Cargo.toml` exists; `cargo test` is plausible | No target-side `ci_gate.sh` visible. Contract-gate parity is a gap when contract surfaces are promoted. |

## Slice 00 Gate Policy

- Proving-side gates remain authoritative for foundational changes.
- Target-side gates are post-promotion compatibility checks.
- Missing target gates must be recorded as gaps, not silently treated as proof.
