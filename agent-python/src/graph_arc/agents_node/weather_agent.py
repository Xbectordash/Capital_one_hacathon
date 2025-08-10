"""
Weather Agent Node
Description: Provides weather information and forecasts for a given location.
"""
from typing import Optional
from graph_arc.state import GlobalState, WeatherAgentState
from utils.loggers import get_logger

def weather_agent(state: GlobalState) -> WeatherAgentState:
    """
    Process weather-related queries and return weather information.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        WeatherAgentState with forecast and recommendations
    """
    logger = get_logger("weather_agent")
    logger.info("[WeatherAgent] Starting weather analysis")
    
    # Extract location from state
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    logger.info(f"[WeatherAgent] Processing weather for location: {location}")
    
    # Extract date information if available
    date_info = state.get("entities", {}).get("date", "today")
    logger.info(f"[WeatherAgent] Date requested: {date_info}")
    
    # Mock forecast data
    forecast = {
        "temperature": "32°C",
        "condition": "Sunny",
        "humidity": "45%",
        "wind_speed": "10 km/h",
        "precipitation": "0%"
    }
    
    # Generate recommendation based on weather
    recommendation = "Good day for crop spraying. Consider irrigation due to high temperatures."
    
    logger.info(f"[WeatherAgent] Generated forecast: {forecast}")
    logger.info(f"[WeatherAgent] Weather recommendation: {recommendation}")
    
    # Return properly typed state
    result = WeatherAgentState(
        date_range=date_info,
        forecast=forecast,
        recommendation=recommendation
    )
    
    logger.info("[WeatherAgent] Weather analysis completed successfully")
    return result
