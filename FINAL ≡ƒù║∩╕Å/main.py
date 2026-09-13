"""
Weather Map backend — FastAPI

Aggregates data from free, keyless APIs for a given coordinate:
  - Open-Meteo Forecast API      (current + hourly + daily weather)
  - Open-Meteo Air Quality API   (AQI + pollutants)
  - Open-Meteo Flood API         (river discharge -> flood risk estimate)
  - Open-Meteo Geocoding API     (city search)
  - BigDataCloud reverse geocode (place name for a lat/lon)

Run locally:
    pip install fastapi uvicorn httpx
    uvicorn main:app --reload --port 8000

Then point the frontend's API_BASE at http://localhost:8000
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI(title="Weather Map API")

# Allow the browser-based frontend (any origin, since this runs locally / behind your own domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TIMEOUT = httpx.Timeout(8.0)

# Reuse one connection pool across requests instead of opening a new one each time — this is
# the biggest lever for cutting latency on repeated calls (TLS/connection setup is expensive).
_client: httpx.AsyncClient | None = None


@app.on_event("startup")
async def startup():
    global _client
    _client = httpx.AsyncClient(timeout=TIMEOUT)


@app.on_event("shutdown")
async def shutdown():
    if _client:
        await _client.aclose()


def aqi_category(aqi):
    if aqi is None:
        return None
    if aqi <= 50:
        return {"label": "Good", "color": "#2A9D6F"}
    if aqi <= 100:
        return {"label": "Moderate", "color": "#E9C46A"}
    if aqi <= 150:
        return {"label": "Unhealthy for sensitive groups", "color": "#F4A261"}
    if aqi <= 200:
        return {"label": "Unhealthy", "color": "#E76F51"}
    if aqi <= 300:
        return {"label": "Very unhealthy", "color": "#9C2C77"}
    return {"label": "Hazardous", "color": "#6A0136"}


def flood_risk(discharge, mean):
    if discharge is None or mean is None or mean == 0:
        return {"level": "unknown", "color": "#94A3B8", "ratio": None}
    ratio = discharge / mean
    if ratio < 1.3:
        level, color = "low", "#2A9D6F"
    elif ratio < 2:
        level, color = "moderate", "#F4A261"
    else:
        level, color = "high", "#E76F51"
    return {"level": level, "color": color, "ratio": round(ratio, 2)}


def flood_trend(discharge_series):
    """
    Simple directional outlook from the flood model's own forecast (not a separate
    prediction model) — compares day 0 to day 2 of the river discharge forecast.
    """
    if not discharge_series or len(discharge_series) < 3:
        return None
    d0, d2 = discharge_series[0], discharge_series[2]
    if d0 is None or d2 is None or d0 == 0:
        return None
    change = (d2 - d0) / d0
    if change > 0.15:
        return {"direction": "rising", "change_pct": round(change * 100)}
    if change < -0.15:
        return {"direction": "falling", "change_pct": round(change * 100)}
    return {"direction": "steady", "change_pct": round(change * 100)}


# GDACS disaster type -> icon + label (earthquakes are handled separately via USGS, below)
DISASTER_TYPES = {
    "FL": {"icon": "🌊", "label": "Flood"},
    "TC": {"icon": "🌀", "label": "Tropical cyclone"},
    "WF": {"icon": "🔥", "label": "Wildfire"},
    "VO": {"icon": "🌋", "label": "Volcanic activity"},
    "DR": {"icon": "🏜️", "label": "Drought"},
}


async def fetch_json(client, url, params=None):
    try:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


@app.get("/api/geocode")
async def geocode(q: str = Query(..., min_length=1), count: int = 5):
    """Search for a place by name."""
    client = _client
    data = await fetch_json(
        client,
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": q, "count": count, "language": "en", "format": "json"},
    )
    if not data or not data.get("results"):
        return {"results": []}
    results = [
        {
            "name": r["name"],
            "admin1": r.get("admin1"),
            "country": r.get("country"),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
        }
        for r in data["results"]
    ]
    return {"results": results}


@app.get("/api/location")
async def location_data(lat: float, lon: float, name: str | None = None):
    """
    Given a coordinate (e.g. from a map click), return aggregated:
    place name, current + hourly + daily weather, air quality, and flood risk.
    This is the endpoint the map click flow calls.
    """
    client = _client
    weather_task = fetch_json(
        client,
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                       "wind_speed_10m,rain,weather_code,pressure_msl,is_day",
            "hourly": "temperature_2m,weather_code,precipitation_probability,visibility",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",
            "forecast_days": 5,
        },
    )
    air_task = fetch_json(
        client,
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        {
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi,pm2_5,pm10,ozone,nitrogen_dioxide",
            "timezone": "auto",
        },
    )
    flood_task = fetch_json(
        client,
        "https://flood-api.open-meteo.com/v1/flood",
        {
            "latitude": lat,
            "longitude": lon,
            "daily": "river_discharge,river_discharge_mean",
            "forecast_days": 5,
            "timezone": "auto",
        },
    )
    reverse_task = fetch_json(
        client,
        "https://api.bigdatacloud.net/data/reverse-geocode-client",
        {"latitude": lat, "longitude": lon, "localityLanguage": "en"},
    )

    weather, air, flood, reverse = await asyncio.gather(
        weather_task, air_task, flood_task, reverse_task
    )

    if weather is None:
        raise HTTPException(status_code=502, detail="Weather data unavailable")

    # --- resolve place name ---
    place_name = name
    if not place_name and reverse:
        parts = [
            reverse.get("city") or reverse.get("locality"),
            reverse.get("principalSubdivision"),
            reverse.get("countryName"),
        ]
        place_name = ", ".join([p for p in parts if p]) or "Selected location"
    if not place_name:
        place_name = "Selected location"

    # --- current + hourly ---
    current = weather.get("current", {})
    hourly_raw = weather.get("hourly", {})
    hourly = []
    if hourly_raw.get("time"):
        now_hour = current.get("time", "")[:13]
        try:
            start = hourly_raw["time"].index(now_hour + ":00")
        except ValueError:
            start = 0
        for i in range(start, min(start + 24, len(hourly_raw["time"]))):
            hourly.append({
                "time": hourly_raw["time"][i],
                "temperature": hourly_raw["temperature_2m"][i],
                "weather_code": hourly_raw["weather_code"][i],
                "precipitation_probability": hourly_raw.get("precipitation_probability", [None])[i]
                    if i < len(hourly_raw.get("precipitation_probability", [])) else None,
            })
    visibility_now = hourly[0]["time"] and hourly_raw.get("visibility", [None])[start] if hourly_raw.get("time") else None

    daily_raw = weather.get("daily", {})
    daily = []
    if daily_raw.get("time"):
        for i, d in enumerate(daily_raw["time"]):
            daily.append({
                "date": d,
                "weather_code": daily_raw["weather_code"][i],
                "max": daily_raw["temperature_2m_max"][i],
                "min": daily_raw["temperature_2m_min"][i],
                "precipitation_probability": daily_raw["precipitation_probability_max"][i],
            })

    # --- air quality ---
    air_quality = None
    if air and air.get("current"):
        aqi = air["current"].get("us_aqi")
        air_quality = {
            "aqi": aqi,
            "pm2_5": air["current"].get("pm2_5"),
            "pm10": air["current"].get("pm10"),
            "ozone": air["current"].get("ozone"),
            "category": aqi_category(aqi),
        }

    # --- flood risk (+ short outlook from the model's own forward forecast) ---
    flood_info = None
    if flood and flood.get("daily") and flood["daily"].get("river_discharge"):
        discharge_list = flood["daily"]["river_discharge"]
        mean_list = flood["daily"].get("river_discharge_mean", [])
        discharge = discharge_list[0] if discharge_list else None
        mean = mean_list[0] if mean_list else None
        risk = flood_risk(discharge, mean)
        flood_info = {"discharge": discharge, "mean": mean, **risk, "trend": flood_trend(discharge_list)}

    return {
        "name": place_name,
        "latitude": lat,
        "longitude": lon,
        "current": current,
        "visibility": visibility_now,
        "hourly": hourly,
        "daily": daily,
        "air_quality": air_quality,
        "flood": flood_info,
    }


@app.get("/api/disaster-alerts")
async def disaster_alerts(days: int = 7):
    """
    Real, reported disaster events (not a model estimate) from GDACS —
    the EU JRC's Global Disaster Alert and Coordination System.
    Covers floods, tropical cyclones, wildfires, volcanic activity, and drought.
    Sourced from government reports, media, and satellite mapping.
    (Earthquakes are handled separately via USGS — see /api/earthquakes — since
    that feed is faster-updating and more granular.)
    """
    from datetime import date, timedelta
    today = date.today()
    fromdate = today - timedelta(days=days)
    client = _client
    data = await fetch_json(
        client,
        "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH",
        {
            "eventlist": "FL;TC;WF;VO;DR",
            "fromdate": fromdate.isoformat(),
            "todate": today.isoformat(),
            "alertlevel": "green;orange;red",
        },
    )
    if not data or not data.get("features"):
        return {"alerts": []}

    alerts = []
    for f in data["features"]:
        props = f.get("properties", {})
        geom = f.get("geometry", {})
        coords = geom.get("coordinates")
        if not coords or len(coords) < 2:
            continue
        etype = props.get("eventtype", "FL")
        meta = DISASTER_TYPES.get(etype, {"icon": "⚠️", "label": "Disaster event"})
        alerts.append({
            "type": etype,
            "icon": meta["icon"],
            "label": meta["label"],
            "name": props.get("eventname") or props.get("name") or meta["label"],
            "country": props.get("country"),
            "alert_level": (props.get("alertlevel") or "green").lower(),
            "from_date": props.get("fromdate"),
            "to_date": props.get("todate"),
            "url": props.get("url", {}).get("report") if isinstance(props.get("url"), dict) else props.get("url"),
            "latitude": coords[1],
            "longitude": coords[0],
        })
    return {"alerts": alerts}


@app.get("/api/earthquakes")
async def earthquakes(min_magnitude: float = 4.5, period: str = "week"):
    """
    Real-time earthquake feed from USGS (updates continuously, no key needed).
    period: hour | day | week | month
    """
    period = period if period in ("hour", "day", "week", "month") else "week"
    feed_mag = "significant" if min_magnitude >= 6 else ("4.5" if min_magnitude >= 4.5 else "2.5")
    client = _client
    data = await fetch_json(
        client,
        f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed_mag}_{period}.geojson",
    )
    if not data or not data.get("features"):
        return {"earthquakes": []}

    quakes = []
    for f in data["features"]:
        props = f.get("properties", {})
        geom = f.get("geometry", {})
        coords = geom.get("coordinates")
        mag = props.get("mag")
        if not coords or len(coords) < 2 or mag is None or mag < min_magnitude:
            continue
        quakes.append({
            "magnitude": mag,
            "place": props.get("place"),
            "time": props.get("time"),  # epoch ms
            "depth_km": coords[2] if len(coords) > 2 else None,
            "url": props.get("url"),
            "latitude": coords[1],
            "longitude": coords[0],
        })
    quakes.sort(key=lambda q: q["magnitude"], reverse=True)
    return {"earthquakes": quakes}


@app.get("/health")
async def health():
    return {"status": "ok"}
