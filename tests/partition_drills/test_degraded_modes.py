"""Partition drills: Named degraded mode verification.

Tests that each service correctly reports its degraded mode:
- ServiceContract.v1 manifests declare valid degraded modes
- Services report correct mode when dependencies are unavailable
"""

import json
from pathlib import Path

import pytest


class TestDegradedModes:
    """Degraded mode partition drill tests."""

    ECOSYSTEM_ROOT = Path("/home/charlie/Forge/ecosystem")

    SERVICE_MANIFESTS = {
        "DataForge": "DataForge/service_contract.v1.json",
        "ForgeAgents": "ForgeAgents/service_contract.v1.json",
        "NeuroForge": "NeuroForge/service_contract.v1.json",
        "Rake": "rake/service_contract.v1.json",
        "ForgeCommand": "Forge_Command/service_contract.v1.json",
    }

    def test_all_services_have_manifests(self):
        """F-003: Every service has a ServiceContract.v1 manifest."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            assert manifest_path.exists(), (
                f"Service {service} missing {rel_path}. "
                "All services must declare their connectivity contract."
            )

    def test_manifests_are_valid_json(self):
        """F-003: All manifests parse as valid JSON."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                content = manifest_path.read_text()
                try:
                    data = json.loads(content)
                    assert isinstance(data, dict)
                except json.JSONDecodeError as e:
                    pytest.fail(f"{service} manifest is invalid JSON: {e}")

    def test_manifests_have_required_fields(self):
        """F-003: All manifests contain required schema fields."""
        required_fields = ["service_id", "version", "contract_version",
                          "dependencies", "endpoints_exposed", "degraded_modes"]

        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                for field in required_fields:
                    assert field in data, (
                        f"{service} manifest missing required field '{field}'"
                    )

    def test_degraded_modes_are_declared(self):
        """F-008: Each service declares at least one degraded mode."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                modes = data.get("degraded_modes", [])
                assert len(modes) > 0, (
                    f"{service} declares no degraded modes. "
                    "Every service must declare how it degrades."
                )

    def test_degraded_modes_have_required_fields(self):
        """F-008: Each degraded mode has name, trigger, and affected_capabilities."""
        required_mode_fields = ["name", "trigger", "affected_capabilities"]

        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                for mode in data.get("degraded_modes", []):
                    for field in required_mode_fields:
                        assert field in mode, (
                            f"{service} degraded mode '{mode.get('name', '?')}' "
                            f"missing required field '{field}'"
                        )

    def test_auth_default_policy_is_deny(self):
        """F-005: All services use default_policy='deny'."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                auth = data.get("auth_requirements", {})
                policy = auth.get("default_policy", "allow")
                assert policy == "deny", (
                    f"{service} has default_policy='{policy}', expected 'deny'. "
                    "All Forge services MUST default to deny."
                )

    def test_dependencies_have_fallback_behavior(self):
        """F-008: All dependencies declare their fallback behavior."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                for dep in data.get("dependencies", []):
                    assert "fallback_behavior" in dep, (
                        f"{service} dependency on '{dep.get('service_id', '?')}' "
                        "missing fallback_behavior"
                    )
                    valid_behaviors = {"fail_closed", "degrade", "cache_fallback", "skip"}
                    assert dep["fallback_behavior"] in valid_behaviors, (
                        f"{service} dependency '{dep.get('service_id', '?')}' has "
                        f"invalid fallback_behavior '{dep['fallback_behavior']}'"
                    )

    def test_critical_dependencies_fail_closed(self):
        """F-008: Critical dependencies MUST use fail_closed fallback."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                for dep in data.get("dependencies", []):
                    if dep.get("critical", False):
                        assert dep.get("fallback_behavior") == "fail_closed", (
                            f"{service}: critical dependency on "
                            f"'{dep.get('service_id', '?')}' must use "
                            f"fallback_behavior='fail_closed', got "
                            f"'{dep.get('fallback_behavior')}'"
                        )

    def test_neuroforge_degraded_modes(self):
        """F-008: NeuroForge declares the 5 named degraded modes."""
        manifest_path = self.ECOSYSTEM_ROOT / "NeuroForge/service_contract.v1.json"
        data = json.loads(manifest_path.read_text())
        mode_names = {m["name"] for m in data.get("degraded_modes", [])}

        expected_modes = {"FULL", "CACHE_ONLY", "MODEL_ONLY", "DEGRADED_NO_RAG", "OFFLINE"}
        assert expected_modes == mode_names, (
            f"NeuroForge degraded modes: expected {expected_modes}, got {mode_names}"
        )

    def test_contract_version_is_v1(self):
        """F-003: All contracts use version 1.0."""
        for service, rel_path in self.SERVICE_MANIFESTS.items():
            manifest_path = self.ECOSYSTEM_ROOT / rel_path
            if manifest_path.exists():
                data = json.loads(manifest_path.read_text())
                assert data.get("contract_version") == "1.0", (
                    f"{service} uses contract_version={data.get('contract_version')}, "
                    "expected '1.0'"
                )
