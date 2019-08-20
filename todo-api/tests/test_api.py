"""Tests for todo-api."""
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
        yield flask_app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


class TestListTodos:
    def test_list_empty_returns_empty(self, client):
        res = client.get('/todos')
        assert res.status_code == 200
        assert json.loads(res.data) == []

    def test_list_returns_created_todo(self, client):
        client.post('/todos', json={"title": "buy milk"})
        res = client.get('/todos')
        data = json.loads(res.data)
        assert len(data) == 1
        assert data[0]['title'] == 'buy milk'

    def test_filter_by_done(self, client):
        client.post('/todos', json={"title": "todo 1"})
        client.post('/todos', json={"title": "todo 2"})
        # mark one done
        todos = json.loads(client.get('/todos').data)
        client.put(f'/todos/{todos[0]["id"]}', json={"done": True})
        res = client.get('/todos?status=done')
        data = json.loads(res.data)
        assert len(data) == 1
        assert data[0]['done'] is True

    def test_filter_by_pending(self, client):
        client.post('/todos', json={"title": "pending"})
        res = client.get('/todos?status=pending')
        data = json.loads(res.data)
        assert len(data) == 1

    def test_pagination_limit(self, client):
        for i in range(5):
            client.post('/todos', json={"title": f"todo {i}"})
        res = client.get('/todos?limit=2')
        data = json.loads(res.data)
        assert len(data) == 2


class TestCreateTodo:
    def test_create_returns_201(self, client):
        res = client.post('/todos', json={"title": "new todo"})
        assert res.status_code == 201

    def test_create_without_title_returns_400(self, client):
        res = client.post('/todos', json={})
        assert res.status_code == 400

    def test_created_todo_has_done_false(self, client):
        client.post('/todos', json={"title": "new"})
        todos = json.loads(client.get('/todos').data)
        assert todos[0]['done'] is False


class TestGetTodo:
    def test_get_returns_todo(self, client):
        client.post('/todos', json={"title": "fetch me"})
        todos = json.loads(client.get('/todos').data)
        todo_id = todos[0]['id']
        res = client.get(f'/todos/{todo_id}')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['title'] == 'fetch me'

    def test_get_nonexistent_returns_404(self, client):
        res = client.get('/todos/9999')
        assert res.status_code == 404


class TestUpdateTodo:
    def test_update_title(self, client):
        client.post('/todos', json={"title": "old title"})
        todos = json.loads(client.get('/todos').data)
        todo_id = todos[0]['id']
        client.put(f'/todos/{todo_id}', json={"title": "new title"})
        res = client.get(f'/todos/{todo_id}')
        assert json.loads(res.data)['title'] == 'new title'

    def test_update_nonexistent_returns_404(self, client):
        res = client.put('/todos/9999', json={"title": "x"})
        assert res.status_code == 404


class TestDeleteTodo:
    def test_delete_todo(self, client):
        client.post('/todos', json={"title": "delete me"})
        todos = json.loads(client.get('/todos').data)
        todo_id = todos[0]['id']
        client.delete(f'/todos/{todo_id}')
        res = client.get(f'/todos/{todo_id}')
        assert res.status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        res = client.delete('/todos/9999')
        assert res.status_code == 404
