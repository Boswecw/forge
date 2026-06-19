# Drift Report: <repo-pair>

Generated: `<generated_at>`

Source repo: `<source_repo>`
Source commit: `<source_commit>`

Target repo: `<target_repo>`
Target commit: `<target_commit>`

## Classification Summary

| Classification | Count |
| --- | ---: |
| same | 0 |
| intentional_app_support_adaptation | 0 |
| source_local_hold | 0 |
| missing_from_target | 0 |
| target_only_glue | 0 |
| dangerous_drift | 0 |
| unknown | 0 |

## Items

| Path | Classification | Recommended action |
| --- | --- | --- |

## Notes

Dangerous drift and unknown drift block promotion until resolved by human
decision, backport, or explicit exception.

## Documentation Placement Rule

- Documentation belongs in `/docs`.
- Inactive plans should be condensed to status, decision, evidence, and next
  action.
- `/doc/system` is the canonical code mirror. Treat `/doc/system` drift as
  mirror drift to verify against live code and repo-local build outputs, not as
  general documentation promotion.
