import requests
from langchain_core.tools import tool


@tool
def forcast_weather(days: int, latitude: float, longitude: float):
    """Get weather forecast information for given days, latitude, and longitude."""

    url = "https://api.open-meteo.com/v1/forecast"

    forecast_days = min(max(int(days), 1), 7)

    params = {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "forecast_days": forecast_days,
        "timezone": "auto",

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),

        "hourly": (
            "rain,"
            "temperature_2m,"
            "relative_humidity_2m,"
            "pressure_msl,"
            "wind_speed_10m,"
            "cloud_cover"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "precipitation_sum"
        )
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    if response.status_code == 429:
        raise ValueError(
            "Open-Meteo rate limit reached. Please try again later."
        )

    response.raise_for_status()

    data = response.json()

    return {
        "current": data.get("current", {}),
        "hourly": data.get("hourly", {}),
        "daily": data.get("daily", {})
    }