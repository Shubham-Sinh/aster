import { useState } from "react";

function Alerts() {
  const [city, setCity] = useState("Delhi");
  const [forecast, setForecast] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkAlerts = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setAlerts([]);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/forecast/${encodeURIComponent(city)}?days=3`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch forecast.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setForecast(data);

      const hourly = data.forecast?.hourly || {};
      const generatedAlerts = [];

      const temperatures = hourly.temperature_2m || [];
      const rainfall = hourly.rain || [];
      const wind = hourly.wind_speed_10m || {};

      const maxTemp =
        temperatures.length > 0 ? Math.max(...temperatures) : 0;

      const maxRain =
        rainfall.length > 0 ? Math.max(...rainfall) : 0;

      const windValues = Array.isArray(wind) ? wind : [];
      const maxWind =
        windValues.length > 0 ? Math.max(...windValues) : 0;

      // Heavy rain
      if (maxRain >= 10) {
        generatedAlerts.push({
          type: "danger",
          icon: "🌧️",
          title: "Heavy Rain Alert",
          message:
            "Heavy rainfall may occur. Farmers should protect harvested crops and check field drainage."
        });
      }

      // High temperature
      if (maxTemp >= 38) {
        generatedAlerts.push({
          type: "warning",
          icon: "🌡️",
          title: "Heat Alert",
          message:
            "High temperature is expected. Increase irrigation monitoring and protect crops from heat stress."
        });
      }

      // Strong wind
      if (maxWind >= 40) {
        generatedAlerts.push({
          type: "warning",
          icon: "💨",
          title: "Strong Wind Alert",
          message:
            "Strong winds may damage crops. Secure agricultural equipment and monitor vulnerable crops."
        });
      }

      // Normal conditions
      if (generatedAlerts.length === 0) {
        generatedAlerts.push({
          type: "safe",
          icon: "✅",
          title: "No Major Weather Alert",
          message:
            "No major weather risk was detected from the available 3-day forecast. Continue monitoring weather updates."
        });
      }

      setAlerts(generatedAlerts);
    } catch (err) {
      setError(err.message);
      setForecast(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-page alerts-page">

      <div className="page-heading">
        <h1>🚨 Weather Alerts</h1>
        <p>
          Get important weather warnings and farmer advisories
          based on the forecast.
        </p>
      </div>

      {/* SEARCH */}

      <div className="weather-search alerts-search">

        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              checkAlerts();
            }
          }}
        />

        <button onClick={checkAlerts} disabled={loading}>
          {loading ? "Checking..." : "Check Alerts"}
        </button>

      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {/* ALERTS */}

      {alerts.length > 0 && (

        <div className="alerts-container">

          <div className="alerts-location">
            📍 Weather alerts for <strong>{forecast?.city}</strong>
          </div>

          {alerts.map((alert, index) => (

            <div
              key={index}
              className={`alert-card ${alert.type}`}
            >

              <div className="alert-icon">
                {alert.icon}
              </div>

              <div className="alert-content">

                <h2>{alert.title}</h2>

                <p>{alert.message}</p>

              </div>

            </div>

          ))}

        </div>
      )}

      {/* FARMER ADVISORY */}

      <div className="alerts-advisory">

        <h2>👨‍🌾 General Farmer Advisory</h2>

        <div className="advisory-grid">

          <div>
            <span>🌧️</span>
            <h3>Rain</h3>
            <p>
              Avoid unnecessary irrigation when significant rainfall
              is expected.
            </p>
          </div>

          <div>
            <span>🌡️</span>
            <h3>Heat</h3>
            <p>
              Monitor soil moisture and provide irrigation when
              crops require it.
            </p>
          </div>

          <div>
            <span>💨</span>
            <h3>Wind</h3>
            <p>
              Secure loose equipment and protect crops vulnerable
              to strong winds.
            </p>
          </div>

          <div>
            <span>📱</span>
            <h3>Stay Updated</h3>
            <p>
              Always verify severe-weather warnings with official
              local authorities.
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Alerts;