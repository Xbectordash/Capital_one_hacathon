"""
Crop Health & Pest Agent Node
Simple crop health data collector - no LLM calls
"""
from src.graph_arc.state import GlobalState, CropHealthState
from src.utils.loggers import get_logger

def crop_health_pest_agent(state: GlobalState) -> CropHealthState:
    """
    Collect crop health information - simple data gathering only.
    """
    logger = get_logger("crop_health_pest_agent")
    logger.info("[CropHealthAgent] Collecting crop health data")
    
    # Extract entities
    crop_type = state.get("entities", {}).get("crop", "Unknown")
    symptoms_raw = state.get("entities", {}).get("symptoms", [])
    
    # Convert symptoms to list format
    if isinstance(symptoms_raw, str):
        symptoms = [symptoms_raw]
    elif isinstance(symptoms_raw, list):
        symptoms = symptoms_raw
    else:
        symptoms = []
    
    logger.info(f"[CropHealthAgent] Crop health data collected for {crop_type}")
    
    return CropHealthState(
        crop_type=crop_type,
        symptoms=symptoms,
        diagnosis=None,  # No individual diagnosis - handled by aggregate node
        treatment=None   # No individual treatment - handled by aggregate node
    )
