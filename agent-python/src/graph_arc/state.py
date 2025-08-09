from typing import TypedDict, Optional

class GlobalState(TypedDict):
    user_id: str
    location: Optional[str]        # Detected from context node
    language: str                  # User preferred/detected language
    device_type: Optional[str]     # Phone/SMS/IVR
    raw_query: str
    intents: list[str]              # ["weather", "soil", ...]
    entities: dict                  # {"crop": "wheat", "mandi": "Azadpur"}
    confidence_score: float

class WeatherAgentState(TypedDict):
    date_range: Optional[str]
    forecast: Optional[dict]
    recommendation: Optional[str]

class SoilAgentState(TypedDict):
    soil_type: Optional[str]
    soil_health: Optional[dict]
    recommended_crops: Optional[list[str]]

class CropHealthState(TypedDict):
    crop_type: str
    symptoms: list[str]
    diagnosis: Optional[str]
    treatment: Optional[str]

class MarketState(TypedDict):
    commodity: str
    mandi_name: Optional[str]
    current_price: Optional[float]
    price_forecast: Optional[str]
    selling_suggestion: Optional[str]

class PolicyState(TypedDict):
    relevant_schemes: list[dict]    # [{"name": "...", "link": "..."}]
    eligibility: Optional[str]
    application_steps: Optional[str]

class OfflineState(TypedDict):
    channel_type: str               # SMS / IVR
    message_format: Optional[str]

class DecisionState(TypedDict):
    aggregated_data: dict           # merged from other agents
    final_advice: str
    explanation: str

class TranslationState(TypedDict):
    detected_language: str
    translated_query: str
    translated_response: Optional[str]
