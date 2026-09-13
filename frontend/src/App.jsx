import "./App.css";

import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import WeatherMap from "./pages/WeatherMap";
import Dashboard from "./pages/Dashboard";
import CurrentWeather from "./pages/CurrentWeather";
import Forecast from "./pages/Forecast";
import HistoricalWeather from "./pages/HistoricalWeather";
import RainPrediction from "./pages/RainPrediction";
import FloodPrediction from "./pages/FloodPrediction";
import WeatherAI from "./pages/WeatherAI";
import FarmerGuidelines from "./pages/FarmerGuidelines";
import Alerts from "./pages/Alerts";

function App() {
  return (
    <BrowserRouter>

      <div className="app-layout">

        {/* LEFT SIDEBAR */}
        <Sidebar />

        {/* MAIN CONTENT */}
        <main className="main-content">

          <Routes>

            {/* Dashboard */}
            <Route
              path="/"
              element={<Dashboard />}
            />

            {/* Current Weather */}
            <Route
              path="/current-weather"
              element={<CurrentWeather />}
            />

            {/* Forecast */}
            <Route
              path="/forecast"
              element={<Forecast />}
            />

            {/* Historical Weather */}
            <Route
              path="/historical-weather"
              element={<HistoricalWeather />}
            />

            {/* Rain Prediction */}
            <Route
              path="/rain-prediction"
              element={<RainPrediction />}
            />

            {/* Flood Prediction */}
            <Route
              path="/flood-prediction"
              element={<FloodPrediction />}
            />

            {/* Weather AI */}
            <Route
              path="/weather-ai"
              element={<WeatherAI />}
            />

            {/* Farmer Guidelines */}
            <Route
              path="/farmer-guidelines"
              element={<FarmerGuidelines />}
            />

            {/* Weather Alerts */}
            <Route
              path="/alerts"
              element={<Alerts />}
            />

            {/* Weather Map */}
            <Route
              path="/weather-map"
              element={<WeatherMap />}
            />

          </Routes>

        </main>

       {/* FLOATING WEATHERGPT BUTTON */}
<Link
  to="/weather-ai"
  className="floating-weathergpt-button"
  title="Ask WeatherGPT"
>
  🤖
</Link>

{/* FLOATING WEATHER MAP BUTTON */}
<Link
  to="/weather-map"
  className="floating-map-button"
  title="Open Weather Map"
>
  🗺️
</Link>

      </div>

    </BrowserRouter>
  );
}

export default App;