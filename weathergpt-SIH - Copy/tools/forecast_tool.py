import time
import requests
from langchain_core.tools import tool


@tool
def forcast_weather(days: int, latitude: float, longitude: float):
    """Get weather forecast information for given days, latitude, and longitude."""

    url = "https://api.open-meteo.com/v1/forecast"

    forecast_days = max(int(days), 1)

    param = {
        "forecast_days": forecast_days,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "timezone": "auto",
        "hourly": "rain,temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,cloud_cover",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    }

    # Try up to 3 times if Open-Meteo temporarily returns 429
    for attempt in range(3):

        response = requests.get(
            url,
            params=param,
            timeout=15
        )

        if response.status_code == 429:

            if attempt < 2:
                time.sleep(3)
                continue

            raise ValueError(
                "Open-Meteo rate limit reached. Please try again later."
            )

        response.raise_for_status()

        res = response.json()

        return {
            "hourly": res.get("hourly", {}),
            "daily": res.get("daily", {})
        }