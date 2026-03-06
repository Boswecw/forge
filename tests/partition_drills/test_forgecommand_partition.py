"""Partition drills: ForgeCommand unavailability.

Tests that when ForgeCommand is partitioned:
- Token requests fail-closed (no local fallback)
- DevTokenProvider only works with FORGE_DEV_MODE=true
- Proper error propagation with reason codes
"""

import os
import pytest
from unittest.mock import AsyncMock, patch

from app.agents.bugcheck.forgecommand import (
    DevTokenProvider,
    ForgeCommandClient,
    ForgeCommandUnavailableError,
)
from app.agents.bugcheck.schemas.models import RunMode, RunScope


class TestForgeCommandPartition:
    """ForgeCommand partition drill tests."""

    @pytest.mark.asyncio
    async def test_token_request_fails_closed_when_forgecommand_down(
        self, mock_forgecommand_down, clean_env
    ):
        """F-001: Token request MUST fail-closed when ForgeCommand unreachable."""
        async with ForgeCommandClient() as client:
            with pytest.raises(ForgeCommandUnavailableError):
                await client.request_run_token(
                    targets=["neuroforge"],
                    mode=RunMode.STANDARD,
                    scope=RunScope.FULL_REPO,
                    commit_sha="a" * 40,
                )

    @pytest.mark.asyncio
    async def test_no_local_fallback_in_production(self, clean_env):
        """F-001: No local token fallback when FORGE_DEV_MODE is not set."""
        assert not DevTokenProvider.is_dev_mode()

        with pytest.raises(RuntimeError, match="FORGE_DEV_MODE"):
            DevTokenProvider.generate_token(
                targets=["neuroforge"],
                mode=RunMode.STANDARD,
                scope=RunScope.FULL_REPO,
                commit_sha="a" * 40,
            )

    def test_dev_token_provider_works_in_dev_mode(self, dev_mode_env):
        """F-001: DevTokenProvider works when FORGE_DEV_MODE=true."""
        assert DevTokenProvider.is_dev_mode()

        run_id, token = DevTokenProvider.generate_token(
            targets=["neuroforge"],
            mode=RunMode.STANDARD,
            scope=RunScope.FULL_REPO,
            commit_sha="a" * 40,
        )

        assert run_id is not None
        assert token.token.startswith("dev-local-")

    def test_dev_tokens_clearly_marked(self, dev_mode_env):
        """F-001: Dev tokens carry clear markers and no authority."""
        _, token = DevTokenProvider.generate_token(
            targets=["test"],
            mode=RunMode.QUICK,
            scope=RunScope.FULL_REPO,
            commit_sha="b" * 40,
        )

        assert "dev-local-" in token.token
        assert token.targets == ["test"]

    @pytest.mark.asyncio
    async def test_error_includes_reason_code(self, mock_forgecommand_down, clean_env):
        """F-001: Error messages include reason codes for observability."""
        async with ForgeCommandClient() as client:
            try:
                await client.request_run_token(
                    targets=["neuroforge"],
                    mode=RunMode.STANDARD,
                    scope=RunScope.FULL_REPO,
                    commit_sha="a" * 40,
                )
                assert False, "Should have raised"
            except ForgeCommandUnavailableError as e:
                assert "FORGE_DEV_MODE" in str(e)
                assert "fail-closed" in str(e).lower() or "Runs cannot start" in str(e)
