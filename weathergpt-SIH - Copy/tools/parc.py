"""import requests
import json
from langchain_core.tools import tool
@tool
def weather_tool(city):
    Get current weather information.
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params={
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    output = data["results"][0]
    #request=requests.get(url,params=param)
    #responces=request.json()
    print("step1")
   # output=responces["results"][0]
    print("step2")
    return{
        "city": output["name"], 
        "latitude":output["latitude"],
        "longitude":output["longitude"]
    }
#outut=weather_tool("delhi")
#print(outut) 
import requests
from langchain_core.tools import tool

@tool
def weather_tool(city: str):
    Get current weather and coordinates for a given city.
    clean_city = city.replace("?", "").strip()
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_city}&count=1&language=en&format=json"
    data = requests.get(url).json()
    
    if "results" not in data or not data["results"]:
        return f"Could not find location {city}"
        
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    
    # Current weather fetch karo
    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    w_res = requests.get(w_url).json()
    curr = w_res.get("current", {})
    
    return {
        "city": data["results"][0]["name"],
        "latitude": lat,
        "longitude": lon,
        "temperature": curr.get("temperature_2m"),
        "humidity": curr.get("relative_humidity_2m"),
        "wind_speed": curr.get("wind_speed_10m")
    } """
import requests
from langchain_core.tools import tool


@tool
def weather_tool(city: str):
    """Get current weather details and coordinates for a given city."""

    clean_city = city.replace("?", "").replace(",", "").strip()

    # -----------------------------
    # 1. Find city coordinates
    # -----------------------------
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
        return f"Unable to connect to weather service: {str(e)}"

    except ValueError:
        return "Invalid response received from weather service."


    # -----------------------------
    # 2. Check location
    # -----------------------------
    if "results" not in geo_res or not geo_res["results"]:
        return f"Location '{city}' not found."


    first = geo_res["results"][0]

    lat = float(first["latitude"])
    lon = float(first["longitude"])


    # -----------------------------
    # 3. Get current weather
    # -----------------------------
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        )
    }

    try:
        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=15
        )

        weather_response.raise_for_status()
        weather_res = weather_response.json()

    except requests.exceptions.Timeout:
        return "Weather forecast service timed out. Please try again."

    except requests.exceptions.RequestException as e:
        return f"Unable to get weather data: {str(e)}"

    except ValueError:
        return "Invalid weather data received."


    # -----------------------------
    # 4. Extract current weather
    # -----------------------------
    curr = weather_res.get("current", {})


    return {
        "city": first["name"],
        "latitude": lat,
        "longitude": lon,
        "temperature": curr.get("temperature_2m"),
        "humidity": curr.get("relative_humidity_2m"),
        "wind_speed": curr.get("wind_speed_10m")
    }