import { useState } from "react";

function Forecast() {
  const [city, setCity] = useState("");
  const [days, setDays] = useState(3);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getForecast = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setForecast(null);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/forecast/${encodeURIComponent(
          city
        )}?days=${days}`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch forecast.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setForecast(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-page">

      <h1>📅 Weather Forecast</h1>

      <p>
        Check upcoming weather conditions and plan your farming activities.
      </p>

      <div className="weather-search">

        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <select
          value={days}
          onChange={(e) => setDays(e.target.value)}
        >
          <option value="3">3 Days</option>
          <option value="5">5 Days</option>
          <option value="7">7 Days</option>
        </select>

        <button onClick={getForecast}>
          {loading ? "Loading..." : "Get Forecast"}
        </button>

      </div>

      {error && (
        <p className="error-message">
          ❌ {error}
        </p>
      )}

      {forecast && (
        <div className="weather-result">

          <h2>📍 {forecast.city}</h2>

          <div className="forecast-grid">

            {forecast.forecast.daily.time.map((date, index) => (

              <div className="forecast-card" key={date}>

                <h3>{date}</h3>

                <div className="forecast-icon">
                  🌦️
                </div>

                <p>
                  🌡️ Max Temperature
                </p>

                <strong>
                  {forecast.forecast.daily.temperature_2m_max[index]}°C
                </strong>

                <p>
                  🧊 Min Temperature
                </p>

                <strong>
                  {forecast.forecast.daily.temperature_2m_min[index]}°C
                </strong>

                <p>
                  🌧️ Rain Probability
                </p>

                <strong>
                  {forecast.forecast.daily.precipitation_probability_max[index]}%
                </strong>

              </div>

            ))}

          </div>

        </div>
      )}

    </div>
  );
}

export default Forecast;