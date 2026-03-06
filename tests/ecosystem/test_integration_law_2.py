"""
Ecosystem-level guard test for Integration Law 2:
All AI calls route through NeuroForge.

Run from ecosystem root:
    pytest tests/ecosystem/test_integration_law_2.py -v

This test scans all consumer repositories (everything except NeuroForge's
approved provider modules) for direct provider SDK imports. Any import of
openai, anthropic, or google.generativeai outside the approved path is a
violation.

Known technical debt is tracked per-repo. This test ensures no NEW
violations are introduced.
"""

import pathlib

import pytest

ECOSYSTEM_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

PROVIDER_SDKS = {"openai", "anthropic", "google.generativeai", "google.genai"}

# Only NeuroForge adapters/ and services/providers/ are approved for direct SDK use
APPROVED_PATHS = {
    "NeuroForge/neuroforge_backend/adapters",
    "NeuroForge/neuroforge_backend/services/providers",
    "NeuroForge/neuroforge_backend/llm_service.py",
    "NeuroForge/neuroforge_backend/services/embedding_service.py",
    "NeuroForge/neuroforge_backend/services/llm_evaluator.py",
}

# Known technical debt — existing violations tracked for migration.
# This set must shrink over time, never grow.
KNOWN_DEBT = {
    "ForgeAgents/app/llm/openai_simple.py",
    "ForgeAgents/app/llm/anthropic_simple.py",
    "ForgeAgents/app/agents/bugcheck/maid/client.py",
}

# Skip non-source directories
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", ".next"}

# Consumer repos to scan (everything that consumes AI but must route through NeuroForge)
CONSUMER_REPOS = [
    "ForgeAgents",
    "Rake",
    "forge-smithy",
    "Canebrake_press",
    "Forge_Command",
]


def _is_approved(relative: str) -> bool:
    """Check if a file path is in an approved location."""
    for approved in APPROVED_PATHS:
        if relative.startswith(approved) or relative == approved:
            return True
    return False


def _scan_repo(repo_path: pathlib.Path) -> list[str]:
    """Scan a repo for provider SDK imports."""
    violations = []
    if not repo_path.exists():
        return violations

    for py_file in repo_path.rglob("*.py"):
        if any(skip in py_file.parts for skip in SKIP_DIRS):
            continue

        try:
            rel = py_file.relative_to(ECOSYSTEM_ROOT).as_posix()
        except ValueError:
            continue

        if _is_approved(rel) or rel in KNOWN_DEBT:
            continue

        try:
            content = py_file.read_text(errors="ignore")
        except OSError:
            continue

        for sdk in PROVIDER_SDKS:
            if f"import {sdk}" in content or f"from {sdk}" in content:
                violations.append(f"{rel}: references {sdk}")

    return violations


def test_no_new_provider_sdk_in_consumer_repos():
    """Consumer repos must not introduce NEW provider SDK imports."""
    violations = []
    for repo_name in CONSUMER_REPOS:
        repo_path = ECOSYSTEM_ROOT / repo_name
        violations.extend(_scan_repo(repo_path))

    assert violations == [], (
        f"Integration Law 2 violations across ecosystem:\n" + "\n".join(violations)
    )


def test_known_debt_does_not_grow():
    """The known technical debt set must not grow."""
    all_violations = []
    for repo_name in CONSUMER_REPOS:
        repo_path = ECOSYSTEM_ROOT / repo_name
        if not repo_path.exists():
            continue
        # Scan WITHOUT skipping known debt
        for py_file in repo_path.rglob("*.py"):
            if any(skip in py_file.parts for skip in SKIP_DIRS):
                continue
            try:
                rel = py_file.relative_to(ECOSYSTEM_ROOT).as_posix()
            except ValueError:
                continue
            if _is_approved(rel):
                continue
            try:
                content = py_file.read_text(errors="ignore")
            except OSError:
                continue
            for sdk in PROVIDER_SDKS:
                if f"import {sdk}" in content or f"from {sdk}" in content:
                    all_violations.append(rel)

    violating_files = set(all_violations)
    new_debt = violating_files - KNOWN_DEBT
    assert new_debt == set(), (
        f"New Integration Law 2 violations (not in KNOWN_DEBT):\n"
        + "\n".join(sorted(new_debt))
    )


def test_neuroforge_approved_dirs_exist():
    """NeuroForge approved provider directories must exist."""
    adapters = ECOSYSTEM_ROOT / "NeuroForge" / "neuroforge_backend" / "adapters"
    providers = ECOSYSTEM_ROOT / "NeuroForge" / "neuroforge_backend" / "services" / "providers"
    assert adapters.is_dir(), f"Missing: {adapters}"
    assert providers.is_dir(), f"Missing: {providers}"
