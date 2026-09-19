"""HTTP routes for weather lookups."""
from flask import Blueprint, current_app, jsonify, render_template, request

from app.services.groq_service import GroqServiceError, explain_weather
from app.services.weather_service import WeatherServiceError, get_current_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.get("/")
def index():
    return render_template("index.html")


@weather_bp.post("/api/weather")
def weather():
    payload = request.get_json(silent=True) or {}
    city = str(payload.get("city", "")).strip()
    if not city:
        return jsonify(error="Enter a city name to search."), 400
    if len(city) > current_app.config["MAX_CITY_LENGTH"]:
        return jsonify(error="City names must be 100 characters or fewer."), 400

    try:
        conditions = get_current_weather(city, current_app.config)
    except WeatherServiceError as exc:
        current_app.logger.warning("Weather lookup failed: %s", exc)
        return jsonify(error=str(exc)), exc.status_code

    response = {"weather": conditions, "ai_explanation": None, "ai_available": False}
    try:
        response["ai_explanation"] = explain_weather(conditions, current_app.config)
        response["ai_available"] = True
    except GroqServiceError as exc:
        # Weather facts remain useful when the optional explanation service fails.
        current_app.logger.warning("Groq explanation failed: %s", exc)
        response["ai_error"] = str(exc)

    return jsonify(response)
