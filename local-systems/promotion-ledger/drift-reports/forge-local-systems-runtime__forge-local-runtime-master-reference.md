# Drift Report: forge-local-systems-runtime__forge-local-runtime-master-reference

Generated: `2026-06-19T09:13:04+00:00`

Source repo: `/home/charlie/Forge/ecosystem/local-systems/forge-local-systems-runtime`
Source branch: `main`
Source commit: `df31e1a98d4789a488e800483a8442643e4036aa`

Target repo: `/home/charlie/Forge/apps/public-app-local-support/forge-local-runtime-master-reference`
Target branch: `main`
Target commit: `c68ae960eb0b609718c93a626f50ccd0a1226c93`

Resolutions applied: `6`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 115 |
| intentional_app_support_adaptation | 5 |
| missing_from_target | 1 |
| target_only_glue | 1 |
| dangerous_drift | 0 |
| unknown | 0 |

## Items

| Path | Classification | Resolution | Recommended action |
| --- | --- | --- | --- |
| `doc/FLSSYSTEM.md` | missing_from_target |  | Review whether this source artifact should be promoted or intentionally excluded. |
| `doc/FOLSYSTEM.md` | target_only_glue | `slice-00-runtime-reference-doc-system-target-only` | Keep as target support mirror glue. Backport only if the proving repo adopts the same aggregate mirror filename. |
| `doc/SYSTEM.md` | intentional_app_support_adaptation | `slice-00-runtime-reference-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime-reference mirror changes. |
| `doc/system/90-appendices.md` | intentional_app_support_adaptation | `slice-00-runtime-reference-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime-reference mirror changes. |
| `doc/system/BUILD.sh` | intentional_app_support_adaptation | `slice-00-runtime-reference-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime-reference mirror changes. |
| `doc/system/_index.md` | intentional_app_support_adaptation | `slice-00-runtime-reference-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime-reference mirror changes. |
| `doc/system/validate_snapshots.sh` | intentional_app_support_adaptation | `slice-00-runtime-reference-doc-system-modified` | Keep as support mirror adaptation. Rebuild /doc/system after runtime-reference mirror changes. |

## Blocking Rule

Dangerous drift and unknown drift block promotion until resolved by human decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as mirror drift to verify against live code and repo-local build outputs, not as general documentation promotion.
