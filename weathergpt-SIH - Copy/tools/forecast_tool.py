"""import requests
import json
from . parc import weather_tool
from langchain_core.tools import tool
# getting the last 7 days weather output
@tool
def forcast_weather(days:int,latitude,longitude):
    Get weather forecast information.
    url = "https://api.open-meteo.com/v1/forecast"
    param={
        "forecast_days":days,
        "latitude": latitude,
        "longitude": longitude,
        "timezone":"auto",
        "hourly":"rain , temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,cloud_cover",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",        
    }
    request=requests.get(url,params=param)
    print("Status:", request.status_code)
    print("Response:", request.text)
    responces=request.json()
    return {
        "hourly":responces["hourly"],
        "daily":responces["daily"]
    }

input_number=input("Enter the City Name:")
daYS=int(input("how much days u want forcast:"))
output=weather_tool(input_number)
langitude=output["latitude"]
longitude=output["longitude"]

responces=forcast_weather(daYS,langitude,longitude)
print(responces) 

import requests
import json
from langchain_core.tools import tool

# getting the weather output
@tool
def forcast_weather(days: int, latitude: float, longitude: float):
    Get weather forecast information for given days, latitude, and longitude.
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Notice: NO SPACES between comma-separated values in hourly
    param = {
        "forecast_days": int(days),
        "latitude": float(latitude),
        "longitude": float(longitude),
        "timezone": "auto",
        "hourly": "rain,temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,cloud_cover",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max"        
    }
    
    request = requests.get(url, params=param)
    responces = request.json()
    
    # Agar API ne error diya toh crash hone se bachaye
    if "hourly" not in responces:
        raise ValueError(f"Open-Meteo API Error: {responces.get('reason', responces)}")
    
    return {
        "hourly": responces["hourly"],
        "daily": responces.get("daily", {})
    }
"""
import requests
from langchain_core.tools import tool

@tool
def forcast_weather(days: int, latitude: float, longitude: float):
    """Get weather forecast information for given days, latitude, and longitude."""
    url = "https://api.open-meteo.com/v1/forecast"
    
    # days agar 0 ya negative aaye toh kam se kam 1 rakho
    forecast_days = max(int(days), 1)
    
    param = {
        "forecast_days": forecast_days,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "timezone": "auto",
        "hourly": "rain,temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,cloud_cover",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    }
    
    response = requests.get(url, params=param)
    res = response.json()
    
    return {
        "hourly": res.get("hourly", {}),
        "daily": res.get("daily", {})
    }