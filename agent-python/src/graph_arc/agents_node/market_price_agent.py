"""
Market Price Agent Node
Description: Provides market price information for commodities.
"""
from src.graph_arc.state import GlobalState, MarketState
from src.utils.loggers import get_logger

def market_price_agent(state: GlobalState) -> MarketState:
    """
    Process market price queries and return price information.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        MarketState with price information and recommendations
    """
    logger = get_logger("market_price_agent")
    logger.info("[MarketPriceAgent] Starting market price analysis")
    
    # Extract relevant entities
    commodity = state.get("entities", {}).get("commodity", "Unknown")
    mandi_name = state.get("entities", {}).get("mandi", None)
    
    logger.info(f"[MarketPriceAgent] Analyzing price for commodity: {commodity}")
    if mandi_name:
        logger.info(f"[MarketPriceAgent] Target mandi: {mandi_name}")
    else:
        logger.info("[MarketPriceAgent] No specific mandi specified, using general pricing")
    
    # Mock current price data (would come from API/database)
    current_price = 2000.0  # in INR per quintal
    logger.info(f"[MarketPriceAgent] Current price retrieved: ₹{current_price}/quintal")
    
    # Generate price forecast and selling suggestions
    price_forecast = "Prices expected to rise by 5% in the next week due to festival season demand."
    
    if current_price > 1800:
        selling_suggestion = "Consider selling now as prices are above average."
        logger.info("[MarketPriceAgent] Price is above average - recommending immediate sale")
    else:
        selling_suggestion = "Consider holding for better prices if storage is available."
        logger.info("[MarketPriceAgent] Price is below average - recommending to hold")
    
    logger.info(f"[MarketPriceAgent] Price forecast: {price_forecast}")
    logger.info(f"[MarketPriceAgent] Selling suggestion: {selling_suggestion}")
    
    # Return properly typed state
    result = MarketState(
        commodity=commodity,
        mandi_name=mandi_name,
        current_price=current_price,
        price_forecast=price_forecast,
        selling_suggestion=selling_suggestion
    )
    
    logger.info("[MarketPriceAgent] Market price analysis completed successfully")
    return result
