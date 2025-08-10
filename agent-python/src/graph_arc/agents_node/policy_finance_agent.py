"""
Policy & Finance Agent Node
Description: Provides information on government policies and finance options.
"""
from graph_arc.state import GlobalState, PolicyState
from utils.loggers import get_logger

def policy_finance_agent(state: GlobalState) -> PolicyState:
    """
    Process policy and finance-related queries.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        PolicyState with relevant schemes and eligibility information
    """
    logger = get_logger("policy_finance_agent")
    logger.info("[PolicyFinanceAgent] Starting policy and finance analysis")
    
    # Extract relevant entities
    farmer_type = state.get("entities", {}).get("farmer_type", "small")
    crop_type = state.get("entities", {}).get("crop", None)
    policy_name = state.get("entities", {}).get("policy", None)
    
    logger.info(f"[PolicyFinanceAgent] Farmer type: {farmer_type}")
    logger.info(f"[PolicyFinanceAgent] Crop type: {crop_type}")
    logger.info(f"[PolicyFinanceAgent] Specific policy requested: {policy_name}")
    
    # Mock policy data
    relevant_schemes = []
    
    # Add general schemes
    relevant_schemes.append({
        "name": "PM Kisan Samman Nidhi",
        "link": "https://pmkisan.gov.in/",
        "description": "Income support of Rs. 6000 per year for all farmers"
    })
    logger.info("[PolicyFinanceAgent] Added PM Kisan Samman Nidhi scheme")
    
    # Add farmer type specific schemes
    if farmer_type.lower() == "small":
        relevant_schemes.append({
            "name": "Small Farmer Agribusiness Consortium",
            "link": "http://sfacindia.com/",
            "description": "Credit linked subsidy for agribusiness projects"
        })
        logger.info("[PolicyFinanceAgent] Added Small Farmer Agribusiness Consortium scheme")
    
    # Add crop specific schemes
    if crop_type:
        relevant_schemes.append({
            "name": f"{crop_type.capitalize()} Insurance Scheme",
            "link": "#",
            "description": f"Specific insurance for {crop_type} crops"
        })
        logger.info(f"[PolicyFinanceAgent] Added crop-specific insurance scheme for {crop_type}")
    
    # Add specific policy details if requested
    if policy_name:
        original_count = len(relevant_schemes)
        relevant_schemes = [scheme for scheme in relevant_schemes if policy_name.lower() in scheme["name"].lower()]
        if not relevant_schemes:
            relevant_schemes.append({
                "name": policy_name,
                "link": "#",
                "description": "Please contact local agriculture office for details on this scheme."
            })
            logger.info(f"[PolicyFinanceAgent] No matching schemes found for '{policy_name}', added placeholder")
        else:
            logger.info(f"[PolicyFinanceAgent] Filtered to {len(relevant_schemes)} schemes matching '{policy_name}'")
    
    # Generate eligibility and application information
    eligibility = f"Farmers with land records, {farmer_type} category farmers prioritized."
    application_steps = "1. Visit local agriculture office\n2. Submit land record documents\n3. Complete application form\n4. Register on scheme portal"
    
    logger.info(f"[PolicyFinanceAgent] Generated eligibility criteria: {eligibility}")
    logger.info(f"[PolicyFinanceAgent] Total schemes identified: {len(relevant_schemes)}")
    
    # Return properly typed state
    result = PolicyState(
        relevant_schemes=relevant_schemes,
        eligibility=eligibility,
        application_steps=application_steps
    )
    
    logger.info("[PolicyFinanceAgent] Policy and finance analysis completed successfully")
    return result
