# Todo List API

Flask REST API for todo management.

## Run
python app.py

## Endpoints
GET    /todos           - List todos (?status=done&page=1&limit=10)
POST   /todos           - Create todo
GET    /todos/<id>      - Get todo
PUT    /todos/<id>      - Update todo
DELETE /todos/<id>      - Delete todo
