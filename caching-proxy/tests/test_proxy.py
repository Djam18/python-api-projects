"""Tests for caching-proxy."""
import sys
import os
import json
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proxy import app as flask_app


@pytest.fixture
def mock_cache(monkeypatch):
    cache = MagicMock()
    cache.get.return_value = None
    cache.set.return_value = True
    return cache


@pytest.fixture
def app(mock_cache, monkeypatch):
    import proxy
    proxy.cache = mock_cache
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class TestProxyEndpoint:
    def test_proxy_without_url_returns_400(self, client):
        res = client.get('/proxy')
        assert res.status_code == 400

    def test_proxy_cache_miss_calls_external(self, client, mock_cache):
        mock_cache.get.return_value = None
        with patch('proxy.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = '<html>Hello</html>'
            mock_response.headers = {'Content-Type': 'text/html'}
            mock_get.return_value = mock_response

            res = client.get('/proxy?url=https://example.com')
            assert res.status_code == 200
            assert res.headers.get('X-Cache') == 'MISS'

    def test_proxy_cache_hit_returns_cached(self, client, mock_cache):
        mock_cache.get.return_value = '<html>Cached</html>'
        res = client.get('/proxy?url=https://example.com')
        assert res.status_code == 200
        assert res.headers.get('X-Cache') == 'HIT'

    def test_proxy_sets_cache_on_miss(self, client, mock_cache):
        mock_cache.get.return_value = None
        with patch('proxy.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = '<html>Content</html>'
            mock_response.headers = {}
            mock_get.return_value = mock_response

            client.get('/proxy?url=https://example.com')
            assert mock_cache.set.called

    def test_proxy_handles_request_error(self, client, mock_cache):
        mock_cache.get.return_value = None
        with patch('proxy.requests.get') as mock_get:
            mock_get.side_effect = Exception("connection refused")
            res = client.get('/proxy?url=https://example.com')
            assert res.status_code == 500
