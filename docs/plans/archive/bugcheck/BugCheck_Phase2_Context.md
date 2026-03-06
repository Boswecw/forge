# BugCheck Phase 2 — Context Packet for VS Code Claude

**Document Version:** 1.0  
**Created:** December 28, 2025  
**Owner:** Charles Tytler, Boswell Digital Solutions LLC  
**Purpose:** Context for implementing BugCheck Phase 2 (ForgeCommand Integration)  
**Phase Duration:** 2 weeks (80 hours)

---

## Current State

### Completed Prerequisites

**BugCheck Phase 1: MVP Foundation** ✅
- Stack detection for Python, JavaScript, Rust
- Check registry with standard interface
- Basic checks: typecheck, lint, unit tests, security
- DataForge integration: runs and findings persist
- CLI interface: `forge-bugcheck run --quick|--standard`
- 80% test coverage

**Infrastructure Ready:**
- **DataForge v5.2:** Vector storage, 296 tests
- **NeuroForge:** LLM orchestration, 100+ tests
- **ForgeAgents:** Agent platform, 120-skill library
- **ForgeCommand:** Mission control dashboard (Tauri-based)

### What Phase 1 Provided

**From `bugcheck/`:**
```
app/
├── detection/stack_detector.py    # Language detection
├── checks/
│   ├── registry.py                # Check interface
│   ├── base.py                    # BaseCheck ABC
│   ├── python/                    # Python checks
│   ├── javascript/                # JS checks
│   └── security/                  # Security checks
├── dataforge_client.py            # DataForge API client
├── models.py                      # Run, Finding, CheckResult
└── cli.py                         # Click CLI
```

**Limitations of Phase 1:**
- ❌ Only checks single service at a time
- ❌ No dependency ordering
- ❌ No cross-service validation
- ❌ No orchestration layer
- ❌ Manual service targeting

---

## Phase 2 Scope: ForgeCommand Integration

### Mission Statement

Transform BugCheck from **single-service tool** to **ecosystem-wide orchestration platform** by integrating with ForgeCommand's control plane, enabling multi-service execution with dependency awareness and cross-service validation.

### What You Will Build

1. **ForgeCommand Operation Registration** - BugCheck as executable operation
2. **Service Topology Discovery** - Read service manifests from DataForge
3. **Parallel Execution Engine** - Multi-service execution with dependency ordering
4. **Cross-Service Checks** - Contract validation, dependency sync, health probes
5. **Ephemeral Container Execution** (optional enhancement)

### What You Will NOT Build (Future Phases)

- ❌ Lifecycle state machine (Phase 2.5)
- ❌ VibeForge UI (Phase 3)
- ❌ MAID fix generation (Phase 4)
- ❌ XAI enrichment (Phase 5)
- ❌ Deep mode / fuzz testing (Phase 6)

---

## Canonical Architecture Rule

**DataForge is the authoritative source of truth** for all Forge ecosystem state, including:
- Service topology (manifests)
- Dependency graphs
- Run records
- Findings
- Historical trends

**ForgeCommand Responsibility:**
- ✅ Orchestrate multi-service runs
- ✅ RBAC enforcement
- ✅ Run token generation
- ✅ Topology management
- ❌ Never execute checks directly
- ❌ Never persist findings (BugCheck writes to DataForge)
- ❌ Never make lifecycle decisions (DataForge owns state machine)

**BugCheck Responsibility:**
- ✅ Execute checks when invoked
- ✅ Generate findings
- ✅ Write to DataForge
- ❌ Never orchestrate itself (ForgeCommand does that)
- ❌ Never manage topology (reads from DataForge)

---

## Service Manifest Specification

### Purpose

Service manifests declare each service's dependencies, health endpoints, and capabilities. Stored in DataForge, they form the topology graph.

### Schema Reference

**File:** `schemas/bugcheck/v1/service_manifest_schema.json` (from Phase 0)

### Example Manifest

**NeuroForge Manifest:**
```yaml
service:
  name: neuroforge
  version: "5.2.1"
  repository: "https://github.com/bds/neuroforge"
  
dependencies:
  runtime:
    - name: openai
      type: external
      version: ">=1.0.0"
    - name: anthropic
      type: external
      version: ">=0.8.0"
  
  services:
    - name: dataforge
      type: internal
      required: true
      health_check: "https://dataforge.onrender.com/health"

health:
  ready: "/fpvs/ready"
  version: "/fpvs/version"
  
contracts:
  provides:
    - endpoint: "/v1/chat/completions"
      schema: "openapi/chat.yaml"
  consumes:
    - service: dataforge
      endpoint: "/api/vectors/search"
      
bugcheck:
  enabled: true
  categories: ["security", "quality", "performance"]
  stack:
    language: python
    tools: ["mypy", "ruff", "pytest"]
```

**DataForge Manifest:**
```yaml
service:
  name: dataforge
  version: "5.2.0"
  repository: "https://github.com/bds/dataforge"

dependencies:
  runtime:
    - name: postgresql
      type: database
      version: ">=14.0"
    - name: redis
      type: cache
      version: ">=7.0"
  
  services: []  # No internal service dependencies

health:
  ready: "/fpvs/ready"
  version: "/fpvs/version"

contracts:
  provides:
    - endpoint: "/api/vectors/search"
      schema: "openapi/vectors.yaml"
    - endpoint: "/api/bugcheck/runs"
      schema: "openapi/bugcheck.yaml"

bugcheck:
  enabled: true
  categories: ["security", "quality"]
  stack:
    language: python
    tools: ["mypy", "ruff", "pytest"]
```

### Manifest Storage in DataForge

**Endpoint:** `POST /api/services/manifests`

**Data Model:**
```python
class ServiceManifest(BaseModel):
    service_name: str
    version: str
    repository: str
    dependencies: Dict[str, List[Dependency]]
    health: HealthConfig
    contracts: ContractSpec
    bugcheck: BugCheckConfig
    updated_at: datetime
```

---

## Service Topology Discovery

### Purpose

Build a dependency graph from service manifests to determine execution order and detect circular dependencies.

### Algorithm

**File:** `bugcheck/app/topology/service_graph.py`

```python
from typing import Dict, List, Set
from dataclasses import dataclass
from ..models import ServiceManifest

@dataclass
class TopologyNode:
    """Node in service dependency graph"""
    service_name: str
    manifest: ServiceManifest
    dependencies: List[str]  # Service names this depends on
    dependents: List[str]    # Services that depend on this

class ServiceGraph:
    """Service dependency graph"""
    
    def __init__(self, manifests: List[ServiceManifest]):
        self.nodes: Dict[str, TopologyNode] = {}
        self._build_graph(manifests)
    
    def _build_graph(self, manifests: List[ServiceManifest]):
        """Build dependency graph from manifests"""
        # Create nodes
        for manifest in manifests:
            self.nodes[manifest.service_name] = TopologyNode(
                service_name=manifest.service_name,
                manifest=manifest,
                dependencies=[],
                dependents=[]
            )
        
        # Link dependencies
        for manifest in manifests:
            node = self.nodes[manifest.service_name]
            for dep in manifest.dependencies.get("services", []):
                if dep.type == "internal":
                    node.dependencies.append(dep.name)
                    if dep.name in self.nodes:
                        self.nodes[dep.name].dependents.append(manifest.service_name)
    
    def get_execution_order(self) -> List[List[str]]:
        """
        Get execution order respecting dependencies.
        
        Returns:
            List of service batches that can execute in parallel.
            Each batch is a list of service names.
        """
        # Topological sort with Kahn's algorithm
        in_degree = {name: len(node.dependencies) for name, node in self.nodes.items()}
        
        batches = []
        remaining = set(self.nodes.keys())
        
        while remaining:
            # Find all nodes with no dependencies
            batch = [name for name in remaining if in_degree[name] == 0]
            
            if not batch:
                # Circular dependency detected
                raise ValueError(f"Circular dependency in services: {remaining}")
            
            batches.append(batch)
            
            # Remove batch from remaining
            for service in batch:
                remaining.remove(service)
                
                # Decrease in-degree for dependents
                for dependent in self.nodes[service].dependents:
                    if dependent in remaining:
                        in_degree[dependent] -= 1
        
        return batches
    
    def get_dependencies(self, service_name: str) -> List[str]:
        """Get all dependencies for a service (transitive)"""
        if service_name not in self.nodes:
            return []
        
        visited = set()
        stack = [service_name]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            
            visited.add(current)
            if current in self.nodes:
                stack.extend(self.nodes[current].dependencies)
        
        visited.remove(service_name)  # Don't include self
        return list(visited)
```

### Execution Order Example

**Services:** NeuroForge, DataForge, Rake, ForgeAgents

**Dependencies:**
```
DataForge: []
Rake: [DataForge]
NeuroForge: [DataForge]
ForgeAgents: [DataForge, NeuroForge, Rake]
```

**Execution Batches:**
```python
[
    ["DataForge"],                      # Batch 1: No dependencies
    ["Rake", "NeuroForge"],            # Batch 2: Depend on DataForge
    ["ForgeAgents"]                    # Batch 3: Depends on all others
]
```

---

## Run Token System

### Purpose

Secure, ephemeral authorization for BugCheck runs. Prevents unauthorized finding injection and provides audit trail.

### Schema Reference

**File:** `schemas/bugcheck/v1/run_token_schema.json` (from Phase 0)

### Token Structure

```python
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class RunToken(BaseModel):
    """Ephemeral authorization token for BugCheck run"""
    token_id: str
    run_id: str
    services: List[str]  # Services this token authorizes
    mode: Literal["quick", "standard", "deep"]
    scope: Literal["single", "ecosystem"]
    commit_sha: str
    issued_at: datetime
    expires_at: datetime
    nonce: str  # Replay protection
    issuer: str = "forgecommand"
```

### Token Generation (ForgeCommand)

```python
import secrets
import hashlib
from datetime import datetime, timedelta, timezone

def generate_run_token(
    run_id: str,
    services: List[str],
    mode: str,
    commit_sha: str,
    ttl_minutes: int = 60
) -> RunToken:
    """Generate run token for BugCheck execution"""
    
    now = datetime.now(timezone.utc)
    
    token = RunToken(
        token_id=f"token_{secrets.token_hex(12)}",
        run_id=run_id,
        services=services,
        mode=mode,
        scope="ecosystem" if len(services) > 1 else "single",
        commit_sha=commit_sha,
        issued_at=now,
        expires_at=now + timedelta(minutes=ttl_minutes),
        nonce=secrets.token_hex(16),
        issuer="forgecommand"
    )
    
    return token

def encode_run_token(token: RunToken, secret_key: str) -> str:
    """Encode token as signed JWT-like string"""
    import jwt
    return jwt.encode(token.model_dump(), secret_key, algorithm="HS256")

def decode_run_token(encoded: str, secret_key: str) -> RunToken:
    """Decode and verify run token"""
    import jwt
    payload = jwt.decode(encoded, secret_key, algorithms=["HS256"])
    return RunToken(**payload)
```

### Token Validation (BugCheck)

```python
async def validate_run_token(
    token: RunToken,
    service: str,
    run_id: str
) -> bool:
    """Validate run token before executing checks"""
    
    now = datetime.now(timezone.utc)
    
    # Check expiry
    if now > token.expires_at:
        raise ValueError("Run token expired")
    
    # Check run_id matches
    if token.run_id != run_id:
        raise ValueError("Run ID mismatch")
    
    # Check service authorized
    if service not in token.services:
        raise ValueError(f"Service {service} not authorized")
    
    # TODO: Check nonce hasn't been used (replay protection)
    # This requires DataForge to track used nonces
    
    return True
```

---

## Parallel Execution Engine

### Purpose

Execute BugCheck across multiple services in parallel, respecting dependency ordering and handling failures gracefully.

### Architecture

**File:** `bugcheck/app/executor/parallel_runner.py`

```python
import asyncio
from typing import List, Dict
from ..topology.service_graph import ServiceGraph
from ..models import BugCheckRun, Finding
from ..dataforge_client import DataForgeClient

class ParallelExecutor:
    """Execute BugCheck across multiple services in parallel"""
    
    def __init__(self, dataforge: DataForgeClient):
        self.dataforge = dataforge
    
    async def execute_ecosystem_run(
        self,
        run_id: str,
        services: List[str],
        mode: str,
        commit_sha: str
    ) -> Dict[str, List[Finding]]:
        """
        Execute BugCheck across multiple services.
        
        Returns:
            Dict mapping service names to findings
        """
        # Get service manifests
        manifests = await self._get_service_manifests(services)
        
        # Build dependency graph
        graph = ServiceGraph(manifests)
        
        # Get execution batches
        batches = graph.get_execution_order()
        
        all_findings = {}
        
        # Execute batches sequentially, services within batch in parallel
        for batch in batches:
            batch_results = await self._execute_batch(
                batch,
                run_id,
                mode,
                commit_sha
            )
            all_findings.update(batch_results)
        
        return all_findings
    
    async def _execute_batch(
        self,
        services: List[str],
        run_id: str,
        mode: str,
        commit_sha: str
    ) -> Dict[str, List[Finding]]:
        """Execute multiple services in parallel"""
        tasks = [
            self._execute_service(service, run_id, mode, commit_sha)
            for service in services
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        findings = {}
        for service, result in zip(services, results):
            if isinstance(result, Exception):
                # Log error but continue
                print(f"Error executing {service}: {result}")
                findings[service] = []
            else:
                findings[service] = result
        
        return findings
    
    async def _execute_service(
        self,
        service: str,
        run_id: str,
        mode: str,
        commit_sha: str
    ) -> List[Finding]:
        """Execute BugCheck for single service"""
        # This calls the Phase 1 BugCheck execution
        # Could be subprocess call to CLI or direct Python import
        
        from ..cli import _run_async
        
        # Execute BugCheck for this service
        findings = await _run_async(
            mode=mode,
            service=service,
            format="json"  # Get structured output
        )
        
        return findings
    
    async def _get_service_manifests(self, services: List[str]) -> List:
        """Fetch service manifests from DataForge"""
        manifests = []
        for service in services:
            manifest = await self.dataforge.get_service_manifest(service)
            manifests.append(manifest)
        return manifests
```

### Error Handling Strategy

**Failures in Batch:**
```python
# If service in batch fails:
# 1. Log error
# 2. Continue with remaining services in batch
# 3. Skip dependent services in later batches
# 4. Mark run as "partial_failure"

async def _execute_batch_with_error_handling(self, batch):
    successful = []
    failed = []
    
    for service, result in zip(batch, results):
        if isinstance(result, Exception):
            failed.append(service)
        else:
            successful.append(service)
    
    # Remove failed services from graph
    for service in failed:
        self._mark_service_failed(service)
        self._remove_dependents(service)
    
    return successful, failed
```

---

## Cross-Service Checks

### Purpose

Validate contracts, dependencies, and health across service boundaries.

### Check Types

**1. Contract Validation**

Verify API contracts match between provider and consumer.

```python
class ContractValidationCheck(BaseCheck):
    name = "cross-service-contract"
    category = "compliance"
    priority = 3
    
    def is_applicable(self, stack: StackInfo) -> bool:
        return True  # Applies when multiple services in run
    
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """Validate API contracts"""
        findings = []
        
        service_name = context["service"]
        manifest = context["manifest"]
        
        # For each service this depends on
        for dep in manifest.dependencies.get("services", []):
            # Fetch dependency's manifest
            dep_manifest = await self._get_manifest(dep.name)
            
            # Check if dependency provides the endpoint we expect
            consumed = manifest.contracts.consumes
            provided = dep_manifest.contracts.provides
            
            for endpoint in consumed:
                if endpoint.service == dep.name:
                    if not self._endpoint_provided(endpoint, provided):
                        findings.append(Finding(
                            # ... finding details
                            title=f"Contract violation: {dep.name} doesn't provide {endpoint.endpoint}",
                            description=f"Service {service_name} expects {endpoint.endpoint} but {dep.name} doesn't provide it"
                        ))
        
        return CheckResult(
            check_name=self.name,
            passed=len(findings) == 0,
            findings=findings,
            duration_seconds=0
        )
```

**2. Dependency Version Sync**

Check if all services use compatible dependency versions.

```python
class DependencySyncCheck(BaseCheck):
    name = "cross-service-dependency-sync"
    category = "quality"
    priority = 4
    
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """Check dependency version consistency"""
        findings = []
        
        # Get all service manifests
        all_manifests = context["all_manifests"]
        
        # Group by dependency name
        dep_versions = {}
        for manifest in all_manifests:
            for dep in manifest.dependencies.get("runtime", []):
                if dep.name not in dep_versions:
                    dep_versions[dep.name] = {}
                dep_versions[dep.name][manifest.service_name] = dep.version
        
        # Check for mismatches
        for dep_name, versions in dep_versions.items():
            if len(set(versions.values())) > 1:
                # Version mismatch
                findings.append(Finding(
                    # ... finding details
                    title=f"Dependency version mismatch: {dep_name}",
                    description=f"Services use different versions: {versions}",
                    severity="S2"
                ))
        
        return CheckResult(
            check_name=self.name,
            passed=len(findings) == 0,
            findings=findings,
            duration_seconds=0
        )
```

**3. Health Probe Check**

Verify all dependent services are healthy before executing checks.

```python
class HealthProbeCheck(BaseCheck):
    name = "cross-service-health"
    category = "quality"
    priority = 1  # Run early
    
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """Check health of dependent services"""
        findings = []
        
        manifest = context["manifest"]
        
        for dep in manifest.dependencies.get("services", []):
            if not dep.health_check:
                continue
            
            # Probe health endpoint
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(dep.health_check, timeout=5.0)
                    
                    if response.status_code != 200:
                        findings.append(Finding(
                            # ... finding details
                            title=f"Dependency unhealthy: {dep.name}",
                            description=f"Health check returned {response.status_code}",
                            severity="S1"  # Dependency down is high severity
                        ))
            except Exception as e:
                findings.append(Finding(
                    # ... finding details
                    title=f"Dependency unreachable: {dep.name}",
                    description=f"Health check failed: {e}",
                    severity="S1"
                ))
        
        return CheckResult(
            check_name=self.name,
            passed=len(findings) == 0,
            findings=findings,
            duration_seconds=0
        )
```

---

## ForgeCommand Integration Points

### 1. Operation Registration

**File:** `forgecommand/operations/bugcheck.py`

```python
from typing import List
from ..models import Operation, OperationResult

class BugCheckOperation(Operation):
    """BugCheck operation for ForgeCommand"""
    
    name = "bugcheck"
    description = "Execute ecosystem-wide quality checks"
    requires_auth = True
    
    async def execute(
        self,
        services: List[str],
        mode: str = "standard",
        commit_sha: str = None
    ) -> OperationResult:
        """Execute BugCheck operation"""
        
        # Generate run token
        run_id = generate_run_id()
        token = generate_run_token(
            run_id=run_id,
            services=services,
            mode=mode,
            commit_sha=commit_sha or self._get_commit_sha()
        )
        
        # Store token in DataForge
        await self.dataforge.store_run_token(token)
        
        # Execute BugCheck via parallel executor
        executor = ParallelExecutor(self.dataforge)
        findings = await executor.execute_ecosystem_run(
            run_id=run_id,
            services=services,
            mode=mode,
            commit_sha=commit_sha
        )
        
        return OperationResult(
            success=True,
            data={
                "run_id": run_id,
                "findings_by_service": {
                    svc: len(flist) for svc, flist in findings.items()
                }
            }
        )
```

### 2. RBAC Integration

```python
class BugCheckPermission:
    """Permission model for BugCheck operations"""
    
    @staticmethod
    def can_execute_bugcheck(user: User, services: List[str]) -> bool:
        """Check if user can execute BugCheck on services"""
        
        # Admin can execute on all services
        if user.role == "admin":
            return True
        
        # Developer can execute on services they own
        if user.role == "developer":
            user_services = get_user_services(user)
            return all(svc in user_services for svc in services)
        
        # Read-only cannot execute
        return False
```

### 3. UI Integration (ForgeCommand Dashboard)

**React Component Example:**

```typescript
// forgecommand/ui/components/BugCheck/TriggerPanel.tsx

interface TriggerPanelProps {
  services: Service[];
}

export function BugCheckTriggerPanel({ services }: TriggerPanelProps) {
  const [selectedServices, setSelectedServices] = useState<string[]>([]);
  const [mode, setMode] = useState<'quick' | 'standard' | 'deep'>('standard');
  
  const handleExecute = async () => {
    const result = await executeOperation('bugcheck', {
      services: selectedServices,
      mode: mode
    });
    
    toast.success(`BugCheck run started: ${result.run_id}`);
  };
  
  return (
    <div className="bugcheck-trigger">
      <h2>Execute BugCheck</h2>
      
      <ServiceSelector
        services={services}
        selected={selectedServices}
        onChange={setSelectedServices}
      />
      
      <ModeSelector value={mode} onChange={setMode} />
      
      <button onClick={handleExecute}>
        Execute BugCheck
      </button>
    </div>
  );
}
```

---

## Ephemeral Container Execution (Optional)

### Purpose

Isolate BugCheck execution in containers for security and reproducibility.

### Implementation (Docker-based)

```python
import docker
from pathlib import Path

class ContainerExecutor:
    """Execute BugCheck in isolated containers"""
    
    def __init__(self):
        self.client = docker.from_env()
    
    async def execute_in_container(
        self,
        service: str,
        repo_path: Path,
        mode: str
    ) -> List[Finding]:
        """Execute BugCheck in ephemeral container"""
        
        # Create container
        container = self.client.containers.run(
            image="bugcheck:latest",
            command=f"bugcheck run --mode {mode} --service {service}",
            volumes={
                str(repo_path): {"bind": "/repo", "mode": "ro"}
            },
            environment={
                "DATAFORGE_URL": os.getenv("DATAFORGE_URL"),
                "DATAFORGE_API_KEY": os.getenv("DATAFORGE_API_KEY")
            },
            network_mode="none",  # No network access
            mem_limit="512m",
            cpu_quota=50000,  # 50% of one CPU
            detach=True
        )
        
        # Wait for completion
        result = container.wait(timeout=600)  # 10 min timeout
        
        # Get logs
        logs = container.logs()
        
        # Cleanup
        container.remove()
        
        # Parse findings from logs
        findings = self._parse_findings_from_logs(logs)
        
        return findings
```

---

## Success Criteria

Before Phase 2 is complete:

### Functional Requirements
- ✅ ForgeCommand can trigger ecosystem-wide BugCheck runs
- ✅ Multi-service execution works in parallel
- ✅ Dependency ordering is respected
- ✅ Cross-service contract validation works
- ✅ Health probes check dependent services
- ✅ Run tokens prevent unauthorized execution
- ✅ Failures in one service don't block others

### Quality Requirements
- ✅ 75% test coverage on new code
- ✅ All integration tests pass
- ✅ Performance: Full ecosystem run < 15 minutes
- ✅ Error handling: Graceful degradation on failures

### Documentation
- ✅ Service manifest format documented
- ✅ Topology discovery algorithm explained
- ✅ Run token system documented
- ✅ ForgeCommand integration guide

---

## Testing Requirements

### Unit Tests

```python
# tests/test_topology.py
def test_dependency_ordering():
    """Test topological sort of services"""
    manifests = [
        create_manifest("dataforge", dependencies=[]),
        create_manifest("neuroforge", dependencies=["dataforge"]),
        create_manifest("forgeagents", dependencies=["neuroforge", "dataforge"])
    ]
    
    graph = ServiceGraph(manifests)
    batches = graph.get_execution_order()
    
    assert batches[0] == ["dataforge"]
    assert "neuroforge" in batches[1]
    assert batches[2] == ["forgeagents"]

def test_circular_dependency_detection():
    """Test circular dependency raises error"""
    manifests = [
        create_manifest("a", dependencies=["b"]),
        create_manifest("b", dependencies=["a"])
    ]
    
    with pytest.raises(ValueError, match="Circular dependency"):
        graph = ServiceGraph(manifests)
        graph.get_execution_order()
```

### Integration Tests

```python
# tests/integration/test_parallel_execution.py
@pytest.mark.asyncio
async def test_parallel_execution_ecosystem():
    """Test full ecosystem execution"""
    
    executor = ParallelExecutor(dataforge_client)
    
    findings = await executor.execute_ecosystem_run(
        run_id="test_run",
        services=["dataforge", "neuroforge", "rake", "forgeagents"],
        mode="quick",
        commit_sha="abc123"
    )
    
    # Verify all services executed
    assert "dataforge" in findings
    assert "neuroforge" in findings
    assert "rake" in findings
    assert "forgeagents" in findings
```

---

## Performance Targets

- **Ecosystem run (4 services):** < 15 minutes in standard mode
- **Service manifest fetch:** < 500ms
- **Topology graph construction:** < 1 second
- **Parallel execution overhead:** < 10% vs sequential
- **Run token generation:** < 100ms

---

## Common Pitfalls to Avoid

### Implementation Pitfalls

❌ **Sequential execution of independent services**  
✅ Execute services in parallel within each batch

❌ **Ignoring circular dependencies**  
✅ Detect and fail fast on circular dependencies

❌ **Hardcoding service list**  
✅ Always read from DataForge manifests

❌ **No timeout on service execution**  
✅ Set timeouts per service, fail gracefully

❌ **Exposing run tokens in logs**  
✅ Redact tokens in all logging output

### Testing Pitfalls

❌ **Testing only success path**  
✅ Test failures, timeouts, partial failures

❌ **Mocking topology graph**  
✅ Use real service manifests in tests

❌ **Not testing RBAC**  
✅ Verify unauthorized users can't execute

---

## Quick Reference

### Key Files to Create
```
bugcheck/app/topology/
  ├── __init__.py
  ├── service_graph.py
  └── manifest_loader.py

bugcheck/app/executor/
  ├── __init__.py
  ├── parallel_runner.py
  └── container_executor.py (optional)

bugcheck/app/checks/cross_service/
  ├── __init__.py
  ├── contract_validation.py
  ├── dependency_sync.py
  └── health_probes.py

forgecommand/operations/
  └── bugcheck.py
```

### DataForge API Extensions Needed
```
GET /api/services/manifests/{service_name}
POST /api/services/manifests
GET /api/bugcheck/run_tokens/{token_id}
POST /api/bugcheck/run_tokens
```

### Execution Flow
```
1. ForgeCommand receives "Execute BugCheck" request
2. Generate run token
3. Store token in DataForge
4. Fetch service manifests
5. Build dependency graph
6. Get execution batches
7. For each batch:
   - Execute services in parallel
   - Wait for all to complete
   - Check for failures
8. Aggregate findings
9. Update run status in DataForge
```

---

**This context packet provides everything needed to implement BugCheck Phase 2 with production-grade quality.**

**Proceed with implementation per BugCheck_Phase2_Prompt.md**
