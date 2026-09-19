from app.services.weather_service import WeatherServiceError, get_current_weather


def test_missing_weather_key_is_a_configuration_error():
    try:
        get_current_weather("Delhi", {"OPENWEATHER_API_KEY": None})
    except WeatherServiceError as exc:
        assert exc.status_code == 503
    else:
        assert False
