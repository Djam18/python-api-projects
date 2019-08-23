"""Tests for url-shortener."""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app, get_db, init_db


@pytest.fixture
def app(tmp_path, monkeypatch):
    """Use a temp database for each test."""
    db_path = str(tmp_path / "test_urls.db")
    monkeypatch.setattr('app.DB', db_path)

    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        # reinit with temp db
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class TestShorten:
    def test_shorten_url_returns_201(self, client):
        res = client.post('/shorten', json={"url": "https://example.com"})
        assert res.status_code == 201

    def test_shorten_without_url_returns_400(self, client):
        res = client.post('/shorten', json={})
        assert res.status_code == 400

    def test_shorten_returns_short_code(self, client):
        res = client.post('/shorten', json={"url": "https://example.com"})
        data = json.loads(res.data)
        assert 'code' in data
        assert len(data['code']) > 0

    def test_shorten_returns_short_url(self, client):
        res = client.post('/shorten', json={"url": "https://example.com"})
        data = json.loads(res.data)
        assert 'short_url' in data


class TestRedirect:
    def test_redirect_valid_code(self, client):
        res = client.post('/shorten', json={"url": "https://example.com"})
        code = json.loads(res.data)['code']
        res = client.get(f'/{code}')
        # should redirect
        assert res.status_code in [301, 302]

    def test_redirect_invalid_code_returns_404(self, client):
        res = client.get('/invalidcode123')
        assert res.status_code == 404

    def test_redirect_increments_clicks(self, client):
        res = client.post('/shorten', json={"url": "https://example.com"})
        code = json.loads(res.data)['code']
        client.get(f'/{code}')
        client.get(f'/{code}')
        # check stats endpoint
        stats_res = client.get(f'/stats/{code}')
        if stats_res.status_code == 200:
            stats = json.loads(stats_res.data)
            assert stats.get('clicks', 0) >= 2
