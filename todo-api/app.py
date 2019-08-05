from flask import Flask, request, jsonify
from database import db
from models import Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/todos', methods=['GET'])
def list_todos():
    """List todos with optional status filter and pagination."""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    query = Todo.query
    if status == 'done':
        query = query.filter_by(done=True)
    elif status == 'pending':
        query = query.filter_by(done=False)

    todos = query.offset((page - 1) * limit).limit(limit).all()
    return jsonify([t.to_dict() for t in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo."""
    title = request.json.get('title')
    if not title:
        return jsonify({"error": "title required"}), 400
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"message": "created", "id": todo.id}), 201


@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    """Get a single todo by id."""
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "not found"}), 404
    return jsonify(todo.to_dict())


@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    """Update a todo."""
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "not found"}), 404
    data = request.json
    if 'title' in data:
        todo.title = data['title']
    if 'done' in data:
        todo.done = data['done']
    db.session.commit()
    return jsonify({"message": "updated"})


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """Delete a todo."""
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
