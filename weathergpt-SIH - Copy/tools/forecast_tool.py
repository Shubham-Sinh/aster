import os
import requests
from langchain_core.tools import tool


@tool
def forcast_weather(days: int, latitude: float, longitude: float):
    """Get weather forecast using WeatherAPI."""

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        raise ValueError("WEATHER_API_KEY is not configured.")

    forecast_days = min(max(int(days), 1), 3)

    url = "https://api.weatherapi.com/v1/forecast.json"

    params = {
        "key": api_key,
        "q": f"{latitude},{longitude}",
        "days": forecast_days,
        "aqi": "no",
        "alerts": "yes"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    # -----------------------------
    # WeatherAPI -> Existing Format
    # -----------------------------

    weather_forecast = data.get("forecast", {})

    hourly_data = []
    daily_data = []

    for forecast_day in weather_forecast.get("forecastday", []):

        # Daily data
        day = forecast_day.get("day", {})

        daily_data.append({
            "time": forecast_day.get("date"),
            "temperature_2m_max": day.get("maxtemp_c"),
            "temperature_2m_min": day.get("mintemp_c"),
            "precipitation_probability_max": day.get(
                "daily_chance_of_rain"
            ),
            "precipitation_sum": day.get("totalprecip_mm")
        })

        # Hourly data
        for hour in forecast_day.get("hour", []):

            hourly_data.append({
                "time": hour.get("time"),
                "temperature_2m": hour.get("temp_c"),
                "relative_humidity_2m": hour.get("humidity"),
                "wind_speed_10m": hour.get("wind_kph"),
                "cloud_cover": hour.get("cloud"),
                "rain": hour.get("precip_mm"),
                "precipitation_probability": hour.get(
                    "chance_of_rain"
                )
            })

    return {
        "current": data.get("current", {}),

        # Compatible with existing backend
        "hourly": {
            "time": [x["time"] for x in hourly_data],
            "temperature_2m": [
                x["temperature_2m"] for x in hourly_data
            ],
            "relative_humidity_2m": [
                x["relative_humidity_2m"] for x in hourly_data
            ],
            "wind_speed_10m": [
                x["wind_speed_10m"] for x in hourly_data
            ],
            "cloud_cover": [
                x["cloud_cover"] for x in hourly_data
            ],
            "rain": [
                x["rain"] for x in hourly_data
            ],
            "precipitation_probability": [
                x["precipitation_probability"]
                for x in hourly_data
            ]
        },

        "daily": {
            "time": [x["time"] for x in daily_data],
            "temperature_2m_max": [
                x["temperature_2m_max"] for x in daily_data
            ],
            "temperature_2m_min": [
                x["temperature_2m_min"] for x in daily_data
            ],
            "precipitation_probability_max": [
                x["precipitation_probability_max"]
                for x in daily_data
            ],
            "precipitation_sum": [
                x["precipitation_sum"] for x in daily_data
            ]
        },

        "alerts": data.get("alerts", {})
    }