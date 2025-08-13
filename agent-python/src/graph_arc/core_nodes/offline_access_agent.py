"""
Offline Access Agent Node
Description: Provides offline access to agricultural information.
"""
from src.graph_arc.state import GlobalState, OfflineState
from src.utils.loggers import get_logger

def offline_access_agent(state: GlobalState) -> OfflineState:
    """
    Process offline access requests and format information for offline channels.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        OfflineState with formatted information for offline access
    """
    logger = get_logger("offline_access_agent")
    logger.info("[OfflineAccessAgent] Starting offline access processing")
    
    # Extract device type or default to SMS
    device_type = state.get("device_type", "SMS").upper()
    logger.info(f"[OfflineAccessAgent] Device type detected: {device_type}")
    
    # Determine the appropriate channel type and format
    if device_type == "IVR":
        channel_type = "IVR"
        message_format = "short_audio"
        logger.info("[OfflineAccessAgent] Configured for IVR with short audio format")
    elif device_type == "FEATURE_PHONE":
        channel_type = "SMS"
        message_format = "short_text"
        logger.info("[OfflineAccessAgent] Configured for feature phone with short text format")
    else:
        channel_type = "SMS"
        message_format = "medium_text"
        logger.info("[OfflineAccessAgent] Configured for default SMS with medium text format")
    
    # Return properly typed state
    result = OfflineState(
        channel_type=channel_type,
        message_format=message_format
    )
    
    logger.info(f"[OfflineAccessAgent] Offline access configuration: {result}")
    logger.info("[OfflineAccessAgent] Offline access processing completed successfully")
    return result
