"""import json
import numpy as np
import joblib
from langchain.tools import tool
from tools.forecast_tool import forcast_weather
from .rain_pred import rain_predictes
model=joblib.load("flood_nodel.pkl")
scaler=joblib.load("flood_scaler.pkl")
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# If model is in the project root:
# model = joblib.load("flood_model.pkl")
# If model is in flood_predicts/:
model = joblib.load(os.path.join(os.path.dirname(BASE_DIR), "flood_predicts", "flood_model.pkl"))
@tool
def ml_model(latitude: float, longitude: float, day: int = 1):
    Predicts flood risks based on weather forecast for a given latitude, longitude, and day offset.
    Args:
        latitude: The numerical latitude (e.g. 25.37)
        longitude: The numerical longitude (e.g. 86.47)
        day: Day forecast index, default is 1
    
    lat = float(latitude)
    lon = float(longitude)
    d = int(day)
    
    output = forcast_weather(d, lat, lon)
    output_version = rain_predictes(output)
    input_own=np.array([
        [
            output_version["rainfall_1h"],
            output_version["rainfall_6h"],
            output_version["rainfall_24h"],
            output_version["temperature"],
            output_version["humidity"],
            output_version["pressure"],
            output_version["wind_speed"],
            output_version["cloud_cover"]
        ]
    ])

    # Now convert it into scaler
    output_scaler=scaler.transform(output_scaler)
   # output_ans=model.fit_transform(output_scaler)
    output_ans=model.predict(output_ans)
    # For probility
    output_prob=model.predict_proba(output_scaler)[0][1]
    # convert into percent
    print(f"probility of flood:{output_prob*100 : .2f}%")
    return {
        output_prob
    }
"""
import os
import joblib
import numpy as np
from typing import Any
from langchain.tools import tool
from tools.forecast_tool import forcast_weather
from .rain_pred import rain_predictes
from langchain.tools import tool

# Base path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Load models
model = joblib.load(os.path.join(PROJECT_ROOT, "flood_nodel.pkl"))
scaler = joblib.load(os.path.join(PROJECT_ROOT, "flood_scaler.pkl"))


@tool
def ml_model(latitude: Any, longitude: Any, day: Any = 1):
    """Predicts flood risks based on weather forecast for a given latitude, longitude, and day offset.
    Args:
        latitude: The numerical latitude
        longitude: The numerical longitude
        day: Day forecast index, default is 1
    """
    lat = float(latitude)
    lon = float(longitude)
    d = int(day)

    output = forcast_weather.func(days=d, latitude=lat, longitude=lon)
    output_version = rain_predictes(output)

    # EXACT 9 FEATURES in order:
    input_own = np.array([
        [
            float(output_version["rainfall_1h"]),
            float(output_version["rainfall_6h"]),
            float(output_version["rainfall_24h"]),
            float(output_version["rainfall_3day"]),   # <-- Missing 9th feature added
            float(output_version["temperature"]),
            float(output_version["humidity"]),
            float(output_version["pressure"]),
            float(output_version["wind_speed"]),
            float(output_version["cloud_cover"])
        ]
    ])

    # 1. Transform with scaler
    output_scaler = scaler.transform(input_own)

    # 2. Model prediction
    output_ans = model.predict(output_scaler)

    # 3. Model probability
    output_prob = float(model.predict_proba(output_scaler)[0][1])

    print(f"probability of flood: {output_prob * 100:.2f}%")

    return f"Flood prediction: Risk flag {output_ans[0]}, Probability: {output_prob * 100:.2f}%"