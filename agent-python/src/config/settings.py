# src/config/settings.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Get the path to the project root (agent-python folder)
project_root = Path(__file__).resolve().parent.parent.parent

# Try multiple .env file locations for flexibility
env_paths = [
    project_root / ".env",           # Root level (preferred for deployment)
    project_root / "env" / ".env",   # Subfolder (legacy)
    Path("/app/.env"),               # Docker/Render deployment path
]

# Load environment variables from the first available .env file
env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"📄 Loaded environment from: {env_path}")
        env_loaded = True
        break

if not env_loaded:
    print("⚠️  No .env file found, using system environment variables")
    load_dotenv()  # Load from system environment

# Get your API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API = os.getenv("WEATHER_API")
QUERY_UNDERSTANDING_MODEL = os.getenv("QUERY_UNDERSTANDING_MODEL", "gemini-2.0-flash")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY")

# Production/Development settings
NODE_ENV = os.getenv("NODE_ENV", "development")
PORT = int(os.getenv("PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Detect production environment
IS_PRODUCTION = NODE_ENV == "production" or os.getenv("RENDER") == "true"

def get_config():
    """
    Returns configuration settings as a dictionary.
    """
    return {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "WEATHER_API": WEATHER_API,
        "QUERY_UNDERSTANDING_MODEL": QUERY_UNDERSTANDING_MODEL,
        "LANGSMITH_TRACING": LANGSMITH_TRACING,
        "LANGSMITH_ENDPOINT": LANGSMITH_ENDPOINT,
        "LANGSMITH_API_KEY": LANGSMITH_API_KEY,
        "AGMARKNET_API_KEY": AGMARKNET_API_KEY,
        "NODE_ENV": NODE_ENV,
        "PORT": PORT,
        "LOG_LEVEL": LOG_LEVEL,
        "IS_PRODUCTION": IS_PRODUCTION,
        "PROJECT_ROOT": str(project_root),
    }

def validate_config():
    """
    Validates that required configuration is present.
    """
    required_keys = ["GEMINI_API_KEY", "WEATHER_API"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        return False
    
    print("✅ All required environment variables are configured")
    return True

if __name__ == "__main__":
    # Check if settings are loading correctly
    config = get_config()
    print("📋 Configuration Loaded:")
    for key, value in config.items():
        if 'API_KEY' in key or 'SECRET' in key:
            masked_value = '[SECRET]' if value else '[NOT SET]'
            print(f"  {key}: {masked_value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n🔍 Validation:")
    validate_config()