# Forge Ecosystem — Single-Page Security Diagram

<!-- CANONICAL SECURITY DIAGRAM OF RECORD -->
<!-- Any architecture change must be reflected here -->
<!-- Last verified: 2025-12-27 -->

> **Purpose:** Provide a one-page, authoritative visual model of credential authority, trust boundaries, and enforcement rules across the Forge Ecosystem.
>
> **Audience:** Internal developers, auditors, future contributors, investors (technical).
>
> **Normative Reference:** `SECURITY.md`

---

## Security Architecture (Mermaid)

```mermaid
flowchart TB
    subgraph USER["USER / OPERATOR"]
        direction LR
        OS["Local OS Account"]
    end

    subgraph DESKTOP["FORGE COMMAND (Desktop) — ROOT OF TRUST"]
        direction TB

        subgraph UI_LAYER["UI Layer (WebView)"]
            SVELTE["SvelteKit UI<br/>• No secrets<br/>• Requests operations"]
        end

        subgraph RUST_LAYER["Rust Backend (Tauri)"]
            BROKER["Credential Broker<br/>• Enforces policy<br/>• Injects auth headers"]
        end

        subgraph VAULT_LAYER["Encrypted Vault"]
            VAULT[("~/.forge-command/local.db<br/>• API keys<br/>• Rotation tokens<br/>• Emergency keys")]
        end

        SVELTE -->|"IPC (operations only)"| BROKER
        BROKER -->|"Internal access"| VAULT
    end

    subgraph SERVICES["BACKEND SERVICES (Zero Trust)"]
        direction LR
        DF["DataForge<br/>Vector Memory"]
        NF["NeuroForge<br/>LLM Orchestration"]
        FA["ForgeAgents<br/>Agent Runtime"]
        RK["Rake<br/>Data Ingestion"]
    end

    subgraph CONSUMERS["CONSUMER APPS (No Credential Ownership)"]
        direction LR
        SMITHY["Forge:SMITH"]
        CORTEX["Cortex BDS"]
        VIBE["VibeForge"]
    end

    OS -->|"UI actions (no secrets)"| SVELTE
    BROKER -->|"Authenticated HTTP<br/>(headers injected in Rust)"| SERVICES

    CONSUMERS -.->|"Brokered access via<br/>ForgeCommand vault"| BROKER

    style USER fill:#e1f5fe,stroke:#01579b
    style DESKTOP fill:#fff3e0,stroke:#e65100
    style VAULT_LAYER fill:#ffebee,stroke:#c62828
    style SERVICES fill:#e8f5e9,stroke:#2e7d32
    style CONSUMERS fill:#f3e5f5,stroke:#7b1fa2
    style VAULT fill:#ffcdd2,stroke:#b71c1c
```

## Trust Boundary Flow

```mermaid
flowchart LR
    subgraph FORBIDDEN["❌ FORBIDDEN"]
        direction TB
        F1["UI → Vault"]
        F2["UI → Service with secrets"]
        F3["IPC returning secrets"]
        F4["Service → Service trust"]
    end

    subgraph ALLOWED["✅ ALLOWED"]
        direction TB
        A1["UI → IPC → Rust"]
        A2["Rust → Vault (internal)"]
        A3["Rust → Service (auth injected)"]
    end

    style FORBIDDEN fill:#ffebee,stroke:#c62828
    style ALLOWED fill:#e8f5e9,stroke:#2e7d32
```

## Credential Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Active: Key Issued
    Active --> Overlap: Rotation Triggered<br/>(outside kitchen hours)
    Overlap --> Active: New Key Primary
    Overlap --> Revoked: 7-day grace expires
    Active --> Emergency: Break-glass
    Emergency --> Active: Normal ops restored
    Revoked --> [*]

    note right of Active
        Normal operation
        API key validates requests
    end note

    note right of Overlap
        Both old + new keys valid
        7-day transition window
    end note

    note left of Emergency
        X-Emergency-Key header
        Mandatory audit log
    end note
```

---

## High-Level Security Topology (ASCII Reference)

<details>
<summary>Click to expand ASCII diagram</summary>

```
┌──────────────────────────────────────────────────────────────────────────┐
│                              USER / OPERATOR                              │
│                       (Local OS Account, Desktop Trust)                    │
└──────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ UI Actions (No Secrets)
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           FORGE COMMAND (DESKTOP)                          │
│                         🔐 ROOT OF TRUST / AUTHORITY                        │
│                                                                            │
│  ┌──────────────────────────────┐      ┌──────────────────────────────┐   │
│  │   SvelteKit UI (WebView)     │─────▶│   Rust Backend (Tauri)        │   │
│  │   • No secrets               │ IPC  │   • Credential broker         │   │
│  │   • Requests operations      │      │   • Enforces policy           │   │
│  └──────────────────────────────┘      └───────────────┬──────────────┘   │
│                                                          │                 │
│                                                          │ Internal Only   │
│                                                          ▼                 │
│                                         ┌──────────────────────────────┐   │
│                                         │  Encrypted SQLite Vault       │   │
│                                         │  ~/.forge-command/local.db    │   │
│                                         │  • API keys                   │   │
│                                         │  • Rotation tokens            │   │
│                                         │  • Emergency keys             │   │
│                                         └──────────────────────────────┘   │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Authenticated HTTP (Headers Injected)
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         FORGE BACKEND SERVICES (ZERO TRUST)                │
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ DataForge    │  │ NeuroForge   │  │ ForgeAgents  │  │ Rake         │   │
│  │              │  │              │  │              │  │              │   │
│  │ • API Key    │  │ • API Key    │  │ • API Key    │  │ • API Key    │   │
│  │ • Admin Key  │  │ • Admin Key  │  │ • Admin Key  │  │ • Admin Key  │   │
│  │ • Emergency  │  │ • Emergency  │  │ • Emergency  │  │ • Emergency  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                            │
│   Rules Enforced Per Request:                                               │
│   • Validate active API key                                                 │
│   • Respect rotation overlap                                                │
│   • Enforce kitchen hours                                                   │
│   • Audit all security events                                               │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

</details>

---

## Trust Boundary Summary

```
[ USER ]
   ↓ (no secrets)
[ UI LAYER ]                ❌ Secrets forbidden
   ↓ IPC (operations only)
[ RUST BACKEND ]            ✅ Trusted executor
   ↓ internal access only
[ VAULT ]                   🔐 Secrets live here
   ↓ authenticated HTTP
[ SERVICES ]                🔒 Zero-trust, verify every request
```

**Key Rule:**
> Secrets move **downward only**, never upward.

---

## Credential Classes & Scope

| Credential Type | Lives Where | Used By | Scope |
|-----------------|-------------|---------|-------|
| Service API Key | ForgeCommand Vault | Rust backend | Normal operations |
| Rotation Admin Token | Service env + vault | ForgeCommand | Key issuance only |
| Emergency Ops Key | Service env + vault | Humans / ForgeCommand | Break-glass |

---

## Explicitly Forbidden Paths

```
❌ UI → Vault
❌ UI → Service (with secrets)
❌ Service → Service trust
❌ IPC returning secrets
❌ Secrets in .env (post-ForgeCommand)
```

If a data flow resembles any of the above, it is **invalid by design**.

---

## Rotation & Emergency Overlay

```
Normal Operation
└─ API Key → Service

Scheduled Rotation (Outside Kitchen Hours)
└─ ForgeCommand → Admin Endpoint → New Key
   └─ 7-Day Overlap → Old Key Revoked

Emergency
└─ X-Emergency-Key → Immediate Access
   └─ Mandatory Audit Log
```

---

## Non-Negotiable Invariant

> **Deleting any UI application must not compromise credentials or service access.**

If removing Forge:SMITH, Cortex, or VibeForge breaks authentication, the security model has been violated.

---

## Canonical References

- `SECURITY.md` — Normative security policy
- Forge Ecosystem Systems Manual — Implementation detail
- Security Alignment Verification — Audit confirmation

---

**Boswell Digital Solutions LLC**  
_“Trust is not granted. It is enforced.”_