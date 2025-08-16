"""
Soil & Crop Recommendation Agent Node
Simple CSV soil data collector - no LLM calls
"""
from src.graph_arc.state import GlobalState, SoilAgentState
from src.utils.loggers import get_logger
from src.data.soil_plugins import get_soil_data_from_csv

def soil_crop_recommendation_agent(state: GlobalState) -> SoilAgentState:
    """
    Collect soil data from CSV - simple data gathering only.
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info("[SoilCropAgent] Collecting soil data")
    
    # Extract location from state
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    user_query = state.get("raw_query", "")
    
    # Fetch soil data using CSV
    try:
        soil_health = get_soil_data_from_csv(location, user_query)
        soil_type = soil_health.get("soil_type", "Unknown")
        recommended_crops = soil_health.get("recommended_crops", [])
        logger.info(f"[SoilCropAgent] Soil data collected for {location}")
    except Exception as e:
        logger.error(f"[SoilCropAgent] Failed to fetch soil data: {e}")
        soil_health = {"error": str(e)}
        soil_type = "Unknown"
        recommended_crops = []
    
    return SoilAgentState(
        soil_type=soil_type,
        soil_health=soil_health,
        recommended_crops=recommended_crops,
        ai_recommendation=None  # No individual recommendations - handled by aggregate node
    )
