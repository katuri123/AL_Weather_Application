"""Small, isolated Groq client for factual-weather explanations."""
from groq import Groq


class GroqServiceError(Exception):
    pass


def explain_weather(weather, config):
    api_key = config.get("GROQ_API_KEY")
    if not api_key:
        raise GroqServiceError("AI explanation is unavailable because Groq is not configured.")
    prompt = (
        "Explain these current weather conditions in 2 concise, friendly sentences. "
        "Use only supplied facts. Do not forecast, add measurements, give medical advice, "
        "or describe this as an official alert. Missing values are unavailable.\n\n"
        f"Location: {weather['location']}, {weather.get('country') or 'unknown'}\n"
        f"Temperature: {weather['temperature']} {weather['temperature_unit']}; "
        f"Feels like: {weather.get('feels_like')} {weather['temperature_unit']}\n"
        f"Condition: {weather.get('description')}\nHumidity: {weather.get('humidity')}%\n"
        f"Wind: {weather.get('wind_speed')} {weather['wind_unit']}, {weather.get('wind_direction')}"
    )
    try:
        client = Groq(api_key=api_key, timeout=config["REQUEST_TIMEOUT"])
        completion = client.chat.completions.create(
            model=config["GROQ_MODEL"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=130,
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("Empty Groq response")
        return content.strip()
    except Exception as exc:
        raise GroqServiceError("AI explanation is temporarily unavailable.") from exc
