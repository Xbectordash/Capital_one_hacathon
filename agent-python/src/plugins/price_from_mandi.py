
import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("AGMARKNET_API_KEY")

class AgmarknetAPIClient:
    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    def __init__(self):
        if not API_KEY:
            raise ValueError("API key not found. Set AGMARKNET_API_KEY in your .env file.")

    def __call__(
        self,
        state: str = "Maharashtra",
        district: str = "Dhule",
        limit: int = 10,
        offset: int = 0,
        commodity: str = None,
        variety: str = None,
        grade: str = None
    ) -> list[dict]:
        """
        Fetch data from Agmarknet API with optional filters.
        Returns a list of records (dictionaries).
        """
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state.keyword]": state,
            "filters[district]": district,
        }

        # Optional filters
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

class PriceFromMandi:
    def __init__(self):
        self.api_client = AgmarknetAPIClient()

    def get_price(self, commodity,state, district, market):
        # Clean and validate inputs
        commodity = commodity.strip() if commodity else ""
        state = state.strip() if state else ""
        district = district.strip() if district else ""
        market = market.strip() if market else ""

        if not commodity:
            print("Commodity name is required.")
            return 0
        if not state:
            print("State name is required.")
            return 0
        if not district:
            print("District name is required.")
            return 0
        if not market:
            print("Market name is required.")
            return 0

        # Fetch mandi data from API
        records = self.api_client(
            state=state,
            district=district,
            commodity=commodity,
            limit=1
        )

        if not records:
            print("No mandi data found.")
            return 0

        # Extract price information (try 'modal_price', fallback to 'min_price')
        record = records[0]
        price = record.get("modal_price") or record.get("min_price") or 0
        try:
            return float(price)
        except Exception:
            return 0

