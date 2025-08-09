# src/config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get your API key for Gemini from here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_config():
    """
    Returns configuration settings as a dictionary.
    """
    return {
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }

if __name__ == "__main__":
    # Check if settings are loading correctly
    config = get_config()
    print("Config Loaded:")
    for key, value in config.items():
        print(f"  {key}: {'[SECRET]' if 'API_KEY' in key else value}")