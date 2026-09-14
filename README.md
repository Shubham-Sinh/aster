
# 🌦️ ASTER — Intelligent Weather & Climate Intelligence Platform


## 🚀 What is ASTER?

**ASTER** is an intelligent weather and climate-awareness platform designed to transform raw environmental data into **understandable insights, predictions, alerts, and actionable recommendations**.

Traditional weather applications mainly answer:

> *"What is the weather today?"*

ASTER goes a step further:

> **"What is happening, why does it matter, what could happen next, and what should I do?"**

The platform combines **real-time weather data, interactive maps, air-quality monitoring, flood-risk analysis, disaster feeds, machine learning, Retrieval-Augmented Generation (RAG), and an AI weather assistant** into a unified system.

---

## ✨ Why ASTER?

Weather data becomes significantly more useful when it is converted into **decisions**.

ASTER is designed around four layers:

```text
🌍 Observe
   ↓
📊 Analyze
   ↓
🤖 Predict
   ↓
💡 Recommend
```

It doesn't simply display environmental information — it attempts to turn that information into **context-aware intelligence**.

---

# 🌟 Key Features

### 🌤️ Real-Time Weather

Get detailed weather information for a selected location, including:

* Current temperature
* Feels-like temperature
* Humidity
* Wind speed and direction
* Cloud cover
* Precipitation
* Sunrise & sunset
* Hourly weather information
* Multi-day forecasts

---

### 🗺️ Interactive Weather Map

Explore weather conditions geographically through an interactive map.

Users can:

* Select locations directly from the map
* Search for locations
* View weather information for selected coordinates
* Explore environmental conditions spatially
* Access location-specific predictions

Built using **Leaflet + React Leaflet**.

---

### 🤖 WeatherGPT — AI Weather Assistant

ASTER includes an AI-powered conversational assistant capable of understanding natural-language questions related to:

* Weather
* Forecasts
* Rainfall
* Flood risk
* Agriculture
* Government schemes
* Weather-related guidance
* Environmental conditions

Instead of forcing users to navigate multiple dashboards, WeatherGPT provides a **conversational interface** for accessing the platform's intelligence.

---

### 🧠 RAG-Based Government Information

For government and agriculture-related queries, ASTER can use a **Retrieval-Augmented Generation (RAG)** approach.

The goal is to provide answers based on retrieved source material rather than allowing the language model to freely invent information.

This is especially useful for questions involving:

* Government schemes
* Agricultural support
* Eligibility information
* Weather-related assistance
* Official guidelines
* Policies and documentation

---

### 🌊 AI/ML Flood Prediction

ASTER incorporates a machine-learning-based flood prediction component.

The model considers environmental variables such as:

| Feature        | Description                     |
| -------------- | ------------------------------- |
| Rainfall 1h    | Recent rainfall                 |
| Rainfall 6h    | Short-term accumulated rainfall |
| Rainfall 24h   | Daily rainfall                  |
| Rainfall 3-day | Multi-day rainfall              |
| Temperature    | Atmospheric temperature         |
| Humidity       | Relative humidity               |
| Pressure       | Atmospheric pressure            |
| Wind Speed     | Wind conditions                 |
| Cloud Cover    | Cloud concentration             |

The resulting model provides a **flood-risk prediction probability**.

---

### 🚨 Disaster Awareness

ASTER integrates external disaster information to provide awareness of major environmental events.

Supported categories include:

* 🌊 Floods
* 🌀 Tropical cyclones
* 🔥 Wildfires
* 🌋 Volcanic activity
* ☀️ Droughts
* 🌎 Earthquakes

This gives users a broader picture of environmental conditions beyond ordinary weather forecasts.

---

### 🌫️ Air Quality Monitoring

The platform also provides air-quality information such as:

* US AQI
* PM2.5
* PM10
* Ozone
* Nitrogen dioxide

This helps users understand not only the weather but also the **quality of the surrounding atmosphere**.

---

### 🌾 Farmer-Focused Guidance

ASTER includes dedicated agricultural guidance designed to help translate weather information into practical decisions.

Potential applications include:

* Rainfall awareness
* Flood preparedness
* Weather-based farming decisions
* Crop protection
* Extreme-weather awareness
* Agricultural recommendations

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      ASTER UI        │
                         │   React + Vite       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │ Weather API │       │ Disaster    │       │ Earthquake  │
       │ Open-Meteo  │       │    Feeds    │       │    USGS     │
       └─────────────┘       └─────────────┘       └─────────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Data Processing    │
                         │   & Risk Analysis    │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
            ┌──────────────┐                ┌──────────────┐
            │ ML Prediction│                │  WeatherGPT  │
            │ Flood Model  │                │  AI + RAG    │
            └──────────────┘                └──────────────┘
```

---

# 🧩 Technology Stack

## Frontend

* **React 19**
* **Vite**
* **React Router**
* **Leaflet**
* **React Leaflet**
* JavaScript
* HTML5
* CSS

## Backend

* **Python**
* **FastAPI**
* **HTTPX**
* REST APIs
* CORS

## Artificial Intelligence

* **LangChain**
* **Ollama**
* **Llama 3.2**
* Retrieval-Augmented Generation (RAG)
* Tool-based AI architecture

## Machine Learning

* Python
* Scikit-learn
* Feature scaling
* Classification
* Probability-based prediction
* Serialized ML models

## External Data Sources

* Open-Meteo
* Open-Meteo Air Quality
* Open-Meteo Flood
* USGS Earthquake Feed
* GDACS Disaster Information
* BigDataCloud Reverse Geocoding

---

# 📊 Backend API

ASTER provides a FastAPI-based REST backend.

| Endpoint               | Purpose                             |
| ---------------------- | ----------------------------------- |
| `/health`              | API health check                    |
| `/api/geocode`         | Location search                     |
| `/api/location`        | Weather + environmental information |
| `/api/disaster-alerts` | Global disaster information         |
| `/api/earthquakes`     | Earthquake information              |

---

## 🔍 Example API Flow

```text
User selects a location
        ↓
Frontend sends coordinates
        ↓
FastAPI receives request
        ↓
Backend collects environmental data
        ↓
Weather + AQI + Flood + Disaster data
        ↓
Data processing
        ↓
Risk analysis / ML prediction
        ↓
Results returned to React
        ↓
User receives actionable information
```

---

# 🤖 WeatherGPT Architecture

WeatherGPT is designed around **specialized tools rather than relying solely on a language model**.

```text
                     User Question
                           │
                           ▼
                    ┌─────────────┐
                    │ WeatherGPT  │
                    └──────┬──────┘
                           │
                    Intent Understanding
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Weather / Flood             Government /
       Related Query               Agriculture Query
              │                         │
              ▼                         ▼
        Tools + ML                  RAG Retrieval
              │                         │
              └────────────┬────────────┘
                           ▼
                     Final Response
```

This architecture allows different types of questions to be handled using the most appropriate information source.

---

# 🧠 Machine Learning Pipeline

The flood prediction workflow follows a conventional ML pipeline:

```text
Weather Data
     ↓
Feature Extraction
     ↓
Feature Scaling
     ↓
ML Model
     ↓
Prediction Probability
     ↓
Flood Risk
```

The model uses environmental features including rainfall, temperature, humidity, pressure, wind speed, and cloud cover.

---

# 🌐 Frontend Modules

The React application contains multiple dedicated interfaces for different types of weather intelligence.

```text
Dashboard
│
├── Current Weather
├── Forecast
├── Historical Weather
├── Weather Map
├── Weather AI
├── Rain Prediction
├── Flood Prediction
├── Alerts
└── Farmer Guidelines
```

---

# 📁 Project Structure

```text
ASTER/
│
├── FINAL.../
│   └── main.py
│
├── weathergpt-SIH - Copy/
│   └── Agent_file/
│       └── ml_agent1.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   │       ├── Dashboard.jsx
│   │       ├── CurrentWeather.jsx
│   │       ├── Forecast.jsx
│   │       ├── HistoricalWeather.jsx
│   │       ├── WeatherMap.jsx
│   │       ├── WeatherAI.jsx
│   │       ├── RainPrediction.jsx
│   │       ├── FloodPrediction.jsx
│   │       ├── FarmerGuidelines.jsx
│   │       └── Alerts.jsx
│   │
│   ├── package.json
│   └── ...
│
└── README.md
```

> Folder names may vary slightly depending on the local project version.

---

# ⚙️ Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Shubham-Sinh/aster.git
cd aster
```

---

## 2. Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will provide the local frontend URL in the terminal.

---

# 🔐 Environment Variables

If your deployment requires API keys or environment-specific configuration, create a `.env` file.

Example:

```env
API_KEY=your_api_key
BACKEND_URL=http://127.0.0.1:8000
```

> Never commit private API keys, tokens, passwords, or credentials to GitHub.

---

# 📡 Data Sources

ASTER combines multiple external sources to create a richer environmental picture.

### Open-Meteo

Used for:

* Weather forecasts
* Air quality
* Flood-related data
* Geocoding

### USGS

Used for:

* Earthquake information

### GDACS

Used for:

* Global disaster events
* Floods
* Cyclones
* Wildfires
* Volcanic activity
* Droughts

### BigDataCloud

Used for:

* Reverse geocoding
* Location information

---

# 🎯 Use Cases

ASTER can be useful for:

### 👨‍🌾 Farmers

Understand rainfall, weather conditions, flood risk, and receive weather-aware agricultural guidance.

### 🏠 General Users

Check current weather, forecasts, air quality, and disaster information.

### 🚨 Disaster Awareness

Monitor environmental events and potential hazards.

### 🎓 Students & Researchers

Explore the integration of:

* AI
* Machine Learning
* RAG
* APIs
* Geospatial visualization
* Environmental data

### 🏛️ Public-Sector Applications

The architecture can be extended toward weather-aware public information and decision-support systems.

---

# 💡 What Makes ASTER Different?

ASTER is not designed as another simple weather dashboard.

It combines:

```text
Weather
   +
Air Quality
   +
Maps
   +
Flood Prediction
   +
Disaster Monitoring
   +
Machine Learning
   +
RAG
   +
Generative AI
   =
Environmental Intelligence
```

The central idea is to convert **data → intelligence → action**.

---

# 🛣️ Future Roadmap

Potential future improvements include:

* [ ] Improved flood prediction model
* [ ] More historical weather analytics
* [ ] Advanced rainfall forecasting
* [ ] Satellite imagery integration
* [ ] More detailed agricultural recommendations
* [ ] Crop-specific weather intelligence
* [ ] Location-based notifications
* [ ] Push alerts for severe weather
* [ ] More government-document sources
* [ ] Model performance monitoring
* [ ] Better multilingual support
* [ ] Mobile application
* [ ] Advanced geospatial visualizations

---

# ⚠️ Disclaimer

ASTER is intended for **educational, analytical, and informational purposes**.

Machine-learning predictions and weather-based risk indicators are estimates and should **not be considered official emergency warnings or replacements for government disaster-management authorities**.

For emergency situations, always follow official alerts and instructions from the relevant authorities.

---

# ⭐ Support the Project

If you find ASTER interesting or useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report bugs
* 💡 Suggest improvements
* 🔧 Contribute new features

>

🌍 About ASTER

ASTER is an AI-powered weather and environmental intelligence platform that brings together real-time weather data, interactive maps, air-quality monitoring, disaster awareness, machine learning, flood prediction, and conversational AI in a single application.

Unlike conventional weather applications that primarily answer:

"What's the weather?"

ASTER is built around a bigger question:

"What is happening, what could happen next, and what should I do?"

The platform transforms raw environmental data into clear, contextual, and actionable intelligence for everyday users, farmers, researchers, and disaster-awareness use cases.

⚡ From Data → Intelligence → Action
---


