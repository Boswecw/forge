# Forge Ecosystem - Render Deployment Documentation
## Master Index

**Document Version:** 1.0.1
**Last Updated:** February 5, 2026
**Ecosystem Version:** 5.2
**System Status:** ✅ HEALTHY (100% Operational)

---

## 📚 Documentation Structure

This comprehensive documentation set covers every aspect of the Forge Render-deployed ecosystem, from system-level architecture down to individual component details.

### Core Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md)** | High-level architecture, service topology, design principles | All stakeholders |
| **[02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md)** | Detailed service-by-service breakdown with capabilities | Developers, Operators |
| **[03_DEPLOYMENT_GUIDE.md](./03_DEPLOYMENT_GUIDE.md)** | Render deployment configurations, CI/CD, environment setup | DevOps, Operators |
| **[04_API_CONTRACTS.md](./04_API_CONTRACTS.md)** | Complete API reference for all services | Developers, Integrators |
| **[05_DATA_FLOW.md](./05_DATA_FLOW.md)** | Database schemas, data flow patterns, persistence | Developers, DBAs |
| **[06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)** | Authentication, authorization, security architecture | Security, DevOps |
| **[07_MONITORING_OPS.md](./07_MONITORING_OPS.md)** | Monitoring, observability, operational runbooks | Operators, SREs |
| **[08_DEVELOPMENT.md](./08_DEVELOPMENT.md)** | Local development setup, testing, workflows | Developers |
| **[09_TROUBLESHOOTING.md](./09_TROUBLESHOOTING.md)** | Common issues, diagnostics, solutions | All technical staff |

---

## 🎯 Quick Navigation

### By Role

**Developers**
- Start: [01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md)
- Next: [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md)
- Reference: [04_API_CONTRACTS.md](./04_API_CONTRACTS.md)
- Local setup: [08_DEVELOPMENT.md](./08_DEVELOPMENT.md)

**DevOps/SREs**
- Start: [03_DEPLOYMENT_GUIDE.md](./03_DEPLOYMENT_GUIDE.md)
- Monitor: [07_MONITORING_OPS.md](./07_MONITORING_OPS.md)
- Security: [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)
- Troubleshoot: [09_TROUBLESHOOTING.md](./09_TROUBLESHOOTING.md)

**Architects**
- System design: [01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md)
- Data architecture: [05_DATA_FLOW.md](./05_DATA_FLOW.md)
- Security architecture: [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)

**Business/Product**
- Executive summary: [01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md) (first 3 sections)
- Service capabilities: [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md) (service summaries)

### By Task

**Setting up a new service**
1. [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md) - Understand existing services
2. [03_DEPLOYMENT_GUIDE.md](./03_DEPLOYMENT_GUIDE.md) - Deployment patterns
3. [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md) - Security requirements
4. [05_DATA_FLOW.md](./05_DATA_FLOW.md) - Database patterns

**Investigating an incident**
1. [09_TROUBLESHOOTING.md](./09_TROUBLESHOOTING.md) - Common issues
2. [07_MONITORING_OPS.md](./07_MONITORING_OPS.md) - Monitoring tools
3. [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md) - Service dependencies

**Integrating with the ecosystem**
1. [04_API_CONTRACTS.md](./04_API_CONTRACTS.md) - API reference
2. [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md) - Authentication
3. [05_DATA_FLOW.md](./05_DATA_FLOW.md) - Data patterns

---

## 🏗️ Ecosystem Overview

### Service Topology

```
┌──────────────────────────────────────────────────────────┐
│         Forge Command (Desktop - Local Only)             │
│         Mission Control Dashboard (Tauri 2.0)            │
│         Real-time monitoring, health checks, tracing      │
└────────────────────┬─────────────────────────────────────┘
                     │ HTTP REST API + WebSocket
                     │
     ┌───────────────┼───────────────────┐
     │               │                   │
     ▼               ▼                   ▼
┌─────────────┐ ┌──────────────┐ ┌────────────────┐ ┌─────────────┐
│ DataForge   │ │ NeuroForge   │ │ ForgeAgents    │ │    Rake     │
│   :8001     │ │    :8000     │ │    :8010       │ │    :8002    │
│ Data/Memory │ │ LLM Routing  │ │Agent Execution │ │  Ingestion  │
└──────┬──────┘ └──────┬───────┘ └────────┬───────┘ └──────┬──────┘
       │               │                   │                │
       │               └──────────┬────────┴────────────────┘
       │                          │
       │                          ▼
       └──────────────► PostgreSQL + pgvector + Redis
                        Single Shared Database (Render Free Tier)
```

### Core Services (Deployed on Render)

| Service | Port | Role | Production URL |
|---------|------|------|----------------|
| **DataForge** | 8001 | Core data & knowledge engine | `https://dataforge.onrender.com` |
| **NeuroForge** | 8000 | LLM orchestration pipeline | `https://neuroforge.onrender.com` |
| **ForgeAgents** | 8010 | AI agent orchestration | `https://forgeagents.onrender.com` |
| **Rake** | 8002 | Data ingestion pipeline | `https://rake.onrender.com` |

### Local Services (Not on Render)

| Service | Port | Role | Type |
|---------|------|------|------|
| **Forge Command** | 1420 | Mission control dashboard | Tauri Desktop App |
| **Forge:SMITH** | 3001 | AI governance workbench | Tauri Desktop App |
| **Cortex BDS** | - | Local semantic file search | Tauri Desktop App |
| **AuthorForge** | - | Private story OS for novelists | In Development |

---

## 📊 System Metrics

### Infrastructure

| Metric | Value |
|--------|-------|
| **Total Services** | 8 (4 deployed, 4 local) |
| **Render Services** | 4 web services |
| **PostgreSQL Databases** | 1 shared (Render Free Tier) |
| **Redis Instances** | 1 shared |
| **Total API Endpoints** | 150+ across all services |
| **Total Code** | 100,000+ lines |
| **Total Documentation** | 25,000+ lines |

### Production Metrics (DataForge)

| Metric | Value |
|--------|-------|
| **API Latency** | <100ms (p95) |
| **Throughput** | 1,000+ RPS sustained |
| **SLA** | 99.99% (multi-node) |
| **Test Coverage** | 82% (critical paths) |
| **Tests Passing** | 296/296 (100%) |

---

## 🚀 Quick Start

### For New Developers

1. **Read the system overview**: [01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md)
2. **Set up local environment**: [08_DEVELOPMENT.md](./08_DEVELOPMENT.md)
3. **Explore service capabilities**: [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md)
4. **Reference APIs**: [04_API_CONTRACTS.md](./04_API_CONTRACTS.md)

### For New Operators

1. **Understand deployment**: [03_DEPLOYMENT_GUIDE.md](./03_DEPLOYMENT_GUIDE.md)
2. **Set up monitoring**: [07_MONITORING_OPS.md](./07_MONITORING_OPS.md)
3. **Review security**: [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)
4. **Prepare for incidents**: [09_TROUBLESHOOTING.md](./09_TROUBLESHOOTING.md)

### For New Architects

1. **System architecture**: [01_SYSTEM_OVERVIEW.md](./01_SYSTEM_OVERVIEW.md)
2. **Service boundaries**: [02_SERVICE_CATALOG.md](./02_SERVICE_CATALOG.md)
3. **Data architecture**: [05_DATA_FLOW.md](./05_DATA_FLOW.md)
4. **Security architecture**: [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)

---

## 🔒 Security & Compliance

All Forge services implement:

- **Authentication**: JWT tokens with 24-hour expiration
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Audit Logging**: Immutable, cryptographically signed events
- **Anomaly Detection**: 6 detector types for security threats
- **Compliance**: GDPR, CCPA, HIPAA, SOC2, PCI-DSS frameworks

**Full details**: [06_SECURITY_AUTH.md](./06_SECURITY_AUTH.md)

---

## 📈 Monitoring & Observability

### Available Metrics

- **Health**: Service status, dependency validation, latency
- **Performance**: Request throughput, error rates, P50/P90/P99 latency
- **Costs**: Token usage, cost per request, monthly projections
- **Business**: Documents processed, agents active, jobs completed

### Monitoring Tools

- **Forge Command**: Real-time dashboard (desktop app)
- **Prometheus**: Time-series metrics collection
- **OpenTelemetry**: Distributed tracing
- **Grafana**: Visualization dashboards
- **Render Dashboard**: Infrastructure monitoring

**Full details**: [07_MONITORING_OPS.md](./07_MONITORING_OPS.md)

---

## 🛠️ Development & Testing

### Local Development

All services can run locally with:
- Python 3.11+ virtual environments
- PostgreSQL 13+ with pgvector
- Redis 6+
- Environment variables in `.env` files

**Full setup guide**: [08_DEVELOPMENT.md](./08_DEVELOPMENT.md)

### Testing

- **Unit Tests**: 296+ tests across all services
- **Integration Tests**: End-to-end workflows
- **Load Tests**: k6 performance benchmarks
- **Security Tests**: Vulnerability scanning

---

## 📞 Support & Resources

### Documentation

- **This documentation set**: `/home/charlie/Forge/ecosystem/docs/render-deployment/`
- **Service READMEs**: Each service has detailed README in its directory
- **Ecosystem docs**: `/home/charlie/Forge/ecosystem/docs/`

### Contact

- **Technical Support**: charlesboswell@boswelldigitalsolutions.com
- **Website**: https://boswelldigital.com
- **GitHub**: https://github.com/Boswell-Digital

### Useful Commands

```bash
# Health check all services
curl https://dataforge.onrender.com/health
curl https://neuroforge.onrender.com/health
curl https://forgeagents.onrender.com/health/render
curl https://rake.onrender.com/health/render

# Start local development
cd DataForge && source venv/bin/activate && uvicorn app.main:app --port 8001
cd NeuroForge/neuroforge_backend && source .venv/bin/activate && uvicorn main:app --port 8000
cd ForgeAgents && source venv/bin/activate && uvicorn app.main:app --port 8010
cd rake && source venv/bin/activate && uvicorn main:app --port 8002

# Run tests
pytest tests/ -v --cov=app
```

---

## 📋 Document Conventions

### Notation

- **[Service:Port]** - Service with its port number (e.g., DataForge:8001)
- **`/api/v1/endpoint`** - API endpoint path
- **`ENV_VAR`** - Environment variable
- **`database_table`** - Database table name
- **✅** - Implemented/Complete
- **🚧** - In progress
- **📋** - Planned

### Version Control

This documentation is version-controlled alongside the codebase. When making changes:

1. Update the document's "Last Updated" date
2. Increment the version number if structure changes
3. Add a note to the CHANGELOG if significant
4. Keep consistent with actual implementation

---

## 📝 Changelog

### Version 1.0.1 (February 5, 2026)

- **Rake Phase 1: Web Discovery** - Complete implementation
  - Added `/api/v1/discover` endpoints (POST, GET)
  - Integrated Tavily (primary search), Serper (fallback), Firecrawl (scraping)
  - Async job-based discovery with background tasks
  - Provider fallback chain with graceful degradation
  - Cost tracking and URL deduplication
  - Documentation updates: Service Catalog, API Contracts, Deployment Guide

### Version 1.0.0 (February 5, 2026)
- Initial comprehensive documentation set
- Complete system overview
- All 9 core documents created
- Service catalog with full capabilities
- Deployment guide for Render
- Complete API reference
- Data flow and database documentation
- Security and authentication guide
- Monitoring and operations runbook
- Development setup guide
- Troubleshooting reference

---

**Maintained by:** Boswell Digital Solutions LLC
**License:** Commercial (see [LICENSE.md](/home/charlie/Forge/ecosystem/DataForge/LICENSE.md))
**Copyright:** © 2025-2026 Boswell Digital Solutions LLC. All rights reserved.
