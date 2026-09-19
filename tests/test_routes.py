from app import create_app


class TestConfig:
    TESTING = True
    MAX_CITY_LENGTH = 100
    OPENWEATHER_API_KEY = None
    GROQ_API_KEY = None


def test_empty_city_is_rejected():
    client = create_app(TestConfig).test_client()
    response = client.post("/api/weather", json={"city": " "})
    assert response.status_code == 400
    assert "city" in response.get_json()["error"].lower()
