# Slice 00 Root Documentation Condensation Proof

Generated: `2026-06-19T07:55:00Z`

This receipt records the root documentation cleanup performed after the
documentation placement rule was established.

## Rule

Human-facing documentation belongs in `/docs`. Root README files should be short
orientation pointers. `CLAUDE.md` files are repo-local agent metadata and remain
at the repo root.

## Changes

| Repo | Change |
| --- | --- |
| `/home/charlie/Forge/apps/public-app-local-support/df-local-foundation` | Condensed `README.md`; moved `CLOSEOUT.md` to `docs/closeout-initial-governed-implementation.md`. |
| `/home/charlie/Forge/apps/public-app-local-support/neuronforge` | Condensed `README.md` to status, docs, scripts, and mirror pointers. |
| `/home/charlie/Forge/apps/public-app-local-support/fa-local` | Condensed `README.md` to status, docs, and mirror pointers. |

## Left In Place

The following root files remain because they are agent metadata rather than
human-facing documentation:

- `df-local-foundation/CLAUDE.md`
- `neuronforge/CLAUDE.md`
- `fa-local/CLAUDE.md`

## Validation

- Stale old-path reference scan: clean.
- `git diff --check`: clean for touched app-support repos.
