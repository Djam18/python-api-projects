# Caching Proxy

HTTP caching proxy with Redis backend. Transparently caches upstream responses.

## Setup

```bash
pip install -r requirements.txt
python proxy.py
```

## Docker

```bash
docker-compose up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /proxy | Proxy a URL (required: ?url=...) |
| DELETE | /cache | Clear all cached responses |

## Examples

```bash
# Proxy a request (first call: cache MISS)
curl "http://localhost:5005/proxy?url=https://jsonplaceholder.typicode.com/todos/1"
# X-Cache: MISS

# Second call: cache HIT
curl "http://localhost:5005/proxy?url=https://jsonplaceholder.typicode.com/todos/1"
# X-Cache: HIT

# Clear the cache
curl -X DELETE http://localhost:5005/cache
```
