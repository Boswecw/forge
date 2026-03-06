# Ecosystem-QC v0.3.0

Meta-runner for quality control across all Forge ecosystem repos. Supports **fast** (docs/stateforge), **deep** (fast + cargo check/test), or **both** modes with deterministic reporting.

## Quick Start

```bash
cd /home/charlie/Forge/ecosystem/tools/ecosystem-qc
bun install
bun run qc                              # default: --mode=both
bun run qc:fast                         # docs + stateforge only
bun run qc:deep                         # full pipeline per repo
bun run qc -- --only=forge-smithy       # single repo
cat out/ecosystem-qc.report.json
```

## CLI Flags

| Flag | Default | Description |
|---|---|---|
| `--root=<path>` | `/home/charlie/Forge/ecosystem` | Ecosystem root directory |
| `--mode=fast\|deep\|both` | `both` | Which phases to run |
| `--only=a,b` | *(all)* | Run only named repos |
| `--skip=a,b` | *(none)* | Skip named repos |
| `--fail-fast` | `false` | Stop at first failing repo |
| `--continue-on-fast-fail` | `false` | In `both` mode, run deep even if fast failed |
| `--concurrency=N` | `2` | Parallel repos in deep phase |
| `--out=<path>` | `out/ecosystem-qc.report.json` | Report output path |

## Phases

### FAST
1. `gitStatus` — warning by default; fatal if `enforceCleanWorkingTree=true`
2. `docSystemBuild` — runs `doc/system/BUILD.sh` if present
3. `docSystemDiffClean` — `git diff --exit-code` after build
4. `stateforge` — runs stateforge if `tools/stateforge/` exists

### DEEP
5. `cargoCheck` — `cargo check --lib`
6. `cargoTest` — `cargo test --lib -q`
7. `nodeTest` — only if explicitly configured in `.forgeqc.json`

In `--mode=deep`, fast checks run first per repo.
In `--mode=both`, fast phase runs across all repos, then deep phase (with skip logic for fast failures).

## Per-Repo Config

Optional `.forgeqc.json` at repo root:

```json
{
  "checks": {
    "docSystemBuild": "bash doc/system/BUILD.sh",
    "docSystemDiffClean": true,
    "stateforge": "bun run stateforge",
    "cargoCheck": "cargo check --lib",
    "cargoTest": "cargo test --lib -q",
    "nodeTest": "bun test"
  },
  "timeoutsMs": {
    "docSystemBuild": 60000,
    "cargoCheck": 300000,
    "cargoTest": 900000
  },
  "phases": {
    "enableFast": true,
    "enableDeep": true
  },
  "enforceCleanWorkingTree": false
}
```

If absent, checks are auto-detected based on file presence (Cargo.toml, BUILD.sh, etc.).

## Exit Codes

- `0` — all selected phases pass
- `1` — any failure (report always written)

## Report

JSON written to `--out` path. Report is always written, even on SIGINT or crash. See `src/types.ts` for full schema.

## CI

See `.github/workflows/ecosystem-qc.yml` for GitHub Actions integration.
