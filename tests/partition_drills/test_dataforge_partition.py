"""Partition drills: DataForge unavailability.

Tests that when DataForge is partitioned:
- BugCheck refuses to start new runs (fail-closed)
- Governed runs fail on persistence errors
- Peek runs degrade gracefully
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.agents.bugcheck.agent import BugCheckAgent, BugCheckError
from app.agents.bugcheck.dataforge_client import DataForgeUnavailableError
from app.agents.bugcheck.schemas.models import RunMode, RunScope
from app.runner.script_runner import PersistenceFailureError


class TestDataForgePartition:
    """DataForge partition drill tests."""

    @pytest.mark.asyncio
    async def test_bugcheck_refuses_to_start_when_dataforge_down(
        self, mock_dataforge_down, clean_env
    ):
        """F-002: BugCheck MUST NOT start a run when DataForge is unreachable."""
        agent = BugCheckAgent()

        with pytest.raises(DataForgeUnavailableError):
            await agent.run(
                targets=["neuroforge"],
                mode=RunMode.QUICK,
                scope=RunScope.FULL_REPO,
            )

    @pytest.mark.asyncio
    async def test_governed_run_fails_on_persistence_error(self):
        """F-002: Governed run persistence failure is fatal."""
        from app.runner.script_runner import ForgeRunRunner, RunRequest, RunResult

        runner = ForgeRunRunner(
            output_dir=MagicMock(),
            enable_persistence=True,
        )

        # Mock persistence to fail
        runner._persistence = MagicMock()
        runner._persistence.persist_run = AsyncMock(
            side_effect=Exception("DataForge write failed")
        )

        result = RunResult(
            success=True,
            final_status="pass",
            run_evidence={"test": "data"},
            run_evidence_hash="abc123",
        )

        with pytest.raises(PersistenceFailureError):
            await runner._persist_run(result, "test-run-001", peek=False)

    @pytest.mark.asyncio
    async def test_peek_run_continues_on_persistence_error(self):
        """F-002: Peek run persistence failure is best-effort (non-fatal)."""
        from app.runner.script_runner import ForgeRunRunner, RunResult

        runner = ForgeRunRunner(
            output_dir=MagicMock(),
            enable_persistence=True,
        )

        runner._persistence = MagicMock()
        runner._persistence.persist_run = AsyncMock(
            side_effect=Exception("DataForge write failed")
        )

        result = RunResult(
            success=True,
            final_status="pass",
            run_evidence={"test": "data"},
            run_evidence_hash="abc123",
        )

        # Should NOT raise — peek mode is best-effort
        await runner._persist_run(result, "test-run-001", peek=True)

    @pytest.mark.asyncio
    async def test_governed_run_requires_persistence_layer(self):
        """F-002: Governed run fails if persistence layer is not configured."""
        from app.runner.script_runner import ForgeRunRunner, RunResult

        runner = ForgeRunRunner(
            output_dir=MagicMock(),
            enable_persistence=False,
        )

        result = RunResult(
            success=True,
            final_status="pass",
            run_evidence={"test": "data"},
            run_evidence_hash="abc123",
        )

        with pytest.raises(PersistenceFailureError, match="persistence layer is not configured"):
            await runner._persist_run(result, "test-run-001", peek=False)
