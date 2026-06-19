# Slice 00 Source Authority Intake Proof

Generated: `2026-06-19T08:19:01Z`

This continuation completes the first source-intake pass from
`docs-condensed-authority-review.md`. It moves target-only support doctrine into
the local-system proving repos as source-truth baselines before any support
promotion decision.

## Source Commits

| Repo | Commit | Scope |
| --- | --- | --- |
| `dataforge-Local` | `536b700fa7f11bf92c75e5f8c540c4b571ebb17b` | Added six DF Local source authority docs for app integration, architecture, backup/export/restore, migration, operational visibility, and privacy. |
| `neuronforge-local-operator` | `006ef57c9ece79b666581b303fce06e54debaa42` | Added five AuthorForge task-routing source docs for envelope, router plan, local/cloud boundary, model routing, and task lanes. |

## Added Source Docs

### DataForge Local

- `docs/app-integration-contract.md`
- `docs/architecture.md`
- `docs/backup-export-restore.md`
- `docs/migration-doctrine.md`
- `docs/operational-visibility.md`
- `docs/privacy-doctrine.md`

### NeuronForge Local Operator

- `docs/authorforge-task-envelope-contract.md`
- `docs/authorforge-task-router-plan.md`
- `docs/local-first-cloud-assist-boundary.md`
- `docs/model-routing-doctrine.md`
- `docs/registries/task-lanes.md`

## Verification

| Command | Result |
| --- | --- |
| `bash doc/system/BUILD.sh` in `dataforge-Local` | Passed; `doc/DLOSYSTEM.md` assembled with 20 parts / 966 lines. |
| `bash doc/system/BUILD.sh` in `neuronforge-local-operator` | Passed; `NLOSYSTEM.md` assembled with 3556 lines. |
| `git diff --cached --check` in both source repos | Passed before commit. |
| `python3 scripts/generate_drift_inventory.py --overwrite` in the ledger | Passed after source commits. |

## Drift Result

The regenerated drift reports still have `unknown: 204`, but the documentation
shape changed:

| Documentation drift shape | Count | Meaning |
| --- | ---: | --- |
| `/docs` unknown present in both source and target | 13 | Source-backed, still content-different and requires reconciliation. |
| `/docs` unknown target-only | 8 | Support-only docs/evidence or still-needing explicit exception/backport. |
| `/docs` missing from target | 65 | Source docs not yet promoted to app-support target. |

The 11 source-intake-required files from the previous review are now present in
the source repos. They intentionally do not copy support claims wholesale:

- DF Local docs anchor to existing migrations/status/registry proof.
- NeuronForge docs mark the general AuthorForge task router and cloud assist as
  planned until source routes, schemas, tests, and receipts prove the behavior.

## Remaining Gate

Next pass: reconcile the 13 source-present `/docs` deltas. Prefer source code and
source `doc/system` truth over support wording. After reconciliation, regenerate
drift reports and promote only source-backed, verified support docs.

Continuation: `source-to-support-doc-reconciliation-proof.md` records the
completed source-to-support reconciliation and the reduced `unknown` count.
