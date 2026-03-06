# Forge Documentation Protocol v1 — Prefix Registry

Every Forge ecosystem repo uses a **2-character prefix** on its assembled system documentation file (`{prefix}SYSTEM.md`). This makes the source repo instantly identifiable when files are copied to external AI assistants.

## Active Prefixes

| Prefix | Repo | Directory | Output File |
|--------|------|-----------|-------------|
| `af` | AuthorForge | `Author-Forge/` | `doc/afSYSTEM.md` |
| `cp` | Canebrake Press | `Canebrake_press/` | `doc/cpSYSTEM.md` |
| `df` | DataForge | `DataForge/` | `doc/dfSYSTEM.md` |
| `fa` | ForgeAgents | `ForgeAgents/` | `doc/faSYSTEM.md` |
| `fc` | ForgeCommand | `Forge_Command/` | `doc/fcSYSTEM.md` |
| `ft` | Forge Telemetry | `DataForge/forge-telemetry/` | `doc/ftSYSTEM.md` |
| `fs` | Forge:SMITH | `forge-smithy/` | `doc/fsSYSTEM.md` |
| `nf` | NeuroForge | `NeuroForge/` | `doc/nfSYSTEM.md` |
| `ra` | Rake | `rake/` | `doc/raSYSTEM.md` |
| `zs` | ZFSS | `zfss/` | `doc/zsSYSTEM.md` |
| `fi` | ForgeImages | `ForgeImages/` | `doc/fiSYSTEM.md` |
| `sp` | Smithy | `smithy/` | `doc/spSYSTEM.md` |
| `cb` | CortexBDS | `cortex_bds/` | `doc/cbSYSTEM.md` |
| `tc` | Tarcie | `tarcie/` | `doc/tcSYSTEM.md` |

## Reserved Prefixes

| Prefix | Repo | Notes |
|--------|------|-------|
| `ec` | Ecosystem | Root-level documentation |

## Usage

```bash
# Build any repo's documentation
bash doc/system/BUILD.sh

# Output appears at doc/{prefix}SYSTEM.md
# e.g. AuthorForge → doc/afSYSTEM.md
```

## BUILD.sh Standard

All repos use the same BUILD.sh template (Forge Documentation Protocol v1):

1. Reads `doc/system/_index.md` as the header
2. Concatenates all `doc/system/[0-9][0-9]-*.md` files in order
3. Outputs to `doc/{prefix}SYSTEM.md`
4. Only the `PREFIX` variable differs between repos

*Last updated: 2026-03-06 (13 active prefixes)*
