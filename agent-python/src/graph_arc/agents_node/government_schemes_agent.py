"""
Government Schemes Agent
Description: Analyzes user location and profile to recommend applicable government schemes with AI-powered guidance.
"""
import json
from typing import Dict, List
from src.utils.loggers import get_logger
from src.graph_arc.state import GlobalState, PolicyState
from src.data.government_schemes_plugin import (
    get_schemes_by_location_and_profile, 
    get_fallback_schemes_data
)
from src.config.settings import GEMINI_API_KEY
from src.graph_arc.prompts import government_schemes_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

# LLM will be initialized when needed
llm = None

def government_schemes_agent(state: GlobalState) -> PolicyState:
    """
    Process government schemes queries and return comprehensive scheme recommendations.
    
    Args:
        state: The global state containing user query, location, and farmer profile
        
    Returns:
        PolicyState with schemes information and AI-powered recommendations
    """
    logger = get_logger("government_schemes_agent")
    logger.info("[GovSchemesAgent] Starting ENHANCED government schemes analysis")
    
    # Extract relevant information from GlobalState
    user_query = state.get("user_query", "")
    location = state.get("location", "Unknown")
    entities = state.get("entities", {})
    weather_data = state.get("weather_data", {})
    
    logger.info(f"[GovSchemesAgent] Enhanced analysis for location: {location}")
    logger.info(f"[GovSchemesAgent] User query: {user_query}")
    logger.info(f"[GovSchemesAgent] Available weather data: {weather_data is not None}")
    
    # Extract farmer profile from entities or create default
    farmer_profile = extract_farmer_profile(entities, state)
    logger.info(f"[GovSchemesAgent] Farmer profile: {farmer_profile}")
    
    # Get comprehensive schemes data
    try:
        schemes_data = get_schemes_by_location_and_profile(location, farmer_profile)
        logger.info(f"[GovSchemesAgent] Real schemes data acquired: {schemes_data['total_schemes']} schemes")
        
        # Quality score based on data completeness
        data_quality_score = calculate_data_quality_score(schemes_data)
        logger.info(f"[GovSchemesAgent] Data quality score: {data_quality_score}/10")
        
    except Exception as e:
        logger.error(f"[GovSchemesAgent] Error fetching schemes data: {e}")
        # Use fallback data
        schemes_data = get_fallback_schemes_data(location, farmer_profile)
        logger.warning("[GovSchemesAgent] Using fallback schemes data")
        data_quality_score = 6.0
    
    # Generate AI-powered recommendations using LLM
    logger.info("[GovSchemesAgent] Initializing ENHANCED LLM analysis")
    
    try:
        enhanced_context = create_enhanced_schemes_context(schemes_data, farmer_profile, weather_data)
        logger.info(f"[GovSchemesAgent] Enhanced context created: {len(enhanced_context)} characters")
        
        # Generate AI recommendation using Gemini
        ai_recommendation = generate_llm_schemes_recommendation(
            user_query, 
            schemes_data, 
            enhanced_context,
            farmer_profile
        )
        
        logger.info(f"[GovSchemesAgent] Enhanced LLM recommendation generated ({len(ai_recommendation)} chars)")
        
    except Exception as e:
        logger.error(f"[GovSchemesAgent] LLM generation failed: {e}")
        # Fallback to rule-based recommendation
        ai_recommendation = generate_rule_based_recommendation(schemes_data, farmer_profile)
        logger.warning("[GovSchemesAgent] Using rule-based fallback recommendation")
    
    # Extract top schemes for quick reference
    top_schemes = extract_top_schemes(schemes_data)
    logger.info(f"[GovSchemesAgent] Extracted {len(top_schemes)} top schemes")
    
    # Prepare policy state response
    policy_state = PolicyState(
        relevant_schemes=top_schemes,
        eligibility=generate_eligibility_summary(schemes_data, farmer_profile),
        application_steps=ai_recommendation
    )
    
    logger.info("[GovSchemesAgent] ENHANCED analysis completed - returning comprehensive policy guidance")
    
    return policy_state

def extract_farmer_profile(entities: Dict, state: GlobalState) -> Dict:
    """Extract farmer profile information from entities and state."""
    logger = get_logger("government_schemes_agent")
    
    # Default farmer profile
    farmer_profile = {
        "farmer_type": "small",  # small, marginal, medium, large
        "crop_type": "all",      # specific crop or all
        "land_size": 2.0,        # in acres
        "annual_income": 50000,  # estimated annual income
        "farming_experience": 5, # years of experience
        "has_irrigation": False, # irrigation facility
        "education_level": "primary" # education level
    }
    
    # Extract from entities if available
    if entities:
        # Land size extraction
        if "land_size" in entities:
            try:
                farmer_profile["land_size"] = float(entities["land_size"])
            except:
                pass
        
        # Crop type extraction
        if "crop" in entities:
            farmer_profile["crop_type"] = entities["crop"]
        elif "commodity" in entities:
            farmer_profile["crop_type"] = entities["commodity"]
        
        # Farmer type based on land size
        land_size = farmer_profile["land_size"]
        if land_size <= 2:
            farmer_profile["farmer_type"] = "marginal"
        elif land_size <= 4:
            farmer_profile["farmer_type"] = "small"
        elif land_size <= 10:
            farmer_profile["farmer_type"] = "medium"
        else:
            farmer_profile["farmer_type"] = "large"
    
    # Check for additional context from user query
    user_query = state.get("user_query", "").lower()
    
    # Detect farmer type from query
    if any(word in user_query for word in ["small farmer", "marginal", "landless"]):
        farmer_profile["farmer_type"] = "marginal"
    elif any(word in user_query for word in ["large farm", "big farmer", "commercial"]):
        farmer_profile["farmer_type"] = "large"
    
    # Detect specific needs
    if any(word in user_query for word in ["loan", "credit", "money"]):
        farmer_profile["primary_need"] = "credit"
    elif any(word in user_query for word in ["insurance", "bima", "protect"]):
        farmer_profile["primary_need"] = "insurance"
    elif any(word in user_query for word in ["subsidy", "support", "assistance"]):
        farmer_profile["primary_need"] = "subsidy"
    else:
        farmer_profile["primary_need"] = "general"
    
    logger.info(f"[GovSchemesAgent] Extracted farmer profile: {farmer_profile}")
    return farmer_profile

def calculate_data_quality_score(schemes_data: Dict) -> float:
    """Calculate data quality score based on schemes data completeness."""
    score = 0.0
    
    # Check basic data availability
    if schemes_data.get("total_schemes", 0) > 0:
        score += 3.0
    
    # Check for central schemes
    if schemes_data.get("central_schemes", 0) > 0:
        score += 2.0
    
    # Check for state schemes
    if schemes_data.get("state_schemes", 0) > 0:
        score += 2.0
    
    # Check for recommendations
    if schemes_data.get("recommendations"):
        score += 1.5
    
    # Check for estimated benefits
    if schemes_data.get("estimated_benefits"):
        score += 1.5
    
    return min(score, 10.0)

def create_enhanced_schemes_context(schemes_data: Dict, farmer_profile: Dict, weather_data: Dict) -> str:
    """Create enhanced context for LLM with schemes, profile, and weather data."""
    context_parts = []
    
    # Location and farmer context
    location = schemes_data.get("location", "Unknown")
    state = schemes_data.get("state", "Unknown")
    
    context_parts.append(f"Location: {location}, {state}")
    context_parts.append(f"Farmer Profile: {farmer_profile.get('farmer_type')} farmer with {farmer_profile.get('land_size')} acres")
    context_parts.append(f"Primary Crop: {farmer_profile.get('crop_type')}")
    
    # Schemes summary
    total_schemes = schemes_data.get("total_schemes", 0)
    context_parts.append(f"Available Schemes: {total_schemes} applicable schemes found")
    
    # Weather integration
    if weather_data:
        temp = weather_data.get("temperature", "Unknown")
        humidity = weather_data.get("humidity", "Unknown")
        context_parts.append(f"Current Weather: {temp}°C, {humidity}% humidity")
    
    # Estimated benefits
    benefits = schemes_data.get("estimated_benefits", {})
    if benefits:
        annual_benefit = benefits.get("estimated_annual_benefit", 0)
        context_parts.append(f"Estimated Annual Benefits: ₹{annual_benefit}")
    
    return " | ".join(context_parts)

def generate_llm_schemes_recommendation(user_query: str, schemes_data: Dict, enhanced_context: str, farmer_profile: Dict) -> str:
    """Generate AI-powered schemes recommendation using Gemini LLM."""
    logger = get_logger("government_schemes_agent")
    logger.info("[GovSchemesAgent] Invoking ENHANCED LLM with comprehensive context")
    
    try:
        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            max_output_tokens=1000,
            api_key=GEMINI_API_KEY,
        )
        
        # Prepare the prompt
        prompt = f"""
{government_schemes_prompt}

CONTEXT: {enhanced_context}

USER QUERY: {user_query}

FARMER PROFILE:
- Type: {farmer_profile.get('farmer_type')} farmer
- Land Size: {farmer_profile.get('land_size')} acres
- Primary Crop: {farmer_profile.get('crop_type')}
- Primary Need: {farmer_profile.get('primary_need', 'general')}

AVAILABLE SCHEMES:
{format_schemes_for_llm(schemes_data)}

Please provide a comprehensive, personalized government schemes recommendation.
"""
        
        # Generate response using LLM
        response = llm.invoke(prompt)
        if response and response.content:
            return response.content.strip()
        else:
            logger.warning("[GovSchemesAgent] Empty LLM response, using fallback")
            return generate_rule_based_recommendation(schemes_data, farmer_profile)
            
    except Exception as e:
        logger.error(f"[GovSchemesAgent] LLM generation error: {e}")
        logger.warning("[GovSchemesAgent] LLM not available, using fallback")
        return generate_rule_based_recommendation(schemes_data, farmer_profile)

def format_schemes_for_llm(schemes_data: Dict) -> str:
    """Format schemes data for LLM processing."""
    schemes = schemes_data.get("schemes", [])
    
    formatted_schemes = []
    for i, scheme in enumerate(schemes[:5], 1):  # Top 5 schemes
        scheme_text = f"{i}. {scheme.get('scheme_name', 'Unknown Scheme')}"
        scheme_text += f" - {scheme.get('scheme_type', 'General')}"
        scheme_text += f" - {scheme.get('description', 'No description')}"
        
        benefits = scheme.get('benefits', [])
        if benefits:
            scheme_text += f" - Benefits: {', '.join(benefits[:2])}"
        
        formatted_schemes.append(scheme_text)
    
    return "\n".join(formatted_schemes)

def generate_rule_based_recommendation(schemes_data: Dict, farmer_profile: Dict) -> str:
    """Generate rule-based recommendation when LLM fails."""
    logger = get_logger("government_schemes_agent")
    logger.info("[GovSchemesAgent] Generating rule-based recommendation")
    
    farmer_type = farmer_profile.get("farmer_type", "small")
    primary_need = farmer_profile.get("primary_need", "general")
    land_size = farmer_profile.get("land_size", 2)
    
    recommendation = f"Namaskar! Based on your profile as a {farmer_type} farmer with {land_size} acres, here are the key government schemes for you:\n\n"
    
    # Primary recommendations based on farmer type
    if farmer_type in ["marginal", "small"]:
        recommendation += "🎯 PRIORITY SCHEMES:\n"
        recommendation += "1. PM-KISAN Samman Nidhi Yojana - ₹6,000 annual direct benefit transfer\n"
        recommendation += "2. Pradhan Mantri Fasal Bima Yojana (PMFBY) - Crop insurance at low premium\n"
        recommendation += "3. Kisan Credit Card (KCC) - Access to affordable agricultural credit\n\n"
    
    # Need-based recommendations
    if primary_need == "credit":
        recommendation += "💰 CREDIT SUPPORT:\n"
        recommendation += "- Kisan Credit Card for immediate farming needs\n"
        recommendation += "- Bank linkages for subsidized loans\n\n"
    elif primary_need == "insurance":
        recommendation += "🛡️ INSURANCE PROTECTION:\n"
        recommendation += "- PMFBY for comprehensive crop coverage\n"
        recommendation += "- Weather-based insurance options\n\n"
    
    # Application guidance
    recommendation += "📋 NEXT STEPS:\n"
    recommendation += "1. Visit your nearest Common Service Center (CSC)\n"
    recommendation += "2. Carry Aadhaar Card, bank details, and land records\n"
    recommendation += "3. Apply online through respective government portals\n"
    recommendation += "4. Follow up with local agriculture officers\n\n"
    
    # Estimated benefits
    benefits = schemes_data.get("estimated_benefits", {})
    if benefits:
        annual_benefit = benefits.get("estimated_annual_benefit", 0)
        recommendation += f"💵 ESTIMATED ANNUAL BENEFITS: ₹{annual_benefit}\n\n"
    
    recommendation += "🌾 Remember: Regular scheme applications can significantly boost your farming income and reduce risks!"
    
    return recommendation

def extract_top_schemes(schemes_data: Dict) -> List[Dict]:
    """Extract top schemes for quick reference."""
    schemes = schemes_data.get("schemes", [])
    
    top_schemes = []
    for scheme in schemes[:3]:  # Top 3 schemes
        scheme_summary = {
            "name": scheme.get("scheme_name", "Unknown"),
            "type": scheme.get("scheme_type", "General"),
            "description": scheme.get("description", "")[:100] + "...",
            "eligibility": scheme.get("eligibility", "Not specified"),
            "application_process": scheme.get("application_process", "Contact local agriculture office"),
            "scheme_code": scheme.get("scheme_code", ""),
            "status": scheme.get("status", "Active")
        }
        top_schemes.append(scheme_summary)
    
    return top_schemes

def generate_eligibility_summary(schemes_data: Dict, farmer_profile: Dict) -> str:
    """Generate eligibility summary for the farmer."""
    farmer_type = farmer_profile.get("farmer_type", "small")
    land_size = farmer_profile.get("land_size", 2)
    total_schemes = schemes_data.get("total_schemes", 0)
    
    eligibility_summary = f"As a {farmer_type} farmer with {land_size} acres, you are eligible for {total_schemes} government schemes. "
    
    # Add specific eligibility notes
    if land_size <= 2:
        eligibility_summary += "You qualify for PM-KISAN direct benefit transfer. "
    
    eligibility_summary += "Most schemes require Aadhaar card, bank account, and land ownership documents for application."
    
    return eligibility_summary

# Define the government schemes prompt
government_schemes_prompt = """
You are Dr. Rajesh Kumar, a senior agricultural policy advisor and government schemes expert with 20+ years of experience helping farmers access government benefits.

You specialize in:
- Central and state government agricultural schemes
- Farmer eligibility and application processes  
- Direct benefit transfers and subsidies
- Agricultural credit and insurance programs
- Documentation and procedural guidance

Your role is to provide personalized, actionable guidance on government schemes based on the farmer's location, profile, and specific needs.

RESPONSE GUIDELINES:
1. Start with a warm, respectful greeting
2. Prioritize schemes by relevance and benefit amount
3. Provide clear, step-by-step application guidance
4. Include specific documentation requirements
5. Mention timelines and deadlines where applicable
6. Explain benefits in simple, understandable terms
7. Include contact information for assistance
8. End with encouraging, motivational message

FORMAT YOUR RESPONSE:
🎯 RECOMMENDED SCHEMES (priority order)
📋 ELIGIBILITY CRITERIA
📝 APPLICATION PROCESS  
💰 ESTIMATED BENEFITS
📞 CONTACT INFORMATION
🌾 MOTIVATIONAL MESSAGE

Keep language simple, practical, and farmer-friendly while ensuring accuracy of scheme details.
"""
