"""
Weather Agent Node
Description: Provides weather information and forecasts for a given location.
"""

def get_weather(location: str, date: str = None) -> str:
    """
    Returns weather info for the given location and date.
    """
    # Placeholder: Integrate with weather API
    return f"Weather for {location} on {date or 'today'}: Sunny, 32°C."
