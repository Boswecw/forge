# ForgeAgents Comprehensive Implementation Plan

**Version:** 1.0 | **Status:** Implementation Ready | **Date:** January 2026

---

## Executive Summary

This plan unifies:
- **120 Capabilities** — What ForgeAgents can do
- **Node Catalog** — How capabilities are organized and executed
- **SMITH Integration** — How governance flows through the system

**Key Insight:** Capabilities are *behaviors*. Nodes are *execution containers*. One node may implement multiple capabilities. One capability may span multiple nodes.

---

## Architecture Clarification

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMITH (Authority Layer)                       │
│  • Approves plans            • Signs executions                  │
│  • Holds governance state    • Issues authority tokens           │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ Authority Token + Plan
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ForgeAgents (Execution Layer)                   │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Tier 0     │  │  Tier 1-4   │  │  Tier 5-6   │              │
│  │  Control    │──│  Execution  │──│  Integration│              │
│  │  Nodes      │  │  Nodes      │  │  Nodes      │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          │                                       │
│                    120 Capabilities                              │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ Evidence + Results
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DataForge (Memory Layer)                      │
│  • Evidence storage    • Execution history    • Context graph    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Critical Corrections & Suggestions

### Correction 1: Capabilities vs Nodes

**Problem:** The 120 capabilities list mixes *what* (behaviors) with *where* (execution context).

**Solution:** Capabilities are atomic behaviors. Nodes are execution containers that invoke capabilities.

```python
# A Node invokes Capabilities
class TypeScriptSpecialistNode(Node):
    """Tier 2 execution node for TypeScript operations."""
    
    capabilities = [
        Capability_050_ExecutionTraceGeneration,  # From Category C
        Capability_051_TokenUsageAccounting,       # From Category C
        Capability_059_CryptographicHashing,       # From Category D
    ]
    
    async def execute(self, plan_step: PlanStep) -> NodeResult:
        # Invoke capabilities as needed
        pass
```

### Correction 2: Node Registration Safety

**Problem:** The node catalog doesn't specify how nodes are registered or validated.

**Solution:** Add a Node Registry with schema validation.

```python
# app/nodes/registry.py
class NodeRegistration(BaseModel):
    """Schema for safe node registration."""
    node_id: str
    node_class: str
    tier: int  # 0-6
    allowed_capabilities: list[int]  # Capability IDs this node can invoke
    tool_restrictions: list[str]  # Tools this node can use
    context_classes: list[str]  # GOVERNED, UNGOVERNED, or both
    max_execution_time_seconds: int
    requires_dry_run: bool
    evidence_types: list[str]  # What evidence this node produces
```

### Correction 3: GOVERNED vs UNGOVERNED Context

**Problem:** Not all nodes should run in GOVERNED context.

**Solution:** Explicit context class mapping.

| Tier | Nodes | GOVERNED | UNGOVERNED |
|------|-------|----------|------------|
| 0 | Control & Safety | ✅ Required | ✅ Required |
| 1 | Code & Repo Intelligence | ✅ Yes | ✅ Yes |
| 2 | Language Specialists | ✅ Yes | ⚠️ Read-only |
| 3 | Build, Test & Verification | ✅ Yes | ✅ Yes |
| 4 | Planning Support | ✅ Yes | ✅ Yes |
| 5 | Ecosystem Integration | ✅ Yes | ❌ No |
| 6 | Release & Post-Execution | ✅ Yes | ❌ No |

### Suggestion 1: Capability Invocation Tracking

Every capability invocation should be tracked:

```python
class CapabilityInvocation(BaseModel):
    """Audit record for every capability invocation."""
    invocation_id: str
    capability_id: int
    node_id: str
    correlation_id: str
    authority_token: str
    started_at: datetime
    completed_at: datetime | None
    success: bool
    evidence_hash: str | None
```

### Suggestion 2: Node Lifecycle States

```
REGISTERED → VALIDATED → READY → EXECUTING → COMPLETED
                                     ↓
                                  FAILED → ROLLBACK_READY
                                     ↓
                                  ABORTED
```

### Suggestion 3: Capability Dependencies

Some capabilities depend on others:

```python
# Capability 56 (Evidence bundle generation) requires:
# - Capability 59 (Cryptographic hashing)
# - Capability 60 (Canonical JSON generation)
# - Capability 64 (Evidence timestamp normalization)

CAPABILITY_DEPENDENCIES = {
    56: [59, 60, 64],
    36: [44, 50, 51],  # MAPO lane execution requires fail-closed, trace, token accounting
    # ...
}
```

---

## Implementation Plan

### Phase 0: Foundation (Week 1)

**Goal:** Create the infrastructure for capabilities and nodes.

#### 0.1 Capability Framework

```
app/capabilities/
├── __init__.py
├── base.py              # Capability base class
├── registry.py          # Capability registration
├── context.py           # CapabilityContext
├── result.py            # CapabilityResult
└── dependencies.py      # Capability dependency graph
```

**Files to create:**

```python
# app/capabilities/base.py
from abc import ABC, abstractmethod
from typing import Any, ClassVar
from pydantic import BaseModel
from enum import Enum

class CapabilityCategory(str, Enum):
    AUTHORITY = "A"
    PLANNING = "B"
    EXECUTION = "C"
    EVIDENCE = "D"
    BUILDGUARD = "E"
    REPOSITORY = "F"
    OBSERVABILITY = "G"

class CapabilityContext(BaseModel):
    """Context passed to every capability."""
    correlation_id: str
    authority_token: str | None = None
    authority_ring: int = 2  # 0 = owner, 1 = operator, 2 = read-only
    execution_mode: str = "read_only"  # "read_only" | "write"
    context_class: str = "UNGOVERNED"  # "GOVERNED" | "UNGOVERNED"
    issuer_id: str | None = None
    policy_version: str = "1.0"
    node_id: str | None = None
    plan_hash: str | None = None

class CapabilityResult(BaseModel):
    """Standard result from capability execution."""
    capability_id: int
    success: bool
    evidence: dict | None = None
    evidence_hash: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    execution_time_ms: int = 0
    token_usage: int = 0

class Capability(ABC):
    """Base class for all 120 capabilities."""
    
    # Class attributes - override in subclasses
    capability_id: ClassVar[int]
    capability_name: ClassVar[str]
    category: ClassVar[CapabilityCategory]
    requires_authority_ring: ClassVar[int] = 2
    requires_governed_context: ClassVar[bool] = False
    produces_evidence: ClassVar[bool] = True
    dependencies: ClassVar[list[int]] = []
    
    @abstractmethod
    async def execute(
        self, 
        context: CapabilityContext, 
        **kwargs
    ) -> CapabilityResult:
        """Execute the capability."""
        pass
    
    def validate_preconditions(
        self, 
        context: CapabilityContext, 
        **kwargs
    ) -> tuple[bool, str | None]:
        """
        Check if capability can execute.
        Returns (can_execute, error_message).
        """
        # Authority ring check
        if context.authority_ring > self.requires_authority_ring:
            return False, f"Requires ring {self.requires_authority_ring}, got {context.authority_ring}"
        
        # Governed context check
        if self.requires_governed_context and context.context_class != "GOVERNED":
            return False, "Requires GOVERNED context"
        
        return True, None
    
    def get_evidence_type(self) -> str:
        """Return the type of evidence this capability produces."""
        return f"capability_{self.capability_id}_evidence"
```

```python
# app/capabilities/registry.py
from typing import Type
from .base import Capability, CapabilityCategory

class CapabilityRegistry:
    """Registry for all 120 capabilities."""
    
    _capabilities: dict[int, Type[Capability]] = {}
    _by_category: dict[CapabilityCategory, list[int]] = {
        cat: [] for cat in CapabilityCategory
    }
    
    @classmethod
    def register(cls, capability_class: Type[Capability]) -> Type[Capability]:
        """Decorator to register a capability."""
        cap_id = capability_class.capability_id
        
        if cap_id in cls._capabilities:
            raise ValueError(f"Capability {cap_id} already registered")
        
        cls._capabilities[cap_id] = capability_class
        cls._by_category[capability_class.category].append(cap_id)
        
        return capability_class
    
    @classmethod
    def get(cls, capability_id: int) -> Type[Capability]:
        """Get a capability class by ID."""
        if capability_id not in cls._capabilities:
            raise KeyError(f"Capability {capability_id} not registered")
        return cls._capabilities[capability_id]
    
    @classmethod
    def get_by_category(cls, category: CapabilityCategory) -> list[Type[Capability]]:
        """Get all capabilities in a category."""
        return [cls._capabilities[cap_id] for cap_id in cls._by_category[category]]
    
    @classmethod
    def all_ids(cls) -> list[int]:
        """Get all registered capability IDs."""
        return list(cls._capabilities.keys())
    
    @classmethod
    def validate_dependencies(cls) -> list[str]:
        """Validate all capability dependencies are registered."""
        errors = []
        for cap_id, cap_class in cls._capabilities.items():
            for dep_id in cap_class.dependencies:
                if dep_id not in cls._capabilities:
                    errors.append(f"Capability {cap_id} depends on unregistered {dep_id}")
        return errors
```

#### 0.2 Node Framework

```
app/nodes/
├── __init__.py
├── base.py              # Node base class
├── registry.py          # Node registration
├── lifecycle.py         # Node lifecycle state machine
├── tiers/
│   ├── __init__.py
│   ├── tier0_control.py
│   ├── tier1_intelligence.py
│   ├── tier2_specialists.py
│   ├── tier3_verification.py
│   ├── tier4_planning.py
│   ├── tier5_integration.py
│   └── tier6_release.py
└── schemas/
    └── registration.py
```

**Files to create:**

```python
# app/nodes/base.py
from abc import ABC, abstractmethod
from typing import ClassVar
from pydantic import BaseModel
from enum import Enum
from ..capabilities.base import Capability, CapabilityContext, CapabilityResult
from ..capabilities.registry import CapabilityRegistry

class NodeTier(int, Enum):
    CONTROL = 0
    INTELLIGENCE = 1
    SPECIALIST = 2
    VERIFICATION = 3
    PLANNING = 4
    INTEGRATION = 5
    RELEASE = 6

class NodeState(str, Enum):
    REGISTERED = "registered"
    VALIDATED = "validated"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"
    ROLLBACK_READY = "rollback_ready"

class NodeContext(BaseModel):
    """Execution context for a node."""
    correlation_id: str
    authority_token: str | None = None
    authority_ring: int = 2
    context_class: str = "UNGOVERNED"
    plan_hash: str | None = None
    plan_step_index: int = 0
    dry_run: bool = False

class NodeResult(BaseModel):
    """Result from node execution."""
    node_id: str
    state: NodeState
    capability_results: list[CapabilityResult] = []
    evidence_hashes: list[str] = []
    error: str | None = None
    execution_time_ms: int = 0

class Node(ABC):
    """Base class for all ForgeAgents nodes."""
    
    # Class attributes - override in subclasses
    node_id: ClassVar[str]
    node_name: ClassVar[str]
    tier: ClassVar[NodeTier]
    allowed_capabilities: ClassVar[list[int]] = []
    allowed_context_classes: ClassVar[list[str]] = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first: ClassVar[bool] = False
    max_execution_time_seconds: ClassVar[int] = 300
    
    def __init__(self):
        self.state = NodeState.REGISTERED
        self._capability_instances: dict[int, Capability] = {}
    
    def validate(self) -> tuple[bool, str | None]:
        """Validate node configuration."""
        # Check all allowed capabilities are registered
        for cap_id in self.allowed_capabilities:
            try:
                CapabilityRegistry.get(cap_id)
            except KeyError:
                return False, f"Capability {cap_id} not registered"
        
        self.state = NodeState.VALIDATED
        return True, None
    
    def get_capability(self, capability_id: int) -> Capability:
        """Get or create a capability instance."""
        if capability_id not in self.allowed_capabilities:
            raise ValueError(f"Node {self.node_id} cannot use capability {capability_id}")
        
        if capability_id not in self._capability_instances:
            cap_class = CapabilityRegistry.get(capability_id)
            self._capability_instances[capability_id] = cap_class()
        
        return self._capability_instances[capability_id]
    
    async def invoke_capability(
        self,
        capability_id: int,
        context: NodeContext,
        **kwargs
    ) -> CapabilityResult:
        """Invoke a capability within this node."""
        capability = self.get_capability(capability_id)
        
        # Convert NodeContext to CapabilityContext
        cap_context = CapabilityContext(
            correlation_id=context.correlation_id,
            authority_token=context.authority_token,
            authority_ring=context.authority_ring,
            context_class=context.context_class,
            node_id=self.node_id,
            plan_hash=context.plan_hash,
            execution_mode="read_only" if context.dry_run else "write",
        )
        
        # Validate preconditions
        can_execute, error = capability.validate_preconditions(cap_context, **kwargs)
        if not can_execute:
            return CapabilityResult(
                capability_id=capability_id,
                success=False,
                error_code="PRECONDITION_FAILED",
                error_message=error,
            )
        
        # Execute
        return await capability.execute(cap_context, **kwargs)
    
    @abstractmethod
    async def execute(self, context: NodeContext, **kwargs) -> NodeResult:
        """Execute the node's primary function."""
        pass
    
    def can_execute_in_context(self, context_class: str) -> bool:
        """Check if node can run in given context class."""
        return context_class in self.allowed_context_classes
```

```python
# app/nodes/registry.py
from typing import Type
from .base import Node, NodeTier

class NodeRegistry:
    """Registry for all ForgeAgents nodes."""
    
    _nodes: dict[str, Type[Node]] = {}
    _by_tier: dict[NodeTier, list[str]] = {tier: [] for tier in NodeTier}
    
    @classmethod
    def register(cls, node_class: Type[Node]) -> Type[Node]:
        """Decorator to register a node."""
        node_id = node_class.node_id
        
        if node_id in cls._nodes:
            raise ValueError(f"Node {node_id} already registered")
        
        cls._nodes[node_id] = node_class
        cls._by_tier[node_class.tier].append(node_id)
        
        return node_class
    
    @classmethod
    def get(cls, node_id: str) -> Type[Node]:
        """Get a node class by ID."""
        if node_id not in cls._nodes:
            raise KeyError(f"Node {node_id} not registered")
        return cls._nodes[node_id]
    
    @classmethod
    def get_by_tier(cls, tier: NodeTier) -> list[Type[Node]]:
        """Get all nodes in a tier."""
        return [cls._nodes[node_id] for node_id in cls._by_tier[tier]]
    
    @classmethod
    def validate_all(cls) -> list[str]:
        """Validate all registered nodes."""
        errors = []
        for node_id, node_class in cls._nodes.items():
            node = node_class()
            valid, error = node.validate()
            if not valid:
                errors.append(f"Node {node_id}: {error}")
        return errors
```

---

### Phase 1: Tier 0 Control Nodes + Authority Capabilities (Week 2)

**Goal:** Build the safety infrastructure that everything else depends on.

#### 1.1 Authority Capabilities (1-20)

```
app/capabilities/authority/
├── __init__.py
├── cap_001_boundary_enforcement.py
├── cap_002_human_gate.py
├── cap_003_execution_mode.py
├── cap_004_scope_containment.py
├── cap_005_intent_validation.py
├── cap_006_issuer_verification.py
├── cap_007_context_class.py
├── cap_008_privilege_escalation.py
├── cap_009_ring_validation.py
├── cap_010_autonomy_rejection.py
├── cap_011_veto_handling.py
├── cap_012_doctrine_blocking.py
├── cap_013_approval_capture.py
├── cap_014_state_locking.py
├── cap_015_execution_prevention.py
├── cap_016_policy_version.py
├── cap_017_service_isolation.py
├── cap_018_provenance_recording.py
├── cap_019_override_logging.py
└── cap_020_revocation_handling.py
```

**Example implementation:**

```python
# app/capabilities/authority/cap_001_boundary_enforcement.py
from ..base import Capability, CapabilityCategory, CapabilityContext, CapabilityResult
from ..registry import CapabilityRegistry
import hashlib
import json
from datetime import datetime, timezone

@CapabilityRegistry.register
class AuthorityBoundaryEnforcement(Capability):
    """
    Capability 1: Authority boundary enforcement
    
    Verifies that the requested operation falls within the granted
    authority boundaries. Checks scope, resources, and actions.
    """
    
    capability_id = 1
    capability_name = "Authority boundary enforcement"
    category = CapabilityCategory.AUTHORITY
    requires_authority_ring = 2  # Any ring can invoke, but checks will vary
    requires_governed_context = False  # Runs in both contexts
    produces_evidence = True
    dependencies = []
    
    async def execute(
        self,
        context: CapabilityContext,
        requested_scope: dict,
        granted_scope: dict,
        **kwargs
    ) -> CapabilityResult:
        """
        Check if requested_scope falls within granted_scope.
        
        Args:
            context: Execution context
            requested_scope: What the operation wants to do
            granted_scope: What the authority token allows
        
        Returns:
            CapabilityResult with success=True if within bounds
        """
        start_time = datetime.now(timezone.utc)
        violations = []
        
        # Check resource boundaries
        requested_resources = set(requested_scope.get("resources", []))
        granted_resources = set(granted_scope.get("resources", []))
        resource_violations = requested_resources - granted_resources
        if resource_violations:
            violations.append({
                "type": "resource_boundary",
                "requested": list(resource_violations),
                "message": f"Resources not in granted scope: {resource_violations}"
            })
        
        # Check action boundaries
        requested_actions = set(requested_scope.get("actions", []))
        granted_actions = set(granted_scope.get("actions", []))
        action_violations = requested_actions - granted_actions
        if action_violations:
            violations.append({
                "type": "action_boundary",
                "requested": list(action_violations),
                "message": f"Actions not in granted scope: {action_violations}"
            })
        
        # Check path boundaries (if applicable)
        requested_paths = requested_scope.get("paths", [])
        granted_paths = granted_scope.get("paths", [])
        if granted_paths:  # Only check if paths are restricted
            path_violations = self._check_path_boundaries(requested_paths, granted_paths)
            violations.extend(path_violations)
        
        # Build evidence
        evidence = {
            "capability_id": self.capability_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": context.correlation_id,
            "authority_ring": context.authority_ring,
            "context_class": context.context_class,
            "requested_scope": requested_scope,
            "granted_scope": granted_scope,
            "violations": violations,
            "decision": "ALLOW" if not violations else "DENY"
        }
        
        evidence_hash = hashlib.sha256(
            json.dumps(evidence, sort_keys=True).encode()
        ).hexdigest()
        
        end_time = datetime.now(timezone.utc)
        execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return CapabilityResult(
            capability_id=self.capability_id,
            success=len(violations) == 0,
            evidence=evidence,
            evidence_hash=evidence_hash,
            error_code="BOUNDARY_VIOLATION" if violations else None,
            error_message=violations[0]["message"] if violations else None,
            execution_time_ms=execution_time_ms,
        )
    
    def _check_path_boundaries(
        self, 
        requested: list[str], 
        granted: list[str]
    ) -> list[dict]:
        """Check if requested paths are within granted path boundaries."""
        violations = []
        for req_path in requested:
            if not any(self._path_within(req_path, g) for g in granted):
                violations.append({
                    "type": "path_boundary",
                    "requested": req_path,
                    "message": f"Path not in granted scope: {req_path}"
                })
        return violations
    
    def _path_within(self, path: str, boundary: str) -> bool:
        """Check if path is within boundary (supports wildcards)."""
        if boundary.endswith("/**"):
            return path.startswith(boundary[:-3])
        if boundary.endswith("/*"):
            import os
            return os.path.dirname(path) == boundary[:-2]
        return path == boundary
```

#### 1.2 Tier 0 Control Nodes

```
app/nodes/tiers/tier0_control.py
```

```python
# app/nodes/tiers/tier0_control.py
from ..base import Node, NodeTier, NodeContext, NodeResult, NodeState
from ..registry import NodeRegistry
from datetime import datetime, timezone

@NodeRegistry.register
class AuthorityGateNode(Node):
    """
    Tier 0: Authority Gate Node
    
    Verifies SMITH-issued authority before any execution.
    Blocks if context_class = GOVERNED without valid signature.
    """
    
    node_id = "authority_gate"
    node_name = "Authority Gate"
    tier = NodeTier.CONTROL
    allowed_capabilities = [1, 5, 6, 9, 15]  # Boundary, intent, issuer, ring, prevention
    allowed_context_classes = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first = False
    max_execution_time_seconds = 10
    
    async def execute(
        self,
        context: NodeContext,
        requested_scope: dict,
        granted_scope: dict,
        **kwargs
    ) -> NodeResult:
        """Validate authority before allowing execution to proceed."""
        self.state = NodeState.EXECUTING
        start_time = datetime.now(timezone.utc)
        capability_results = []
        
        # In GOVERNED context, require authority token
        if context.context_class == "GOVERNED":
            if not context.authority_token:
                self.state = NodeState.FAILED
                return NodeResult(
                    node_id=self.node_id,
                    state=self.state,
                    error="GOVERNED context requires authority token",
                )
            
            # Verify issuer (Capability 6)
            issuer_result = await self.invoke_capability(
                6, context, authority_token=context.authority_token
            )
            capability_results.append(issuer_result)
            if not issuer_result.success:
                self.state = NodeState.FAILED
                return NodeResult(
                    node_id=self.node_id,
                    state=self.state,
                    capability_results=capability_results,
                    error="Issuer verification failed",
                )
        
        # Check authority boundaries (Capability 1)
        boundary_result = await self.invoke_capability(
            1, context, 
            requested_scope=requested_scope,
            granted_scope=granted_scope
        )
        capability_results.append(boundary_result)
        
        if not boundary_result.success:
            self.state = NodeState.FAILED
            return NodeResult(
                node_id=self.node_id,
                state=self.state,
                capability_results=capability_results,
                error="Authority boundary violation",
            )
        
        # Validate ring (Capability 9)
        ring_result = await self.invoke_capability(
            9, context, required_ring=kwargs.get("required_ring", 2)
        )
        capability_results.append(ring_result)
        
        if not ring_result.success:
            self.state = NodeState.FAILED
            return NodeResult(
                node_id=self.node_id,
                state=self.state,
                capability_results=capability_results,
                error="Authority ring insufficient",
            )
        
        self.state = NodeState.COMPLETED
        end_time = datetime.now(timezone.utc)
        
        return NodeResult(
            node_id=self.node_id,
            state=self.state,
            capability_results=capability_results,
            evidence_hashes=[r.evidence_hash for r in capability_results if r.evidence_hash],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )


@NodeRegistry.register
class ScopeFenceNode(Node):
    """
    Tier 0: Scope Fence Node
    
    Enforces allow/deny lists for files, dirs, commands, APIs.
    """
    
    node_id = "scope_fence"
    node_name = "Scope Fence"
    tier = NodeTier.CONTROL
    allowed_capabilities = [4, 8, 17]  # Scope containment, privilege escalation, service isolation
    allowed_context_classes = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first = False
    max_execution_time_seconds = 10
    
    async def execute(
        self,
        context: NodeContext,
        requested_resources: list[str],
        allow_list: list[str] | None = None,
        deny_list: list[str] | None = None,
        **kwargs
    ) -> NodeResult:
        """Enforce scope boundaries."""
        self.state = NodeState.EXECUTING
        start_time = datetime.now(timezone.utc)
        capability_results = []
        
        # Check scope containment (Capability 4)
        scope_result = await self.invoke_capability(
            4, context,
            requested_resources=requested_resources,
            allow_list=allow_list or [],
            deny_list=deny_list or [],
        )
        capability_results.append(scope_result)
        
        if not scope_result.success:
            self.state = NodeState.FAILED
            return NodeResult(
                node_id=self.node_id,
                state=self.state,
                capability_results=capability_results,
                error="Scope fence violation",
            )
        
        self.state = NodeState.COMPLETED
        end_time = datetime.now(timezone.utc)
        
        return NodeResult(
            node_id=self.node_id,
            state=self.state,
            capability_results=capability_results,
            evidence_hashes=[r.evidence_hash for r in capability_results if r.evidence_hash],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )


@NodeRegistry.register 
class DryRunNode(Node):
    """
    Tier 0: Dry-Run Node
    
    Simulates execution without mutation.
    Mandatory for risky operations.
    """
    
    node_id = "dry_run"
    node_name = "Dry-Run Simulation"
    tier = NodeTier.CONTROL
    allowed_capabilities = [80, 50, 54]  # Dry-run validation, trace generation, drift detection
    allowed_context_classes = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first = False  # This IS the dry-run
    max_execution_time_seconds = 60
    
    async def execute(
        self,
        context: NodeContext,
        target_node_id: str,
        target_kwargs: dict,
        **kwargs
    ) -> NodeResult:
        """Simulate execution of another node."""
        self.state = NodeState.EXECUTING
        start_time = datetime.now(timezone.utc)
        capability_results = []
        
        # Force dry_run in context
        dry_context = NodeContext(
            **context.model_dump(),
            dry_run=True
        )
        
        # Get target node and execute in dry-run mode
        from ..registry import NodeRegistry
        target_node_class = NodeRegistry.get(target_node_id)
        target_node = target_node_class()
        
        # Execute with dry_run=True
        target_result = await target_node.execute(dry_context, **target_kwargs)
        
        # Validate dry-run (Capability 80)
        validation_result = await self.invoke_capability(
            80, context,
            target_result=target_result.model_dump(),
        )
        capability_results.append(validation_result)
        
        self.state = NodeState.COMPLETED
        end_time = datetime.now(timezone.utc)
        
        return NodeResult(
            node_id=self.node_id,
            state=self.state,
            capability_results=capability_results,
            evidence_hashes=[r.evidence_hash for r in capability_results if r.evidence_hash],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )


@NodeRegistry.register
class FailClosedSentinel(Node):
    """
    Tier 0: Fail-Closed Sentinel
    
    Halts execution on ambiguity, timeout, or missing data.
    """
    
    node_id = "fail_closed_sentinel"
    node_name = "Fail-Closed Sentinel"
    tier = NodeTier.CONTROL
    allowed_capabilities = [44, 10, 11]  # Fail-closed logic, autonomy rejection, veto handling
    allowed_context_classes = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first = False
    max_execution_time_seconds = 5
    
    async def execute(
        self,
        context: NodeContext,
        check_type: str,  # "ambiguity" | "timeout" | "missing_data"
        check_data: dict,
        **kwargs
    ) -> NodeResult:
        """Check for conditions that require fail-closed behavior."""
        self.state = NodeState.EXECUTING
        start_time = datetime.now(timezone.utc)
        capability_results = []
        
        # Fail-closed logic (Capability 44)
        failsafe_result = await self.invoke_capability(
            44, context,
            check_type=check_type,
            check_data=check_data,
        )
        capability_results.append(failsafe_result)
        
        if not failsafe_result.success:
            self.state = NodeState.ABORTED
            return NodeResult(
                node_id=self.node_id,
                state=self.state,
                capability_results=capability_results,
                error=f"Fail-closed triggered: {check_type}",
            )
        
        self.state = NodeState.COMPLETED
        end_time = datetime.now(timezone.utc)
        
        return NodeResult(
            node_id=self.node_id,
            state=self.state,
            capability_results=capability_results,
            evidence_hashes=[r.evidence_hash for r in capability_results if r.evidence_hash],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )


@NodeRegistry.register
class EvidenceEmitterNode(Node):
    """
    Tier 0: Evidence Emitter Node
    
    Emits execution traces + artifacts for DataForge.
    Every execution path must pass through this node.
    """
    
    node_id = "evidence_emitter"
    node_name = "Evidence Emitter"
    tier = NodeTier.CONTROL
    allowed_capabilities = [56, 57, 59, 60, 68]  # Bundle gen, sufficiency, hash, canonical, storage
    allowed_context_classes = ["GOVERNED", "UNGOVERNED"]
    requires_dry_run_first = False
    max_execution_time_seconds = 30
    
    async def execute(
        self,
        context: NodeContext,
        execution_results: list[NodeResult],
        **kwargs
    ) -> NodeResult:
        """Emit evidence bundle for completed execution."""
        self.state = NodeState.EXECUTING
        start_time = datetime.now(timezone.utc)
        capability_results = []
        
        # Generate evidence bundle (Capability 56)
        bundle_result = await self.invoke_capability(
            56, context,
            execution_results=[r.model_dump() for r in execution_results],
        )
        capability_results.append(bundle_result)
        
        if not bundle_result.success:
            self.state = NodeState.FAILED
            return NodeResult(
                node_id=self.node_id,
                state=self.state,
                capability_results=capability_results,
                error="Evidence bundle generation failed",
            )
        
        # Check evidence sufficiency (Capability 57)
        sufficiency_result = await self.invoke_capability(
            57, context,
            evidence=bundle_result.evidence,
        )
        capability_results.append(sufficiency_result)
        
        # Store to DataForge (Capability 68)
        storage_result = await self.invoke_capability(
            68, context,
            evidence=bundle_result.evidence,
            evidence_hash=bundle_result.evidence_hash,
        )
        capability_results.append(storage_result)
        
        self.state = NodeState.COMPLETED
        end_time = datetime.now(timezone.utc)
        
        return NodeResult(
            node_id=self.node_id,
            state=self.state,
            capability_results=capability_results,
            evidence_hashes=[bundle_result.evidence_hash],
            execution_time_ms=int((end_time - start_time).total_seconds() * 1000),
        )
```

---

### Phase 2: Evidence & Planning Capabilities (Week 3)

**Goal:** Build capabilities 21-35 (Planning) and 56-75 (Evidence).

#### Directory Structure

```
app/capabilities/
├── planning/
│   ├── __init__.py
│   ├── cap_021_plan_parsing.py
│   ├── cap_022_goal_extraction.py
│   ├── ... (through cap_035)
│
├── evidence/
│   ├── __init__.py
│   ├── cap_056_bundle_generation.py
│   ├── cap_057_sufficiency_validation.py
│   ├── ... (through cap_075)
```

---

### Phase 3: Execution Capabilities + Tier 1-2 Nodes (Week 4)

**Goal:** Build capabilities 36-55 (ETCOS Execution) and Tier 1-2 nodes.

#### Capability → Node Mapping for Tiers 1-2

| Node | Capabilities Used |
|------|-------------------|
| Repo Scanner | 96, 97, 98, 106 |
| AST Analysis | 50, 106, 110 |
| Dependency Graph | 50, 106 |
| Impact Analysis | 32, 50 |
| Diff Generator | 50, 59, 60 |
| TypeScript Specialist | 36, 50, 51, 106 |
| Rust Specialist | 36, 50, 51, 106 |
| Python Specialist | 36, 50, 51, 106 |
| Shell/Bash Node | 36, 50, 51, 44, 106 |
| Config & Infra Node | 36, 50, 51, 106 |
| Frontend Framework Node | 36, 50, 51, 106 |
| CSS/Styling Node | 36, 50, 51, 106 |
| Test Authoring Node | 36, 50, 51, 79, 106 |

---

### Phase 4: BuildGuard & Verification (Week 5)

**Goal:** Build capabilities 76-95 and Tier 3 nodes.

---

### Phase 5: Repository, Observability & Integration (Week 6)

**Goal:** Build capabilities 96-120 and Tier 4-6 nodes.

---

## Node → Capability Complete Mapping

| Node ID | Tier | Capabilities |
|---------|------|--------------|
| `authority_gate` | 0 | 1, 5, 6, 9, 15 |
| `scope_fence` | 0 | 4, 8, 17 |
| `dry_run` | 0 | 50, 54, 80 |
| `fail_closed_sentinel` | 0 | 10, 11, 44 |
| `evidence_emitter` | 0 | 56, 57, 59, 60, 68 |
| `repo_scanner` | 1 | 96, 97, 98, 106 |
| `ast_analysis` | 1 | 50, 106, 110 |
| `dependency_graph` | 1 | 50, 106 |
| `impact_analysis` | 1 | 32, 50 |
| `diff_generator` | 1 | 50, 59, 60 |
| `typescript_specialist` | 2 | 36, 50, 51, 106 |
| `rust_specialist` | 2 | 36, 50, 51, 106 |
| `python_specialist` | 2 | 36, 50, 51, 106 |
| `shell_bash` | 2 | 36, 44, 50, 51, 106 |
| `config_infra` | 2 | 36, 50, 51, 106 |
| `frontend_framework` | 2 | 36, 50, 51, 106 |
| `css_styling` | 2 | 36, 50, 51, 106 |
| `test_authoring` | 2 | 36, 50, 51, 79, 106 |
| `build_executor` | 3 | 50, 51, 52, 53, 106 |
| `test_runner` | 3 | 50, 51, 79, 106 |
| `static_analysis` | 3 | 50, 76, 77, 106 |
| `security_scan` | 3 | 50, 76, 77, 106 |
| `performance_probe` | 3 | 50, 51, 52, 106 |
| `plan_decomposer` | 4 | 21, 22, 23, 24, 25, 26 |
| `risk_assessor` | 4 | 32, 89, 90 |
| `alternative_strategy` | 4 | 27, 31, 35 |
| `estimate` | 4 | 32, 49 |
| `dataforge_client` | 5 | 68, 115, 120 |
| `rake_trigger` | 5 | 106, 110 |
| `neuroforge_call` | 5 | 36, 37, 38, 51, 52, 53 |
| `forgecommand_sync` | 5 | 106, 107, 110, 113 |
| `verification_summary` | 6 | 91, 92, 95 |
| `rollback_prep` | 6 | 46, 47, 105 |
| `release_artifact` | 6 | 56, 59, 60, 75 |
| `postmortem_draft` | 6 | 95, 119, 120 |

---

## Testing Strategy

### Per-Capability Tests

```python
# tests/capabilities/test_cap_001.py
import pytest
from app.capabilities.authority.cap_001_boundary_enforcement import AuthorityBoundaryEnforcement
from app.capabilities.base import CapabilityContext

@pytest.fixture
def capability():
    return AuthorityBoundaryEnforcement()

@pytest.fixture
def context():
    return CapabilityContext(
        correlation_id="test-123",
        authority_ring=1,
        context_class="GOVERNED",
    )

@pytest.mark.asyncio
async def test_boundary_allows_valid_scope(capability, context):
    """Test that valid scope passes boundary check."""
    result = await capability.execute(
        context,
        requested_scope={"resources": ["file_a"], "actions": ["read"]},
        granted_scope={"resources": ["file_a", "file_b"], "actions": ["read", "write"]},
    )
    assert result.success is True
    assert result.evidence is not None
    assert result.evidence["decision"] == "ALLOW"

@pytest.mark.asyncio
async def test_boundary_blocks_invalid_scope(capability, context):
    """Test that invalid scope is blocked."""
    result = await capability.execute(
        context,
        requested_scope={"resources": ["file_c"], "actions": ["delete"]},
        granted_scope={"resources": ["file_a"], "actions": ["read"]},
    )
    assert result.success is False
    assert result.error_code == "BOUNDARY_VIOLATION"
    assert result.evidence["decision"] == "DENY"
```

### Per-Node Tests

```python
# tests/nodes/test_authority_gate.py
import pytest
from app.nodes.tiers.tier0_control import AuthorityGateNode
from app.nodes.base import NodeContext, NodeState

@pytest.fixture
def node():
    node = AuthorityGateNode()
    node.validate()
    return node

@pytest.mark.asyncio
async def test_governed_requires_token(node):
    """Test that GOVERNED context requires authority token."""
    context = NodeContext(
        correlation_id="test-123",
        context_class="GOVERNED",
        authority_token=None,  # Missing!
    )
    result = await node.execute(
        context,
        requested_scope={},
        granted_scope={},
    )
    assert result.state == NodeState.FAILED
    assert "authority token" in result.error.lower()
```

---

## API Endpoints

Add these endpoints to `app/api.py`:

```python
# Capability endpoints
@router.get("/v1/capabilities")
async def list_capabilities():
    """List all registered capabilities."""
    
@router.get("/v1/capabilities/{capability_id}")
async def get_capability(capability_id: int):
    """Get capability details."""

@router.post("/v1/capabilities/{capability_id}/execute")
async def execute_capability(capability_id: int, request: CapabilityExecuteRequest):
    """Execute a single capability (for testing/debugging)."""

# Node endpoints
@router.get("/v1/nodes")
async def list_nodes():
    """List all registered nodes."""

@router.get("/v1/nodes/{node_id}")
async def get_node(node_id: str):
    """Get node details."""

@router.post("/v1/nodes/{node_id}/execute")
async def execute_node(node_id: str, request: NodeExecuteRequest):
    """Execute a node."""

# Pipeline endpoints (called by SMITH)
@router.post("/v1/pipeline/execute")
async def execute_pipeline(request: PipelineExecuteRequest):
    """Execute a full pipeline of nodes."""
```

---

## Summary

| Week | Focus | Capabilities | Nodes | Tests |
|------|-------|--------------|-------|-------|
| 1 | Foundation | Framework only | Framework only | 20 |
| 2 | Authority + Tier 0 | 1-20 | 5 Tier 0 nodes | 50 |
| 3 | Planning + Evidence | 21-35, 56-75 | — | 70 |
| 4 | Execution + Tier 1-2 | 36-55 | 13 Tier 1-2 nodes | 80 |
| 5 | BuildGuard + Tier 3 | 76-95 | 5 Tier 3 nodes | 60 |
| 6 | Repo/Observability + Tier 4-6 | 96-120 | 9 Tier 4-6 nodes | 50 |

**Total:** 120 capabilities, 32 nodes, ~330 tests

---

## Next Steps for Claude Code

1. Start with `app/capabilities/base.py` and `app/capabilities/registry.py`
2. Build `app/nodes/base.py` and `app/nodes/registry.py`
3. Implement Capability 1 as the template
4. Implement Authority Gate Node as the template
5. Proceed through phases

**Do not proceed to Phase 2 without completing and testing Phase 1.**
