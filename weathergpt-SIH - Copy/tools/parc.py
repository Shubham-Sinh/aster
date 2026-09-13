import requests
from langchain_core.tools import tool


@tool
def weather_tool(city: str):
    """Find city coordinates using Open-Meteo geocoding."""

    clean_city = city.replace("?", "").replace(",", "").strip()

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": clean_city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=15
        )

        geo_response.raise_for_status()
        geo_res = geo_response.json()

    except requests.exceptions.Timeout:
        return "Weather service timed out. Please try again."

    except requests.exceptions.RequestException as e:
        return f"Unable to connect to location service: {str(e)}"

    except ValueError:
        return "Invalid response received from location service."

    if "results" not in geo_res or not geo_res["results"]:
        return f"Location '{city}' not found."

    first = geo_res["results"][0]

    return {
        "city": first["name"],
        "latitude": float(first["latitude"]),
        "longitude": float(first["longitude"])
    }