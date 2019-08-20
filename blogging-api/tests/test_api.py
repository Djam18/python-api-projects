"""Tests for blogging-api posts endpoints."""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from database import db as _db


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with flask_app.app_context():
        _db.create_all()
        # also init auth db
        from auth import init_auth_db
        init_auth_db()
        yield flask_app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Register and login, return token."""
    client.post('/register', json={"username": "testuser", "password": "password123"})
    res = client.post('/login', json={"username": "testuser", "password": "password123"})
    return json.loads(res.data)['token']


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


class TestListPosts:
    def test_list_empty(self, client):
        res = client.get('/posts')
        assert res.status_code == 200
        assert json.loads(res.data) == []

    def test_list_returns_posts(self, client, auth_headers):
        client.post('/posts', json={"title": "Hello World"}, headers=auth_headers)
        res = client.get('/posts')
        data = json.loads(res.data)
        assert len(data) == 1


class TestCreatePost:
    def test_create_without_auth_returns_401(self, client):
        res = client.post('/posts', json={"title": "test"})
        assert res.status_code == 401

    def test_create_with_auth_returns_201(self, client, auth_headers):
        res = client.post('/posts', json={"title": "First post"}, headers=auth_headers)
        assert res.status_code == 201

    def test_create_without_title_returns_400(self, client, auth_headers):
        res = client.post('/posts', json={}, headers=auth_headers)
        assert res.status_code == 400

    def test_create_with_tags(self, client, auth_headers):
        res = client.post('/posts', json={"title": "Tagged", "tags": ["python", "flask"]}, headers=auth_headers)
        assert res.status_code == 201


class TestGetPost:
    def test_get_post(self, client, auth_headers):
        client.post('/posts', json={"title": "Fetch me"}, headers=auth_headers)
        posts = json.loads(client.get('/posts').data)
        post_id = posts[0]['id']
        res = client.get(f'/posts/{post_id}')
        assert res.status_code == 200

    def test_get_nonexistent_returns_404(self, client):
        res = client.get('/posts/9999')
        assert res.status_code == 404
