# Weather Agent - Quick Start Guide

## 🌤️ Overview

AI-powered weather agent that provides real-time weather data and intelligent agricultural recommendations using OpenWeatherMap API and Google Gemini LLM.

## 🚀 Quick Setup

### 1. Get API Keys

- **OpenWeatherMap**: https://openweathermap.org/api (Free: 1000 calls/day)
- **Google Gemini**: https://ai.google.dev/

### 2. Configure Environment

Add to `env/.env`:

```env
WEATHER_API=your_openweather_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Install Dependencies

```bash
pip install requests python-dotenv langchain-google-genai
```

## 🔧 Usage

### Basic Weather Data

```python
from data.weather_plugins import fetch_weather_data

weather = fetch_weather_data("Delhi")
# Returns: {"temperature": "33.6°C", "condition": "Rain", ...}
```

### AI Recommendations

```python
from graph_arc.agents_node.weather_agent import weather_agent

state = {
    "location": "Punjab",
    "raw_query": "Should I harvest my wheat today?",
    "entities": {"location": "Punjab"}
}

result = weather_agent(state)
# Returns weather + AI recommendation for farming
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/test_weather_plugins.py -v -s

# Test specific functionality
python -m pytest tests/test_weather_plugins.py::TestWeatherPluginsRealAPI::test_weather_agent_llm_recommendations -v -s
```

## ✅ Features

- ✅ Real-time weather data (7 major Indian cities tested)
- ✅ AI-powered agricultural recommendations
- ✅ Context-aware farming advice
- ✅ Error handling & fallback systems
- ✅ Comprehensive test suite
- ✅ Production-ready code

## 📊 Test Results

```
6/6 tests PASSED ✅
- API Integration: All locations return status 200
- Authentication: Valid/invalid key handling
- LLM Recommendations: Context-aware agricultural advice
- Error Handling: Graceful fallbacks for failures
```

## 🎯 Sample Output

```
Weather for Delhi:
- Temperature: 33.6°C
- Condition: Rain
- Humidity: 52%

AI Recommendation:
"Given the high temperature and light rain, postpone pesticide spraying on your wheat crop today. The rain may wash away the pesticide, reducing its effectiveness. Focus instead on monitoring for pest pressure and plan spraying for a cooler, drier day."
```

## 📁 File Structure

```
├── data/weather_plugins.py          # API integration
├── graph_arc/agents_node/weather_agent.py  # Main agent
├── graph_arc/prompts.py             # LLM prompts
├── tests/test_weather_plugins.py    # Test suite
├── config/settings.py               # Configuration
└── docs/weather_agent_documentation.md  # Full docs
```

## 🔍 Need Help?

See full documentation: `docs/weather_agent_documentation.md`

---

**Status**: Production Ready ✅  
**Version**: 1.0.0  
**Last Updated**: August 11, 2025
