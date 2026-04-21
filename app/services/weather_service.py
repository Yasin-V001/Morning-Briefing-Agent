import httpx
from app.config import settings
from app.schemas import WeatherSummary
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)


WEATHER_CODE_MAP = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
}


async def fetch_weather_summary() -> WeatherSummary:
    params = {
        "latitude": settings.weather_latitude,
        "longitude": settings.weather_longitude,
        "current": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": settings.timezone,
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(settings.weather_api_base_url, params=params)
        response.raise_for_status()
        data = response.json()

    current_temp_c = data.get("current", {}).get("temperature_2m")
    current_temp_f = None
    if current_temp_c is not None:
        current_temp_f = round((current_temp_c * 9 / 5) + 32, 1)

    weather_code = data.get("current", {}).get("weather_code")
    condition = WEATHER_CODE_MAP.get(weather_code, "Unknown")

    daily = data.get("daily", {})
    high_c = daily.get("temperature_2m_max", [None])[0]
    low_c = daily.get("temperature_2m_min", [None])[0]
    precip = daily.get("precipitation_probability_max", [None])[0]

    logger.info("Weather summary fetched successfully.")

    return WeatherSummary(
        current_temp_c=current_temp_c,
        current_temp_f=current_temp_f,
        condition=condition,
        high_c=high_c,
        low_c=low_c,
        precipitation_probability_max=precip,
    )