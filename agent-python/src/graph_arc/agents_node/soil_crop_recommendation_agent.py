"""
Soil & Crop Recommendation Agent Node
Description: Recommends crops based on soil and location data.
"""
from graph_arc.state import GlobalState, SoilAgentState
from utils.loggers import get_logger

def soil_crop_recommendation_agent(state: GlobalState) -> SoilAgentState:
    """
    Process soil and crop recommendation queries.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        SoilAgentState with soil information and crop recommendations
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info("[SoilCropAgent] Starting soil and crop recommendation analysis")
    
    # Extract relevant entities
    soil_type = state.get("entities", {}).get("soil_type", "Unknown")
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    
    logger.info(f"[SoilCropAgent] Analyzing soil type: {soil_type} for location: {location}")
    
    # Mock soil health data
    soil_health = {
        "ph": "6.5",
        "nitrogen": "Medium",
        "phosphorus": "High",
        "potassium": "Medium",
        "organic_matter": "3.2%"
    }
    
    logger.info(f"[SoilCropAgent] Soil health assessment: {soil_health}")
    
    # Generate crop recommendations based on soil type and location
    if soil_type.lower() == "black":
        recommended_crops = ["Cotton", "Sugarcane", "Wheat"]
        logger.info("[SoilCropAgent] Black soil detected - recommending cotton, sugarcane, wheat")
    elif soil_type.lower() == "red":
        recommended_crops = ["Groundnut", "Millet", "Rice"]
        logger.info("[SoilCropAgent] Red soil detected - recommending groundnut, millet, rice")
    elif soil_type.lower() == "alluvial":
        recommended_crops = ["Rice", "Wheat", "Sugarcane", "Maize"]
        logger.info("[SoilCropAgent] Alluvial soil detected - recommending rice, wheat, sugarcane, maize")
    else:
        recommended_crops = ["Wheat", "Maize", "Pulses"]
        logger.info(f"[SoilCropAgent] Unknown soil type '{soil_type}' - providing default recommendations")
    
    logger.info(f"[SoilCropAgent] Final crop recommendations: {recommended_crops}")
    
    # Return properly typed state
    result = SoilAgentState(
        soil_type=soil_type,
        soil_health=soil_health,
        recommended_crops=recommended_crops
    )
    
    logger.info("[SoilCropAgent] Soil and crop analysis completed successfully")
    return result
