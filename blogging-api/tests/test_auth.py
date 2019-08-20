"""Tests for blogging-api auth endpoints."""
import json
import pytest


class TestRegister:
    def test_register_new_user(self, client):
        res = client.post('/register', json={"username": "newuser", "password": "pass123"})
        assert res.status_code == 201

    def test_register_duplicate_user_returns_400(self, client):
        client.post('/register', json={"username": "alice", "password": "pass"})
        res = client.post('/register', json={"username": "alice", "password": "pass"})
        assert res.status_code == 400


class TestLogin:
    def test_login_valid_credentials(self, client):
        client.post('/register', json={"username": "bob", "password": "secret"})
        res = client.post('/login', json={"username": "bob", "password": "secret"})
        assert res.status_code == 200
        data = json.loads(res.data)
        assert 'token' in data

    def test_login_wrong_password_returns_401(self, client):
        client.post('/register', json={"username": "carol", "password": "right"})
        res = client.post('/login', json={"username": "carol", "password": "wrong"})
        assert res.status_code == 401

    def test_login_nonexistent_user_returns_401(self, client):
        res = client.post('/login', json={"username": "nobody", "password": "pass"})
        assert res.status_code == 401
