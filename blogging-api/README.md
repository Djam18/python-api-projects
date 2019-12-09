# Blogging API

Flask REST API for a multi-user blog platform with JWT authentication.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login, get JWT token |
| GET | /posts | List posts (optional ?tag=python) |
| POST | /posts | Create post (auth required) |
| GET | /posts/`<id>` | Get post |
| PUT | /posts/`<id>` | Update post (owner only) |
| DELETE | /posts/`<id>` | Delete post (owner only) |

## Examples

```bash
# Register
curl -X POST http://localhost:5002/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'

# Login
curl -X POST http://localhost:5002/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
# {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}

# Create post
curl -X POST http://localhost:5002/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Hello Flask", "content": "My first post", "tags": "python,flask"}'

# Filter by tag
curl "http://localhost:5002/posts?tag=python"
```
