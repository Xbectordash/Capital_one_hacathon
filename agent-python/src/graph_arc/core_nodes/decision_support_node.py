"""
Decision Support Node
Description: Aggregates outputs from all agent nodes for final advice using LLM.
"""
from src.graph_arc.state import GlobalState
from src.utils.loggers import get_logger
from langchain_core.runnables import RunnableConfig
from src.config.model_conf import Configuration
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GEMINI_API_KEY
from src.graph_arc.prompts import decision_support_prompt
from typing import Dict, Any
import json
import re

def decision_support_agent(state: GlobalState) -> Dict[str, Any]:
    """
    Process decision support requests and aggregate information from other agents.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        Decision dictionary with aggregated data and recommendations
    """
    logger = get_logger("decision_support_agent")
    logger.info(f"[DecisionSupportAgent] Processing decision support for query: {state.get('raw_query', 'Unknown')}")
    
    # For a real implementation, this would have access to results from other agents
    # through AgentResultsState, but for this dummy implementation we'll mock the data
    
    # Mock aggregated data
    aggregated_data = {
        "weather": {
            "forecast": "Sunny, 32°C",
            "recommendation": "Good day for crop spraying."
        },
        "soil": {
            "type": "Alluvial",
            "recommended_crops": ["Wheat", "Rice", "Maize"]
        },
        "market": {
            "commodity": "Wheat",
            "current_price": 2000,
            "trend": "Rising"
        }
    }
    
    logger.info(f"[DecisionSupportAgent] Using aggregated data: {aggregated_data}")
    
    # Generate comprehensive advice based on aggregated data
    final_advice = "Based on current weather, soil conditions, and market trends, consider planting wheat and applying fertilizer today. Current market prices for wheat are favorable."
    
    # Provide explanation for the advice
    explanation = """
    1. Weather is suitable for field operations
    2. Soil type supports wheat cultivation
    3. Market prices for wheat are rising
    4. Current temperature supports optimal growth
    """
    
    logger.info(f"[DecisionSupportAgent] Generated final advice: {final_advice}")
    
    # Return properly formatted dictionary
    return {
        "aggregated_data": aggregated_data,
        "final_advice": final_advice,
        "explanation": explanation
    }

def aggregate_decisions(state: GlobalState, config: RunnableConfig) -> GlobalState:
    """
    Aggregates results from all agents and provides comprehensive decision support using LLM.
    
    Args:
        state: The GlobalState with agent_results from the router
        config: LangGraph configuration
        
    Returns:
        Updated GlobalState with LLM-generated decision support information
    """
    logger = get_logger("aggregate_decisions")
    logger.info("[AggregateDecisions] Starting decision aggregation process")
    
    # Extract agent results from the GlobalState
    agent_results = state.get("agent_results", {})
    original_query = state.get("raw_query", "")
    
    logger.info(f"[AggregateDecisions] Processing {len(agent_results)} agent results for query: '{original_query}'")
    logger.info(f"[AggregateDecisions] Available agent results: {list(agent_results.keys())}")
    
    # Debug: Print the actual agent_results content
    logger.info(f"[AggregateDecisions] Full agent_results content: {agent_results}")
    
    # Prepare agent results summary for LLM
    agent_results_summary = {}
    for agent_type, agent_output in agent_results.items():
        if agent_output:  # Only include non-empty results
            agent_results_summary[agent_type] = agent_output
            logger.info(f"[AggregateDecisions] Including {agent_type} results in summary")
    
    # If no agent results available, provide fallback
    if not agent_results_summary:
        logger.warning("[AggregateDecisions] No agent results available, providing fallback decision")
        fallback_decision = {
            "aggregated_data": {},
            "final_advice": "Insufficient data available to provide specific recommendations. Please provide more details about your agricultural needs.",
            "explanation": "No specific agent data was available to analyze."
        }
        updated_state = GlobalState(**state)
        updated_state["decision"] = fallback_decision
        return updated_state
    
    try:
        # Initialize LLM
        configurable = Configuration.from_runnable_config(config)
        llm = ChatGoogleGenerativeAI(
            model=configurable.decision_support_model,
            temperature=0.3,
            max_output_tokens=2000,
            api_key=GEMINI_API_KEY,
        )
        logger.info("[AggregateDecisions] Initialized LLM for decision support")
        
        # Format the prompt with agent results
        formatted_prompt = decision_support_prompt.format(
            original_query=original_query,
            agent_results=json.dumps(agent_results_summary, indent=2)
        )
        
        logger.info("[AggregateDecisions] Invoking LLM for comprehensive decision support")
        response = llm.invoke(formatted_prompt)
        raw_content = response.content
        logger.info(f"[AggregateDecisions] Raw LLM response received: {len(raw_content)} characters")
        
        # Debug: Log the actual raw response to see what we're getting
        logger.info(f"[AggregateDecisions] Raw response content: {raw_content[:500]}...")
        
        # Clean and parse LLM response
        cleaned_content = re.sub(r"```json|```", "", raw_content).strip()
        
        try:
            parsed_decision = json.loads(cleaned_content)
            logger.info("[AggregateDecisions] Successfully parsed LLM decision response")
            
            # Store the complete parsed JSON as the final_advice for comprehensive display
            decision = {
                "aggregated_data": agent_results_summary,
                "final_advice": json.dumps(parsed_decision, indent=2),  # Store full JSON
                "explanation": parsed_decision.get("detailed_explanation", "No explanation provided")
            }
            
            # Log the decision components
            logger.info(f"[AggregateDecisions] Full JSON response stored for comprehensive display")
            logger.info(f"[AggregateDecisions] Confidence from LLM: {parsed_decision.get('confidence_score', 'Not provided')}")
            
            # Update GlobalState with decision
            updated_state = GlobalState(**state)
            updated_state["decision"] = decision
            return updated_state
            
        except json.JSONDecodeError as e:
            logger.error(f"[AggregateDecisions] Failed to parse LLM JSON response: {e}")
            logger.error(f"[AggregateDecisions] Raw response was: {cleaned_content}")
            
            # Fallback to rule-based decision
            return _generate_fallback_decision(agent_results_summary, original_query, logger, state)
            
    except Exception as e:
        logger.error(f"[AggregateDecisions] Error during LLM processing: {e}")
        return _generate_fallback_decision(agent_results_summary, original_query, logger, state)

def _generate_fallback_decision(agent_results: Dict[str, Any], original_query: str, logger, state: GlobalState) -> GlobalState:
    """
    Generate a fallback decision when LLM processing fails.
    
    Args:
        agent_results: Results from various agents
        original_query: Original user query
        logger: Logger instance
        state: Current GlobalState
        
    Returns:
        Updated GlobalState with fallback decision
    """
    logger.info("[AggregateDecisions] Generating fallback decision using rule-based approach")
    
    # Generate a comprehensive advice based on the available data
    advice_components = []
    
    if "weather" in agent_results:
        weather = agent_results["weather"]
        if weather.get("recommendation"):
            advice_components.append(f"Weather: {weather['recommendation']}")
    
    if "soil_crop_recommendation" in agent_results:
        soil = agent_results["soil_crop_recommendation"]
        if soil.get("recommended_crops"):
            crop_list = ", ".join(soil["recommended_crops"][:3])  # Take first 3 crops
            advice_components.append(f"Consider growing: {crop_list}")
    
    if "market_price" in agent_results:
        market = agent_results["market_price"]
        if market.get("selling_suggestion"):
            advice_components.append(f"Market: {market['selling_suggestion']}")
    
    if "crop_health_pest" in agent_results:
        health = agent_results["crop_health_pest"]
        if health.get("treatment"):
            advice_components.append(f"Crop health: {health['treatment']}")
    
    # Join all advice components
    if advice_components:
        final_advice = " ".join(advice_components)
    else:
        final_advice = "Please provide more specific information about your agricultural needs for better recommendations."
    
    # Create explanation from available data
    explanation_points = []
    for agent_type, data in agent_results.items():
        explanation_points.append(f"• Based on {agent_type} analysis")
    
    explanation = "\n".join(explanation_points) if explanation_points else "Limited data available for comprehensive analysis."
    
    # Create decision state
    decision = {
        "aggregated_data": agent_results,
        "final_advice": final_advice,
        "explanation": explanation
    }
    
    logger.info(f"[AggregateDecisions] Fallback decision generated: {final_advice[:100]}...")
    
    # Update GlobalState with fallback decision
    updated_state = GlobalState(**state)
    updated_state["decision"] = decision
    return updated_state
