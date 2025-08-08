
import os
import requests
from dotenv import load_dotenv

# Always load .env from repo root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'env', '.env'))
API_KEY = os.getenv("AGMARKNET_API_KEY")

class AgmarknetAPIClient:
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    def __init__(self):
        if not API_KEY:
            raise ValueError("API key not found. Set AGMARKNET_API_KEY in your .env file.")

    def __call__(
        self,
        state: str = None,
        district: str = None,
        market: str = None,
        commodity: str = None,
        variety: str = None,
        grade: str = None,
        limit: int = 10,
        offset: int = 0,
        format: str = "json"
    ) -> list[dict]:
        """
        Fetch data from Agmarknet API with optional filters.
        Returns a list of records (dictionaries).
        """
        params = {
            "api-key": API_KEY,
            "format": format,
            "limit": limit,
            "offset": offset,
        }
        if state:
            params["filters[state.keyword]"] = state
        if district:
            params["filters[district]"] = district
        if market:
            params["filters[market]"] = market
        if commodity:
            params["filters[commodity]"] = commodity
        if variety:
            params["filters[variety]"] = variety
        if grade:
            params["filters[grade]"] = grade

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=20)
            response.raise_for_status()
            return response.json().get("records", [])
        except Exception as e:
            print(f"[AgmarknetAPIClient] Error: {e}")
            return []

