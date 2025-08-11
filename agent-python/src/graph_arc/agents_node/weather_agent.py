"""
Weather Agent Node
Description: Provides weather information and forecasts for a given location.
"""
from typing import Optional
from graph_arc.state import GlobalState, WeatherAgentState
from utils.loggers import get_logger
from data.weather_plugins import fetch_weather_data
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
from graph_arc.prompts import weather_recommendation_prompt

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

    # Fetch real weather data using the plugin
    try:
        forecast = fetch_weather_data(location)
        logger.info(forecast);
    except ValueError as e:
        logger.error(f"[WeatherAgent] Failed to fetch weather data: {e}")
        forecast = {
            "temperature": "N/A",
            "condition": "N/A",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "precipitation": "N/A"
        }

    # Generate recommendation based on weather using LLM
    try:
        logger.info("[WeatherAgent] Initializing LLM for weather recommendation")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            max_output_tokens=500,
            api_key=GEMINI_API_KEY,
        )
        
        # Format the prompt with weather data and user query
        format_prompt = weather_recommendation_prompt.format(
            temperature=forecast["temperature"],
            condition=forecast["condition"],
            humidity=forecast["humidity"],
            wind_speed=forecast["wind_speed"],
            precipitation=forecast["precipitation"],
            location=location,
            user_query=state.get("raw_query", "General weather advice request")
        )
        
        logger.info("[WeatherAgent] Invoking LLM for weather recommendation")
        response = llm.invoke(format_prompt)
        recommendation = response.content.strip()
        logger.info(f"[WeatherAgent] LLM generated recommendation: {recommendation}")
        
    except Exception as e:
        logger.error(f"[WeatherAgent] Failed to generate LLM recommendation: {e}")
        # Fallback to simple rule-based recommendation
        if forecast["condition"].lower() in ["clear", "sunny"]:
            recommendation = "Good day for crop spraying. Consider irrigation due to high temperatures."
        elif forecast["condition"].lower() in ["rain", "drizzle", "thunderstorm"]:
            recommendation = "Avoid field operations due to rain. Monitor drainage and protect crops from waterlogging."
        else:
            recommendation = "Monitor weather conditions closely and adjust farming activities accordingly."

    logger.info(f"[WeatherAgent] Generated forecast: {forecast}")
    logger.info(f"[WeatherAgent] Weather recommendation: {recommendation}")
    
    # Return properly typed state
    result = WeatherAgentState(
        date_range="today",  # Keeping date as "today" for now
        forecast=forecast,
        recommendation=recommendation
    )
    
    logger.info("[WeatherAgent] Weather analysis completed successfully")
    return result
