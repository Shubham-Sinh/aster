import React, { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

// const API_BASE_URL = "https://aster-4.onrender.com";
const API_BASE_URL = "https://aster-4.onrender.com";

function MapMover({ location }) {
  const map = useMap();

  if (location) {
    map.flyTo(
      [location.latitude, location.longitude],
      10,
      { duration: 1.5 }
    );
  }

  return null;
}

function WeatherMap() {
  const [city, setCity] = useState("");
  const [location, setLocation] = useState(null);
  const [weather, setWeather] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const defaultPosition = [22.9734, 78.6569];

  const searchLocation = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setWeather(null);

    try {
      // -----------------------------
      // 1. SEARCH LOCATION
      // -----------------------------

      const locationResponse = await fetch(
        `${API_BASE_URL}/api/geocode?q=${encodeURIComponent(
          city
        )}&count=1`
      );

      if (!locationResponse.ok) {
        throw new Error("Location search failed");
      }

      const locationData = await locationResponse.json();

      if (
        !locationData.results ||
        locationData.results.length === 0
      ) {
        setError("Location not found.");
        return;
      }

      const result = locationData.results[0];

      const searchedLocation = {
        name: result.name,
        latitude: Number(result.latitude),
        longitude: Number(result.longitude),
      };

      setLocation(searchedLocation);

      // -----------------------------
      // 2. GET CURRENT WEATHER
      // -----------------------------

      const weatherResponse = await fetch(
        `${API_BASE_URL}/weather/${encodeURIComponent(
          searchedLocation.name
        )}`
      );

      if (!weatherResponse.ok) {
        throw new Error("Weather request failed");
      }

      const weatherData = await weatherResponse.json();

      if (weatherData.error) {
        throw new Error(weatherData.error);
      }

      setWeather(weatherData);

    } catch (err) {
      console.error("WEATHER MAP ERROR:", err);

      setError(
        err.message ||
        "Unable to get weather information."
      );

    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      searchLocation();
    }
  };

  return (
    <div className="weather-map-page">

      {/* HEADER */}
      <div className="weather-map-header">
        <h1>Weather Map</h1>

        <p>
          Explore weather conditions across different locations
        </p>
      </div>

      {/* SEARCH */}
      <div className="map-search-box">

        <input
          type="text"
          placeholder="Search city..."
          value={city}
          onChange={(event) =>
            setCity(event.target.value)
          }
          onKeyDown={handleKeyDown}
        />

        <button onClick={searchLocation}>
          {loading ? "Loading..." : "Search"}
        </button>

      </div>

      {/* ERROR */}
      {error && (
        <div className="map-error">
          {error}
        </div>
      )}

      {/* WEATHER CARD */}
      {weather && (
        <div className="map-weather-card">

          <h2>
            {weather.city}
          </h2>

          <div className="weather-details">

            <div className="weather-item">
              <span>🌡️</span>
              <div>
                <small>Temperature</small>
                <strong>
                  {weather.temperature} °C
                </strong>
              </div>
            </div>

            <div className="weather-item">
              <span>💧</span>
              <div>
                <small>Humidity</small>
                <strong>
                  {weather.humidity} %
                </strong>
              </div>
            </div>

            <div className="weather-item">
              <span>💨</span>
              <div>
                <small>Wind Speed</small>
                <strong>
                  {weather.wind_speed} km/h
                </strong>
              </div>
            </div>

          </div>

        </div>
      )}

      {/* MAP */}
      <div className="weather-map-container">

        <MapContainer
          center={defaultPosition}
          zoom={5}
          scrollWheelZoom={true}
          style={{
            height: "100%",
            width: "100%",
          }}
        >

          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {location && (
            <>
              <MapMover
                location={location}
              />

              <Marker
                position={[
                  location.latitude,
                  location.longitude,
                ]}
              >

                <Popup>
                  <strong>
                    {location.name}
                  </strong>

                  <br />

                  Temperature:{" "}
                  {weather?.temperature ?? "--"} °C

                  <br />

                  Humidity:{" "}
                  {weather?.humidity ?? "--"} %

                  <br />

                  Wind:{" "}
                  {weather?.wind_speed ?? "--"} km/h
                </Popup>

              </Marker>
            </>
          )}

        </MapContainer>

      </div>

    </div>
  );
}

export default WeatherMap;