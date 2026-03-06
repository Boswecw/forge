# Forge Ecosystem Documentation Index

> Master map of all documentation across the Forge ecosystem.

Last updated: 2026-03-06

---

## Tier 1: Ecosystem Root

Intentional root-level entrypoints and governance surfaces.

| File | Purpose |
|------|---------|
| `CLAUDE.md` | AI assistant context for Claude Code sessions |
| `README.md` | Ecosystem overview, governance-repo entrypoint, and operator orientation |
| `PORT_REGISTRY.md` | Canonical port assignments for all services |

---

## Tier 2: Ecosystem System Docs (`doc/`)

The Forge Documentation Protocol v1 governs how protocol-bearing repo surfaces structure and compile system documentation.

| File | Purpose |
|------|---------|
| `../docs/canonical/documentation_protocol_v1.md` | The canonical documentation standard |
| `doc/PREFIX_REGISTRY.md` | 2-char prefix assignments for all 12 repos |
| `doc/SYSTEM.md` | Compiled ecosystem-level system documentation |
| `doc/system/*.md` | Modular ecosystem sections assembled into `doc/SYSTEM.md` |
| `doc/system/BUILD.sh` | Assembly script |

### Per-Service System Outputs

Every service compiles its own `{prefix}SYSTEM.md` via `bash doc/system/BUILD.sh`:

| Prefix | Service | Output |
|--------|---------|--------|
| `af` | AuthorForge | `Author-Forge/doc/afSYSTEM.md` |
| `cp` | Canebrake Press | `Canebrake_press/doc/cpSYSTEM.md` |
| `cb` | CortexBDS | `cortex_bds/doc/cbSYSTEM.md` |
| `df` | DataForge | `DataForge/doc/dfSYSTEM.md` |
| `fa` | ForgeAgents | `ForgeAgents/doc/faSYSTEM.md` |
| `fc` | ForgeCommand | `Forge_Command/doc/fcSYSTEM.md` |
| `fi` | ForgeImages | `ForgeImages/doc/fiSYSTEM.md` |
| `fs` | Forge:SMITH | `forge-smithy/doc/fsSYSTEM.md` |
| `nf` | NeuroForge | `NeuroForge/doc/nfSYSTEM.md` |
| `ra` | Rake | `rake/doc/raSYSTEM.md` |
| `sp` | Smithy | `smithy/doc/spSYSTEM.md` |
| `tc` | Tarcie | `tarcie/doc/tcSYSTEM.md` |
| `zs` | ZFSS | `zfss/doc/zsSYSTEM.md` |

---

## Tier 3: Ecosystem Reference (`docs/`)

Cross-cutting reference documentation, plans, audits, and archives.

| Directory | Purpose |
|-----------|---------|
| `docs/DOCUMENTATION_INDEX.md` | This file — master documentation map |
| `docs/canonical/` | Authoritative doctrine (`ecosystem_canonical.md`, `FORGE_SYSTEMS_MANUAL.md`, `security.md`) |
| `docs/architecture/` | Architecture diagrams (single-page security diagram) |
| `docs/contracts/` | API contracts, JSON schemas, specifications |
| `docs/audits/` | Quality audits (build readiness, UX, ForgeCommand) |
| `docs/plans/active/` | Current implementation plans and roadmaps |
| `docs/plans/archive/` | Superseded plans (bugcheck, forgeagents, fpvs, doctrine) |
| `docs/archive/` | Historical documents and archived holding material |
| `docs/archive/session-reports/` | One-off session reports and gap closure reports |
| `docs/changelog/` | Ecosystem-wide changelogs |
| `docs/qa/` | QA documentation |
| `docs/render-deployment/` | Render.com deployment guides |

---

## Tier 4: Per-Service Documentation

Each service maintains supplementary docs in its own `docs/` folder, alongside the protocol-aligned system docs in `doc/system/`.

| Service | System Doc | Supplementary Docs | README |
|---------|---------------|-------------------|--------|
| AuthorForge | `Author-Forge/doc/afSYSTEM.md` | `Author-Forge/docs/` | `Author-Forge/README.md` |
| Canebrake Press | `canebrake_press/doc/cpSYSTEM.md` | `canebrake_press/docs/` | `canebrake_press/README.md` |
| CortexBDS | `cortex_bds/doc/cbSYSTEM.md` | `cortex_bds/docs/` | `cortex_bds/README.md` |
| DataForge | `DataForge/doc/dfSYSTEM.md` | `DataForge/docs/` | `DataForge/README.md` |
| ForgeAgents | `ForgeAgents/doc/faSYSTEM.md` | `ForgeAgents/docs/` | `ForgeAgents/README.md` |
| ForgeCommand | `Forge_Command/doc/fcSYSTEM.md` | `Forge_Command/docs/` | `Forge_Command/README.md` |
| ForgeImages | `ForgeImages/doc/fiSYSTEM.md` | — | `ForgeImages/README.md` |
| Forge:SMITH | `forge-smithy/doc/fsSYSTEM.md` | `forge-smithy/docs/` | `forge-smithy/README.md` |
| NeuroForge | `NeuroForge/doc/nfSYSTEM.md` | `NeuroForge/docs/` | `NeuroForge/README.md` |
| Rake | `rake/doc/raSYSTEM.md` | `rake/docs/` | `rake/README.md` |
| Smithy | `smithy/doc/spSYSTEM.md` | — | `smithy/README.md` |
| Tarcie | `tarcie/doc/tcSYSTEM.md` | — | `tarcie/README.md` |
| ZFSS | `zfss/doc/zsSYSTEM.md` | `zfss/docs/` | `zfss/README.md` |

---

## Tier 5: Support Directories

Shared libraries, assets, and utilities.

| Directory | Purpose |
|-----------|---------|
| `contracts/` | TypeScript contract validation utilities (canonical JSON, run evidence) |
| `doctrine/` | Governance policy definitions |
| `fixtures/` | Governance flow examples (Phase A-E JSON) |
| `forge-brand/` | Brand assets, logos, design tokens |
| `schemas/` | Shared JSON schemas for cross-service contracts |
| `scripts/` | Ecosystem utility scripts (context bundler, connectivity validator) |
| `tools/` | Documentation build tools (`build-ecosystem-docs.mjs`) |

---

## Where to Put New Documentation

| Type of Document | Location |
|-----------------|----------|
| Service system documentation | `{service}/doc/system/` |
| Service guides, API refs, deep-dives | `{service}/docs/` |
| Ecosystem-wide architecture | `docs/architecture/` |
| API contracts and schemas | `docs/contracts/` |
| Active implementation plans | `docs/plans/active/` |
| Completed/superseded plans | `docs/plans/archive/` |
| Audit reports | `docs/audits/` |
| Session reports, one-off investigations | `docs/archive/session-reports/` |
| Canonical doctrine | `docs/canonical/` |
| Deployment guides | `docs/render-deployment/` |
| Root-level loose legacy notes under review | `docs/archive/root-holding/` |
