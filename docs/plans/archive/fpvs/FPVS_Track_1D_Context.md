# FPVS Track 1D — Context Packet for VS Code Claude

**Document Version:** 1.0  
**Created:** December 28, 2025  
**Owner:** Charles Tytler, Boswell Digital Solutions LLC  
**Purpose:** Context for implementing Checkly Integration (Track 1D)

---

## Current State

### Completed Work (Tracks 1C + 2A0)

**Track 1C: Deploy & Verify FPVS** ✅
- Enhanced `/version` endpoint across all 4 backend services:
  - NeuroForge: `neuroforge_backend/routers/fpvs.py` (commit `b9dcb224`)
  - DataForge: `app/api/fpvs_router.py` (commit `8e4f3cd9`)
  - Rake: `api/fpvs.py` (commit `8b0db11`)
  - ForgeAgents: `app/api/fpvs.py` (commit `24b0de0`)
- New fields added: `schema_version` ("1.0.0"), `python_version` (runtime version)
- Created operational documentation:
  - `docs/ops/FPVS_PROD_VERIFICATION.md`
  - `docs/ops/FPVS_TROUBLESHOOTING.md`
  - `docs/ops/FPVS_EMERGENCY_ROLLBACK.md`

**Track 2A0: BugCheck Phase 0** ✅
- 7 JSON schemas in `schemas/bugcheck/v1/`
- Validator harness: `scripts/validate_schemas.py`
- Valid/invalid fixture samples
- CI workflow: `.github/workflows/schemas.yml`

### Production Endpoints Available

All 4 services now expose:

**GET /fpvs/ready**
```json
{
  "status": "ok"
}
```

**GET /fpvs/version**
```json
{
  "service_name": "neuroforge",
  "version": "5.2.1",
  "commit": "b9dcb224",
  "schema_version": "1.0.0",
  "python_version": "3.11.x"
}
```

**Service URLs:**
- NeuroForge: `https://neuroforge.onrender.com`
- DataForge: `https://dataforge.onrender.com`
- Rake: `https://rake.onrender.com`
- ForgeAgents: `https://forgeagents.onrender.com`

---

## Track 1D Scope: Checkly Integration

### Goal

Create external monitoring documentation and local test scripts for production health checks with specific, tested thresholds.

### Deliverables

1. **docs/ops/CHECKLY_SETUP.md** - Complete Checkly configuration guide
2. **scripts/test_checkly_assertions.sh** - Local assertion validation script
3. Optional: Infrastructure-as-code config if applicable

### Why This Matters

- **External verification**: Catches issues before users report them
- **SLA enforcement**: 500ms/1000ms thresholds validate production performance
- **Incident response**: Alerts trigger before cascading failures
- **Pre-deployment confidence**: Test script validates changes locally

---

## Core Constraints (Forge Standard)

### Performance Targets

**Ready Endpoint (`/fpvs/ready`):**
- **Threshold:** < 500ms (99th percentile)
- **Rationale:** Stateless heartbeat, should be fast
- **No database queries or external dependencies**

**Version Endpoint (`/fpvs/version`):**
- **Threshold:** < 1000ms (99th percentile)
- **Rationale:** Accommodates Render free tier cold starts (30-60s wake, then ~500ms)
- **May include version metadata lookups**

### Alert Policy

- **Frequency:** 
  - Ready: Every 2 minutes
  - Version: Every 5 minutes
- **Alert trigger:** 2 consecutive failures
- **Locations:** US East, US West (for redundancy)
- **Notification:** Email (charles@boswelldigitalsolutions.com), Discord webhook (optional)

### Critical Business Constraint

**Kitchen Hours:** Charles works as chef 10 AM - 10 PM, five days/week. Checkly checks run 24/7 but alerts are acceptable (passive monitoring, no automated actions required during kitchen hours).

---

## Technical Specifications

### Check 1: Ready Heartbeat

**Configuration:**
```yaml
Name: "FPVS - Ready Heartbeat ({SERVICE})"
Type: API Check
URL: https://{service}.onrender.com/fpvs/ready
Method: GET
Frequency: Every 2 minutes
Timeout: 10 seconds
Locations: US East, US West
```

**Assertions:**
1. Status code equals `200`
2. JSON body contains `status` key
3. JSON `status === "ok"`
4. Response time < 500ms (99th percentile)

**Alert Policy:**
- Notify after 2 consecutive failures
- Channels: Email, Discord (optional)

### Check 2: Version Metadata

**Configuration:**
```yaml
Name: "FPVS - Version Metadata ({SERVICE})"
Type: API Check
URL: https://{service}.onrender.com/fpvs/version
Method: GET
Frequency: Every 5 minutes
Timeout: 15 seconds
Locations: US East, US West
```

**Assertions:**
1. Status code equals `200`
2. JSON contains `service_name` (non-empty string)
3. JSON contains `version` (matches semver: `^\d+\.\d+\.\d+$`)
4. JSON contains `commit` (at least 7 characters)
5. JSON contains `schema_version` (non-empty string)
6. JSON contains `python_version` (non-empty string)
7. Response time < 1000ms (99th percentile)

**Alert Policy:**
- Notify after 2 consecutive failures
- Channels: Email, Discord (optional)

---

## Multi-Service Strategy

### Services to Monitor

All 4 backend services require identical check configurations:

1. **NeuroForge** - LLM orchestration and routing
2. **DataForge** - Vector storage and semantic memory
3. **Rake** - Document ingestion pipeline
4. **ForgeAgents** - Agent orchestration with 120-skill library

### Implementation Approach

**Option 1: Manual Setup (Acceptable)**
- Document setup procedure in `CHECKLY_SETUP.md`
- Repeat configuration for each service
- Pros: Simple, no infrastructure dependencies
- Cons: Manual effort, drift risk

**Option 2: Infrastructure-as-Code (Preferred if time allows)**
- Terraform or Pulumi configuration
- Single source of truth for all checks
- Pros: Repeatable, version controlled
- Cons: Additional setup complexity

**Recommendation:** Start with Option 1 (manual documentation), note Option 2 as future enhancement.

---

## Test Script Requirements

### Purpose

Local validation script that simulates Checkly assertions before deploying checks.

### Functional Requirements

**Script:** `scripts/test_checkly_assertions.sh`

**Behavior:**
1. Accept service URL as parameter or default to localhost:8000
2. Test `/fpvs/ready` assertions:
   - Status code 200
   - JSON contains `status === "ok"`
   - Response time < 500ms
3. Test `/fpvs/version` assertions:
   - Status code 200
   - All required fields present
   - Version matches semver pattern
   - Commit length >= 7
   - Response time < 1000ms
4. Output clear pass/fail with timing
5. Exit 0 if all pass, exit 1 if any fail

**Enhanced Feature:** Batch mode to test all 4 production services:

```bash
# Test single service
./scripts/test_checkly_assertions.sh https://neuroforge.onrender.com

# Test all production services
./scripts/test_checkly_assertions.sh --all

# Test local development
./scripts/test_checkly_assertions.sh http://localhost:8000
```

### Output Format

```
Testing Checkly assertions against https://neuroforge.onrender.com

→ Testing /fpvs/ready endpoint...
  ✅ Status code: 200
  ✅ JSON status field: ok
  ✅ Response time: 287ms (< 500ms threshold)

→ Testing /fpvs/version endpoint...
  ✅ Status code: 200
  ✅ Service name: neuroforge
  ✅ Version format: 5.2.1 (matches semver)
  ✅ Commit length: 8 chars (b9dcb224)
  ✅ Schema version: 1.0.0
  ✅ Python version: 3.11.9
  ✅ Response time: 423ms (< 1000ms threshold)

✅ All assertions passed!
Ready to configure Checkly checks.
```

---

## Documentation Structure

### CHECKLY_SETUP.md Sections

1. **Account Setup**
   - Sign up at https://checklyhq.com
   - Free tier: 10 checks, 1-minute intervals
   - API key creation and storage (1Password vault)

2. **Check Configuration**
   - Ready Heartbeat check (complete YAML/JSON)
   - Version Metadata check (complete YAML/JSON)
   - Multi-service setup instructions

3. **Alert Configuration**
   - Notification channels setup
   - Alert message templates
   - Escalation policy (none - immediate notification)

4. **Testing Checks Locally**
   - How to run `test_checkly_assertions.sh`
   - Expected output
   - Troubleshooting common failures

5. **Maintenance**
   - Review check history weekly
   - Adjust thresholds if false positives
   - Archive old alerts after resolution

---

## File Locations

### Where to Create Files

**Documentation:**
```
docs/ops/CHECKLY_SETUP.md
```

**Scripts:**
```
scripts/test_checkly_assertions.sh
```

**Optional Infrastructure-as-Code:**
```
infra/checkly.tf          # Terraform
infra/checkly/checks.ts   # Pulumi TypeScript
```

### Existing Reference Files

Look at these for consistency:
- `docs/ops/FPVS_PROD_VERIFICATION.md` - Verification procedures format
- `docs/ops/FPVS_TROUBLESHOOTING.md` - Documentation style
- `scripts/validate_schemas.py` - Script conventions

---

## Success Criteria

### Documentation Quality

- ✅ Complete Checkly account setup instructions
- ✅ Copy-paste ready check configurations
- ✅ Specific thresholds documented (500ms/1000ms)
- ✅ Alert policy clearly defined
- ✅ Multi-service setup procedure
- ✅ Testing procedure with expected output

### Script Functionality

- ✅ Script tests both `/fpvs/ready` and `/fpvs/version`
- ✅ All assertions implemented correctly
- ✅ Response time measurement accurate
- ✅ Clear pass/fail output
- ✅ Batch mode tests all 4 services
- ✅ Works against localhost and production URLs

### Integration Testing

Before considering Track 1D complete:

```bash
# Test script against all production services
./scripts/test_checkly_assertions.sh --all

# Expected: All 4 services pass all assertions
```

---

## Working Style Guidelines

### Code Style

- **Shell script best practices:**
  - Use `set -e` (exit on error)
  - Use `set -u` (error on undefined variables)
  - Add usage/help message
  - Validate inputs before execution
  - Use descriptive variable names
  - Add comments for complex logic

- **Output style:**
  - Use emoji for visual parsing (✅ ❌ ⚠️)
  - Show timing for performance assertions
  - Clear error messages with context
  - Exit codes: 0 = success, 1 = failure

### Documentation Style

- **Clarity over brevity:** Step-by-step instructions
- **Copy-paste ready:** Complete configurations, no placeholders
- **Examples throughout:** Show expected output
- **Troubleshooting section:** Common issues and fixes
- **Markdown formatting:** Headers, code blocks, tables

### Commit Strategy

```
Track 1D: Checkly Integration

- Add docs/ops/CHECKLY_SETUP.md with complete configuration
- Add scripts/test_checkly_assertions.sh with batch mode
- Document multi-service monitoring strategy

Closes Track 1D (Production Verification & Monitoring)
```

---

## Implementation Time Estimate

**Total:** ~1 hour

**Breakdown:**
- CHECKLY_SETUP.md: 30 minutes
  - Account setup section: 5 min
  - Ready check config: 5 min
  - Version check config: 10 min
  - Alert configuration: 5 min
  - Multi-service setup: 5 min
- test_checkly_assertions.sh: 25 minutes
  - Basic script structure: 10 min
  - Assertion implementation: 10 min
  - Batch mode feature: 5 min
- Testing & verification: 5 minutes
  - Test against localhost
  - Test against production

---

## Common Pitfalls to Avoid

### Documentation Pitfalls

❌ **DON'T:** Use placeholder values like `{YOUR_API_KEY}`  
✅ **DO:** Show exact format: `api_key: sk_live_1234567890abcdef`

❌ **DON'T:** Say "configure the check"  
✅ **DO:** Provide complete JSON/YAML configuration

❌ **DON'T:** Assume reader knows Checkly  
✅ **DO:** Include screenshots or step-by-step CLI commands

### Script Pitfalls

❌ **DON'T:** Use `curl` without error handling  
✅ **DO:** Check exit codes and capture stderr

❌ **DON'T:** Parse JSON with `grep` or `sed`  
✅ **DO:** Use `jq` for JSON parsing

❌ **DON'T:** Hardcode URLs  
✅ **DO:** Accept URLs as parameters with sensible defaults

❌ **DON'T:** Silent failures  
✅ **DO:** Loud, clear error messages with context

---

## Testing Checklist

Before marking Track 1D complete:

### Local Testing
- [ ] Script runs successfully against localhost (development)
- [ ] Script measures response times accurately
- [ ] Script validates all JSON fields correctly
- [ ] Script exits 0 on success, 1 on failure
- [ ] Batch mode tests all 4 services correctly

### Production Testing
- [ ] Script runs successfully against NeuroForge production
- [ ] Script runs successfully against DataForge production
- [ ] Script runs successfully against Rake production
- [ ] Script runs successfully against ForgeAgents production
- [ ] Response times are within thresholds (500ms/1000ms)

### Documentation Testing
- [ ] CHECKLY_SETUP.md is complete and readable
- [ ] Check configurations are copy-paste ready
- [ ] Alert policy is clearly documented
- [ ] Multi-service setup procedure is clear
- [ ] Testing procedure includes expected output

---

## Next Steps After Track 1D

Once Track 1D is complete, proceed to:

**Track 3B: SMITH Phase 3 - Evidence Export**
- Evidence bundle structure with standalone verification
- `verification/verify.sh` script
- Add `VERIFYING_EVIDENCE` state to pipeline
- Determinism and tamper detection tests
- **Estimated Time:** 5 hours

---

## Quick Reference

### Key Thresholds
- `/fpvs/ready`: < 500ms (99th percentile)
- `/fpvs/version`: < 1000ms (99th percentile)

### Check Frequencies
- Ready: Every 2 minutes
- Version: Every 5 minutes

### Alert Policy
- Trigger: 2 consecutive failures
- Channels: Email, Discord (optional)

### Production URLs
```
https://neuroforge.onrender.com/fpvs/ready
https://neuroforge.onrender.com/fpvs/version
https://dataforge.onrender.com/fpvs/ready
https://dataforge.onrender.com/fpvs/version
https://rake.onrender.com/fpvs/ready
https://rake.onrender.com/fpvs/version
https://forgeagents.onrender.com/fpvs/ready
https://forgeagents.onrender.com/fpvs/version
```

---

**This context packet provides everything needed to implement Track 1D with production-grade quality.**

**Proceed with implementation per FPVS_Track_1D_Prompt.md**
