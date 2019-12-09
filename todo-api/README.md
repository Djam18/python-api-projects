# Todo List API

Flask REST API for todo management with SQLAlchemy persistence.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Docker

```bash
docker-compose up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /todos | List all todos |
| POST | /todos | Create a todo |
| GET | /todos/`<id>` | Get a todo |
| PUT | /todos/`<id>` | Update a todo |
| DELETE | /todos/`<id>` | Delete a todo |

## Examples

```bash
# Create a todo
curl -X POST http://localhost:5001/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
# {"id": 1, "title": "Buy groceries", "done": false, "created_at": "2019-12-01T10:00:00"}

# List all todos
curl http://localhost:5001/todos

# Get a specific todo
curl http://localhost:5001/todos/1

# Mark as done
curl -X PUT http://localhost:5001/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a todo
curl -X DELETE http://localhost:5001/todos/1
```
