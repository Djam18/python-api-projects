from flask import Blueprint, request, jsonify
from models import get_db

workouts_bp = Blueprint('workouts', __name__)


@workouts_bp.route('/workouts', methods=['GET'])
def list_workouts():
    conn = get_db()
    workouts = conn.execute("SELECT * FROM workouts ORDER BY date DESC").fetchall()
    conn.close()
    return jsonify([dict(w) for w in workouts])


@workouts_bp.route('/workouts', methods=['POST'])
def create_workout():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO workouts (date, type, duration, notes) VALUES (?, ?, ?, ?)",
        (data.get('date'), data.get('type', 'general'), data.get('duration', 0), data.get('notes', ''))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@workouts_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    conn = get_db()
    workout = conn.execute("SELECT * FROM workouts WHERE id = ?", (id,)).fetchone()
    if not workout:
        conn.close()
        return jsonify({"error": "not found"}), 404
    exercises = conn.execute("SELECT * FROM exercises WHERE workout_id = ?", (id,)).fetchall()
    conn.close()
    result = dict(workout)
    result['exercises'] = [dict(e) for e in exercises]
    return jsonify(result)


@workouts_bp.route('/workouts/<int:id>/exercises', methods=['POST'])
def add_exercise(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO exercises (workout_id, name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)",
        (id, data['name'], data.get('sets', 1), data.get('reps', 1), data.get('weight', 0))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "exercise added"}), 201
