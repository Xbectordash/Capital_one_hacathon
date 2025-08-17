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
    agent_results: Optional[dict]   # Results from various agents
    decision: Optional[dict]        # Final decision from decision support
    translation: Optional[dict]     # Translation results from translation agent