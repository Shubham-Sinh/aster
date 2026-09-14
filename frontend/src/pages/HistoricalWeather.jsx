import { useState } from "react";

function HistoricalWeather() {
  const [city, setCity] = useState("");
  const [days, setDays] = useState(7);
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getHistory = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setHistory(null);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/historical-weather/${encodeURIComponent(
          city
        )}?days=${days}`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch historical weather.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      // history_tool returns JSON as a string
      const parsedHistory =
        typeof data.history === "string"
          ? JSON.parse(data.history)
          : data.history;

      setHistory({
        city: data.city,
        dates: parsedHistory.dates,
        maxTemperatures: parsedHistory.max_temperatures,
        minTemperatures: parsedHistory.min_temperatures,
      });

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-page">

      <h1>📊 Historical Weather</h1>

      <p>
        View past temperature conditions to understand weather trends.
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
          onChange={(e) => setDays(Number(e.target.value))}
        >
          <option value={3}>3 Days</option>
          <option value={7}>7 Days</option>
          <option value={14}>14 Days</option>
        </select>

        <button onClick={getHistory}>
          {loading ? "Loading..." : "Get History"}
        </button>

      </div>

      {error && (
        <p className="error-message">
          ❌ {error}
        </p>
      )}

      {history && (
        <div className="weather-result">

          <h2>📍 {history.city}</h2>

          <div className="history-grid">

            {history.dates.map((date, index) => (
              <div className="history-card" key={date}>

                <h3>{date}</h3>

                <div className="history-temperature">
                  🌡️
                </div>

                <p>Maximum Temperature</p>

                <strong>
                  {history.maxTemperatures[index]}°C
                </strong>

                <p>Minimum Temperature</p>

                <strong>
                  {history.minTemperatures[index]}°C
                </strong>

              </div>
            ))}

          </div>

        </div>
      )}

    </div>
  );
}

export default HistoricalWeather;