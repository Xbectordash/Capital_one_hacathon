"""
Crop Health & Pest Agent Node
Description: Diagnoses crop health and pest issues.
"""
from src.graph_arc.state import GlobalState, CropHealthState
from src.utils.loggers import get_logger

def crop_health_pest_agent(state: GlobalState) -> CropHealthState:
    """
    Process crop health and pest-related queries.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        CropHealthState with diagnosis and treatment recommendations
    """
    logger = get_logger("crop_health_pest_agent")
    logger.info("[CropHealthAgent] Starting crop health and pest analysis")
    
    # Extract relevant entities
    crop_type = state.get("entities", {}).get("crop", "Unknown")
    symptoms_raw = state.get("entities", {}).get("symptoms", [])
    
    logger.info(f"[CropHealthAgent] Analyzing crop: {crop_type}")
    logger.info(f"[CropHealthAgent] Raw symptoms data: {symptoms_raw}")
    
    # Convert symptoms to list if it's a string
    if isinstance(symptoms_raw, str):
        symptoms = [symptoms_raw]
        logger.info("[CropHealthAgent] Converted string symptoms to list")
    elif isinstance(symptoms_raw, list):
        symptoms = symptoms_raw
        logger.info("[CropHealthAgent] Using provided list of symptoms")
    else:
        symptoms = []
        logger.warning("[CropHealthAgent] No recognizable symptoms provided")
    
    logger.info(f"[CropHealthAgent] Processing symptoms: {symptoms}")
    
    # Generate diagnosis based on crop and symptoms
    if "yellow" in str(symptoms).lower() and "leaves" in str(symptoms).lower():
        diagnosis = "Possible nitrogen deficiency or fungal infection."
        treatment = "Apply nitrogen-rich fertilizer and check for proper irrigation. Consider fungicide application if symptoms persist."
        logger.info("[CropHealthAgent] Diagnosed: Yellow leaves - nitrogen deficiency/fungal infection")
    elif "spots" in str(symptoms).lower():
        diagnosis = "Possible fungal leaf spot disease."
        treatment = "Apply copper-based fungicide. Ensure proper spacing between plants for air circulation."
        logger.info("[CropHealthAgent] Diagnosed: Spots - fungal leaf spot disease")
    elif "wilting" in str(symptoms).lower():
        diagnosis = "Possible root rot or bacterial wilt."
        treatment = "Check irrigation practices. Avoid waterlogging. Apply appropriate bactericide."
        logger.info("[CropHealthAgent] Diagnosed: Wilting - root rot/bacterial wilt")
    else:
        diagnosis = f"General health assessment for {crop_type}: Unable to diagnose specific issue without more symptoms."
        treatment = "Monitor crop closely. Take photos of affected areas for more accurate diagnosis."
        logger.info("[CropHealthAgent] General assessment - insufficient symptoms for specific diagnosis")
    
    logger.info(f"[CropHealthAgent] Final diagnosis: {diagnosis}")
    logger.info(f"[CropHealthAgent] Treatment recommendation: {treatment}")
    
    # Return properly typed state
    result = CropHealthState(
        crop_type=crop_type,
        symptoms=symptoms,
        diagnosis=diagnosis,
        treatment=treatment
    )
    
    logger.info("[CropHealthAgent] Crop health analysis completed successfully")
    return result
