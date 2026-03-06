# Forge Ecosystem — Complete System Reference

**Document version:** 1.4 (2026-03-06) — Normalized canonical vs snapshot facts, resolved cross-section contradictions, and added documentation truth policy
**Protocol:** Forge Documentation Protocol v1

This document is the **ecosystem-level compilation** of the Forge core backend services, the forge-smithy desktop authority layer, and Forge Eval as the standalone deterministic evaluation subsystem. It combines and clarifies the relationships between NeuroForge, DataForge, ForgeAgents, Rake, forge-smithy, Forge Eval, and the surrounding workspace into a unified reference. Each subsystem maintains its own `doc/system/` for deep detail; this layer provides the cross-cutting view.

Documentation truth classes in this reference are explicit:
- Canonical facts define subsystem roles, ports, boundaries, authority, stage ordering, and failure doctrine.
- Snapshot facts record audit-derived counts such as routers, commands, files, tests, coverage, or schema totals as of this document version.

Assembly contract:
- Command: `bash doc/system/BUILD.sh`
- Output: `doc/SYSTEM.md`

| Part | File | Contents |
|------|------|----------|
| §1 | [01-overview-philosophy.md](01-overview-philosophy.md) | Ecosystem identity, canonical doctrine, service roles, design principles |
| §2 | [02-architecture.md](02-architecture.md) | System architecture, data flow, per-service pipelines, infrastructure |
| §3 | [03-tech-stack.md](03-tech-stack.md) | Unified dependency matrix, shared and per-service stacks |
| §4 | [04-project-structure.md](04-project-structure.md) | Repository layout, per-service structure, shared patterns |
| §5 | [05-config-env.md](05-config-env.md) | Master environment variable registry, secret management |
| §6 | [06-design-system.md](06-design-system.md) | Design tokens, colors, typography, spacing, component conventions |
| §7 | [07-frontend.md](07-frontend.md) | Svelte 5, Tauri IPC, routing, stores, component patterns |
| §8 | [08-api-layer.md](08-api-layer.md) | Unified API reference, authentication matrix, endpoint registry |
| §9 | [09-backend-internals.md](09-backend-internals.md) | Key subsystems: inference, search, ingestion, agents, state machines |
| §10 | [10-ecosystem-integration.md](10-ecosystem-integration.md) | Master integration map, contracts, access control, data lifecycle |
| §11 | [11-database-schema.md](11-database-schema.md) | All ORM models, table definitions, indexes, constraints |
| §12 | [12-ai-integration.md](12-ai-integration.md) | LLM providers, prompt routing, MAID, RTCFX, cost controls |
| §13 | [13-error-handling.md](13-error-handling.md) | Failure modes, degradation, circuit breakers, retry contracts |
| §14 | [14-testing.md](14-testing.md) | Testing infrastructure, QA tiers T0-T6, severity gates S0-S4 |
| §15 | [15-handover.md](15-handover.md) | Critical constraints, known issues, maintenance, sync workflow |
| §16 | [16-documentation-truth-policy.md](16-documentation-truth-policy.md) | Canonical vs snapshot labeling rules for future audits |

## Per-Service Documentation

For deep detail on individual services, see their own `doc/system/` directories:

| Service | Location | Port | Role |
|---------|----------|------|------|
| NeuroForge | [NeuroForge/doc/system/](../../NeuroForge/doc/system/_index.md) | 8000 | AI inference orchestration |
| DataForge | [DataForge/doc/system/](../../DataForge/doc/system/_index.md) | 8001 | Source of truth — data persistence |
| ForgeAgents | [ForgeAgents/doc/system/](../../ForgeAgents/doc/system/_index.md) | 8010 | Agent execution runtime |
| Rake | [rake/doc/system/](../../rake/doc/system/_index.md) | 8002 | Data ingestion pipeline |
| forge-smithy | [forge-smithy/docs/smith/](../../forge-smithy/docs/smith/README.md) | — | Desktop authority layer (Tauri 2.0 + Svelte 5) |
| Forge Eval | [forge-eval/repo/doc/system/](../../forge-eval/repo/doc/system/_index.md) | — | Standalone deterministic evaluation subsystem (Packs A-J) |

## Quick Assembly

```bash
./BUILD.sh                              # Assembles all parts into ../SYSTEM.md
../scripts/context-bundle.sh full       # Full context bundle
../scripts/context-bundle.sh frontend   # Frontend-focused bundle
```

*Last updated: 2026-03-06*
