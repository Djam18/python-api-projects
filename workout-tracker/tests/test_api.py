"""Tests for workout-tracker."""
import sys
import os
import json
import sqlite3
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app


@pytest.fixture
def app(tmp_path, monkeypatch):
    """Use temp database for tests."""
    db_path = str(tmp_path / "test_workouts.db")
    monkeypatch.setattr('models.DB', db_path)

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            duration INTEGER,
            notes TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            name TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL
        )
    """)
    conn.commit()
    conn.close()

    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class TestListWorkouts:
    def test_list_empty_returns_empty(self, client):
        res = client.get('/workouts')
        assert res.status_code == 200
        assert json.loads(res.data) == []

    def test_list_after_create(self, client):
        client.post('/workouts', json={"date": "2019-08-20", "type": "running"})
        res = client.get('/workouts')
        data = json.loads(res.data)
        assert len(data) == 1


class TestCreateWorkout:
    def test_create_returns_201(self, client):
        res = client.post('/workouts', json={"date": "2019-08-20", "type": "running", "duration": 30})
        assert res.status_code == 201

    def test_create_with_minimal_data(self, client):
        res = client.post('/workouts', json={})
        assert res.status_code == 201


class TestGetWorkout:
    def test_get_workout(self, client):
        client.post('/workouts', json={"date": "2019-08-20", "type": "cycling"})
        workouts = json.loads(client.get('/workouts').data)
        w_id = workouts[0]['id']
        res = client.get(f'/workouts/{w_id}')
        assert res.status_code == 200

    def test_get_nonexistent_returns_404(self, client):
        res = client.get('/workouts/9999')
        assert res.status_code == 404


class TestAddExercise:
    def test_add_exercise_to_workout(self, client):
        client.post('/workouts', json={"date": "2019-08-20", "type": "strength"})
        workouts = json.loads(client.get('/workouts').data)
        w_id = workouts[0]['id']
        res = client.post(f'/workouts/{w_id}/exercises', json={"name": "squat", "sets": 3, "reps": 10})
        assert res.status_code == 201

    def test_workout_includes_exercises(self, client):
        client.post('/workouts', json={"date": "2019-08-20", "type": "strength"})
        workouts = json.loads(client.get('/workouts').data)
        w_id = workouts[0]['id']
        client.post(f'/workouts/{w_id}/exercises', json={"name": "deadlift", "sets": 5, "reps": 5})
        res = client.get(f'/workouts/{w_id}')
        data = json.loads(res.data)
        assert 'exercises' in data
        assert len(data['exercises']) == 1
        assert data['exercises'][0]['name'] == 'deadlift'
