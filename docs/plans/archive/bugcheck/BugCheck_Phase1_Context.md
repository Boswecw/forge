# BugCheck Phase 1 — Context Packet for VS Code Claude

**Document Version:** 1.0  
**Created:** December 28, 2025  
**Owner:** Charles Tytler, Boswell Digital Solutions LLC  
**Purpose:** Context for implementing BugCheck Phase 1 (MVP Foundation)  
**Phase Duration:** 2 weeks (80 hours)

---

## Current State

### Completed Prerequisites

**FPVS Track 2A0: BugCheck Phase 0** ✅
- 7 JSON schemas in `schemas/bugcheck/v1/`:
  - `service_manifest_schema.json`
  - `bugcheck_run_schema.json`
  - `finding_schema.json`
  - `enrichment_schema.json`
  - `lifecycle_event_schema.json`
  - `run_token_schema.json`
  - `user_token_schema.json`
- Validator harness: `scripts/validate_schemas.py`
- Valid/invalid fixture samples
- CI workflow: `.github/workflows/schemas.yml`

**Infrastructure Ready:**
- DataForge v5.2: 296 tests, vector storage operational
- NeuroForge: LLM orchestration, 100+ tests, 89% coverage
- ForgeAgents: Agent orchestration, 120-skill library
- Rake v1.0: Document ingestion, 77 tests

### What Exists (Do Not Rebuild)

**From ForgeAgents** (reference implementation):
- Agent lifecycle manager (5-phase execution)
- Tool router with automatic registration
- Policy engine (11 policies)
- Memory manager with DataForge integration

**From FPVS** (reference patterns):
- Evidence bundle creation
- Tamper-evident verification
- State machine enforcement
- Schema validation

---

## Phase 1 Scope: MVP Foundation

### Mission Statement

Build the **core detection engine** that executes checks across Forge services, generates findings, and persists to DataForge. This establishes the foundation for all future phases.

### What You Will Build

1. **Stack Detection Module** - Auto-detect language/framework
2. **Check Registry** - Standard interface for all checks
3. **Basic Checks** - Typecheck, lint, unit tests, security scans
4. **DataForge Integration** - Persist runs and findings
5. **CLI Interface** - Command-line execution

### What You Will NOT Build (Future Phases)

- ❌ ForgeCommand orchestration (Phase 2)
- ❌ Cross-service checks (Phase 2)
- ❌ VibeForge UI (Phase 3)
- ❌ MAID fix generation (Phase 4)
- ❌ XAI enrichment (Phase 5)
- ❌ Deep/fuzz modes (Phase 6)

---

## Canonical Rule

**DataForge is the authoritative source of truth** for all Forge ecosystem state, history, and intelligence artifacts. No other service owns durable truth.

**BugCheck Responsibility:**
- ✅ Execute checks
- ✅ Generate raw findings
- ✅ Write to DataForge
- ❌ Never persist locally (except transient run state)
- ❌ Never make lifecycle decisions (DataForge owns state machine)
- ❌ Never orchestrate multi-service runs (ForgeCommand owns that)

---

## Architecture Specifications

### Component Hierarchy

```
bugcheck/
├── app/
│   ├── detection/
│   │   └── stack_detector.py      # Language/framework detection
│   ├── checks/
│   │   ├── registry.py             # Check interface and registration
│   │   ├── base.py                 # BaseCheck abstract class
│   │   ├── python/
│   │   │   ├── typecheck.py        # mypy integration
│   │   │   ├── lint.py             # ruff/pylint
│   │   │   └── unit_tests.py       # pytest execution
│   │   ├── javascript/
│   │   │   ├── typecheck.py        # tsc integration
│   │   │   └── lint.py             # eslint
│   │   └── security/
│   │       ├── gitleaks.py         # Secret scanning
│   │       └── dependencies.py     # npm audit, pip-audit
│   ├── dataforge_client.py         # DataForge API client
│   ├── models.py                   # Pydantic models for Run, Finding
│   ├── cli.py                      # Click CLI interface
│   └── config.py                   # Configuration management
├── tests/
│   ├── test_stack_detector.py
│   ├── test_checks/
│   └── test_dataforge_client.py
├── pyproject.toml
└── README.md
```

### Stack Detection Strategy

**Purpose:** Auto-detect language, framework, and tooling from repository contents

**Detection Criteria:**

**Python:**
```python
PYTHON_INDICATORS = {
    "files": ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile"],
    "extensions": [".py"],
    "patterns": {
        "test_framework": ["pytest", "unittest", "nose"],
        "type_checker": ["mypy", "pyright", "pyre"],
        "linter": ["ruff", "pylint", "flake8"],
    }
}
```

**JavaScript/TypeScript:**
```python
JS_INDICATORS = {
    "files": ["package.json", "tsconfig.json", ".eslintrc"],
    "extensions": [".js", ".ts", ".jsx", ".tsx"],
    "patterns": {
        "test_framework": ["jest", "mocha", "vitest"],
        "type_checker": ["typescript"],
        "linter": ["eslint", "prettier"],
    }
}
```

**Rust:**
```python
RUST_INDICATORS = {
    "files": ["Cargo.toml"],
    "extensions": [".rs"],
    "patterns": {
        "test_framework": ["cargo test"],
        "linter": ["clippy"],
    }
}
```

**Detection Algorithm:**
```python
def detect_stack(repo_path: Path) -> StackInfo:
    """
    Detect language stack from repository structure.
    
    Returns:
        StackInfo with language, frameworks, tools detected
    """
    detected = StackInfo()
    
    # Check for Python
    if any((repo_path / f).exists() for f in PYTHON_INDICATORS["files"]):
        detected.add_language("python")
        detected.add_tools(detect_python_tools(repo_path))
    
    # Check for JavaScript/TypeScript
    if (repo_path / "package.json").exists():
        package_json = json.loads((repo_path / "package.json").read_text())
        detected.add_language("javascript")
        if "typescript" in package_json.get("devDependencies", {}):
            detected.add_language("typescript")
        detected.add_tools(detect_js_tools(repo_path))
    
    # Check for Rust
    if (repo_path / "Cargo.toml").exists():
        detected.add_language("rust")
        detected.add_tools(detect_rust_tools(repo_path))
    
    return detected
```

---

## Check Registry Design

### BaseCheck Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel

class CheckResult(BaseModel):
    """Result from a single check execution"""
    check_name: str
    passed: bool
    findings: List['Finding']
    duration_seconds: float
    metadata: dict = {}

class BaseCheck(ABC):
    """Abstract base class for all checks"""
    
    name: str
    category: str  # "typecheck", "lint", "security", "test"
    priority: int  # 1 (highest) to 10 (lowest)
    timeout_seconds: int = 300
    
    @abstractmethod
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """
        Execute the check against repository.
        
        Args:
            repo_path: Path to repository root
            context: Execution context (stack info, config, etc.)
        
        Returns:
            CheckResult with findings
        """
        pass
    
    @abstractmethod
    def is_applicable(self, stack: StackInfo) -> bool:
        """
        Determine if this check applies to the detected stack.
        
        Args:
            stack: Detected stack information
        
        Returns:
            True if check should run
        """
        pass
```

### Check Registry

```python
class CheckRegistry:
    """Registry for all available checks"""
    
    def __init__(self):
        self._checks: Dict[str, BaseCheck] = {}
    
    def register(self, check: BaseCheck):
        """Register a check"""
        self._checks[check.name] = check
    
    def get_applicable_checks(
        self, 
        stack: StackInfo,
        mode: str = "standard"
    ) -> List[BaseCheck]:
        """
        Get checks applicable for stack and mode.
        
        Args:
            stack: Detected stack
            mode: "quick", "standard", "deep"
        
        Returns:
            List of checks to execute, sorted by priority
        """
        applicable = [
            check for check in self._checks.values()
            if check.is_applicable(stack)
        ]
        
        # Filter by mode
        if mode == "quick":
            applicable = [c for c in applicable if c.priority <= 3]
        elif mode == "standard":
            applicable = [c for c in applicable if c.priority <= 7]
        # "deep" includes all checks
        
        # Sort by priority (1 = highest)
        return sorted(applicable, key=lambda c: c.priority)
```

---

## Finding Model

**Schema Reference:** `schemas/bugcheck/v1/finding_schema.json`

**Pydantic Model:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class Finding(BaseModel):
    """
    Individual issue detected during BugCheck run.
    
    Matches finding.schema.json from Phase 0.
    """
    id: str = Field(description="Unique finding ID")
    fingerprint: str = Field(description="Stable identifier for deduplication")
    
    # Classification
    category: Literal["security", "quality", "performance", "compliance"]
    severity: Literal["S0", "S1", "S2", "S3", "S4"]
    
    # Location
    service: str
    file_path: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    
    # Content
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10)
    rule_id: Optional[str] = None  # e.g., "E501" for pylint
    
    # Metadata
    check_name: str
    tool_name: Optional[str] = None
    tool_version: Optional[str] = None
    
    # Provenance
    run_id: str
    commit_sha: str
    created_at: datetime
    
    # Optional enrichment references
    cve_ids: List[str] = []
    remediation: Optional[str] = None

def generate_fingerprint(finding: Finding) -> str:
    """
    Generate stable fingerprint for finding.
    
    Fingerprint allows deduplication across runs and historical trending.
    """
    components = [
        finding.category,
        finding.check_name,
        finding.file_path,
        str(finding.line_number or 0),
        finding.rule_id or "",
    ]
    
    fingerprint_string = ":".join(components)
    return hashlib.sha256(fingerprint_string.encode()).hexdigest()[:16]
```

---

## DataForge Integration

### Client Interface

```python
import httpx
from typing import List, Optional

class DataForgeClient:
    """Client for DataForge API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def create_run(self, run: BugCheckRun) -> str:
        """
        Create a new BugCheck run record.
        
        Returns:
            run_id
        """
        response = await self.client.post(
            "/api/bugcheck/runs",
            json=run.model_dump()
        )
        response.raise_for_status()
        return response.json()["run_id"]
    
    async def write_findings(self, findings: List[Finding]):
        """Write findings to DataForge"""
        response = await self.client.post(
            "/api/bugcheck/findings",
            json=[f.model_dump() for f in findings]
        )
        response.raise_for_status()
    
    async def update_run_status(
        self, 
        run_id: str, 
        status: str,
        summary: dict
    ):
        """Update run status and summary"""
        response = await self.client.patch(
            f"/api/bugcheck/runs/{run_id}",
            json={"status": status, "summary": summary}
        )
        response.raise_for_status()
    
    async def get_historical_findings(
        self,
        fingerprint: str,
        limit: int = 10
    ) -> List[Finding]:
        """Query historical findings by fingerprint"""
        response = await self.client.get(
            "/api/bugcheck/findings",
            params={"fingerprint": fingerprint, "limit": limit}
        )
        response.raise_for_status()
        return [Finding(**f) for f in response.json()]
```

---

## CLI Interface Specifications

### Command Structure

```bash
# Quick mode (fast checks only, < 60s)
forge bugcheck --quick

# Standard mode (default, < 10min)
forge bugcheck --standard

# Deep mode (comprehensive, < 30min) - Future phase
forge bugcheck --deep

# Single service
forge bugcheck --service neuroforge

# Multiple services
forge bugcheck --service neuroforge --service dataforge

# Specific categories
forge bugcheck --category security

# Output formats
forge bugcheck --format json
forge bugcheck --format table
forge bugcheck --format github  # GitHub Actions annotations
```

### CLI Implementation

```python
import click
from pathlib import Path

@click.group()
def cli():
    """BugCheck: Ecosystem-wide quality enforcement"""
    pass

@cli.command()
@click.option(
    "--mode",
    type=click.Choice(["quick", "standard", "deep"]),
    default="standard",
    help="Execution mode"
)
@click.option(
    "--service",
    multiple=True,
    help="Specific service(s) to check"
)
@click.option(
    "--category",
    multiple=True,
    type=click.Choice(["security", "quality", "performance"]),
    help="Specific check categories"
)
@click.option(
    "--format",
    type=click.Choice(["table", "json", "github"]),
    default="table",
    help="Output format"
)
async def run(mode, service, category, format):
    """Execute BugCheck run"""
    
    # Detect repository
    repo_path = Path.cwd()
    
    # Detect stack
    stack = await detect_stack(repo_path)
    click.echo(f"Detected stack: {stack}")
    
    # Get applicable checks
    registry = get_registry()
    checks = registry.get_applicable_checks(stack, mode)
    
    if category:
        checks = [c for c in checks if c.category in category]
    
    click.echo(f"Running {len(checks)} checks...")
    
    # Create run record in DataForge
    dataforge = get_dataforge_client()
    run_id = await dataforge.create_run(...)
    
    # Execute checks
    findings = []
    for check in checks:
        result = await check.execute(repo_path, {"stack": stack})
        findings.extend(result.findings)
        
        # Progress indicator
        status = "✅" if result.passed else "❌"
        click.echo(f"{status} {check.name} ({result.duration_seconds:.1f}s)")
    
    # Write findings to DataForge
    await dataforge.write_findings(findings)
    
    # Output results
    if format == "table":
        display_table(findings)
    elif format == "json":
        click.echo(json.dumps([f.model_dump() for f in findings], indent=2))
    elif format == "github":
        display_github_annotations(findings)
```

---

## Example Check Implementations

### Python Type Check

```python
class PythonTypeCheck(BaseCheck):
    name = "python-typecheck"
    category = "quality"
    priority = 2
    
    def is_applicable(self, stack: StackInfo) -> bool:
        return "python" in stack.languages and "mypy" in stack.tools
    
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """Run mypy type checking"""
        start = time.time()
        
        # Execute mypy
        result = subprocess.run(
            ["mypy", ".", "--output-format=json"],
            cwd=repo_path,
            capture_output=True,
            timeout=self.timeout_seconds
        )
        
        # Parse mypy output
        findings = []
        if result.returncode != 0:
            mypy_output = json.loads(result.stdout)
            for error in mypy_output:
                findings.append(Finding(
                    id=generate_finding_id(),
                    fingerprint=generate_fingerprint(...),
                    category="quality",
                    severity=map_mypy_severity(error),
                    service=context.get("service", "unknown"),
                    file_path=error["file"],
                    line_number=error["line"],
                    title=f"Type error: {error['message'][:50]}",
                    description=error["message"],
                    rule_id=error.get("error_code"),
                    check_name=self.name,
                    tool_name="mypy",
                    tool_version=get_mypy_version(),
                    run_id=context["run_id"],
                    commit_sha=context["commit_sha"],
                    created_at=datetime.now(timezone.utc)
                ))
        
        duration = time.time() - start
        
        return CheckResult(
            check_name=self.name,
            passed=len(findings) == 0,
            findings=findings,
            duration_seconds=duration
        )
```

### Security - Gitleaks

```python
class GitleaksCheck(BaseCheck):
    name = "security-gitleaks"
    category = "security"
    priority = 1  # Highest priority
    
    def is_applicable(self, stack: StackInfo) -> bool:
        return True  # Applies to all repos
    
    async def execute(self, repo_path: Path, context: dict) -> CheckResult:
        """Scan for secrets with gitleaks"""
        start = time.time()
        
        # Execute gitleaks
        result = subprocess.run(
            ["gitleaks", "detect", "--report-format=json", "-v"],
            cwd=repo_path,
            capture_output=True,
            timeout=self.timeout_seconds
        )
        
        findings = []
        if result.returncode != 0:
            gitleaks_output = json.loads(result.stdout)
            for leak in gitleaks_output:
                findings.append(Finding(
                    id=generate_finding_id(),
                    fingerprint=generate_fingerprint(...),
                    category="security",
                    severity="S0",  # Secrets always critical
                    service=context.get("service", "unknown"),
                    file_path=leak["File"],
                    line_number=leak.get("StartLine"),
                    title=f"Secret detected: {leak['RuleID']}",
                    description=f"Potential {leak['Description']} found. Secret redacted for security.",
                    rule_id=leak["RuleID"],
                    check_name=self.name,
                    tool_name="gitleaks",
                    tool_version=get_gitleaks_version(),
                    run_id=context["run_id"],
                    commit_sha=context["commit_sha"],
                    created_at=datetime.now(timezone.utc),
                    remediation="Remove secret from repository history and rotate credentials immediately."
                ))
        
        duration = time.time() - start
        
        return CheckResult(
            check_name=self.name,
            passed=len(findings) == 0,
            findings=findings,
            duration_seconds=duration
        )
```

---

## Configuration Management

### config.yaml Structure

```yaml
bugcheck:
  dataforge:
    url: "https://dataforge.onrender.com"
    api_key: "${DATAFORGE_API_KEY}"  # Environment variable
  
  checks:
    python:
      typecheck:
        enabled: true
        config_file: "mypy.ini"
      lint:
        enabled: true
        tool: "ruff"  # or "pylint"
    
    javascript:
      typecheck:
        enabled: true
      lint:
        enabled: true
        config_file: ".eslintrc.json"
    
    security:
      gitleaks:
        enabled: true
      dependencies:
        enabled: true
        python_tool: "pip-audit"
        javascript_tool: "npm audit"
  
  modes:
    quick:
      max_duration_seconds: 60
      max_checks: 5
    standard:
      max_duration_seconds: 600
      max_checks: 20
    deep:
      max_duration_seconds: 1800
      max_checks: 50
```

---

## Testing Requirements

### Test Coverage Target

**Minimum:** 80% code coverage

**Critical Paths:**
- Stack detection: 90% coverage
- Check execution: 85% coverage
- DataForge integration: 90% coverage
- Fingerprint generation: 100% coverage

### Test Categories

**Unit Tests:**
```python
# tests/test_stack_detector.py
def test_detect_python_stack():
    """Test Python stack detection"""
    repo = create_temp_repo_with_python()
    stack = detect_stack(repo)
    assert "python" in stack.languages
    assert "mypy" in stack.tools

# tests/test_fingerprint.py
def test_fingerprint_stability():
    """Fingerprints must be stable across runs"""
    finding1 = create_test_finding()
    finding2 = create_test_finding()  # Identical
    
    fp1 = generate_fingerprint(finding1)
    fp2 = generate_fingerprint(finding2)
    
    assert fp1 == fp2

def test_fingerprint_uniqueness():
    """Different findings must have different fingerprints"""
    finding1 = create_test_finding(line=10)
    finding2 = create_test_finding(line=20)
    
    fp1 = generate_fingerprint(finding1)
    fp2 = generate_fingerprint(finding2)
    
    assert fp1 != fp2
```

**Integration Tests:**
```python
# tests/test_dataforge_integration.py
@pytest.mark.asyncio
async def test_write_findings_to_dataforge():
    """Test writing findings to DataForge"""
    client = DataForgeClient(...)
    
    findings = [create_test_finding()]
    await client.write_findings(findings)
    
    # Verify persisted
    retrieved = await client.get_historical_findings(
        findings[0].fingerprint
    )
    assert len(retrieved) == 1
    assert retrieved[0].fingerprint == findings[0].fingerprint
```

---

## Success Criteria

Before Phase 1 is complete:

### Functional Requirements
- ✅ Detects Python, JavaScript, Rust stacks correctly
- ✅ Executes typecheck, lint, unit tests
- ✅ Finds secrets with gitleaks
- ✅ Scans dependencies for vulnerabilities
- ✅ Generates stable fingerprints
- ✅ Writes runs and findings to DataForge
- ✅ CLI accepts all specified flags
- ✅ Quick mode completes in < 60 seconds
- ✅ Standard mode completes in < 10 minutes

### Quality Requirements
- ✅ 80% test coverage overall
- ✅ 90% coverage on critical paths
- ✅ < 5% false positive rate
- ✅ All tests pass in CI

### Documentation
- ✅ README with usage examples
- ✅ Architecture documentation
- ✅ API reference for checks
- ✅ Configuration guide

---

## Common Pitfalls to Avoid

### Implementation Pitfalls

❌ **Persisting state locally**  
✅ All durable state goes to DataForge

❌ **Non-deterministic fingerprints**  
✅ Fingerprints must be stable across runs

❌ **Exposing secrets in findings**  
✅ Redact secret values, only show file/line

❌ **Blocking on external API calls**  
✅ Use async/await, set timeouts

❌ **Hardcoding tool paths**  
✅ Use `shutil.which()` to find tools

### Testing Pitfalls

❌ **Testing only success cases**  
✅ Test failures, timeouts, edge cases

❌ **Mocking DataForge client**  
✅ Use real DataForge test instance

❌ **Skipping integration tests**  
✅ Verify end-to-end flow

---

## Quick Reference

### Key Files to Create
```
app/detection/stack_detector.py
app/checks/registry.py
app/checks/base.py
app/checks/python/typecheck.py
app/checks/python/lint.py
app/checks/security/gitleaks.py
app/dataforge_client.py
app/models.py
app/cli.py
tests/test_stack_detector.py
tests/test_checks/
```

### Performance Targets
- Quick mode: < 60s
- Standard mode: < 10min
- Stack detection: < 1s
- Single check: < 30s average

### DataForge Endpoints
```
POST /api/bugcheck/runs
POST /api/bugcheck/findings
PATCH /api/bugcheck/runs/{run_id}
GET /api/bugcheck/findings?fingerprint={fp}
```

---

**This context packet provides everything needed to implement BugCheck Phase 1 with production-grade quality.**

**Proceed with implementation per BugCheck_Phase1_Prompt.md**
