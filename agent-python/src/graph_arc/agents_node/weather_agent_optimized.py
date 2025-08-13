"""
Optimized Weather Agent Node
Description: Fast weather information and forecasts with optimized LLM calls.
"""
from src.graph_arc.state import GlobalState, WeatherAgentState
from src.utils.loggers import get_logger
from src.data.weather_plugins import fetch_weather_data
from src.graph_arc.llm_optimizer import get_optimized_llm_response, get_agent_prompt
import asyncio
import json

async def weather_agent_optimized(state: GlobalState) -> WeatherAgentState:
    """
    Optimized weather agent with faster processing and smart caching
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        WeatherAgentState with forecast and recommendations
    """
    logger = get_logger("weather_agent_optimized")
    logger.info("[WeatherAgentOpt] Starting optimized weather analysis")
    
    # Extract location from state
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    logger.info(f"[WeatherAgentOpt] Processing weather for location: {location}")

    # Fetch real weather data using the plugin (this is fast)
    try:
        forecast = fetch_weather_data(location)
        logger.info(f"[WeatherAgentOpt] Weather data retrieved: {forecast}")
    except ValueError as e:
        logger.error(f"[WeatherAgentOpt] Failed to fetch weather data: {e}")
        forecast = {
            "temperature": "N/A",
            "condition": "N/A", 
            "humidity": "N/A",
            "wind_speed": "N/A",
            "precipitation": "N/A"
        }

    # Skip LLM for missing weather data
    if forecast.get("temperature") == "N/A":
        logger.warning("[WeatherAgentOpt] Weather data unavailable, using fallback")
        recommendation = "Because critical weather data (temperature, humidity, precipitation, wind speed) for " + \
                        f"{location} is missing, I cannot provide specific irrigation, spraying, or harvesting recommendations. " + \
                        "To determine if irrigation is needed today, immediately obtain a local weather report for " + \
                        f"{location}, including temperature, humidity, and rainfall data. Then, assess soil moisture " + \
                        "and crop water stress levels to make an informed decision."
        
        result = WeatherAgentState(
            date_range="today",
            forecast=forecast,
            recommendation=recommendation
        )
        logger.info("[WeatherAgentOpt] Returned fallback recommendation")
        return result

    # Generate optimized recommendation using cached LLM
    try:
        logger.info("[WeatherAgentOpt] Generating optimized LLM recommendation")
        
        # Prepare optimized prompt data
        prompt_data = {
            "location": location,
            "raw_query": state.get("raw_query", "General weather advice request"),
            "weather_forecast": forecast
        }
        
        # Get optimized prompt
        optimized_prompt = get_agent_prompt("weather", prompt_data)
        
        # Use optimized LLM call with caching
        recommendation = await get_optimized_llm_response(optimized_prompt, "fast")
        
        logger.info(f"[WeatherAgentOpt] Generated optimized recommendation: {recommendation[:100]}...")
        
    except Exception as e:
        logger.error(f"[WeatherAgentOpt] LLM optimization failed: {e}")
        # Fast fallback to rule-based recommendation
        temp_val = float(forecast.get("temperature", "0").replace("°C", "").replace("°", ""))
        humidity_val = int(forecast.get("humidity", "0").replace("%", ""))
        condition = forecast.get("condition", "").lower()
        
        if "rain" in condition or "storm" in condition:
            recommendation = f"Rain expected in {location}. Avoid field operations and protect crops from waterlogging."
        elif temp_val > 30 and humidity_val < 60:
            recommendation = f"Hot and dry conditions in {location} ({temp_val}°C, {humidity_val}% humidity). " + \
                           "Consider irrigation and avoid midday fieldwork."
        elif temp_val > 25 and "clear" in condition:
            recommendation = f"Good weather conditions in {location}. Suitable for spraying and field operations."
        else:
            recommendation = f"Monitor weather conditions in {location}. Adjust farming activities based on " + \
                           f"current temperature ({forecast['temperature']}) and conditions ({forecast['condition']})."

    logger.info(f"[WeatherAgentOpt] Generated forecast: {forecast}")
    logger.info(f"[WeatherAgentOpt] Weather recommendation: {recommendation}")
    
    # Return properly typed state
    result = WeatherAgentState(
        date_range="today",
        forecast=forecast,
        recommendation=recommendation
    )
    
    logger.info("[WeatherAgentOpt] Optimized weather analysis completed successfully")
    return result

# Wrapper for sync compatibility
def weather_agent_fast(state: GlobalState) -> WeatherAgentState:
    """Synchronous wrapper for optimized weather agent"""
    return asyncio.run(weather_agent_optimized(state))
