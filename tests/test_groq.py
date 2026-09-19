from app.services.groq_service import GroqServiceError, explain_weather


def test_missing_groq_key_is_handled():
    try:
        explain_weather({"location": "Delhi"}, {"GROQ_API_KEY": None})
    except GroqServiceError:
        pass
    else:
        assert False
