"""Weather-provider client and response normalization."""
from datetime import datetime, timezone

import requests


class WeatherServiceError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def _wind_direction(degrees):
    if degrees is None:
        return None
    directions = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    return directions[round(float(degrees) / 45) % 8]


def get_current_weather(city, config):
    """Fetch and normalize OpenWeather current conditions for *city*."""
    api_key = config.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError("Weather service is not configured. Add OPENWEATHER_API_KEY.", 503)

    try:
        response = requests.get(
            config["OPENWEATHER_URL"],
            params={"q": city, "appid": api_key, "units": config["WEATHER_UNITS"]},
            timeout=config["REQUEST_TIMEOUT"],
        )
    except requests.Timeout as exc:
        raise WeatherServiceError("The weather service timed out. Please try again.", 504) from exc
    except requests.RequestException as exc:
        raise WeatherServiceError("Could not reach the weather service. Please try again.") from exc

    if response.status_code == 404:
        raise WeatherServiceError("City not found. Try adding a country code, such as 'Paris, FR'.", 404)
    if response.status_code in (401, 403):
        raise WeatherServiceError("Weather service authentication failed.", 503)
    if response.status_code == 429:
        raise WeatherServiceError("Weather service rate limit reached. Please try again shortly.", 429)
    if not response.ok:
        raise WeatherServiceError("Weather service is currently unavailable. Please try again.")

    try:
        data = response.json()
        main, wind = data["main"], data.get("wind", {})
        condition = data["weather"][0]
        observed_at = datetime.fromtimestamp(data["dt"], tz=timezone.utc).isoformat()
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherServiceError("The weather service returned incomplete data. Please try again.") from exc

    unit = "°C" if config["WEATHER_UNITS"] == "metric" else "°F"
    wind_unit = "m/s" if config["WEATHER_UNITS"] == "metric" else "mph"
    return {
        "location": data.get("name", city),
        "country": data.get("sys", {}).get("country"),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "temperature_unit": unit,
        "condition": condition.get("main"),
        "description": condition.get("description"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "wind_direction": _wind_direction(wind.get("deg")),
        "wind_unit": wind_unit,
        "observed_at": observed_at,
        "timezone_offset": data.get("timezone", 0),
        "source": "OpenWeather",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
