from flask import Flask, jsonify
import requests
import redis
import json
from config import API_KEY, BASE_URL, REDIS_HOST, REDIS_PORT

app = Flask(__name__)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route('/')
def index():
    return jsonify({"message": "Weather API"})


@app.route('/weather/<city>')
def get_weather(city):
    cached = r.get(city)
    if cached:
        data = json.loads(cached)
        data['from_cache'] = True
        return jsonify(data)

    url = f"{BASE_URL}/{city}?key={API_KEY}&contentType=json"
    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({"error": "city not found"}), 404

    data = res.json()
    result = {
        "city": data.get("address"),
        "temp": data["currentConditions"]["temp"],
        "feels_like": data["currentConditions"]["feelslike"],
        "humidity": data["currentConditions"]["humidity"],
        "description": data["currentConditions"]["conditions"],
        "from_cache": False
    }
    r.setex(city, 43200, json.dumps(result))
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
