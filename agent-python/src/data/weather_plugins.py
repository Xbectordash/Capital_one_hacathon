import os
import requests
from typing import Dict
from src.utils.loggers import get_logger
from src.config.settings import WEATHER_API

def fetch_weather_data(city_name: str) -> Dict:
    """
    Fetch current weather data for a given city using OpenWeatherMap API.

    Args:
        city_name (str): Name of the city to fetch weather data for.

    Returns:
        Dict: A dictionary containing weather details (temperature, condition, humidity, wind speed, precipitation).
    """
    logger = get_logger("weather_plugins")
    logger.info(f"[WeatherPlugins] Fetching weather data for city: {city_name}")

    # Get API key from environment variables
    
    if not WEATHER_API:
        logger.error("[WeatherPlugins] WEATHER_API key is not set in the environment variables.")
        raise ValueError("WEATHER_API key is missing.")

    # Construct the API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&units=metric"

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data from the API response
        forecast = {
            "temperature": f"{data['main']['temp']}°C",
            "condition": data['weather'][0]['main'],
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} km/h",
            "precipitation": f"{data.get('rain', {}).get('1h', 0)} mm"
        }

        logger.info(f"[WeatherPlugins] Weather data fetched successfully: {forecast}")
        return forecast

    except requests.exceptions.RequestException as e:
        logger.error(f"[WeatherPlugins] Error fetching weather data: {e}")
        raise ValueError("Failed to fetch weather data.")