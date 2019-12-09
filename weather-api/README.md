# Weather API

Flask weather API with Redis caching. Data from Visual Crossing.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
python app.py
```

## Docker

```bash
docker-compose up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | API info |
| GET | /health | Health check with Redis status |
| GET | /weather/`<city>` | Get weather for city |
| DELETE | /cache/clear | Clear Redis cache |

## Examples

```bash
# Get weather for London
curl http://localhost:5000/weather/London

# Response (cache MISS):
# {
#   "city": "London, England, United Kingdom",
#   "temp": 12.3,
#   "feels_like": 10.1,
#   "humidity": 78.0,
#   "description": "Overcast",
#   "X-Cache": "MISS"
# }

# Second request hits cache:
curl http://localhost:5000/weather/London
# "X-Cache": "HIT"

# Health check
curl http://localhost:5000/health
# {"status": "ok", "redis": true}

# Clear cache
curl -X DELETE http://localhost:5000/cache/clear
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| WEATHER_API_KEY | Visual Crossing API key | required |
| REDIS_HOST | Redis host | localhost |
| REDIS_PORT | Redis port | 6379 |
