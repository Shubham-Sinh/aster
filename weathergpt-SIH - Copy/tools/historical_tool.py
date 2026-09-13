import requests
import json
from datetime import date,timedelta
from .parc import weather_tool
from langchain_core.tools import tool
import requests
import json
from langchain_core.tools import tool

@tool
def history_tool(latitude: float, longitude: float, days: int = 7) -> str:
    """Get historical / past weather data for given latitude, longitude, and past days count."""
    try:
        # Recent past days ke liye standard API with past_days parameter best hoti hai
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "past_days": days,
            "forecast_days": 1,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "daily" in data:
            daily_data = data["daily"]
            # Sirf past days ka data filter karein
            return json.dumps({
                "dates": daily_data.get("time", [])[:days],
                "max_temperatures": daily_data.get("temperature_2m_max", [])[:days],
                "min_temperatures": daily_data.get("temperature_2m_min", [])[:days]
            })
        else:
            return f"Weather API Error: {data.get('reason', 'Could not fetch past weather data')}"

    except Exception as e:
        return f"Tool Execution Error: {str(e)}"
"""
@tool
def history_tool(days:int,latitude,longitude):
       Get historical weather data for a location.
       url = "https://archive-api.open-meteo.com/v1/archive"
       end_date=date.today()-timedelta(days=1)
       start_date=end_date-timedelta(days=days-1)
       param={
              "latitude":latitude,
              "longitude":longitude,
               "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
              "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max", 
              "timezone":"auto",
               
       }
       request=requests.get(url,params=param)
       responces=request.json()
       return {
            "output_between":responces["daily"]
   }

city_name=input("Enter the city name:")
days=int(input("Enter the previeus day output:"))
output_hip=weather_tool.invoke({
       "city":city_name
})
latitude=output_hip["latitude"]
longitude=output_hip["longitude"]
history_answer=history_tool.invoke({
       "days":days,
       "latitude":latitude,
       "longitude":longitude
})
print(history_answer)
"""

   