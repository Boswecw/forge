# scripts/

Ecosystem utility scripts for documentation and infrastructure management.

## Contents

| Script | Purpose |
|--------|---------|
| `build-ecosystem-docs.cjs` | Aggregates service documentation into a single snapshot (output is not committed) |
| `check-documentation-protocol.py` | Registry-driven protocol checker for README contracts, `doc/system/` surfaces, builder compliance, legacy marker drift, and audit report coverage |
| `collect-doc-audit-paths.sh` | CI-oriented changed-file collector for `doc-audit --changed-only` |
| `doc-audit` | First-class documentation governance command for discovery, checker execution, stale assembled-doc detection, optional builder runs, and CI-friendly exit codes |
| `doc-audit.py` | Python implementation behind `doc-audit` |
| `doc_registry.py` | Shared registry loader and policy metadata helper used by documentation governance tools |
| `emit-doc-audit-annotations.py` | Converts `doc-audit` JSON output into GitHub annotations and a step summary |
| `render-doc-audit-comment.py` | Renders a concise PR comment body from `doc-audit` JSON output |
| `context-bundle.sh` | Generates context bundles for AI assistant sessions |
| `validate-connectivity-checklist.mjs` | Validates inter-service connectivity |

## `doc-audit` Highlights

- `bash scripts/doc-audit --strict --run-builds`
  - full registry-driven compliance and builder verification
- `bash scripts/doc-audit --changed-only`
  - auto-scopes to changed nested repos using per-repo `git status`
- `bash scripts/doc-audit --changed-only --changed-path README.md --changed-path forge-eval/repo/doc/system/_index.md`
  - explicit scope for workspace-root or CI-provided path sets
- `bash scripts/doc-audit --changed-only --changed-paths-file /tmp/changed-paths.txt`
  - scopes from an external changed-file list without relying on local git state
- stale assembled-doc findings now include rebuild hints and source-file context

## CI Path Collection

- `bash scripts/collect-doc-audit-paths.sh --base <sha> --head <sha> --output /tmp/doc-audit-paths.txt`
  - produces the changed-path input file used by the documentation workflow
- if `--base` is missing or all-zero, the collector falls back to the single head commit
- the documentation workflow also writes:
  - `/tmp/doc-audit-report.md`
  - `/tmp/doc-audit-report.json`
  - and uploads them as CI artifacts even when the audit step fails
- the workflow also runs:
  - `python3 scripts/emit-doc-audit-annotations.py --json /tmp/doc-audit-report.json`
  - which emits GitHub annotations and appends a step summary when audit results exist
  - `python3 scripts/render-doc-audit-comment.py --json /tmp/doc-audit-report.json --out /tmp/doc-audit-comment.md`
  - which produces the sticky pull-request comment body used by the documentation workflow, including changed-path context when the scoped path list is short
