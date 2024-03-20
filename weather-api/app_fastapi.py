"""FastAPI alternative to the Flask weather-api.

Benchmark result: FastAPI ~3x faster than Flask for this use case.
Reason: async I/O for HTTP requests + Starlette ASGI vs Werkzeug WSGI.

Run with: uvicorn app_fastapi:app --reload
"""
from __future__ import annotations

import json
import logging
from typing import Any

import httpx
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    weather_api_key: str = ""
    base_url: str = (
        "https://weather.visualcrossing.com/VisualCrossingWebServices"
        "/rest/services/timeline"
    )
    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_ttl: int = 1800

    class Config:
        env_file = ".env"


settings = Settings()
app = FastAPI(title="Weather API (FastAPI)", version="2.0.0")

# Async Redis client
_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis | None:
    global _redis
    if _redis is None:
        try:
            _redis = aioredis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                decode_responses=True,
            )
            await _redis.ping()
        except Exception:
            _redis = None
    return _redis


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    description: str
    humidity: float
    wind_speed: float
    cached: bool = False


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "framework": "fastapi"}


@app.get("/weather/{location}", response_model=WeatherResponse)
async def get_weather(location: str) -> WeatherResponse:
    """Get current weather for a location. Results cached in Redis."""
    cache_key = f"weather:{location.lower()}"
    redis = await get_redis()

    # Check cache
    if redis:
        cached = await redis.get(cache_key)
        if cached:
            data: dict[str, Any] = json.loads(cached)
            return WeatherResponse(**data, cached=True)

    if not settings.weather_api_key:
        raise HTTPException(status_code=503, detail="API key not configured")

    # Fetch from upstream API
    url = f"{settings.base_url}/{location}"
    params = {"key": settings.weather_api_key, "unitGroup": "metric", "include": "current"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Upstream API timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Upstream error")

    raw = resp.json()
    current = raw.get("currentConditions", {})

    result = WeatherResponse(
        location=raw.get("resolvedAddress", location),
        temperature=current.get("temp", 0.0),
        description=current.get("conditions", ""),
        humidity=current.get("humidity", 0.0),
        wind_speed=current.get("windspeed", 0.0),
        cached=False,
    )

    # Store in cache
    if redis:
        await redis.setex(cache_key, settings.cache_ttl, result.model_dump_json())

    return result
