import requests
import json
from .parc import weather_tool
from langchain_core.tools import tool
@tool
def weather_output(lagtitude:str,longitude:str):
    """Find the latitude and longitude of a location."""
    url = "https://api.open-meteo.com/v1/forecast"
    param={
        "days":int,
        "latitude":lagtitude,
        "longitude":longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone":"auto"
    }
    request=requests.get(url,params=param)
    responces=request.json()
    return{
        "responces":responces["current"]
    }
"""
output_name=input("enter the name:")
print(output_name)
output_val=weather_tool(output_name)
langtitude=output_val["latitude"]
longitude=output_val["longitude"]
langwork=weather_output(langtitude,longitude)
print(langwork)

"""