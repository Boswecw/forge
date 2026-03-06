# 🔐 SECURITY.md
**Forge Ecosystem — Security & Credential Governance Policy**

**Status:** Enforced  
**Applies To:** Forge Command, Forge:SMITH, Cortex BDS, DataForge, NeuroForge, Rake, ForgeAgents  
**Maintainer:** Boswell Digital Solutions LLC  
**Classification:** Internal Security Policy  
**Last Updated:** 2025-12-27

---

## 1. Security Philosophy

The Forge Ecosystem follows a **governance-first security model** designed for high-leverage, solo operations.

**Core belief:**
> _Security is a system property, not a checklist._

This policy prioritizes:
- Deterministic control over credentials
- Auditability over convenience
- Fail-fast rejection over silent degradation
- Desktop-first trust boundaries over exposed web secrets

---

## 2. Credential Authority (Non-Negotiable)

### Forge Command is the Single Credential Authority

- **All long-lived secrets** (API keys, database credentials, rotation tokens) are stored **exclusively** in Forge Command’s encrypted local SQLite vault:

```
~/.forge-command/local.db
```

- No other Forge application may store or persist long-lived secrets.
- `.env` files **must never** contain service API keys once Forge Command is in use.

Violations of this rule are considered **security defects**, not implementation mistakes.

---

## 3. Brokered Access Model

### Secrets Never Cross UI Boundaries

Forge applications use a **brokered execution model**:

1. **UI Layer (Svelte)**
   - Requests *operations*, not credentials
   - Uses Tauri IPC (`invoke(...)`)
   - Never sees plaintext secrets

2. **Rust Backend (Tauri)**
   - Retrieves secrets internally from Forge Command vault
   - Injects auth headers into outbound HTTP calls
   - Returns **results only** to the UI

### Forbidden Patterns
❌ Returning API keys over IPC  
❌ Logging secrets  
❌ Storing secrets in localStorage, IndexedDB, or config files  
❌ Passing credentials to JavaScript for request construction

---

## 4. IPC Boundary Enforcement

### IPC-Callable (Safe)
These commands may be called by UIs and return **metadata only**:

- `forgecommand_is_available`
- `forgecommand_get_status`
- `forgecommand_list_credentials`
- `rotate_service_key`
- `get_scheduler_status`

### Internal-Only (Never Exposed)
These functions **must never cross IPC boundaries**:

- `get_active_api_key`
- `get_neuroforge_key`
- `get_dataforge_key`
- `get_rake_key`
- `get_forgeagents_key`

Any attempt to expose these over IPC is a **critical security violation**.

---

## 5. Encryption & Vault Security

### Vault Protection
- Secrets are stored encrypted at rest
- Encryption keys are derived from:
  - OS user context
  - Machine-bound key material
- Vault auto-unlocks **only on the originating machine**

### Recovery Mechanism
- Offline recovery phrase (stored physically)
- Allows vault restoration on new hardware
- No cloud dependency

---

## 6. API Key Rotation Policy

### Rotation Schedule
- **Automatic every 30 days**
- **7-day overlap window** where old + new keys are valid
- Old keys are revoked after overlap expiration

### Kitchen Hours Protection
- Automated rotation blocked between:
```
10:00 – 22:00 local time
```

### Emergency Override
- `EMERGENCY_OPS_KEY` header bypasses kitchen hours
- All usage is audit-logged
- Intended for break-glass scenarios only

---

## 7. Rotation Authority Model

Backend services enforce **three independent authorization paths**:

| Method | Purpose |
|------|-------|
| Active API Key | Normal authenticated access |
| ROTATION_ADMIN_TOKEN | Key generation + rotation |
| EMERGENCY_OPS_KEY | Emergency bypass |

Rotation tokens:
- Are long-lived
- Are **not** used for normal API traffic
- Are stored only in Forge Command vault or service environment

---

## 8. Audit & Telemetry Requirements

All security-relevant actions **must be logged**:

- Credential access
- Key rotation attempts
- Emergency overrides
- Scheduler execution
- Failed authorization checks

Logs must include:
- Timestamp
- Service name
- Operation type
- Result (success/failure)
- Reason (if failure or emergency)

Silent failures are forbidden.

---

## 9. Desktop-First Security Boundary

Forge Command runs as a native desktop application to guarantee:

- No open network ports
- No exposed admin endpoints
- OS-level file permission enforcement
- Local-only secret storage

Forge Command **must never** be deployed as a hosted service.

---

## 10. Incident Response

### Credential Compromise
1. Rotate affected keys immediately
2. Use `EMERGENCY_OPS_KEY` if required
3. Review audit logs
4. Verify dependent services
5. Update vault backups

### Vault Corruption
1. Restore from recovery phrase
2. Re-establish service connectivity
3. Validate key integrity
4. Rotate keys if uncertainty exists

---

## 11. Hard Rules Summary

These rules are absolute:

- 🔒 Secrets never reach UI layers
- 🧠 Forge Command owns all credentials
- 🔁 All keys rotate
- 🧾 Everything is auditable
- 🚫 No silent failures
- 🧨 Emergency access is logged and rare

If a feature cannot comply with these rules, **the feature is not shipped**.

---

## 12. Related Documents

- [Single-Page Security Diagram](forge_ecosystem_single_page_security_diagram.md) — Canonical topology and credential lifecycle
- Forge Ecosystem Systems Manual (v1.0)
- ForgeCommand Key Rotation Master Plan (v3.0)
- CONTRIBUTING.md
- ARCHITECTURE.md

---

**Boswell Digital Solutions LLC**  
_“Governance is what allows speed without regret.”_

