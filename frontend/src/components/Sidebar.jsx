import { useState } from "react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  const [open, setOpen] = useState(false);

  const menuItems = [
    { path: "/", label: "Dashboard", icon: "🏠" },
    { path: "/current-weather", label: "Current Weather", icon: "🌡️" },
    { path: "/forecast", label: "Forecast", icon: "📅" },
    { path: "/historical-weather", label: "Historical Weather", icon: "📊" },
    { path: "/rain-prediction", label: "Rain Prediction", icon: "🌧️" },
    { path: "/flood-prediction", label: "Flood Prediction", icon: "🌊" },
    { path: "/weather-ai", label: "Weather AI", icon: "🤖" },
    { path: "/farmer-guidelines", label: "Farmer Guidelines", icon: "👨‍🌾" },
    { path: "/alerts", label: "Alerts", icon: "🔔" },
  ];

  const closeSidebar = () => {
    setOpen(false);
  };

  return (
    <>
      {/* Mobile Header */}
      <div className="mobile-header">
        <button
          className="menu-button"
          onClick={() => setOpen(!open)}
        >
          ☰
        </button>

        <div className="mobile-logo">
          🌦️ WeatherGPT
        </div>
      </div>

      {/* Overlay for mobile */}
      {open && (
        <div
          className="sidebar-overlay"
          onClick={closeSidebar}
        ></div>
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>

        {/* Logo */}
        <div className="sidebar-logo">

          <div className="logo-icon">
            🌦️
          </div>

          <div>
            <h2>WeatherGPT</h2>
            <span>Smart Farmer Platform</span>
          </div>

        </div>


        {/* Navigation */}
        <nav className="sidebar-nav">

          <p className="nav-title">
            MAIN MENU
          </p>

          {menuItems.map((item) => (

            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `sidebar-link ${
                  isActive ? "sidebar-link-active" : ""
                }`
              }
              onClick={closeSidebar}
            >

              <span className="sidebar-link-icon">
                {item.icon}
              </span>

              <span className="sidebar-link-text">
                {item.label}
              </span>

            </NavLink>

          ))}

        </nav>


        {/* Bottom Farmer Card */}
        <div className="sidebar-bottom-card">

          <div className="bottom-card-icon">
            🌾
          </div>

          <div>
            <strong>
              Farmer First
            </strong>

            <p>
              Weather insights for better farming
            </p>
          </div>

        </div>


        {/* Version */}
        <div className="sidebar-version">
          WeatherGPT v1.0
        </div>

      </aside>
    </>
  );
}

export default Sidebar;