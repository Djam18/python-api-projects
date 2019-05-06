# Weather API

Flask weather API with Redis caching.

## Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

## Run
python app.py

## Endpoints
GET /         - API info
GET /health   - Health check
GET /weather/<city>  - Get weather for city
GET /cache/clear     - Clear Redis cache

## Environment Variables
WEATHER_API_KEY - Visual Crossing API key
REDIS_HOST      - Redis host (default: localhost)
REDIS_PORT      - Redis port (default: 6379)
