# Import agent node functions
from graph_arc.agents_node.weather_agent import weather_agent
from graph_arc.agents_node.soil_crop_recommendation_agent import soil_crop_recommendation_agent
from graph_arc.agents_node.market_price_agent import market_price_agent
from graph_arc.agents_node.crop_health_pest_agent import crop_health_pest_agent
from graph_arc.agents_node.policy_finance_agent import policy_finance_agent
from graph_arc.core_nodes.offline_access_agent import offline_access_agent
# Import state types
from graph_arc.state import GlobalState, AgentResultsState
from utils.loggers import get_logger
from typing import Dict, Any, List, Union

def conditional_router(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Routes the query to appropriate agent nodes based on detected intents.
    In LangGraph, this node processes the state and returns an updated state
    with agent results added.
    
    Args:
        state: The current state containing user query, intents, and entities
        
    Returns:
        Updated state with agent results
    """
    logger = get_logger("conditional_router")
    logger.info("[ConditionalRouter] Starting agent routing process")
    
    intents = state.get("intents", [])
    raw_query = state.get("raw_query", "")
    
    logger.info(f"[ConditionalRouter] Processing query: '{raw_query}'")
    logger.info(f"[ConditionalRouter] Detected intents: {intents}")
    
    # Initialize empty results dictionary
    results: AgentResultsState = {}
    
    # Process each intent through the appropriate agent
    for intent in intents:
        logger.info(f"[ConditionalRouter] Processing intent: {intent}")
        
        if intent == "weather":
            logger.info("[ConditionalRouter] Invoking weather agent")
            results["weather"] = weather_agent(state)
            logger.info("[ConditionalRouter] Weather agent completed")
        elif intent == "soil":
            logger.info("[ConditionalRouter] Invoking soil crop recommendation agent")
            results["soil_crop_recommendation"] = soil_crop_recommendation_agent(state)
            logger.info("[ConditionalRouter] Soil crop agent completed")
        elif intent == "market":
            logger.info("[ConditionalRouter] Invoking market price agent")
            results["market_price"] = market_price_agent(state)
            logger.info("[ConditionalRouter] Market price agent completed")
        elif intent == "crop_health":
            logger.info("[ConditionalRouter] Invoking crop health pest agent")
            results["crop_health_pest"] = crop_health_pest_agent(state)
            logger.info("[ConditionalRouter] Crop health agent completed")
        elif intent == "policy":
            logger.info("[ConditionalRouter] Invoking policy finance agent")
            results["policy_finance"] = policy_finance_agent(state)
            logger.info("[ConditionalRouter] Policy finance agent completed")
        elif intent == "offline":
            logger.info("[ConditionalRouter] Invoking offline access agent")
            results["offline_access"] = offline_access_agent(state)
            logger.info("[ConditionalRouter] Offline access agent completed")
        elif intent not in ["translation", "decision_support"]:  # These are handled separately
            logger.warning(f"[ConditionalRouter] No handler found for intent: {intent}")
            results[intent] = {"error": f"No handler for intent '{intent}'"}
    
    logger.info(f"[ConditionalRouter] Agent routing completed. Processed {len(results)} agents")
    logger.info(f"[ConditionalRouter] Agent results keys: {list(results.keys())}")
    
    # In LangGraph style, we return the entire state with updates
    # We create a new dict to avoid mutating the input state
    return {**state, "agent_results": results}