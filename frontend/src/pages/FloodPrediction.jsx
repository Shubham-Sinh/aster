import { useState } from "react";

function FloodPrediction() {
  const [city, setCity] = useState("");
  const [day, setDay] = useState(1);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const predictFlood = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/flood-prediction/${encodeURIComponent(
          city
        )}?day=${day}`
      );

      if (!response.ok) {
        throw new Error("Unable to get flood prediction.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      const predictionText = data.prediction;

      // Extract risk flag
      const riskMatch = predictionText.match(/Risk flag\s+(\d)/i);

      // Extract probability
      const probabilityMatch = predictionText.match(
        /Probability:\s*([\d.]+)%/i
      );

      const riskFlag = riskMatch ? Number(riskMatch[1]) : 0;
      const probability = probabilityMatch
        ? Number(probabilityMatch[1])
        : 0;

      setResult({
        city: data.city,
        latitude: data.latitude,
        longitude: data.longitude,
        riskFlag,
        probability,
        message: predictionText,
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevel = () => {
    if (!result) return "";

    if (result.riskFlag === 1 || result.probability >= 50) {
      return "HIGH";
    }

    if (result.probability >= 30) {
      return "MODERATE";
    }

    return "LOW";
  };

  return (
    <div className="weather-page flood-page">
      <div className="page-heading">
        <h1>🌊 Flood Prediction</h1>
        <p>
          Check AI-based flood risk using forecasted weather conditions.
        </p>
      </div>

      <div className="weather-search flood-search">
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              predictFlood();
            }
          }}
        />

        <select
          value={day}
          onChange={(e) => setDay(Number(e.target.value))}
        >
          <option value={1}>Next Day</option>
          <option value={2}>Day 2</option>
          <option value={3}>Day 3</option>
        </select>

        <button onClick={predictFlood}>
          {loading ? "Analyzing..." : "Predict Flood Risk"}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {result && (
        <div className="flood-result">

          <div className="flood-location">
            <h2>📍 {result.city}</h2>
            <p>
              Latitude: {result.latitude.toFixed(4)} | Longitude:{" "}
              {result.longitude.toFixed(4)}
            </p>
          </div>

          <div className={`flood-risk-card ${getRiskLevel().toLowerCase()}`}>
            <div className="flood-icon">🌊</div>

            <div>
              <p className="risk-label">FLOOD RISK</p>

              <h2>{getRiskLevel()}</h2>

              <p className="risk-probability">
                Probability: <strong>{result.probability.toFixed(2)}%</strong>
              </p>
            </div>
          </div>

          <div className="flood-info-grid">

            <div className="flood-info-card">
              <span>🤖</span>
              <p>AI Risk Flag</p>
              <strong>
                {result.riskFlag === 1 ? "Risk Detected" : "No Risk"}
              </strong>
            </div>

            <div className="flood-info-card">
              <span>📅</span>
              <p>Forecast</p>
              <strong>Day {day}</strong>
            </div>

            <div className="flood-info-card">
              <span>📊</span>
              <p>Probability</p>
              <strong>{result.probability.toFixed(2)}%</strong>
            </div>

          </div>

          <div className="farmer-warning">
            <h3>👨‍🌾 Farmer Advisory</h3>

            {getRiskLevel() === "HIGH" && (
              <p>
                ⚠️ High flood risk detected. Protect crops, livestock and
                agricultural equipment. Avoid low-lying areas and follow
                local government warnings.
              </p>
            )}

            {getRiskLevel() === "MODERATE" && (
              <p>
                ⚠️ Moderate flood risk. Monitor rainfall and local weather
                alerts closely. Keep drainage channels clear and prepare
                for possible water accumulation.
              </p>
            )}

            {getRiskLevel() === "LOW" && (
              <p>
                ✅ Current conditions indicate a low flood risk. Continue
                normal farming activities while monitoring weather updates.
              </p>
            )}
          </div>

        </div>
      )}
    </div>
  );
}

export default FloodPrediction;