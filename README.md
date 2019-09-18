# Python API Projects

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-green.svg)
![Tests](https://img.shields.io/badge/tests-pytest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Flask REST API projects from [roadmap.sh](https://roadmap.sh/projects) — learning backend development with Python.

## Table of Contents

- [Projects](#projects)
- [Stack](#stack)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Docker](#docker)
- [Project Details](#project-details)

## Projects

| Project | Level | Stack | Description |
|---------|-------|-------|-------------|
| [weather-api](./weather-api/) | intermediate | Flask + Redis + SQLAlchemy | Weather with Redis caching |
| [todo-api](./todo-api/) | beginner | Flask + SQLAlchemy | Todo CRUD with persistent DB |
| [blogging-api](./blogging-api/) | intermediate | Flask + JWT + SQLAlchemy | Blog platform with auth |
| [expense-api](./expense-api/) | beginner | Flask + SQLAlchemy | Expense tracker with reports |
| [url-shortener](./url-shortener/) | intermediate | Flask + SQLite | URL shortener with analytics |
| [markdown-notes](./markdown-notes/) | beginner | Flask + markdown2 | Notes with markdown rendering |
| [caching-proxy](./caching-proxy/) | intermediate | Flask + Redis | HTTP caching proxy |
| [workout-tracker](./workout-tracker/) | beginner | Flask + SQLAlchemy + Blueprints | Workout progress tracking |
| [broadcast-server](./broadcast-server/) | advanced | asyncio + websockets | WebSocket chat with rooms |
| [image-processing](./image-processing/) | intermediate | Flask + Pillow | Image resize/crop/rotate API |
| [ecommerce-api](./ecommerce-api/) | intermediate | Flask + SQLAlchemy + Stripe | E-commerce with payments |

## Stack

- **Python** 3.7+
- **Flask** 2.x
- **SQLAlchemy** — ORM for all database-backed projects
- **SQLite** — development database
- **Redis** — caching (weather-api, caching-proxy)
- **JWT** auth (PyJWT) + **bcrypt** (password hashing)
- **Docker Compose** — containerized setup for key projects
- **pytest** — test suite for all projects

## Setup

Each project is independent. Run from the project directory:

```bash
cd weather-api
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
python app.py
```

Or use Docker Compose (for projects that support it):

```bash
cd weather-api
docker-compose up
```

## Running Tests

From any project directory:

```bash
pip install pytest
pytest tests/ -v
```

Run all tests from root:

```bash
for d in weather-api todo-api blogging-api expense-api url-shortener caching-proxy workout-tracker ecommerce-api; do
  echo "=== $d ==="
  (cd $d && pytest tests/ -v --tb=short)
done
```

## Docker

Projects with Docker Compose support:

| Project | Services |
|---------|----------|
| weather-api | Flask + Redis |
| todo-api | Flask + SQLite volume |
| caching-proxy | Flask + Redis |

Start with:
```bash
docker-compose up --build
```

## Project Details

### weather-api — port 5000

Real weather data with Redis caching (60s TTL). Requires `WEATHER_API_KEY` from OpenWeatherMap.

```bash
GET /weather?city=London
GET /weather?city=Paris&units=metric
DELETE /cache          # clear all cached responses
```

### todo-api — port 5001

Simple task management with SQLAlchemy persistence.

```bash
GET    /todos
POST   /todos          {"title": "Buy groceries", "done": false}
GET    /todos/1
PUT    /todos/1        {"done": true}
DELETE /todos/1
```

### blogging-api — port 5002

Multi-user blog with JWT authentication, tags, and post filtering.

```bash
POST   /auth/register  {"username": "alice", "password": "secret"}
POST   /auth/login     {"username": "alice", "password": "secret"}
GET    /posts?tag=python
POST   /posts          {"title": "My Post", "content": "...", "tags": "python,flask"}
PUT    /posts/1        # auth required, own posts only
DELETE /posts/1        # auth required, own posts only
```

### expense-api — port 5003

Track expenses by category with monthly reports.

```bash
GET    /expenses?category=food&start=2019-01-01&end=2019-12-31
POST   /expenses       {"amount": 12.50, "description": "Lunch", "category": "food"}
GET    /expenses/summary?month=2019-09
DELETE /expenses/1
```

### url-shortener — port 5004

Shorten URLs and track click counts.

```bash
POST   /shorten        {"url": "https://example.com/very/long/url"}
GET    /<short_code>   # redirects to original URL
GET    /stats/<code>   # click count and original URL
```

### caching-proxy — port 5005

Transparent HTTP caching proxy with Redis backend.

```bash
GET    /proxy?url=https://api.example.com/data
DELETE /cache          # clear proxy cache
```

## Shared Utilities

The `shared/` directory contains reusable modules:

- `shared/error_handlers.py` — centralized Flask error handlers (404, 405, 500 + custom exceptions)
- `shared/logging_config.py` — standardized logging setup

## Environment Variables

Each project has a `.env.example`. Common variables:

```
WEATHER_API_KEY=your_openweathermap_key
SECRET_KEY=your_flask_secret_key
DATABASE_URL=sqlite:///app.db
REDIS_HOST=localhost
REDIS_PORT=6379
```
