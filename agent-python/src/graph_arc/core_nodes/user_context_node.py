from graph_arc.state import GlobalState
from utils.loggers import get_logger

"""
User Context Node
Description: Detects user location, language, and device info.
"""

def get_user_context(state: GlobalState) -> GlobalState:
    """
    Returns user context (location, language, device) from request.
    """
    logger = get_logger("user_context_node")
    logger.info("[UserContextNode] Starting user context extraction")
    
    # Placeholder: Extract from request/session
    original_language = state.get("language")
    original_location = state.get("location")
    original_device = state.get("device_type")
    
    state["language"] = state.get("language") or "en"
    state["location"] = state.get("location") or "Delhi, India"
    state["device_type"] = state.get("device_type") or "web"

    logger.info(f"[UserContextNode] Language: {original_language} -> {state['language']}")
    logger.info(f"[UserContextNode] Location: {original_location} -> {state['location']}")
    logger.info(f"[UserContextNode] Device type: {original_device} -> {state['device_type']}")
    
    print(f"[UserContextNode] Updated state: {state}")
    logger.info("[UserContextNode] User context extraction completed successfully")
    return state
