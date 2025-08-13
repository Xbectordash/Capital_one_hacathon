"""
Optimized Decision Support Node
Description: Fast aggregation of agent outputs with streamlined LLM processing.
"""
from src.graph_arc.state import GlobalState, AgentResultsState, DecisionState
from src.utils.loggers import get_logger
from langchain_core.runnables import RunnableConfig
from src.config.model_conf import Configuration
from src.graph_arc.llm_optimizer import get_optimized_llm_response, get_agent_prompt
from typing import Dict, Any
import json
import asyncio

async def aggregate_decisions_optimized(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """
    Optimized decision aggregation with fast LLM processing and smart fallbacks.
    
    Args:
        state: The current state with agent_results from the router
        config: LangGraph configuration
        
    Returns:
        Updated state with optimized decision support information
    """
    logger = get_logger("aggregate_decisions_optimized")
    logger.info("[AggregateDecisionsOpt] Starting optimized decision aggregation")
    
    # Extract agent results from the state
    agent_results = state.get("agent_results", {})
    original_query = state.get("raw_query", "")
    location = state.get("location", "Unknown")
    
    logger.info(f"[AggregateDecisionsOpt] Processing {len(agent_results)} agent results")
    logger.info(f"[AggregateDecisionsOpt] Available agents: {list(agent_results.keys())}")
    
    # Quick validation and filtering
    valid_results = {}
    for agent_type, agent_output in agent_results.items():
        if agent_output and not agent_output.get("error"):
            valid_results[agent_type] = agent_output
    
    logger.info(f"[AggregateDecisionsOpt] Valid results from {len(valid_results)} agents")
    
    # Fast fallback for no valid results
    if not valid_results:
        logger.warning("[AggregateDecisionsOpt] No valid agent results, using quick fallback")
        fallback_decision = DecisionState(
            aggregated_data={},
            final_advice=f"Unable to get specific recommendations for {location}. Please provide more details about your agricultural needs or check your internet connection.",
            explanation="No agent data was available for analysis."
        )
        return {**state, "decision": fallback_decision}
    
    # Prioritize important agents for faster decisions
    priority_agents = ["weather", "soil_crop_recommendation", "market_price"]
    has_priority_data = any(agent in valid_results for agent in priority_agents)
    
    try:
        if has_priority_data and len(valid_results) <= 2:
            # Fast path: Use rule-based decision for simple cases
            logger.info("[AggregateDecisionsOpt] Using fast rule-based decision path")
            decision = await _generate_fast_decision(valid_results, original_query, location, logger)
        else:
            # Standard path: Use optimized LLM
            logger.info("[AggregateDecisionsOpt] Using optimized LLM decision path")
            decision = await _generate_llm_decision(valid_results, original_query, location, logger)
        
        logger.info(f"[AggregateDecisionsOpt] Decision generated: {decision['final_advice'][:100]}...")
        return {**state, "decision": decision}
        
    except Exception as e:
        logger.error(f"[AggregateDecisionsOpt] Error during optimization: {e}")
        # Ultra-fast fallback
        return await _generate_emergency_fallback(valid_results, original_query, location, logger, state)

async def _generate_fast_decision(valid_results: Dict[str, Any], query: str, location: str, logger) -> DecisionState:
    """Generate fast rule-based decision for simple cases"""
    logger.info("[AggregateDecisionsOpt] Generating fast rule-based decision")
    
    advice_parts = []
    explanation_parts = []
    
    # Weather-based advice
    if "weather" in valid_results:
        weather = valid_results["weather"]
        weather_advice = weather.get("recommendation", "")
        if weather_advice:
            advice_parts.append(weather_advice)
            explanation_parts.append("• Weather conditions analyzed")
    
    # Soil-based advice
    if "soil_crop_recommendation" in valid_results:
        soil = valid_results["soil_crop_recommendation"]
        if soil.get("recommended_crops"):
            crops = soil["recommended_crops"][:3]  # Top 3 crops
            advice_parts.append(f"Recommended crops for {location}: {', '.join(crops)}")
            explanation_parts.append("• Soil analysis and crop suitability evaluated")
    
    # Market advice
    if "market_price" in valid_results:
        market = valid_results["market_price"]
        if market.get("selling_suggestion"):
            advice_parts.append(market["selling_suggestion"])
            explanation_parts.append("• Market prices and trends considered")
    
    # Combine advice
    if advice_parts:
        final_advice = " ".join(advice_parts)
    else:
        final_advice = f"Based on available data for {location}, monitor weather conditions and consider local agricultural extension advice."
    
    explanation = "\n".join(explanation_parts) if explanation_parts else "Analysis based on available agricultural data."
    
    return DecisionState(
        aggregated_data=valid_results,
        final_advice=final_advice,
        explanation=explanation
    )

async def _generate_llm_decision(valid_results: Dict[str, Any], query: str, location: str, logger) -> DecisionState:
    """Generate LLM-based decision with optimization"""
    logger.info("[AggregateDecisionsOpt] Generating optimized LLM decision")
    
    # Prepare optimized prompt data
    prompt_data = {
        "location": location,
        "raw_query": query,
        "agent_results": valid_results
    }
    
    # Get optimized prompt
    optimized_prompt = get_agent_prompt("decision", prompt_data)
    
    # Use optimized LLM call
    response = await get_optimized_llm_response(optimized_prompt, "decision")
    
    try:
        # Try to parse JSON response
        parsed_response = json.loads(response)
        final_advice = parsed_response.get("final_advice", response)
        explanation = parsed_response.get("explanation", "LLM-generated agricultural recommendation")
        
    except json.JSONDecodeError:
        # Use raw response if JSON parsing fails
        logger.warning("[AggregateDecisionsOpt] Could not parse LLM JSON, using raw response")
        final_advice = response
        explanation = "Comprehensive agricultural analysis based on available data"
    
    return DecisionState(
        aggregated_data=valid_results,
        final_advice=final_advice,
        explanation=explanation
    )

async def _generate_emergency_fallback(valid_results: Dict[str, Any], query: str, location: str, logger, state: Dict[str, Any]) -> Dict[str, Any]:
    """Ultra-fast emergency fallback"""
    logger.warning("[AggregateDecisionsOpt] Using emergency fallback decision")
    
    emergency_advice = f"Agricultural data processed for {location}. "
    
    if "weather" in valid_results:
        emergency_advice += "Check weather conditions before field operations. "
    if "soil" in valid_results or "soil_crop_recommendation" in valid_results:
        emergency_advice += "Consider soil-appropriate crops for current season. "
    if "market" in valid_results or "market_price" in valid_results:
        emergency_advice += "Monitor market prices before selling produce."
    
    emergency_decision = DecisionState(
        aggregated_data=valid_results,
        final_advice=emergency_advice,
        explanation="Emergency fallback recommendation based on available data."
    )
    
    return {**state, "decision": emergency_decision}

# Wrapper for sync compatibility
def aggregate_decisions_fast(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """Synchronous wrapper for optimized decision aggregation"""
    return asyncio.run(aggregate_decisions_optimized(state, config))
