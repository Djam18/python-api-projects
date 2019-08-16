"""Tests for weather-api."""
import json
import pytest
from unittest.mock import patch, MagicMock


MOCK_WEATHER_RESPONSE = {
    "address": "London",
    "currentConditions": {
        "temp": 15.5,
        "feelslike": 13.0,
        "humidity": 72,
        "conditions": "Partly cloudy",
    }
}


class TestHealthEndpoints:
    def test_index_returns_200(self, client):
        res = client.get('/')
        assert res.status_code == 200

    def test_index_returns_weather_api_message(self, client):
        data = json.loads(res := client.get('/'))
        res = client.get('/')
        data = json.loads(res.data)
        assert "Weather API" in data['message']

    def test_health_returns_ok(self, client):
        res = client.get('/health')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['status'] == 'ok'


class TestWeatherEndpoint:
    def test_cache_miss_calls_external_api(self, client, mock_redis):
        mock_redis.get.return_value = None

        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = MOCK_WEATHER_RESPONSE
            mock_get.return_value = mock_response

            res = client.get('/weather/london')
            assert res.status_code == 200
            data = json.loads(res.data)
            assert data['city'] == 'London'
            assert data['X-Cache'] == 'MISS'

    def test_cache_hit_returns_cached_data(self, client, mock_redis):
        cached = json.dumps({
            "city": "London",
            "temp": 15.5,
            "feels_like": 13.0,
            "humidity": 72,
            "description": "Partly cloudy",
        })
        mock_redis.get.return_value = cached

        res = client.get('/weather/london')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['X-Cache'] == 'HIT'
        assert data['city'] == 'London'

    def test_invalid_city_returns_404(self, client, mock_redis):
        mock_redis.get.return_value = None

        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            res = client.get('/weather/invalidcityxyz')
            assert res.status_code == 404

    def test_weather_response_has_required_fields(self, client, mock_redis):
        mock_redis.get.return_value = None

        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = MOCK_WEATHER_RESPONSE
            mock_get.return_value = mock_response

            res = client.get('/weather/london')
            data = json.loads(res.data)
            assert 'temp' in data
            assert 'humidity' in data
            assert 'description' in data

    def test_cache_is_set_on_cache_miss(self, client, mock_redis):
        mock_redis.get.return_value = None

        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = MOCK_WEATHER_RESPONSE
            mock_get.return_value = mock_response

            client.get('/weather/london')
            assert mock_redis.setex.called


class TestClearCache:
    def test_clear_cache_returns_200(self, client, mock_redis):
        res = client.delete('/cache/clear')
        assert res.status_code == 200

    def test_clear_cache_flushes_db(self, client, mock_redis):
        client.delete('/cache/clear')
        assert mock_redis.flushdb.called
