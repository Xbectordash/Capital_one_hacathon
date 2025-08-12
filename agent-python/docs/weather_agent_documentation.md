# Weather Agent Documentation

## Overview

The Weather Agent is an intelligent agricultural weather advisory system that provides real-time weather data and AI-powered farming recommendations. It integrates with OpenWeatherMap API to fetch current weather conditions and uses Google's Gemini LLM to generate context-aware agricultural advice.

## Architecture

### Components

1. **Weather Plugin** (`data/weather_plugins.py`)

   - Handles OpenWeatherMap API integration
   - Fetches real-time weather data
   - Error handling and data formatting

2. **Weather Agent** (`graph_arc/agents_node/weather_agent.py`)

   - Main agent logic
   - Coordinates weather data fetching and recommendation generation
   - Integrates with LLM for intelligent recommendations

3. **Prompts** (`graph_arc/prompts.py`)

   - Contains LLM prompts for weather-based recommendations
   - Structured prompt engineering for agricultural context

4. **Configuration** (`config/settings.py`)

   - Environment variable management
   - API key configuration

5. **Tests** (`tests/test_weather_plugins.py`)
   - Comprehensive test suite
   - Real API testing
   - LLM recommendation validation

## Features

### ✅ Real-Time Weather Data

- Temperature, humidity, wind speed
- Weather conditions (sunny, rainy, cloudy)
- Precipitation measurements
- Location-based weather fetching

### ✅ AI-Powered Recommendations

- Context-aware agricultural advice
- Crop-specific recommendations
- Weather-based farming decisions
- Irrigation, spraying, and harvesting guidance

### ✅ Error Handling

- Graceful API failure handling
- Fallback recommendations
- Invalid location management

### ✅ Comprehensive Testing

- Real API integration tests
- LLM recommendation validation
- Error scenario testing
- Multi-location weather testing

## Installation & Setup

### 1. Environment Configuration

Create `.env` file in the `env/` directory:

```env
# Weather API Key from OpenWeatherMap
WEATHER_API=your_openweathermap_api_key_here

# Gemini API Key for LLM recommendations
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. API Key Setup

#### OpenWeatherMap API:

1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Get API key (1000 calls/day free)
4. Add to `.env` file as `WEATHER_API`

#### Google Gemini API:

1. Visit: https://ai.google.dev/
2. Get API key
3. Add to `.env` file as `GEMINI_API_KEY`

### 3. Dependencies

```bash
pip install requests python-dotenv langchain-google-genai
```

## Usage

### Basic Weather Data Fetching

```python
from data.weather_plugins import fetch_weather_data

# Fetch weather data for a city
weather_data = fetch_weather_data("Delhi")
print(weather_data)

# Output:
{
    "temperature": "33.6°C",
    "condition": "Rain",
    "humidity": "52%",
    "wind_speed": "5.3 km/h",
    "precipitation": "2.82 mm"
}
```

### Weather Agent with LLM Recommendations

```python
from graph_arc.agents_node.weather_agent import weather_agent

# Create state with user query and location
state = {
    "location": "Punjab",
    "raw_query": "Is it a good day for harvesting wheat?",
    "entities": {"location": "Punjab"}
}

# Get weather analysis and recommendations
result = weather_agent(state)
print(result)

# Output:
{
    "date_range": "today",
    "forecast": {
        "temperature": "41.33°C",
        "condition": "Clear",
        "humidity": "27%",
        "wind_speed": "3.5 km/h",
        "precipitation": "0 mm"
    },
    "recommendation": "Given the extremely high temperature (41.33°C) and low humidity (27%) in Punjab, immediate and aggressive irrigation is crucial to prevent severe crop stress, especially for wheat nearing harvest. Avoid midday field work due to heat stress; harvesting wheat can proceed in the early morning or late evening hours to minimize heat damage, but prioritize irrigation first."
}
```

## API Reference

### Weather Plugin Functions

#### `fetch_weather_data(city_name: str) -> Dict`

Fetches current weather data for a given city.

**Parameters:**

- `city_name` (str): Name of the city to fetch weather data for

**Returns:**

- `Dict`: Weather data with keys: temperature, condition, humidity, wind_speed, precipitation

**Raises:**

- `ValueError`: If API key is missing or API request fails

**Example:**

```python
weather = fetch_weather_data("Bangalore")
# Returns: {"temperature": "25.5°C", "condition": "Clouds", ...}
```

### Weather Agent Functions

#### `weather_agent(state: GlobalState) -> WeatherAgentState`

Main weather agent function that processes weather queries and generates recommendations.

**Parameters:**

- `state` (GlobalState): Contains user query, location, and entities

**Returns:**

- `WeatherAgentState`: Contains date_range, forecast, and LLM-generated recommendation

**Example:**

```python
state = {
    "location": "Delhi",
    "raw_query": "Should I spray pesticides today?",
    "entities": {"location": "Delhi"}
}
result = weather_agent(state)
```

## LLM Integration

### Prompt Engineering

The weather agent uses a specialized prompt for generating agricultural recommendations:

```
You are an expert agricultural advisor specializing in weather-based farming recommendations.

Based on the following weather data, provide specific, actionable agricultural recommendations for farmers:

Weather Data:
- Temperature: {temperature}
- Condition: {condition}
- Humidity: {humidity}
- Wind Speed: {wind_speed}
- Precipitation: {precipitation}
- Location: {location}

User Query Context: {user_query}
```

### Recommendation Categories

The LLM provides advice on:

- **Irrigation needs** based on temperature and humidity
- **Crop protection measures** for adverse weather
- **Spraying/pesticide application timing** considering wind and rain
- **Harvesting considerations** for optimal conditions
- **Field work activities** safety and timing

## Testing

### Running Tests

```bash
# Run all weather plugin tests
python -m pytest tests/test_weather_plugins.py -v -s

# Run specific test categories
python -m pytest tests/test_weather_plugins.py::TestWeatherPluginsRealAPI::test_weather_agent_llm_recommendations -v -s
```

### Test Categories

1. **API Integration Tests**

   - Status code validation (200 for valid, 404 for invalid locations)
   - Authentication testing (401 for invalid API keys)
   - Multiple location testing

2. **Function Testing**

   - `fetch_weather_data()` validation
   - Data structure verification
   - Error handling testing

3. **LLM Recommendation Tests**

   - Context-aware advice generation
   - Agricultural keyword relevance
   - Query-specific recommendations

4. **Error Handling Tests**
   - Invalid location handling
   - API failure scenarios
   - Fallback recommendation systems

### Sample Test Results

```
=== Testing API Status Codes for Different Locations ===

📍 Testing location: Delhi
   Status Code: 200
   ✅ City Name: Delhi
   ✅ Temperature: 33.6°C
   ✅ Condition: Rain
   ✅ Humidity: 52%

📍 Testing location: Punjab
   Status Code: 200
   ✅ City Name: Punjab
   ✅ Temperature: 41.33°C
   ✅ Condition: Clear
   ✅ Humidity: 27%

=== Testing Weather Agent LLM Recommendations ===

📍 Testing weather agent for: Delhi
   Query: Should I spray pesticides on my wheat crop today?
   ✅ LLM Recommendation: Given the high temperature (33.6°C), light rain (2.82mm), and moderate humidity (52%), postpone pesticide spraying on your wheat crop today. The rain may wash away the pesticide, reducing its effectiveness...
   ✅ Relevant keywords found: 3/4
```

## Error Handling

### API Failures

- Network timeouts → Fallback to cached/default recommendations
- Invalid API keys → Clear error messages and graceful degradation
- Rate limiting → Retry mechanisms with exponential backoff

### Invalid Locations

- 404 responses → Return "N/A" values with appropriate messaging
- Spelling errors → Suggestion system (future enhancement)

### LLM Failures

- API timeouts → Rule-based fallback recommendations
- Invalid responses → Default agricultural advice based on weather patterns

## Performance Considerations

### API Rate Limits

- OpenWeatherMap: 1000 calls/day (free tier)
- Gemini LLM: Rate limits based on usage tier
- Implement caching for frequent locations

### Response Times

- Weather API: ~200-500ms average response time
- LLM generation: ~2-4 seconds for recommendations
- Total agent execution: ~3-5 seconds

### Optimization Strategies

- Cache weather data for 10-15 minutes
- Batch multiple location requests
- Asynchronous processing for multiple agents

## Future Enhancements

### Planned Features

1. **Extended Forecasts**: 7-day and 14-day weather predictions
2. **Historical Data**: Weather pattern analysis and trends
3. **Crop-Specific Models**: Specialized recommendations per crop type
4. **Regional Adaptation**: Local farming practice integration
5. **Weather Alerts**: Extreme weather notifications
6. **Seasonal Planning**: Long-term agricultural planning support

### Technical Improvements

1. **Caching Layer**: Redis integration for performance
2. **Monitoring**: Logging and metrics collection
3. **A/B Testing**: Recommendation quality optimization
4. **Multi-language**: Regional language support
5. **Mobile Optimization**: Lightweight response formats

## Troubleshooting

### Common Issues

**1. "WEATHER_API key is missing" Error**

```
Solution: Check .env file in env/ directory, ensure WEATHER_API is set
```

**2. "Failed to fetch weather data" Error**

```
Solution:
- Verify internet connection
- Check API key validity
- Confirm location name spelling
```

**3. "LLM recommendation failed" Error**

```
Solution:
- Check GEMINI_API_KEY in .env
- Verify Gemini API quota
- Check network connectivity
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Contributors

- **Weather Plugin Development**: Integration with OpenWeatherMap API
- **LLM Integration**: Gemini-powered recommendation system
- **Testing Framework**: Comprehensive test suite development
- **Documentation**: Complete system documentation

## License

This weather agent is part of the Agricultural Advisory System and follows the project's licensing terms.

---

**Last Updated**: August 11, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅
