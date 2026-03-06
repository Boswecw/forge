# FPVS Track 3B — Context Packet for VS Code Claude

**Document Version:** 1.0  
**Created:** December 28, 2025  
**Owner:** Charles Tytler, Boswell Digital Solutions LLC  
**Purpose:** Context for implementing SMITH Phase 3 Evidence Export (Track 3B)

---

## Current State

### Completed Work (Tracks 1C, 2A0, 1D)

**Track 1C: Deploy & Verify FPVS** ✅
- Enhanced `/version` endpoint across all 4 backend services
- New fields: `schema_version` ("1.0.0"), `python_version`
- Operational documentation: verification, troubleshooting, rollback

**Track 2A0: BugCheck Phase 0** ✅
- 7 JSON schemas in `schemas/bugcheck/v1/`
- Validator harness and CI workflow
- Valid/invalid fixture samples

**Track 1D: Checkly Integration** ✅
- External monitoring documentation (`docs/ops/CHECKLY_SETUP.md`)
- Local test script (`scripts/test_checkly_assertions.sh`)
- Multi-service monitoring strategy

### Available Services

All 4 backend services with FPVS endpoints:
- **NeuroForge:** `https://neuroforge.onrender.com`
- **DataForge:** `https://dataforge.onrender.com`
- **Rake:** `https://rake.onrender.com`
- **ForgeAgents:** `https://forgeagents.onrender.com`

---

## Track 3B Scope: SMITH Phase 3 Evidence Export

### Mission Statement

Complete "evidence export" so governed operations produce **audit-grade, tamper-evident bundles** with **standalone verification** requiring no FPVS installation.

### Why This Matters

**Audit Trail:** Every FPVS validation run must produce forensic-grade evidence that can be independently verified years later, even if FPVS no longer exists.

**Compliance:** Evidence bundles support regulatory compliance, security audits, and incident investigations.

**Transparency:** Standalone verification script allows third parties to validate evidence integrity without trusting FPVS.

**Chain of Custody:** Evidence chain support links operations together, preventing evidence tampering or deletion.

---

## Core Principles (Forge Standard)

### Determinism
**Rule:** Same inputs → Same manifest/hashes  
**Implementation:** Canonical JSON serialization, stable iteration order, reproducible timestamps

### Tamper Evidence
**Rule:** Any modification → Loud verification failure  
**Implementation:** SHA-256 hashes for all artifacts, manifest hash verification, fail-closed logic

### Portability
**Rule:** Bundle verifiable without FPVS installation  
**Implementation:** Standalone `verify.sh` using only `sha256sum`, self-contained ZIP archive

### Inspectability
**Rule:** Bundle contents are human-readable  
**Implementation:** JSON manifests, plain text logs, descriptive filenames

### Fail-Closed
**Rule:** Uncertainty → Escalation, not execution  
**Implementation:** Missing files fail verification, hash mismatches halt processing, errors are loud

---

## Evidence Bundle Structure

### Directory Layout

```
evidence_bundle_{timestamp}_{operation_id}.zip
├── manifest.json                    # Canonical record of bundle contents
├── hashes.json                      # SHA-256 hashes for all artifacts
├── metadata/
│   ├── operation_log.json          # Complete execution timeline
│   ├── tool_versions.json          # Python version, package versions, system info
│   └── runtime_env.json            # Environment variables (sanitized), config
├── artifacts/
│   ├── {operation_id}_input.json   # Operation inputs (schemas, configs)
│   ├── {operation_id}_output.json  # Operation outputs (validation results)
│   ├── {operation_id}_logs.txt     # Execution logs (stdout/stderr)
│   └── {operation_id}_metrics.json # Performance metrics (optional)
└── verification/
    ├── verify.sh                    # Standalone verification script (bash)
    ├── verify.py                    # Python verification (optional)
    └── README.md                    # Verification instructions
```

### File Naming Convention

**Pattern:** `{operation_id}_{artifact_type}.{ext}`

**Examples:**
- `validate_20260115_143022_input.json`
- `validate_20260115_143022_output.json`
- `validate_20260115_143022_logs.txt`

**Operation ID Format:** `{operation}_{YYYYMMDD}_{HHMMSS}_{short_uuid}`

---

## Schema Specifications

### manifest.json

**Purpose:** Canonical record of bundle contents and metadata

**Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "bundle_id",
    "operation_id",
    "schema_version",
    "created_at",
    "fpvs_version",
    "fpvs_commit",
    "artifacts"
  ],
  "properties": {
    "bundle_id": {
      "type": "string",
      "pattern": "^bundle_[0-9]{8}_[0-9]{6}_[a-z0-9]{8}$",
      "description": "Unique bundle identifier"
    },
    "operation_id": {
      "type": "string",
      "description": "FPVS operation that generated this bundle"
    },
    "schema_version": {
      "type": "string",
      "pattern": "^v[0-9]+$",
      "description": "Evidence bundle schema version (e.g., 'v1')"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when bundle was created"
    },
    "fpvs_version": {
      "type": "string",
      "description": "FPVS service version that created bundle"
    },
    "fpvs_commit": {
      "type": "string",
      "minLength": 7,
      "description": "Git commit SHA of FPVS service"
    },
    "chain": {
      "type": "object",
      "description": "Evidence chain linkage (optional)",
      "properties": {
        "parent_hash": {
          "type": "string",
          "pattern": "^sha256:[a-f0-9]{64}$",
          "description": "SHA-256 hash of parent bundle manifest"
        },
        "chain_height": {
          "type": "integer",
          "minimum": 0,
          "description": "Position in evidence chain (0 = genesis)"
        }
      }
    },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "hash", "size_bytes", "created_at"],
        "properties": {
          "path": {
            "type": "string",
            "description": "Relative path within bundle"
          },
          "hash": {
            "type": "string",
            "pattern": "^sha256:[a-f0-9]{64}$",
            "description": "SHA-256 hash of file contents"
          },
          "size_bytes": {
            "type": "integer",
            "minimum": 0,
            "description": "File size in bytes"
          },
          "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "When artifact was created"
          }
        }
      }
    }
  }
}
```

**Example:**
```json
{
  "bundle_id": "bundle_20260115_143022_abc123ef",
  "operation_id": "validate_schemas_20260115_143022",
  "schema_version": "v1",
  "created_at": "2026-01-15T14:30:22Z",
  "fpvs_version": "0.1.0",
  "fpvs_commit": "b9dcb224",
  "chain": {
    "parent_hash": "sha256:9f4e8d3c2b1a0f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e",
    "chain_height": 42
  },
  "artifacts": [
    {
      "path": "artifacts/validate_schemas_20260115_143022_input.json",
      "hash": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
      "size_bytes": 4096,
      "created_at": "2026-01-15T14:30:22Z"
    },
    {
      "path": "metadata/operation_log.json",
      "hash": "sha256:2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c",
      "size_bytes": 8192,
      "created_at": "2026-01-15T14:30:25Z"
    }
  ]
}
```

### hashes.json

**Purpose:** Quick reference for verification (SHA-256 hashes only)

**Schema:**
```json
{
  "algorithm": "sha256",
  "hashes": {
    "manifest.json": "sha256:abc123...",
    "artifacts/input.json": "sha256:def456...",
    "metadata/operation_log.json": "sha256:789abc..."
  }
}
```

**Note:** This file is for convenience. The canonical hashes are in `manifest.json`.

### metadata/operation_log.json

**Purpose:** Complete execution timeline with events

**Schema:**
```json
{
  "operation_id": "validate_schemas_20260115_143022",
  "started_at": "2026-01-15T14:30:22Z",
  "completed_at": "2026-01-15T14:30:45Z",
  "duration_seconds": 23,
  "status": "completed",
  "events": [
    {
      "timestamp": "2026-01-15T14:30:22Z",
      "event_type": "operation_started",
      "message": "Schema validation initiated"
    },
    {
      "timestamp": "2026-01-15T14:30:25Z",
      "event_type": "validation_progress",
      "message": "Validated 5/7 schemas"
    },
    {
      "timestamp": "2026-01-15T14:30:45Z",
      "event_type": "operation_completed",
      "message": "All schemas validated successfully"
    }
  ]
}
```

### metadata/tool_versions.json

**Purpose:** Environment reproducibility

**Schema:**
```json
{
  "python_version": "3.11.9",
  "fpvs_version": "0.1.0",
  "fpvs_commit": "b9dcb224",
  "dependencies": {
    "fastapi": "0.109.0",
    "pydantic": "2.5.3",
    "jsonschema": "4.20.0"
  },
  "system": {
    "os": "Linux",
    "platform": "x86_64",
    "hostname": "srv-12345"
  }
}
```

### metadata/runtime_env.json

**Purpose:** Configuration snapshot (sanitized)

**Schema:**
```json
{
  "config": {
    "validation_mode": "strict",
    "schema_version": "v1",
    "allowed_schemas": ["bugcheck", "evidence"]
  },
  "environment": {
    "FPVS_ENV": "production",
    "FPVS_LOG_LEVEL": "INFO"
  }
}
```

**CRITICAL:** Never include secrets (API keys, passwords, tokens) in this file.

---

## Standalone Verification Script

### verification/verify.sh

**Purpose:** Portable verification requiring only `sha256sum` and `jq`

**Requirements:**
1. **No FPVS dependencies** - Works on any Linux/macOS with standard tools
2. **Deterministic** - Same bundle → same verification result
3. **Fail-closed** - Any uncertainty → loud failure
4. **Clear output** - Visual pass/fail indicators
5. **Exit codes** - 0 = verified, 1 = tampered/missing files

**Script Template:**

```bash
#!/bin/bash
# Standalone evidence bundle verification
# Requires: sha256sum, jq
# No FPVS installation required

set -e

BUNDLE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BUNDLE_DIR"

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Verifying evidence bundle..."
echo "Bundle: $BUNDLE_DIR"
echo ""

# Check required files exist
if [ ! -f "manifest.json" ]; then
    echo -e "${RED}❌ manifest.json missing${NC}"
    exit 1
fi

if [ ! -f "hashes.json" ]; then
    echo -e "${RED}❌ hashes.json missing${NC}"
    exit 1
fi

# Extract expected hashes from hashes.json
EXPECTED_HASHES=$(jq -r '.hashes | to_entries[] | "\(.value)  \(.key)"' hashes.json)

# Verify each file
FAILURES=0
while IFS= read -r line; do
    EXPECTED_HASH=$(echo "$line" | awk '{print $1}' | sed 's/sha256://')
    FILE_PATH=$(echo "$line" | awk '{print $2}')
    
    if [ ! -f "$FILE_PATH" ]; then
        echo -e "${RED}❌ Missing: $FILE_PATH${NC}"
        ((FAILURES++))
        continue
    fi
    
    ACTUAL_HASH=$(sha256sum "$FILE_PATH" | awk '{print $1}')
    
    if [ "$EXPECTED_HASH" = "$ACTUAL_HASH" ]; then
        echo -e "${GREEN}✅ $FILE_PATH${NC}"
    else
        echo -e "${RED}❌ $FILE_PATH (hash mismatch)${NC}"
        echo "   Expected: $EXPECTED_HASH"
        echo "   Actual:   $ACTUAL_HASH"
        ((FAILURES++))
    fi
done <<< "$EXPECTED_HASHES"

echo ""

if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✅ All artifacts verified successfully${NC}"
    echo "Bundle integrity: INTACT"
    exit 0
else
    echo -e "${RED}❌ Verification failed: $FAILURES file(s) tampered or missing${NC}"
    echo "Bundle integrity: COMPROMISED"
    exit 1
fi
```

### verification/README.md

**Purpose:** Human-readable verification instructions

**Content:**
```markdown
# Evidence Bundle Verification

This bundle contains tamper-evident evidence from FPVS operation.

## Quick Verification

```bash
cd verification/
./verify.sh
```

Expected output:
```
🔍 Verifying evidence bundle...
Bundle: /path/to/bundle

✅ manifest.json
✅ artifacts/input.json
✅ metadata/operation_log.json
...

✅ All artifacts verified successfully
Bundle integrity: INTACT
```

## Manual Verification

1. Extract bundle: `unzip evidence_bundle_*.zip`
2. Verify hashes: `sha256sum -c hashes.txt`
3. Inspect manifest: `cat manifest.json | jq .`

## What This Verifies

- ✅ All artifacts are present and unmodified
- ✅ Cryptographic hashes match manifest
- ✅ Bundle has not been tampered with

## What This Does NOT Verify

- ❌ Original operation correctness (trust assumption)
- ❌ Timestamp authenticity (no digital signature)
- ❌ Chain of custody before bundling

## Evidence Chain

If `manifest.json` contains `chain.parent_hash`, this bundle is part of a chain:
- `chain.parent_hash`: SHA-256 of parent bundle manifest
- `chain.chain_height`: Position in chain (0 = genesis)

Verify chain integrity by checking parent bundle exists and hash matches.
```

---

## State Machine Integration

### New State: VERIFYING_EVIDENCE

**Current States (assumed):**
```python
class ExecutionState(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
```

**Enhanced States:**
```python
class ExecutionState(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    VERIFYING_EVIDENCE = "verifying_evidence"  # NEW
    COMPLETED = "completed"
    FAILED = "failed"
```

**Valid State Transitions:**
```python
VALID_TRANSITIONS = {
    ExecutionState.QUEUED: [ExecutionState.RUNNING],
    ExecutionState.RUNNING: [
        ExecutionState.VERIFYING_EVIDENCE,
        ExecutionState.FAILED
    ],
    ExecutionState.VERIFYING_EVIDENCE: [
        ExecutionState.COMPLETED,
        ExecutionState.FAILED
    ],
    ExecutionState.COMPLETED: [],
    ExecutionState.FAILED: [],
}
```

**Transition Logic:**
```python
# After operation execution completes successfully
operation.state = ExecutionState.VERIFYING_EVIDENCE
operation.save()

# Create evidence bundle
bundle_path = create_evidence_bundle(operation)

# Verify bundle integrity
success, errors = verify_evidence_bundle(bundle_path)

if success:
    operation.state = ExecutionState.COMPLETED
    operation.evidence_bundle_path = bundle_path
else:
    operation.state = ExecutionState.FAILED
    operation.error_message = f"Evidence verification failed: {errors}"

operation.save()
```

---

## Implementation Architecture

### Core Components

**1. Evidence Exporter** (`app/evidence/exporter.py`)
- `create_evidence_bundle(operation_id, artifacts, output_dir) -> Path`
- `generate_manifest(artifacts, metadata) -> dict`
- `compute_artifact_hashes(artifacts) -> dict`
- `create_zip_bundle(bundle_dir) -> Path`

**2. Evidence Verifier** (`app/evidence/verifier.py`)
- `verify_evidence_bundle(bundle_path) -> Tuple[bool, List[str]]`
- `verify_artifact_hash(file_path, expected_hash) -> bool`
- `verify_manifest_integrity(manifest) -> bool`

**3. Evidence Chain Manager** (`app/evidence/chain.py` - optional)
- `link_to_parent(current_bundle, parent_bundle) -> dict`
- `verify_chain(bundle_path) -> Tuple[bool, int]`
- `get_chain_height(bundle_path) -> int`

**4. State Machine Extension** (`app/models/execution.py`)
- Add `VERIFYING_EVIDENCE` state
- Add `evidence_bundle_path` field
- Update state transition validation

---

## Testing Requirements

### Unit Tests

**Test: Determinism** (`tests/test_evidence_determinism.py`)
```python
def test_evidence_bundle_is_deterministic(tmp_path):
    """Same inputs produce identical manifest and hashes"""
    
    artifacts = {
        "input.json": b'{"test": true}',
        "output.json": b'{"result": "success"}'
    }
    
    bundle1 = create_evidence_bundle(
        operation_id="test_op_1",
        artifacts=artifacts,
        output_dir=tmp_path / "bundle1"
    )
    
    bundle2 = create_evidence_bundle(
        operation_id="test_op_1",
        artifacts=artifacts,
        output_dir=tmp_path / "bundle2"
    )
    
    # Load manifests
    manifest1 = json.loads((bundle1 / "manifest.json").read_text())
    manifest2 = json.loads((bundle2 / "manifest.json").read_text())
    
    # Remove timestamp fields for comparison
    del manifest1["created_at"]
    del manifest2["created_at"]
    for artifact in manifest1["artifacts"]:
        del artifact["created_at"]
    for artifact in manifest2["artifacts"]:
        del artifact["created_at"]
    
    assert manifest1 == manifest2
    assert manifest1["artifacts"] == manifest2["artifacts"]
```

**Test: Tamper Detection** (`tests/test_evidence_tamper.py`)
```python
def test_verification_fails_when_artifact_modified(tmp_path):
    """Verification detects tampering"""
    
    # Create bundle
    bundle_path = create_evidence_bundle(
        operation_id="test_op_2",
        artifacts={"data.json": b'{"original": "data"}'},
        output_dir=tmp_path
    )
    
    # Verify original is valid
    success, errors = verify_evidence_bundle(bundle_path)
    assert success
    assert len(errors) == 0
    
    # Tamper with artifact
    artifact_path = bundle_path / "artifacts" / "data.json"
    artifact_path.write_text('{"tampered": "data"}')
    
    # Verification should fail
    success, errors = verify_evidence_bundle(bundle_path)
    assert not success
    assert any("hash mismatch" in err.lower() for err in errors)

def test_verification_fails_when_artifact_missing(tmp_path):
    """Verification detects missing files"""
    
    bundle_path = create_evidence_bundle(
        operation_id="test_op_3",
        artifacts={"critical.json": b'{"important": "data"}'},
        output_dir=tmp_path
    )
    
    # Delete artifact
    (bundle_path / "artifacts" / "critical.json").unlink()
    
    # Verification should fail
    success, errors = verify_evidence_bundle(bundle_path)
    assert not success
    assert any("missing" in err.lower() for err in errors)
```

**Test: Standalone Verification** (`tests/test_standalone_verification.sh`)
```bash
#!/bin/bash
# Test standalone verification script

set -e

# Create test bundle
python -c "
from app.evidence.exporter import create_evidence_bundle
bundle = create_evidence_bundle(
    'test_op_standalone',
    {'test.json': b'{\"test\": true}'},
    '/tmp/test_bundle'
)
"

# Run standalone verification
cd /tmp/test_bundle
chmod +x verification/verify.sh
./verification/verify.sh

echo "✅ Standalone verification test passed"
```

### Integration Tests

**Test: End-to-End Evidence Pipeline**
```python
async def test_evidence_pipeline_integration(client):
    """Test complete evidence export flow"""
    
    # Start validation operation
    response = await client.post("/validate", json={
        "schema": "bugcheck",
        "fixtures": ["valid/finding_1.json"]
    })
    operation_id = response.json()["operation_id"]
    
    # Wait for completion
    while True:
        status = await client.get(f"/operations/{operation_id}")
        state = status.json()["state"]
        
        if state == "completed":
            break
        elif state == "failed":
            pytest.fail("Operation failed")
        
        await asyncio.sleep(0.1)
    
    # Verify evidence bundle exists
    bundle_path = status.json()["evidence_bundle_path"]
    assert Path(bundle_path).exists()
    
    # Verify bundle integrity
    success, errors = verify_evidence_bundle(Path(bundle_path))
    assert success
    assert len(errors) == 0
```

---

## File Locations

### Where to Create Files

**Evidence Export Logic:**
```
app/evidence/
├── __init__.py
├── exporter.py          # Bundle creation logic
├── verifier.py          # Verification logic
└── chain.py             # Evidence chain (optional)
```

**Tests:**
```
tests/
├── test_evidence_determinism.py
├── test_evidence_tamper.py
├── test_evidence_integration.py
└── test_standalone_verification.sh
```

**Documentation:**
```
docs/evidence/
├── BUNDLE_FORMAT.md     # Bundle structure specification
├── VERIFICATION.md      # Verification procedures
└── CHAIN_OF_CUSTODY.md  # Evidence chain documentation
```

**Schemas:**
```
schemas/evidence/v1/
├── manifest.schema.json
├── operation_log.schema.json
└── tool_versions.schema.json
```

---

## Security Considerations

### Secrets Handling

**NEVER include in evidence bundles:**
- API keys or tokens
- Database credentials
- Private keys or certificates
- User passwords
- Session tokens

**Sanitize runtime_env.json:**
```python
def sanitize_environment(env: dict) -> dict:
    """Remove sensitive environment variables"""
    SENSITIVE_PATTERNS = [
        r".*KEY.*",
        r".*SECRET.*",
        r".*TOKEN.*",
        r".*PASSWORD.*",
        r".*CREDENTIAL.*"
    ]
    
    sanitized = {}
    for key, value in env.items():
        if any(re.match(pattern, key, re.I) for pattern in SENSITIVE_PATTERNS):
            sanitized[key] = "***REDACTED***"
        else:
            sanitized[key] = value
    
    return sanitized
```

### Hash Algorithm

**Use SHA-256 exclusively:**
- Industry standard for cryptographic integrity
- No known practical collision attacks
- Supported natively on all platforms
- Fast enough for evidence bundles (< 100MB typically)

**Do NOT use:**
- MD5 (collision attacks)
- SHA-1 (deprecated)
- Custom hash functions

---

## Performance Considerations

### Bundle Size Optimization

**Target:** Evidence bundles < 10MB for typical operations

**Strategies:**
1. **Compress logs:** Use gzip for large log files
2. **Exclude binaries:** Don't include compiled artifacts
3. **Sample metrics:** Don't store every metric tick
4. **Limit log retention:** Truncate logs > 1MB

**Example:**
```python
def create_artifact(content: bytes, compress: bool = True) -> bytes:
    """Create artifact with optional compression"""
    if compress and len(content) > 10_000:  # 10KB threshold
        return gzip.compress(content)
    return content
```

### Verification Speed

**Target:** Verification < 1 second for typical bundles

**Optimizations:**
1. **Parallel hash computation:** Use multiprocessing for large bundles
2. **Early exit:** Stop on first failure (fail-fast)
3. **Skip manifest re-hash:** Only verify artifact hashes

---

## Evidence Chain (Optional Enhancement)

### Purpose

Link evidence bundles together to create tamper-evident audit trail.

### Implementation

**Parent Hash:**
```python
def link_to_parent(current_manifest: dict, parent_bundle_path: Path) -> dict:
    """Link current bundle to parent in evidence chain"""
    
    # Load parent manifest
    parent_manifest = json.loads((parent_bundle_path / "manifest.json").read_text())
    
    # Compute parent manifest hash
    parent_hash = hashlib.sha256(
        json.dumps(parent_manifest, sort_keys=True).encode()
    ).hexdigest()
    
    # Update current manifest
    current_manifest["chain"] = {
        "parent_hash": f"sha256:{parent_hash}",
        "chain_height": parent_manifest.get("chain", {}).get("chain_height", -1) + 1
    }
    
    return current_manifest
```

**Chain Verification:**
```python
def verify_chain(bundle_path: Path, parent_bundle_path: Path) -> bool:
    """Verify evidence chain linkage"""
    
    # Load current manifest
    manifest = json.loads((bundle_path / "manifest.json").read_text())
    
    if "chain" not in manifest:
        return True  # No chain = valid (genesis bundle)
    
    # Load parent manifest
    parent_manifest = json.loads((parent_bundle_path / "manifest.json").read_text())
    
    # Compute parent hash
    expected_hash = hashlib.sha256(
        json.dumps(parent_manifest, sort_keys=True).encode()
    ).hexdigest()
    
    actual_hash = manifest["chain"]["parent_hash"].replace("sha256:", "")
    
    return expected_hash == actual_hash
```

**Note:** Evidence chain is optional for initial implementation. Document as future enhancement if time constrained.

---

## Success Criteria

### Code Quality
- ✅ Evidence bundle creation is deterministic
- ✅ Standalone verification works without FPVS
- ✅ All artifacts have SHA-256 hashes
- ✅ Missing files cause loud verification failure
- ✅ Modified files cause loud verification failure
- ✅ Secrets are never included in bundles

### Testing Coverage
- ✅ Determinism test passes
- ✅ Tamper detection test passes
- ✅ Missing file detection test passes
- ✅ Standalone verification script test passes
- ✅ Integration test covers full pipeline

### Documentation
- ✅ Bundle format specification complete
- ✅ Verification procedures documented
- ✅ Chain of custody guide (if implemented)
- ✅ Security considerations documented

### State Machine
- ✅ `VERIFYING_EVIDENCE` state added
- ✅ State transitions validated
- ✅ `evidence_bundle_path` field added to models

---

## Common Pitfalls to Avoid

### Implementation Pitfalls

❌ **Non-deterministic bundle creation**  
✅ Use stable JSON serialization (`sort_keys=True`)

❌ **Including secrets in bundles**  
✅ Sanitize environment variables and config

❌ **Silent verification failures**  
✅ Loud, clear error messages with file paths

❌ **Hardcoding FPVS dependencies in verify.sh**  
✅ Use only `sha256sum`, `jq`, standard bash

❌ **Incomplete artifact tracking**  
✅ Every file in bundle must be in manifest

### Testing Pitfalls

❌ **Testing only success cases**  
✅ Test tamper detection, missing files, corrupt bundles

❌ **Mocking hash computation**  
✅ Use real SHA-256 hashes in tests

❌ **Not testing standalone verification**  
✅ Run `verify.sh` in clean environment

---

## Quick Reference

### Key Deliverables
```
app/evidence/exporter.py
app/evidence/verifier.py
tests/test_evidence_determinism.py
tests/test_evidence_tamper.py
docs/evidence/BUNDLE_FORMAT.md
schemas/evidence/v1/manifest.schema.json
verification/verify.sh (created per bundle)
```

### Hash Format
```
sha256:a1b2c3d4e5f6...
```

### Bundle ID Format
```
bundle_20260115_143022_abc123ef
```

### State Transition
```
RUNNING → VERIFYING_EVIDENCE → COMPLETED
                             → FAILED
```

---

**This context packet provides everything needed to implement Track 3B with forensic-grade quality.**

**Proceed with implementation per FPVS_Track_3B_Prompt.md**
