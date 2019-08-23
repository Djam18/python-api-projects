"""Tests for expense-api."""
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


class TestListExpenses:
    def test_list_empty_returns_empty(self, client):
        res = client.get('/expenses')
        assert res.status_code == 200
        assert json.loads(res.data) == []

    def test_list_returns_created_expense(self, client):
        client.post('/expenses', json={"amount": 15.50, "category": "food"})
        res = client.get('/expenses')
        data = json.loads(res.data)
        assert len(data) == 1
        assert data[0]['amount'] == 15.50


class TestCreateExpense:
    def test_create_returns_201(self, client):
        res = client.post('/expenses', json={"amount": 10.0})
        assert res.status_code == 201

    def test_create_without_amount_returns_400(self, client):
        res = client.post('/expenses', json={"category": "food"})
        assert res.status_code == 400

    def test_create_with_category(self, client):
        client.post('/expenses', json={"amount": 5.0, "category": "transport"})
        res = client.get('/expenses')
        data = json.loads(res.data)
        assert data[0]['category'] == 'transport'


class TestDeleteExpense:
    def test_delete_expense(self, client):
        client.post('/expenses', json={"amount": 10.0})
        expenses = json.loads(client.get('/expenses').data)
        exp_id = expenses[0]['id']
        client.delete(f'/expenses/{exp_id}')
        res = client.get('/expenses')
        assert json.loads(res.data) == []

    def test_delete_nonexistent_returns_404(self, client):
        res = client.delete('/expenses/9999')
        assert res.status_code == 404


class TestFilterExpenses:
    def test_filter_by_category(self, client):
        client.post('/expenses', json={"amount": 5.0, "category": "food"})
        client.post('/expenses', json={"amount": 10.0, "category": "transport"})
        res = client.get('/expenses?category=food')
        data = json.loads(res.data)
        assert len(data) == 1
        assert data[0]['category'] == 'food'
