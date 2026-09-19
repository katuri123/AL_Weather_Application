import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    WEATHER_UNITS = os.getenv("WEATHER_UNITS", "metric")
    REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_CITY_LENGTH = 100
