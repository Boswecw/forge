#!/usr/bin/env python3
"""Audit nested Git repositories against BDS-REPO-NAMING-v1."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GENERAL_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PREFERRED_RE = re.compile(
    r"^(authorforge|neuronforge|neuroforge|forge-command|dataforge|forgecustomer|bds)(-[a-z0-9]+)+$"
)
GITHUB_RE = re.compile(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?$")

PREFIXES = {
    "authorforge": {
        "plane": "Product Plane",
        "authority": "Customer-facing application authority",
    },
    "neuronforge": {
        "plane": "Local Runtime Plane",
        "authority": "Local AI/runtime authority",
    },
    "neuroforge": {
        "plane": "Cloud Runtime Plane",
        "authority": "Cloud AI/provider authority",
    },
    "forge-command": {
        "plane": "Control Plane",
        "authority": "Governance, registry, audit, orchestration authority",
    },
    "dataforge": {
        "plane": "Data Plane",
        "authority": "Data, memory, persistence authority",
    },
    "forgecustomer": {
        "plane": "Customer Plane",
        "authority": "Customer, billing, entitlement authority",
    },
    "bds": {
        "plane": "Doctrine Plane",
        "authority": "Canonical protocol and doctrine authority",
    },
}

FORBIDDEN_NAMES = {
    "backend",
    "frontend",
    "main-app",
    "test-repo",
    "new-system",
    "ai-agent",
    "control",
    "registry2",
    "final-backend",
}

STATUS_RANK = {
    "compliant": 0,
    "legacy": 1,
    "reserved": 2,
    "deprecated": 3,
    "invalid": 4,
}

PRUNE_DIRS = {
    ".cache",
    ".git",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".svelte-kit",
    ".venv",
    ".venv_verify",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "out",
    "playwright-report",
    "target",
    "test-results",
}


def run_git(repo: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"ERROR: {exc}"
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        return f"ERROR: {message}"
    return completed.stdout.strip()


def normalize_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", name.lower())
    return re.sub(r"-+", "-", normalized).strip("-")


def discover_repos(root: Path) -> list[Path]:
    repos: list[Path] = []
    for dirpath, dirnames, _filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in PRUNE_DIRS and not dirname.endswith(".egg-info")
        ]
        if (current / ".git").exists():
            repos.append(current)
    return sorted(set(repos), key=lambda path: str(path.relative_to(root)))


def prefix_for(name: str) -> str | None:
    for prefix in sorted(PREFIXES, key=len, reverse=True):
        if name == prefix or name.startswith(f"{prefix}-"):
            return prefix
    return None


def location_hint(relative_path: str) -> str:
    parts = relative_path.split("/")
    if relative_path == ".":
        return "ecosystem-root"
    if "cloud-systems" in parts:
        return "cloud-systems"
    if "local-systems" in parts:
        return "local-systems"
    if "contracts" in parts:
        return "contracts"
    return "ecosystem"


def candidate_prefix_for(relative_path: str, normalized: str) -> str:
    hint = location_hint(relative_path)
    if hint == "cloud-systems":
        if "customer" in normalized:
            return "forgecustomer"
        if "data" in normalized:
            return "dataforge"
        if "agent" in normalized:
            return "forge-command"
        return "neuroforge"
    if hint == "local-systems":
        if "data" in normalized:
            return "dataforge"
        return "neuronforge"
    if hint == "contracts":
        return "bds"
    if "command" in normalized:
        return "forge-command"
    if "customer" in normalized:
        return "forgecustomer"
    if "data" in normalized:
        return "dataforge"
    if "neuro" in normalized:
        return "neuroforge"
    if "neuron" in normalized:
        return "neuronforge"
    return "bds"


def classify(name: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not GENERAL_RE.match(name):
        reasons.append("fails lowercase kebab-case validation regex")
        return "invalid", reasons
    if name in FORBIDDEN_NAMES:
        reasons.append("matches a forbidden vague repository pattern")
        return "deprecated", reasons
    if PREFERRED_RE.match(name):
        return "compliant", ["matches preferred BDS prefix and role pattern"]
    if name in PREFIXES:
        reasons.append("uses a reserved canonical prefix without a role suffix")
        return "reserved", reasons
    reasons.append("valid lowercase kebab-case but not a preferred BDS pattern")
    return "legacy", reasons


def worst_status(*statuses: str) -> str:
    present = [status for status in statuses if status]
    if not present:
        return "invalid"
    return max(present, key=lambda status: STATUS_RANK[status])


def first_existing(repo: Path, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if (repo / candidate).exists():
            return candidate
    return None


def has_workflows(repo: Path) -> bool:
    workflows = repo / ".github" / "workflows"
    return workflows.exists() and any(workflows.glob("*.y*ml"))


def has_promotion_ledger(repo: Path) -> bool:
    names = {
        "promotion-ledger",
        "promotion_ledger",
        "promotion-ledger.yaml",
        "promotion-ledger.yml",
        "promotion-ledger.json",
    }
    for candidate in names:
        if (repo / candidate).exists():
            return True
    return False


def origin_url(repo: Path) -> str:
    remotes = run_git(repo, ["remote", "-v"])
    for line in remotes.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "origin" and parts[2] == "(fetch)":
            return parts[1]
    return ""


def github_full_name(url: str) -> str:
    match = GITHUB_RE.search(url)
    return match.group(1) if match else ""


def audit_repo(root: Path, repo: Path) -> dict[str, Any]:
    relative = "." if repo == root else str(repo.relative_to(root))
    name = repo.name
    normalized = normalize_name(name)
    local_status, local_reasons = classify(name)
    prefix = prefix_for(name)
    normalized_prefix = prefix_for(normalized)
    preferred_prefix = prefix or normalized_prefix or candidate_prefix_for(relative, normalized)

    url = origin_url(repo)
    full_name = github_full_name(url)
    origin_repo_name = full_name.rsplit("/", 1)[-1] if full_name else ""
    origin_status = ""
    origin_reasons: list[str] = []
    if origin_repo_name:
        origin_status, origin_reasons = classify(origin_repo_name)

    status = worst_status(local_status, origin_status) if origin_status else local_status
    reasons = [f"local checkout: {reason}" for reason in local_reasons]
    reasons.extend(f"origin repository: {reason}" for reason in origin_reasons)

    if status == "compliant":
        candidate = name
        action = "No rename needed."
    elif local_status == "compliant" and origin_status and origin_status != "compliant":
        candidate = name
        action = "Rename the GitHub origin to match the compliant local checkout after approval."
    elif local_status == "reserved":
        candidate = f"{name}-<role>"
        action = "Add an explicit role suffix after human approval."
    elif PREFERRED_RE.match(normalized):
        candidate = normalized
        action = "Mechanical local/GitHub rename may be enough, but still requires rename-policy approval."
    elif normalized in PREFIXES:
        candidate = f"{normalized}-<role>"
        action = "Normalize casing/separators and add an approved role suffix."
    else:
        candidate = f"{preferred_prefix}-<approved-role>"
        action = "Classify authority, approve a canonical BDS name, then update references."

    system_doc = first_existing(repo, ["SYSTEM.md", "doc/SYSTEM.md", "docs/SYSTEM.md"])
    doc_system = first_existing(repo, ["doc/system", "docs/system"])
    manifest = first_existing(repo, ["repo.manifest.yaml", "repo.manifest.yml"])

    return {
        "name": name,
        "relative_path": relative,
        "location_hint": location_hint(relative),
        "status": status,
        "reasons": reasons,
        "local_name_status": {
            "name": name,
            "status": local_status,
            "reasons": local_reasons,
        },
        "origin_name_status": {
            "name": origin_repo_name,
            "status": origin_status,
            "reasons": origin_reasons,
        },
        "normalized_name": normalized,
        "preferred_prefix": preferred_prefix,
        "plane": PREFIXES.get(preferred_prefix, {}).get("plane", "unverified-repo"),
        "authority": PREFIXES.get(preferred_prefix, {}).get("authority", "unverified-repo"),
        "rename_candidate": candidate,
        "required_action": action,
        "git": {
            "branch": run_git(repo, ["branch", "--show-current"]),
            "status": run_git(repo, ["status", "--short", "--branch", "--untracked-files=no"]),
            "origin_url": url,
            "github_full_name": full_name,
        },
        "agent_rule_evidence": {
            "system_md": system_doc or "",
            "doc_system": doc_system or "",
            "ci_policy": ".github/workflows" if has_workflows(repo) else "",
            "promotion_ledger": "present" if has_promotion_ledger(repo) else "",
            "repo_manifest": manifest or "",
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def evidence_summary(evidence: dict[str, str]) -> str:
    markers = []
    if evidence["system_md"]:
        markers.append("SYSTEM")
    if evidence["doc_system"]:
        markers.append("doc/system")
    if evidence["ci_policy"]:
        markers.append("CI")
    if evidence["promotion_ledger"]:
        markers.append("ledger")
    if evidence["repo_manifest"]:
        markers.append("manifest")
    return ", ".join(markers) if markers else "none"


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = payload["repositories"]
    summary = payload["summary"]
    lines = [
        "# BDS Repository Naming Compliance Report",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        f"Root: `{payload['root']}`",
        "",
        "Protocol: [`docs/protocols/BDS_REPO_NAMING_v1.md`](../docs/protocols/BDS_REPO_NAMING_v1.md)",
        "",
        "No repositories were renamed by this audit. Non-compliant names require the protocol rename policy: explicit canonical approval, GitHub reference updates, CI/CD updates, deployment-provider updates, local clone path updates, protocol/index updates, and promotion-ledger evidence.",
        "",
        "## Summary",
        "",
        f"- Total repositories discovered: `{summary['total']}`",
        "- Overall status uses the stricter result across the local checkout name and GitHub origin repository name.",
    ]
    for level in ["compliant", "legacy", "deprecated", "invalid", "reserved"]:
        lines.append(f"- {level}: `{summary['levels'].get(level, 0)}`")
    lines.append("")
    lines.append("Local checkout counts: " + ", ".join(
        f"{level} `{summary['local_levels'].get(level, 0)}`"
        for level in ["compliant", "legacy", "deprecated", "invalid", "reserved"]
    ))
    lines.append("GitHub origin counts: " + ", ".join(
        f"{level} `{summary['origin_levels'].get(level, 0)}`"
        for level in ["compliant", "legacy", "deprecated", "invalid", "reserved"]
    ))
    lines.extend(
        [
            "",
            "## Repository Inventory",
            "",
            "| Status | Local repository | Origin repository | Path | Plane | Evidence | Rename candidate / action |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for repo in rows:
        evidence = evidence_summary(repo["agent_rule_evidence"])
        action = f"`{repo['rename_candidate']}` - {repo['required_action']}"
        origin_name = repo["origin_name_status"]["name"] or "none"
        lines.append(
            "| {status} | `{name}` | `{origin_name}` | `{path}` | {plane} | {evidence} | {action} |".format(
                status=repo["status"],
                name=repo["name"],
                origin_name=origin_name,
                path=repo["relative_path"],
                plane=repo["plane"],
                evidence=evidence,
                action=action,
            )
        )

    lines.extend(
        [
            "",
            "## Non-Compliant Repositories",
            "",
        ]
    )
    non_compliant = [repo for repo in rows if repo["status"] != "compliant"]
    if not non_compliant:
        lines.append("All discovered repositories are compliant.")
    else:
        for repo in non_compliant:
            reasons = "; ".join(repo["reasons"])
            lines.extend(
                [
                    f"### `{repo['relative_path']}`",
                    "",
                    f"- Current name: `{repo['name']}`",
                    f"- Origin repository: `{repo['origin_name_status']['name'] or 'none'}`",
                    f"- Status: `{repo['status']}`",
                    f"- Reason: {reasons}",
                    f"- Local name status: `{repo['local_name_status']['status']}`",
                    f"- Origin name status: `{repo['origin_name_status']['status'] or 'unverified-repo'}`",
                    f"- Preferred prefix: `{repo['preferred_prefix']}`",
                    f"- Candidate: `{repo['rename_candidate']}`",
                    f"- Required action: {repo['required_action']}",
                    "",
                ]
            )

    while lines and lines[-1] == "":
        lines.pop()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_payload(root: Path) -> dict[str, Any]:
    repos = [audit_repo(root, repo) for repo in discover_repos(root)]
    levels = Counter(repo["status"] for repo in repos)
    local_levels = Counter(repo["local_name_status"]["status"] for repo in repos)
    origin_levels = Counter(
        repo["origin_name_status"]["status"]
        for repo in repos
        if repo["origin_name_status"]["status"]
    )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "protocol_id": "BDS-REPO-NAMING-v1",
        "root": str(root),
        "summary": {
            "total": len(repos),
            "levels": dict(sorted(levels.items())),
            "local_levels": dict(sorted(local_levels.items())),
            "origin_levels": dict(sorted(origin_levels.items())),
        },
        "repositories": repos,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="ecosystem root to audit")
    parser.add_argument("--json", type=Path, help="write machine-readable audit payload")
    parser.add_argument("--markdown", type=Path, help="write human-readable audit report")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when any repo is not compliant")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    payload = build_payload(root)
    if args.json:
        write_json(args.json, payload)
    if args.markdown:
        write_markdown(args.markdown, payload)
    if not args.json and not args.markdown:
        print(json.dumps(payload, indent=2, sort_keys=True))

    if args.strict and payload["summary"]["levels"].get("compliant", 0) != payload["summary"]["total"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
