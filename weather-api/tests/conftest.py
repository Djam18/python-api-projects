"""Shared fixtures for weather-api tests."""
import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_redis(monkeypatch):
    """Mock Redis to avoid needing a real Redis server."""
    mock = MagicMock()
    mock.get.return_value = None
    mock.setex.return_value = True
    mock.ping.return_value = True
    return mock


@pytest.fixture
def app(mock_redis, monkeypatch):
    """Create app with mocked Redis."""
    monkeypatch.setenv("REDIS_HOST", "localhost")
    monkeypatch.setenv("REDIS_PORT", "6379")

    import app as app_module
    app_module.r = mock_redis
    app_module.REDIS_AVAILABLE = True

    app_module.app.config['TESTING'] = True
    return app_module.app


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()
