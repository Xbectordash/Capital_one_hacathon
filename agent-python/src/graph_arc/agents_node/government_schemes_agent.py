"""
Government Schemes Agent Node
Simple schemes data collector - no LLM calls
"""
from src.graph_arc.state import GlobalState
from src.utils.loggers import get_logger
from src.data.government_schemes_plugin import get_schemes_by_location_and_profile
from typing import Dict, Any

def government_schemes_agent(state: GlobalState) -> Dict[str, Any]:
    """
    Collect government schemes data - simple data gathering only.
    """
    logger = get_logger("government_schemes_agent")
    logger.info("[GovSchemesAgent] Collecting schemes data")
    
    # Extract basic info
    location = state.get("location", "Unknown")
    entities = state.get("entities", {})
    
    # Create basic farmer profile
    farmer_profile = {
        "farmer_type": entities.get("farmer_type", "small"),
        "crop_type": entities.get("crop", "all"),
        "land_size": 2.0
    }
    
    # Get schemes data
    try:
        schemes_data = get_schemes_by_location_and_profile(location, farmer_profile)
        relevant_schemes = schemes_data.get("schemes", [])[:3]  # Top 3 schemes
        logger.info(f"[GovSchemesAgent] Schemes data collected for {location}")
    except Exception as e:
        logger.error(f"[GovSchemesAgent] Failed to fetch schemes: {e}")
        relevant_schemes = []
    
    return {
        "relevant_schemes": relevant_schemes,
        "eligibility": None,        # No individual eligibility - handled by aggregate node
        "application_steps": None   # No individual steps - handled by aggregate node
    }
