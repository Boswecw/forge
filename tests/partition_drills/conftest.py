"""Shared fixtures for partition drill tests.

Provides mock services, network partition simulation, and
common test infrastructure for connectivity contract validation.
"""

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_dataforge_down():
    """Simulate DataForge being completely unreachable."""
    with patch("httpx.AsyncClient.get") as mock_get, \
         patch("httpx.AsyncClient.post") as mock_post:
        mock_get.side_effect = ConnectionError("DataForge unreachable")
        mock_post.side_effect = ConnectionError("DataForge unreachable")
        yield mock_get, mock_post


@pytest.fixture
def mock_forgecommand_down():
    """Simulate ForgeCommand being completely unreachable."""
    with patch("httpx.AsyncClient.post") as mock_post, \
         patch("httpx.AsyncClient.get") as mock_get:
        mock_post.side_effect = ConnectionError("ForgeCommand unreachable")
        mock_get.side_effect = ConnectionError("ForgeCommand unreachable")
        yield mock_post, mock_get


@pytest.fixture
def mock_neuroforge_down():
    """Simulate NeuroForge being completely unreachable."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = ConnectionError("NeuroForge unreachable")
        yield mock_get


@pytest.fixture
def mock_dataforge_slow():
    """Simulate DataForge responding slowly (>5s)."""
    async def slow_response(*args, **kwargs):
        await asyncio.sleep(10)
        raise asyncio.TimeoutError("DataForge timeout")

    with patch("httpx.AsyncClient.get", side_effect=slow_response) as mock:
        yield mock


@pytest.fixture
def mock_dataforge_available():
    """Simulate DataForge being available and healthy."""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "healthy"}

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_forgecommand_available():
    """Simulate ForgeCommand being available."""
    mock_response = AsyncMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "run_id": "test-run-001",
        "token": "test-token-abc",
        "nonce": "test-nonce",
    }

    with patch("httpx.AsyncClient.post", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def clean_env(monkeypatch):
    """Ensure clean environment without FORGE_DEV_MODE."""
    monkeypatch.delenv("FORGE_DEV_MODE", raising=False)
    yield


@pytest.fixture
def dev_mode_env(monkeypatch):
    """Enable FORGE_DEV_MODE for dev token testing."""
    monkeypatch.setenv("FORGE_DEV_MODE", "true")
    yield
