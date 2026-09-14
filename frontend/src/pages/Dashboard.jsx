import { useState } from "react";
import { Link } from "react-router-dom";

// const API_BASE_URL = "https://aster-4.onrender.com";

const API_BASE_URL = "https://aster-4.onrender.com";

function Dashboard() {
  const [city, setCity] = useState("Delhi");
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [forecastError, setForecastError] = useState("");

  // =====================================================
  // CHECK WEATHER
  // =====================================================

  const checkWeather = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }

    setLoading(true);
    setError("");
    setForecastError("");

    // Clear old data while loading
    setWeather(null);
    setForecast(null);

    const cityName = encodeURIComponent(city.trim());

    // =====================================================
    // 1. CURRENT WEATHER
    // =====================================================

    try {
      console.log("Fetching current weather...");

      const weatherResponse = await fetch(
        `${API_BASE_URL}/weather/${cityName}`
      );

      console.log(
        "Weather response status:",
        weatherResponse.status
      );

      const weatherData = await weatherResponse.json();

      console.log("Weather data:", weatherData);

      if (!weatherResponse.ok) {
        throw new Error(
          weatherData?.detail ||
            weatherData?.error ||
            `Weather API returned ${weatherResponse.status}`
        );
      }

      if (weatherData?.error) {
        throw new Error(weatherData.error);
      }

      setWeather(weatherData);
    } catch (err) {
      console.error("CURRENT WEATHER ERROR:", err);

      setWeather(null);

      setError(
        err.message ||
          "Unable to get current weather. Please check the backend."
      );

      // Current weather failed,
      // so there is no reason to call forecast.
      setLoading(false);
      return;
    }

    // =====================================================
    // 2. 3-DAY FORECAST
    // =====================================================

    try {
      console.log("Fetching 3-day forecast...");

      const forecastResponse = await fetch(
        `${API_BASE_URL}/forecast/${cityName}?days=3`
      );

      console.log(
        "Forecast response status:",
        forecastResponse.status
      );

      const forecastData = await forecastResponse.json();

      console.log("Forecast data:", forecastData);

      if (!forecastResponse.ok) {
        throw new Error(
          forecastData?.detail ||
            forecastData?.error ||
            `Forecast API returned ${forecastResponse.status}`
        );
      }

      if (forecastData?.error) {
        throw new Error(forecastData.error);
      }

      setForecast(forecastData);
    } catch (err) {
      console.error("FORECAST ERROR:", err);

      // IMPORTANT:
      // Current weather should remain visible
      // even if forecast fails.

      setForecast(null);

      setForecastError(
        err.message ||
          "Forecast could not be loaded."
      );
    }

    setLoading(false);
  };

  // =====================================================
  // GET FORECAST DAY
  // =====================================================

  const getForecastDay = (index) => {
    if (!forecast?.forecast?.daily) {
      return null;
    }

    const daily = forecast.forecast.daily;

    return {
      date: daily.time?.[index],

      maxTemp:
        daily.temperature_2m_max?.[index],

      minTemp:
        daily.temperature_2m_min?.[index],

      rainProbability:
        daily.precipitation_probability_max?.[index],
    };
  };

  // =====================================================
  // FORMAT DATE
  // =====================================================

  const formatDate = (date) => {
    if (!date) {
      return "Forecast";
    }

    const d = new Date(date);

    return d.toLocaleDateString("en-IN", {
      weekday: "short",
      day: "numeric",
      month: "short",
    });
  };

  // =====================================================
  // WEATHER ICON
  // =====================================================

  const getWeatherIcon = (rainProbability) => {
    if (rainProbability >= 70) {
      return "🌧️";
    }

    if (rainProbability >= 40) {
      return "🌦️";
    }

    if (rainProbability >= 20) {
      return "⛅";
    }

    return "☀️";
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="dashboard-page">

      {/* =================================================
          HERO
      ================================================== */}

      <section className="dashboard-hero">

        <div>

          <p className="hero-tag">
            🌱 SMART FARMER PLATFORM
          </p>

          <h1>
            Weather Intelligence
            <br />
            for Better Farming
          </h1>

          <p className="hero-description">
            Get real-time weather insights, forecasts and
            AI-powered agricultural guidance to make smarter
            farming decisions.
          </p>

          <div className="hero-buttons">

            <Link
              to="/weather-ai"
              className="hero-ai-button"
            >
              🤖 Ask Weather AI
            </Link>

            <Link
              to="/farmer-guidelines"
              className="hero-secondary-button"
            >
              🌾 Farmer Guidelines
            </Link>

          </div>

        </div>

        <div className="hero-weather-icon">
          🌦️
        </div>

      </section>


      {/* =================================================
          LOCATION SEARCH
      ================================================== */}

      <section className="dashboard-search">

        <div className="search-heading">

          <h2>
            📍 Check Your Farm Location
          </h2>

          <p>
            Enter your city to get live weather intelligence
            for your farming activities.
          </p>

        </div>


        <div className="dashboard-search-box">

          <input
            type="text"
            value={city}
            onChange={(e) => {
              setCity(e.target.value);
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                checkWeather();
              }
            }}
            placeholder="Enter city name"
          />

          <button
            onClick={checkWeather}
            disabled={loading}
          >
            {loading
              ? "Checking..."
              : "Check Weather"}
          </button>

        </div>


        {/* Current weather error */}

        {error && (
          <div className="dashboard-error">
            ⚠️ {error}
          </div>
        )}


        {/* Forecast-only error */}

        {forecastError && !error && (
          <div className="dashboard-error">
            ⚠️ Forecast unavailable: {forecastError}
          </div>
        )}

      </section>


      {/* =================================================
          CURRENT WEATHER
      ================================================== */}

      {weather && (

        <section className="dashboard-weather">

          <div className="location-title">

            <div>

              <p>
                LIVE WEATHER CONDITIONS
              </p>

              <h2>
                📍 {weather.city}
              </h2>

            </div>

            <span className="location-weather-icon">
              🌤️
            </span>

          </div>


          <div className="dashboard-card-grid">

            {/* Temperature */}

            <div className="dashboard-card">

              <div className="dashboard-card-icon">
                🌡️
              </div>

              <p>
                Temperature
              </p>

              <h3>
                {weather.temperature ?? "--"}°C
              </h3>

              <small>
                Current temperature
              </small>

            </div>


            {/* Humidity */}

            <div className="dashboard-card">

              <div className="dashboard-card-icon">
                💧
              </div>

              <p>
                Humidity
              </p>

              <h3>
                {weather.humidity ?? "--"}%
              </h3>

              <small>
                Relative humidity
              </small>

            </div>


            {/* Wind */}

            <div className="dashboard-card">

              <div className="dashboard-card-icon">
                💨
              </div>

              <p>
                Wind Speed
              </p>

              <h3>
                {weather.wind_speed ?? "--"}
              </h3>

              <small>
                km/h
              </small>

            </div>


            {/* Coordinates */}

            <div className="dashboard-card">

              <div className="dashboard-card-icon">
                📍
              </div>

              <p>
                Coordinates
              </p>

              <h3>
                {Number(weather.latitude).toFixed(2)}
              </h3>

              <small>
                Lat:{" "}
                {Number(weather.latitude).toFixed(2)}
                {" | "}
                Lon:{" "}
                {Number(weather.longitude).toFixed(2)}
              </small>

            </div>

          </div>

        </section>

      )}


      {/* =================================================
          FARMING RISK
      ================================================== */}

      <section className="dashboard-risk-section">

        <div className="section-heading">

          <div>

            <p className="section-label">
              FARMING SAFETY
            </p>

            <h2>
              Weather Risk Monitoring
            </h2>

          </div>

          <Link to="/alerts">
            View all alerts →
          </Link>

        </div>


        <div className="risk-grid">

          {/* Rain */}

          <div className="risk-card">

            <div className="risk-card-top">

              <div className="risk-icon">
                🌧️
              </div>

              <span className="risk-label">
                RAIN
              </span>

            </div>

            <h3>
              Rain Prediction
            </h3>

            <p>
              Monitor upcoming rainfall to plan
              irrigation, harvesting and field work.
            </p>

            <Link to="/rain-prediction">
              Check rain prediction →
            </Link>

          </div>


          {/* Flood */}

          <div className="risk-card">

            <div className="risk-card-top">

              <div className="risk-icon">
                🌊
              </div>

              <span className="risk-label">
                FLOOD
              </span>

            </div>

            <h3>
              Flood Risk
            </h3>

            <p>
              AI-powered flood risk prediction for
              your selected location.
            </p>

            <Link to="/flood-prediction">
              Check flood risk →
            </Link>

          </div>


          {/* Alerts */}

          <div className="risk-card">

            <div className="risk-card-top">

              <div className="risk-icon">
                🔔
              </div>

              <span className="risk-label">
                ALERTS
              </span>

            </div>

            <h3>
              Weather Alerts
            </h3>

            <p>
              Stay informed about heavy rain, heat,
              wind and other weather risks.
            </p>

            <Link to="/alerts">
              View weather alerts →
            </Link>

          </div>

        </div>

      </section>


      {/* =================================================
          3 DAY FORECAST
      ================================================== */}

      <section className="dashboard-forecast-section">

        <div className="section-heading">

          <div>

            <p className="section-label">
              UPCOMING WEATHER
            </p>

            <h2>
              3-Day Forecast
            </h2>

          </div>

          <Link to="/forecast">
            Full forecast →
          </Link>

        </div>


        {/* Forecast error */}

        {forecastError && (

          <div className="dashboard-error">

            ⚠️ Forecast could not be loaded:
            {" "}
            {forecastError}

          </div>

        )}


        <div className="mini-forecast-grid">

          {[0, 1, 2].map((index) => {

            const day = getForecastDay(index);

            return (

              <div
                className="mini-forecast-card"
                key={index}
              >

                <p>

                  {day?.date
                    ? formatDate(day.date)
                    : `Day ${index + 1}`}

                </p>


                <h3>

                  {index === 0
                    ? "Today"
                    : index === 1
                    ? "Tomorrow"
                    : "Day 3"}

                </h3>


                <div className="forecast-icon">

                  {getWeatherIcon(
                    day?.rainProbability ?? 0
                  )}

                </div>


                <strong>

                  {day?.maxTemp != null
                    ? `${day.maxTemp}°C`
                    : "--"}

                </strong>


                <span>

                  Min:{" "}

                  {day?.minTemp != null
                    ? `${day.minTemp}°C`
                    : "--"}

                </span>


                <small>

                  🌧️ Rain probability:{" "}

                  {day?.rainProbability != null
                    ? `${day.rainProbability}%`
                    : "--"}

                </small>

              </div>

            );

          })}

        </div>

      </section>


      {/* =================================================
          DASHBOARD ALERT
      ================================================== */}

      <section className="dashboard-alert-section">

        <div className="section-heading">

          <div>

            <p className="section-label">
              FARMER NOTICE
            </p>

            <h2>
              Weather Safety
            </h2>

          </div>

        </div>


        <div className="dashboard-alert-box">

          <div className="alert-box-icon">
            ⚠️
          </div>

          <div>

            <h3>
              Monitor weather before field activities
            </h3>

            <p>
              Weather conditions can change quickly.
              Check rainfall, temperature, wind and
              flood-risk information before irrigation,
              spraying, harvesting or other important
              farming activities.
            </p>

          </div>

        </div>

      </section>


      {/* =================================================
          FARMER ADVICE
      ================================================== */}

      <section className="farmer-advice-section">

        <div className="advice-icon">
          👨‍🌾
        </div>

        <div className="advice-content">

          <h2>
            Smart Decisions Start With Weather
          </h2>

          <p>
            WeatherGPT combines real-time weather data,
            forecasts, AI predictions and agricultural
            knowledge to help farmers make informed
            decisions.
          </p>

          <Link to="/farmer-guidelines">
            Explore farmer guidelines →
          </Link>

        </div>

      </section>


      {/* =================================================
          FARMER TOOLS
      ================================================== */}

      <section className="dashboard-features">

        <div className="section-heading">

          <div>

            <p className="section-label">
              FARMER TOOLS
            </p>

            <h2>
              Smart Weather Features
            </h2>

          </div>

        </div>


        <div className="feature-grid">

          <Link
            to="/forecast"
            className="feature-card"
          >

            <span>
              📅
            </span>

            <h3>
              Weather Forecast
            </h3>

            <p>
              Plan farming activities using
              upcoming weather conditions.
            </p>

          </Link>


          <Link
            to="/rain-prediction"
            className="feature-card"
          >

            <span>
              🌧️
            </span>

            <h3>
              Rain Prediction
            </h3>

            <p>
              Understand rainfall conditions and
              prepare your farm accordingly.
            </p>

          </Link>


          <Link
            to="/flood-prediction"
            className="feature-card"
          >

            <span>
              🌊
            </span>

            <h3>
              Flood Prediction
            </h3>

            <p>
              Get AI-powered flood risk information
              for your location.
            </p>

          </Link>


          <Link
            to="/weather-ai"
            className="feature-card"
          >

            <span>
              🤖
            </span>

            <h3>
              Weather AI
            </h3>

            <p>
              Ask AI questions about weather,
              farming and agriculture.
            </p>

          </Link>


          <Link
            to="/historical-weather"
            className="feature-card"
          >

            <span>
              📊
            </span>

            <h3>
              Historical Weather
            </h3>

            <p>
              Analyze previous weather conditions
              for better planning.
            </p>

          </Link>


          <Link
            to="/farmer-guidelines"
            className="feature-card"
          >

            <span>
              🌾
            </span>

            <h3>
              Farmer Guidelines
            </h3>

            <p>
              Get agriculture and government
              guideline information.
            </p>

          </Link>

        </div>

      </section>


      {/* =================================================
          QUICK ACTIONS
      ================================================== */}

      <section className="dashboard-actions">

        <h2>
          Quick Actions
        </h2>


        <div className="action-grid">

          <Link to="/current-weather">
            🌡️ Current Weather
          </Link>

          <Link to="/forecast">
            📅 Forecast
          </Link>

          <Link to="/rain-prediction">
            🌧️ Rain
          </Link>

          <Link to="/flood-prediction">
            🌊 Flood Risk
          </Link>

          <Link to="/alerts">
            🔔 Alerts
          </Link>

        </div>

      </section>

    </div>
  );
}

export default Dashboard;