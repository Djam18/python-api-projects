import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("WEATHER_API_KEY", "")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
