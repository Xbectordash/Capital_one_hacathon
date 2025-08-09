from graph_arc.state import GlobalState

"""
User Context Node
Description: Detects user location, language, and device info.
"""

def get_user_context(state: GlobalState) -> GlobalState:
    """
    Returns user context (location, language, device) from request.
    """
    # Placeholder: Extract from request/session
    state["language"] = state.get("language") or "en"
    state["location"] = state.get("location") or "Delhi, India"
    state["device_type"] = state.get("device_type") or "web"

    print(f"[UserContextNode] Updated state: {state}")
    return state
