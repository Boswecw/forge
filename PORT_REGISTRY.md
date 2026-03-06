# Forge Ecosystem — Canonical Port Registry

> **This file is the single source of truth for all port assignments.**
> Every service, every `.env`, every hardcoded default MUST match this registry.
> When adding a new service, claim a port here FIRST.

## Port Map

### Core Platform (8000–8009)

| Port | Service | Role | Protocol |
| ---- | ------- | ---- | -------- |
| 8000 | NeuroForge | AI Gateway — Law 2 hub (embeddings, chat, inference) | HTTP |
| 8001 | DataForge | Persistence Layer — Law 3 source of truth | HTTP |
| 8002 | Rake | Data Ingestion Pipeline (scraping, fetching, cleaning) | HTTP |
| 8003 | ForgeCommand Orchestrator | Auth, token rotation, run intents, orchestration | HTTP |
| 8004 | ForgeCommand API | Entitlements, OAuth, Stripe webhooks | HTTP |
| 8005 | *(reserved)* | Future core service | — |
| 8006 | *(reserved)* | Future core service | — |
| 8007 | *(reserved)* | Future core service | — |
| 8008 | *(reserved)* | Future core service | — |
| 8009 | *(reserved)* | Future core service | — |

### Agent Layer (8010–8019)

| Port | Service | Role | Protocol |
| ---- | ------- | ---- | -------- |
| 8010 | ForgeAgents | Agent Orchestration (BugCheck, BDS, Sentinel, Cortex) | HTTP/WS |
| 8011 | *(reserved)* | Future agent service | — |
| 8012 | *(reserved)* | Future agent service | — |
| 8013–8019 | *(reserved)* | Future agent services | — |

### Application Layer (8020–8039)

| Port | Service | Role | Protocol |
| ---- | ------- | ---- | -------- |
| 8020 | AuthorForge Backend | Public Writing Studio (FastAPI) | HTTP |
| 8021 | AuthorForge API Gateway | Bun/Fastify reverse proxy | HTTP |
| 8022 | AuthorForge Frontend | SvelteKit SSR | HTTP |
| 8023 | Canebrake Press Backend | BDS Writing Studio (FastAPI) | HTTP |
| 8024 | Canebrake Press API Gateway | Bun/Fastify reverse proxy | HTTP |
| 8025 | Canebrake Press Frontend | SvelteKit SSR | HTTP |
| 8026–8039 | *(reserved)* | Future applications | — |

### Desktop / UI Layer (8040–8049)

| Port | Service | Role | Protocol |
| ---- | ------- | ---- | -------- |
| 8040 | forge-smithy (dev) | Vite dev server for SMITH desktop app | HTTP |
| 8041–8049 | *(reserved)* | Future desktop tools | — |

### Auxiliary / Infrastructure

| Port | Service | Role |
| ---- | ------- | ---- |
| 8790 | ForgeCommand token bridge | Localhost-only public-key and token bridge for token-aware local clients |
| 5432 | PostgreSQL (primary) | Shared by DataForge, NeuroForge, Rake |
| 5433 | PostgreSQL (AuthorForge) | Dedicated AuthorForge instance |
| 5434 | PostgreSQL (Canebrake Press) | Dedicated Canebrake Press instance |
| 6379 | Redis | Optional cache (DataForge, ForgeAgents) |
| 6333 | Qdrant | Optional vector DB (AuthorForge) |

## Rules

1. **Claim before coding.** Add your port to this file and get it reviewed before writing any config.
2. **One named boundary, one port.** No port sharing. Auxiliary localhost bridges must be named explicitly.
3. **127.0.0.1, not localhost.** All local service URLs use `127.0.0.1` to avoid IPv6 resolution issues.
4. **Env vars over hardcoded.** Port should come from `PORT` env var or service-specific `*_URL` env var. Hardcoded defaults must match this registry.
5. **Gaps are intentional.** Reserved ranges exist for future services. Do not compress.
6. **This file is canonical.** If code disagrees with this file, the code is wrong.

## Cross-Service URL Convention

```
NEUROFORGE_URL=http://127.0.0.1:8000
DATAFORGE_URL=http://127.0.0.1:8001
RAKE_URL=http://127.0.0.1:8002
FORGECOMMAND_URL=http://127.0.0.1:8003
FORGEAGENTS_URL=http://127.0.0.1:8010
AUTHORFORGE_URL=http://127.0.0.1:8020
CANEBRAKE_PRESS_URL=http://127.0.0.1:8023
```

## History

| Date | Change | Author |
| ---- | ------ | ------ |
| 2026-02-24 | Initial registry. Resolved port 8000 conflict (AuthorForge→8020). Consolidated ForgeCommand (8789→8003, 8800→8004), ForgeAgents (8787→8010) into standard ranges. | Claude Code |
| 2026-03-01 | Added Canebrake Press (8023–8025). Renamed from AuthorForgeBDS — now distinct ecosystem identity. | Claude Code |
| 2026-03-06 | Added ForgeCommand token bridge on 8790 as an auxiliary localhost boundary. Clarified that canonical service URLs remain 8003/8004/8010. | Codex |
