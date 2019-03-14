from flask import Flask, request, jsonify, Response
import requests
import hashlib
from cache import RedisCache

app = Flask(__name__)
cache = RedisCache()


@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "url parameter required"}), 400

    cache_key = hashlib.md5(url.encode()).hexdigest()
    cached = cache.get(cache_key)

    if cached:
        return Response(cached, headers={'X-Cache': 'HIT', 'Content-Type': 'text/html'})

    try:
        res = requests.get(url, timeout=10)
        content = res.text
        cache.set(cache_key, content, ttl=3600)
        return Response(content, headers={'X-Cache': 'MISS', 'Content-Type': res.headers.get('Content-Type', 'text/html')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5006)
