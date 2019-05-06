# Caching Proxy

HTTP proxy with Redis caching.

## Run
python proxy.py

## Usage
GET /proxy?url=https://example.com

Response headers:
X-Cache: HIT or MISS
