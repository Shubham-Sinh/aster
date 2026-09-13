import { useState } from "react";

function CurrentWeather() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getWeather = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setWeather(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/weather/${encodeURIComponent(city)}`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch weather.");
      }

      const data = await response.json();

      if (typeof data === "string") {
        throw new Error(data);
      }

      setWeather(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-page">

      <h1>🌡️ Current Weather</h1>

      <p>
        Get real-time weather information for your city.
      </p>

      <div className="weather-search">
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <button onClick={getWeather}>
          {loading ? "Loading..." : "Get Weather"}
        </button>
      </div>

      {error && (
        <p className="error-message">
          ❌ {error}
        </p>
      )}

      {weather && (
        <div className="weather-result">

          <h2>📍 {weather.city}</h2>

          <div className="weather-data">

            <div>
              <span>🌡️</span>
              <strong>{weather.temperature}°C</strong>
              <p>Temperature</p>
            </div>

            <div>
              <span>💧</span>
              <strong>{weather.humidity}%</strong>
              <p>Humidity</p>
            </div>

            <div>
              <span>💨</span>
              <strong>{weather.wind_speed} km/h</strong>
              <p>Wind Speed</p>
            </div>

          </div>

          <p className="coordinates">
            📍 Latitude: {weather.latitude} | Longitude:{" "}
            {weather.longitude}
          </p>

        </div>
      )}

    </div>
  );
}

export default CurrentWeather;