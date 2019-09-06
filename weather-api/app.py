from flask import Flask, jsonify
import requests
import redis
import json
import logging
from config import API_KEY, BASE_URL, REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    REDIS_AVAILABLE = True
    logger.info("Redis connected at %s:%s", REDIS_HOST, REDIS_PORT)
except Exception:
    REDIS_AVAILABLE = False
    r = None
    logger.warning("Redis not available, caching disabled")


def cache_get(key):
    if REDIS_AVAILABLE and r:
        return r.get(key)
    return None


def cache_set(key, value, ttl):
    if REDIS_AVAILABLE and r:
        r.setex(key, ttl, value)


@app.route('/')
def index():
    return jsonify({"message": "Weather API", "cache": "redis" if REDIS_AVAILABLE else "none"})


@app.route('/health')
def health():
    return jsonify({"status": "ok", "redis": REDIS_AVAILABLE})


@app.route('/weather/<city>')
def get_weather(city):
    cached = cache_get(city)
    if cached:
        data = json.loads(cached)
        data['X-Cache'] = 'HIT'
        return jsonify(data)

    url = f"{BASE_URL}/{city}?key={API_KEY}&contentType=json"
    logger.info("Cache miss for city: %s, fetching from API", city)
    res = requests.get(url)
    if res.status_code != 200:
        logger.error("Weather API returned %s for city: %s", res.status_code, city)
        return jsonify({"error": "city not found"}), 404

    data = res.json()
    result = {
        "city": data.get("address"),
        "temp": data["currentConditions"]["temp"],
        "feels_like": data["currentConditions"]["feelslike"],
        "humidity": data["currentConditions"]["humidity"],
        "description": data["currentConditions"]["conditions"],
        "X-Cache": "MISS"
    }
    cache_set(city, json.dumps({k: v for k, v in result.items() if k != 'X-Cache'}), 43200)
    return jsonify(result)


@app.route('/cache/clear', methods=['DELETE'])
def clear_cache():
    if REDIS_AVAILABLE and r:
        r.flushdb()
        return jsonify({"message": "cache cleared"})
    return jsonify({"message": "no cache to clear"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
