"""
Weather Agent Node
Simple weather data collector - no LLM calls
"""
from src.graph_arc.state import GlobalState, WeatherAgentState
from src.utils.loggers import get_logger
from src.data.weather_plugins import fetch_weather_data

def weather_agent(state: GlobalState) -> WeatherAgentState:
    """
    Collect weather data from API - simple data gathering only.
    """
    logger = get_logger("weather_agent")
    logger.info("[WeatherAgent] Collecting weather data")
    
    # Extract location from state
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    
    # Fetch weather data
    try:
        forecast = fetch_weather_data(location)
        logger.info(f"[WeatherAgent] Weather data collected for {location}")
    except Exception as e:
        logger.error(f"[WeatherAgent] Failed to fetch weather: {e}")
        forecast = {
            "temperature": "N/A",
            "condition": "N/A", 
            "humidity": "N/A",
            "wind_speed": "N/A",
            "precipitation": "N/A"
        }
    
    return WeatherAgentState(
        date_range="today",
        forecast=forecast,
        recommendation=None  # No individual recommendations - handled by aggregate node
    )
