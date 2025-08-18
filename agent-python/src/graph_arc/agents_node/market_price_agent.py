"""
Market Price Agent Node
Simple market data collector - no LLM calls
"""
from src.graph_arc.state import GlobalState
from src.utils.loggers import get_logger
from src.tools.mandi_price_tool import get_mandi_price
from typing import Dict, Any

def market_price_agent(state: GlobalState) -> Dict[str, Any]:
    """
    Collect market price data from mandi API - simple data gathering only.
    """
    logger = get_logger("market_price_agent")
    logger.info("[MarketPriceAgent] Collecting market price data")
    
    # Extract entities for API call
    entities = state.get("entities", {})
    commodity = entities.get("commodity", "Unknown")
    mandi_name = entities.get("mandi", None)
    market = entities.get("market", None)
    state_name = entities.get("state", None)
    district = entities.get("district", None)
    
    # Try to get price data from mandi API
    try:
        price_data = get_mandi_price.invoke({
            "commodity": commodity,
            "state": state_name,
            "district": district,
            "market": market or mandi_name
        })
        current_price = price_data if isinstance(price_data, (int, float)) else 0.0
        logger.info(f"[MarketPriceAgent] Price data collected for {commodity}: ₹{current_price}")
    except Exception as e:
        logger.error(f"[MarketPriceAgent] Failed to fetch price: {e}")
        current_price = None
    
    return {
        "commodity": commodity,
        "mandi_name": mandi_name or market,
        "current_price": current_price,
        "price_forecast": None,  # No individual forecasts - handled by aggregate node
        "selling_suggestion": None  # No individual suggestions - handled by aggregate node
    }
