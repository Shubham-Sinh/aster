from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools.parc import weather_tool
from tools.forecast_tool import forcast_weather
from tools.historical_tool import history_tool
from Agent_file.rain_pred import rain_predictes
from Agent_file.ml_agent1 import ml_model
from datetime import datetime
from Agent_file.agent_file3 import ask_weather_gpt
import requests


app = FastAPI(
    title="WeatherGPT API",
    description="AI-powered weather platform for farmers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://aster18-gamma.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/geocode")
def geocode_location(q: str, count: int = 5):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": q,
        "count": count,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        return {
            "error": "Geocoding service timed out."
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Unable to connect to geocoding service: {str(e)}"
        }

@app.get("/")
def home():
    return {"message": "WeatherGPT API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/weather/{city}")
def get_weather(city: str):
    result = weather_tool.invoke(city)
    return result

@app.get("/forecast/{city}")
def get_forecast(city: str, days: int = 7):
    try:
        # First find city's coordinates
        location = weather_tool.invoke(city)

        if isinstance(location, str):
            return {"error": location}

        # Get forecast
        result = forcast_weather.invoke({
            "days": days,
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        })

        return {
            "city": location["city"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "forecast": result
        }

    except Exception as e:
        print("FORECAST ERROR:", repr(e))
        return {
            "error": "Forecast failed",
            "details": str(e)
        }
@app.get("/historical-weather/{city}")
def get_historical_weather(city: str, days: int = 7):

    location = weather_tool.invoke(city)

    if isinstance(location, str):
        return {"error": location}

    result = history_tool.invoke({
        "days": days,
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    })

    return {
        "city": location["city"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "history": result
    }

@app.get("/rain-prediction/{city}")
def get_rain_prediction(city: str, days: int = 3):

    location = weather_tool.invoke(city)

    if isinstance(location, str):
        return {"error": location}

    forecast = forcast_weather.invoke({
        "days": days,
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    })

    rain_data = rain_predictes(forecast["hourly"])

    return {
        "city": location["city"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "prediction": rain_data
    }

@app.get("/flood-prediction/{city}")
def get_flood_prediction(city: str, day: int = 1):

    location = weather_tool.invoke(city)

    if isinstance(location, str):
        return {"error": location}

    result = ml_model.invoke({
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "day": day
    })

    return {
        "city": location["city"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "prediction": result
    }

@app.get("/weather-ai")
def weather_ai(question: str):
    if not question.strip():
        return {
            "error": "Please enter a question."
        }

    answer = ask_weather_gpt(question)

    return {
        "question": question,
        "answer": answer
    }

@app.get("/alerts/{city}")
def get_weather_alerts(city: str, days: int = 3):

    # -----------------------------
    # 1. Get city location
    # -----------------------------
    location = weather_tool.invoke(city)

    if isinstance(location, str):
        return {
            "error": location
        }

    latitude = location["latitude"]
    longitude = location["longitude"]

    # -----------------------------
    # 2. Get forecast
    # -----------------------------
    forecast = forcast_weather.invoke({
        "days": days,
        "latitude": latitude,
        "longitude": longitude
    })

    hourly = forecast.get("hourly", {})
    daily = forecast.get("daily", {})

    alerts = []

    # -----------------------------
    # Helper function
    # -----------------------------
    def add_alert(
        alert_type,
        severity,
        title,
        message,
        icon
    ):
        alerts.append({
            "type": alert_type,
            "severity": severity,
            "title": title,
            "message": message,
            "icon": icon
        })

    # ==================================================
    # 3. HEAVY RAIN ALERT
    # ==================================================

    rain_values = hourly.get("rain", [])

    if rain_values:

        max_rain = max(
            [float(x or 0) for x in rain_values]
        )

        total_rain = sum(
            [float(x or 0) for x in rain_values]
        )

        if max_rain >= 20:

            add_alert(
                "rain",
                "high",
                "Heavy Rain Alert",
                f"Heavy rainfall is possible. "
                f"Maximum hourly rainfall may reach {max_rain:.1f} mm. "
                f"Farmers should protect harvested crops and avoid unnecessary field operations.",
                "🌧️"
            )

        elif max_rain >= 10:

            add_alert(
                "rain",
                "medium",
                "Moderate Rain Alert",
                f"Moderate rainfall is expected with a maximum hourly rainfall of "
                f"{max_rain:.1f} mm. Ensure proper field drainage.",
                "🌦️"
            )

    # ==================================================
    # 4. TOTAL RAINFALL ALERT
    # ==================================================

    if rain_values:

        total_rain = sum(
            [float(x or 0) for x in rain_values]
        )

        if total_rain >= 100:

            add_alert(
                "rainfall_accumulation",
                "high",
                "High Rainfall Accumulation",
                f"Forecast rainfall accumulation may reach approximately "
                f"{total_rain:.1f} mm over the forecast period. "
                f"Low-lying agricultural areas may experience waterlogging.",
                "🌊"
            )

    # ==================================================
    # 5. EXTREME HEAT ALERT
    # ==================================================

    temperature_values = hourly.get(
        "temperature_2m",
        []
    )

    if temperature_values:

        max_temperature = max(
            [float(x or 0) for x in temperature_values]
        )

        if max_temperature >= 40:

            add_alert(
                "heat",
                "high",
                "Extreme Heat Alert",
                f"Temperature may reach {max_temperature:.1f}°C. "
                f"Farmers should avoid heavy field work during peak afternoon heat "
                f"and provide adequate water to livestock.",
                "🌡️"
            )

        elif max_temperature >= 35:

            add_alert(
                "heat",
                "medium",
                "High Temperature Alert",
                f"Temperature may reach {max_temperature:.1f}°C. "
                f"Consider irrigation during suitable hours and monitor crops for heat stress.",
                "☀️"
            )

    # ==================================================
    # 6. HIGH WIND ALERT
    # ==================================================

    wind_values = hourly.get(
        "wind_speed_10m",
        []
    )

    if wind_values:

        max_wind = max(
            [float(x or 0) for x in wind_values]
        )

        if max_wind >= 50:

            add_alert(
                "wind",
                "high",
                "Strong Wind Alert",
                f"Wind speed may reach {max_wind:.1f} km/h. "
                f"Secure agricultural equipment, young plants and temporary structures.",
                "💨"
            )

        elif max_wind >= 35:

            add_alert(
                "wind",
                "medium",
                "High Wind Alert",
                f"Wind speed may reach {max_wind:.1f} km/h. "
                f"Farmers should monitor vulnerable crops and structures.",
                "🌬️"
            )

    # ==================================================
    # 7. HIGH HUMIDITY ALERT
    # ==================================================

    humidity_values = hourly.get(
        "relative_humidity_2m",
        []
    )

    if humidity_values:

        max_humidity = max(
            [float(x or 0) for x in humidity_values]
        )

        if max_humidity >= 90:

            add_alert(
                "humidity",
                "medium",
                "High Humidity Alert",
                f"Relative humidity may reach {max_humidity:.0f}%. "
                f"High humidity can increase the risk of fungal diseases in susceptible crops.",
                "💧"
            )

    # ==================================================
    # 8. CLOUD COVER ALERT
    # ==================================================

    cloud_values = hourly.get(
        "cloud_cover",
        []
    )

    if cloud_values:

        max_cloud = max(
            [float(x or 0) for x in cloud_values]
        )

        if max_cloud >= 90:

            add_alert(
                "cloud",
                "low",
                "Very Cloudy Conditions",
                "Very high cloud cover is expected during parts of the forecast period. "
                "Sunlight availability may be lower than normal.",
                "☁️"
            )

    # ==================================================
    # 9. FLOOD ML PREDICTION
    # ==================================================

    try:

        flood_result = ml_model.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "day": 1
        })

        flood_text = str(flood_result)

        if "Probability:" in flood_text:

            probability_text = (
                flood_text
                .split("Probability:")[1]
                .replace("%", "")
                .strip()
            )

            flood_probability = float(
                probability_text
            )

            if flood_probability >= 70:

                add_alert(
                    "flood",
                    "high",
                    "High Flood Risk",
                    f"AI flood model estimates a flood probability of "
                    f"{flood_probability:.1f}%. "
                    f"Farmers in low-lying areas should monitor local warnings "
                    f"and protect livestock and agricultural equipment.",
                    "🌊"
                )

            elif flood_probability >= 40:

                add_alert(
                    "flood",
                    "medium",
                    "Moderate Flood Risk",
                    f"AI flood model estimates a flood probability of "
                    f"{flood_probability:.1f}%. "
                    f"Monitor rainfall and drainage conditions.",
                    "🌊"
                )

    except Exception as e:

        print(
            f"Flood alert model error: {e}"
        )

    # ==================================================
    # 10. SORT ALERTS BY SEVERITY
    # ==================================================

    severity_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    alerts.sort(
        key=lambda x: severity_order.get(
            x["severity"],
            4
        )
    )

    # ==================================================
    # 11. NORMAL CONDITION
    # ==================================================

    if not alerts:

        alerts.append({
            "type": "normal",
            "severity": "normal",
            "title": "No Major Weather Alert",
            "message": (
                "No major weather-related risk was detected "
                "for the selected forecast period. "
                "Continue monitoring local weather conditions."
            ),
            "icon": "🟢"
        })

    # ==================================================
    # 12. RESPONSE
    # ==================================================

    return {
        "city": location["city"],
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": days,
        "alerts": alerts,
        "alert_count": len(
            [a for a in alerts if a["severity"] != "normal"]
        )
    }