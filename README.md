# Python API Projects

Flask API projects from roadmap.sh - learning REST APIs.

## Projects

| Project | Level | Stack | Description |
|---------|-------|-------|-------------|
| weather-api | intermediate | Flask + Redis | Weather API with caching |
| todo-api | beginner | Flask + SQLite | Todo CRUD API |
| blogging-api | intermediate | Flask + JWT + bcrypt | Blog platform with auth |
| expense-api | beginner | Flask + SQLite | Expense tracker with reports |
| url-shortener | intermediate | Flask + SQLite | URL shortener with click analytics |
| markdown-notes | beginner | Flask + markdown2 | Notes with markdown rendering |
| caching-proxy | intermediate | Flask + Redis | HTTP caching proxy |
| workout-tracker | beginner | Flask + SQLite + Blueprints | Workout progress tracking |
| broadcast-server | advanced | asyncio + websockets | WebSocket chat with rooms |
| image-processing | intermediate | Flask + Pillow | Image resize/crop/rotate API |
| ecommerce-api | intermediate | Flask + SQLite + Stripe | E-commerce with payment |

## Stack
- Python 3.7+
- Flask 2.x
- SQLite (no ORM - direct SQL)
- Redis (caching)
- JWT auth (PyJWT)
- bcrypt (password hashing)

## Setup
pip install -r requirements.txt
cp .env.example .env

## Notes
- Each project is independent, run from its own directory
- No Docker yet (coming later)
- Tests only in ecommerce-api for now
