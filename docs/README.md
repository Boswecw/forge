# Forge Ecosystem Documentation

Central documentation hub for the Forge platform.

See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for the master documentation map.

## Directory Structure

```
docs/
├── canonical/           # Authoritative platform documentation
├── architecture/        # System architecture diagrams
├── audits/              # Quality and compliance audits
│   └── forgecommand/    # ForgeCommand-specific audits
├── contracts/           # API contracts and schemas
├── plans/               # Implementation plans and roadmaps
│   ├── active/          # Current plans
│   └── archive/         # Superseded plans (bugcheck, forgeagents, fpvs, doctrine)
├── changelog/           # Ecosystem-wide changelogs
├── archive/             # Historical/superseded documents
│   └── session-reports/ # One-off session reports
├── qa/                  # QA test documentation
└── render-deployment/   # Render.com deployment guides
```

## Canonical Documentation

Core platform reference documents:

| Document | Description |
|----------|-------------|
| [ecosystem_canonical.md](canonical/ecosystem_canonical.md) | Authoritative doctrine - defines what Forge is, invariants, architectural intent |
| [FORGE_SYSTEMS_MANUAL.md](canonical/FORGE_SYSTEMS_MANUAL.md) | Complete systems manual for the ecosystem |
| [security.md](canonical/security.md) | Security guidelines and policies |

## Architecture

| Document | Description |
|----------|-------------|
| [forge_ecosystem_single_page_security_diagram.md](architecture/forge_ecosystem_single_page_security_diagram.md) | Single-page security architecture overview |

## Implementation Plans

### Active Plans

Current implementation roadmaps in `plans/active/`:

| Document | Description |
|----------|-------------|
| [FORGE_NEXT_PRIORITIES_IMPLEMENTATION_PROMPT.md](plans/active/FORGE_NEXT_PRIORITIES_IMPLEMENTATION_PROMPT.md) | Master sequenced implementation plan (Phases 1-7) |
| [FORGE_DICTIONARY_COMPRESSION_PLAN.md](plans/active/FORGE_DICTIONARY_COMPRESSION_PLAN.md) | Zstandard dictionary compression proposal (P2) |

### Archived Plans

Superseded plans preserved in `plans/archive/`:

| Directory | Description |
|-----------|-------------|
| [bugcheck/](plans/archive/bugcheck/) | BugCheck Agent implementation (superseded by master plan) |
| [forgeagents/](plans/archive/forgeagents/) | ForgeAgents implementation plans |
| [fpvs/](plans/archive/fpvs/) | Forge Publishing and Verification System |
| [doctrine/](plans/archive/doctrine/) | Doctrine validation system |

## Audits

Quality assurance and compliance audit reports.

### Ecosystem Audits

| Document | Description |
|----------|-------------|
| [BUILD_READINESS_AUDIT.md](audits/BUILD_READINESS_AUDIT.md) | Build readiness assessment |
| [UX_UI_AUDIT_REPORT.md](audits/UX_UI_AUDIT_REPORT.md) | UX/UI compliance audit |
| [UX_REMEDIATION_PLAN.md](audits/UX_REMEDIATION_PLAN.md) | UX remediation action plan |

### ForgeCommand Audits

| Document | Description |
|----------|-------------|
| [Production_Readiness_Audit.md](audits/forgecommand/ForgeCommand_Production_Readiness_Audit_CORRECTED.md) | Production readiness assessment |
| [API_COMPLIANCE_AUDIT_REPORT.md](audits/forgecommand/API_COMPLIANCE_AUDIT_REPORT.md) | API compliance review |
| [WIRING_AUDIT_REPORT.md](audits/forgecommand/WIRING_AUDIT_REPORT.md) | Command wiring verification |

## Contracts

API contracts, schemas, and specifications.

| Document | Description |
|----------|-------------|
| [run_intent.v1.schema.json](contracts/run_intent.v1.schema.json) | RunIntent v1 JSON schema |
| [RunIntent_v1_Authority_Contract.docx](contracts/RunIntent_v1_Authority_Contract_Rev5_FINAL.docx) | RunIntent authority contract (Rev5) |
| [SMITH_Assist_Chatbot_Specification.docx](contracts/SMITH_Assist_Chatbot_Specification.docx) | SMITH chatbot integration spec |

## Service Documentation

Each service maintains its own documentation. For BDS system docs, see each service's `doc/{prefix}SYSTEM.md`. For SMITH UI tracking, see [forge-smithy/docs/smith/](../forge-smithy/docs/smith/).

| Service | Location | Description |
|---------|----------|-------------|
| AuthorForge | [Author-Forge/docs/](../Author-Forge/docs/) | Public writing studio |
| Canebrake Press | [Canebrake_press/docs/](../Canebrake_press/docs/) | BDS business writing studio |
| CortexBDS | [cortex_bds/docs/](../cortex_bds/docs/) | File intelligence system |
| DataForge | [DataForge/docs/](../DataForge/docs/) | Data persistence layer (Source of Truth) |
| ForgeAgents | [ForgeAgents/docs/](../ForgeAgents/docs/) | Agent execution runtime |
| Forge_Command | [Forge_Command/docs/](../Forge_Command/docs/) | CLI and orchestration |
| forge-smithy | [forge-smithy/docs/](../forge-smithy/docs/) | Desktop authority layer |
| NeuroForge | [NeuroForge/docs/](../NeuroForge/docs/) | ML/NLP services |
| Rake | [rake/docs/](../rake/docs/) | Data pipeline tooling |
| ZFSS | [zfss/docs/](../zfss/docs/) | File storage services |
| checkly | [checkly/docs/](../checkly/docs/) | Monitoring infrastructure |

## Related Files

- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Master documentation map
- [CLAUDE.md](../CLAUDE.md) - AI assistant project context
- [README.md](../README.md) - Main ecosystem README
- [PORT_REGISTRY.md](../PORT_REGISTRY.md) - Canonical port assignments
