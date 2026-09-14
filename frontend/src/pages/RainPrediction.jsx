import { useState } from "react";

function RainPrediction() {
  const [city, setCity] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getPrediction = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/rain-prediction/${encodeURIComponent(city)}?days=3`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch rain prediction.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setPrediction(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-page">

      <h1>🌧️ Rain Prediction</h1>

      <p>
        Analyze recent rainfall and weather conditions for your area.
      </p>

      <div className="weather-search">

        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <button onClick={getPrediction}>
          {loading ? "Analyzing..." : "Predict Rain"}
        </button>

      </div>

      {error && (
        <p className="error-message">
          ❌ {error}
        </p>
      )}

      {prediction && (
        <div className="weather-result">

          <h2>📍 {prediction.city}</h2>

          <div className="rain-prediction-grid">

            <div className="rain-card">
              <span>🌧️</span>
              <p>Last 1 Hour</p>
              <strong>
                {prediction.prediction.rainfall_1h} mm
              </strong>
            </div>

            <div className="rain-card">
              <span>🌧️</span>
              <p>Last 6 Hours</p>
              <strong>
                {prediction.prediction.rainfall_6h} mm
              </strong>
            </div>

            <div className="rain-card">
              <span>🌧️</span>
              <p>Last 24 Hours</p>
              <strong>
                {prediction.prediction.rainfall_24h} mm
              </strong>
            </div>

            <div className="rain-card">
              <span>🌦️</span>
              <p>Last 3 Days</p>
              <strong>
                {prediction.prediction.rainfall_3day} mm
              </strong>
            </div>

          </div>

          <div className="rain-details">

            <h3>🌤️ Current Conditions</h3>

            <p>
              🌡️ Temperature:
              <strong> {prediction.prediction.temperature}°C</strong>
            </p>

            <p>
              💧 Humidity:
              <strong> {prediction.prediction.humidity}%</strong>
            </p>

            <p>
              💨 Wind Speed:
              <strong> {prediction.prediction.wind_speed} km/h</strong>
            </p>

            <p>
              ☁️ Cloud Cover:
              <strong> {prediction.prediction.cloud_cover}%</strong>
            </p>

            <p>
              📊 Pressure:
              <strong> {prediction.prediction.pressure} hPa</strong>
            </p>

          </div>

        </div>
      )}

    </div>
  );
}

export default RainPrediction;