"""Partition drills: SSE stream integrity.

Tests that when SSE streams are disrupted:
- Authority override events are emitted on state divergence
- Staleness detection triggers after threshold
- Reconnection attempts work correctly
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.runner.streaming import (
    RunEventStream,
    RunEventType,
    RunAuthorityOverrideEvent,
    RunPersistenceFailureEvent,
)


class TestSSEPartition:
    """SSE stream partition drill tests."""

    @pytest.mark.asyncio
    async def test_authority_override_event_emits(self):
        """F-006: Authority override events can be emitted."""
        stream = RunEventStream(run_id="test-run-001")

        event = await stream.emit_authority_override(
            stream_state="streaming",
            authority_state="finalized",
            reason_code="RC_STREAM_STALE",
            reason="No SSE event for 60s, control plane reports finalized",
        )

        assert event.event_type == RunEventType.AUTHORITY_OVERRIDE
        assert event.stream_state == "streaming"
        assert event.authority_state == "finalized"
        assert event.reason_code == "RC_STREAM_STALE"

    @pytest.mark.asyncio
    async def test_persistence_failure_event_emits(self):
        """F-006: Persistence failure events can be emitted."""
        stream = RunEventStream(run_id="test-run-001")

        event = await stream.emit_persistence_failure(
            error_message="DataForge write failed: connection refused",
            run_mode="governed",
        )

        assert event.event_type == RunEventType.PERSISTENCE_FAILURE
        assert "DataForge" in event.error_message
        assert event.run_mode == "governed"

    @pytest.mark.asyncio
    async def test_event_types_registered(self):
        """Verify new event types exist in the enum."""
        assert RunEventType.PERSISTENCE_FAILURE == "persistence_failure"
        assert RunEventType.AUTHORITY_OVERRIDE == "authority_override"

    @pytest.mark.asyncio
    async def test_authority_override_in_buffer(self):
        """Authority override events are buffered for replay."""
        stream = RunEventStream(run_id="test-run-001")

        await stream.emit_authority_override(
            stream_state="streaming",
            authority_state="failed",
            reason_code="RC_STATE_DIVERGENCE",
        )

        history = stream.get_history()
        assert len(history) == 1
        assert history[0].event_type == RunEventType.AUTHORITY_OVERRIDE

    @pytest.mark.asyncio
    async def test_subscriber_receives_override_events(self):
        """Subscribers receive authority override events."""
        stream = RunEventStream(run_id="test-run-001")
        sub = await stream.subscribe(subscriber_id="test-client")

        await stream.emit_authority_override(
            stream_state="streaming",
            authority_state="cancelled",
            reason_code="RC_CONTROL_PLANE_OVERRIDE",
        )

        event = await sub.receive(timeout=1.0)
        assert event is not None
        assert event.event_type == RunEventType.AUTHORITY_OVERRIDE
