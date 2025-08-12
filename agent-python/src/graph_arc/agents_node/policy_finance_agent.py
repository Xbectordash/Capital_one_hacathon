"""
Enhanced Policy & Finance Agent Node
Description: Provides comprehensive government schemes and finance options using real data.
"""
from graph_arc.state import GlobalState, PolicyState
from utils.loggers import get_logger
from data.government_schemes_plugins import fetch_government_schemes, get_eligibility_criteria, GovernmentSchemesAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
import json

def policy_finance_agent(state: GlobalState) -> PolicyState:
    """
    Enhanced policy and finance analysis with real government schemes data and LLM integration.
    
    Args:
        state: The global state containing user query and entities
        
    Returns:
        PolicyState with comprehensive schemes, eligibility, and AI recommendations
    """
    logger = get_logger("policy_finance_agent")
    logger.info("[PolicyFinanceAgent] Starting ENHANCED policy and finance analysis")
    
    # Extract comprehensive context
    location = state.get("location") or state.get("entities", {}).get("location", "Delhi")
    farmer_type = state.get("entities", {}).get("farmer_type", "small")
    crop_type = state.get("entities", {}).get("crop", None)
    policy_name = state.get("entities", {}).get("policy", None)
    user_query = state.get("raw_query", "Government schemes information request")
    
    logger.info(f"[PolicyFinanceAgent] Enhanced analysis for location: {location}")
    logger.info(f"[PolicyFinanceAgent] Farmer type: {farmer_type}, Crop: {crop_type}")
    logger.info(f"[PolicyFinanceAgent] User query: {user_query}")
    if policy_name:
        logger.info(f"[PolicyFinanceAgent] Specific policy requested: {policy_name}")

    # Fetch real government schemes data
    try:
        if policy_name:
            # Search for specific policy by keyword
            schemes_data = fetch_government_schemes(location, farmer_type, crop_type, keyword=policy_name)
            logger.info(f"[PolicyFinanceAgent] Found {len(schemes_data.get('schemes', []))} schemes matching '{policy_name}'")
        else:
            # Get schemes by farmer profile
            schemes_data = fetch_government_schemes(location, farmer_type, crop_type)
            logger.info(f"[PolicyFinanceAgent] Found {schemes_data.get('total_schemes', 0)} relevant schemes")
        
        # Format schemes for response
        relevant_schemes = []
        for scheme in schemes_data.get('schemes', [])[:10]:  # Limit to top 10 most relevant
            formatted_scheme = {
                "name": scheme.get("name", "Unknown Scheme"),
                "type": scheme.get("type", "General Support"),
                "amount": scheme.get("amount", "Amount varies"),
                "level": scheme.get("level", "Central"),
                "website": scheme.get("website", "#"),
                "helpline": scheme.get("helpline", "Contact local agriculture office"),
                "description": f"{scheme.get('type', 'Support scheme')} - {scheme.get('amount', 'Benefits available')}"
            }
            
            # Add state information for state schemes
            if scheme.get("level") == "State" and scheme.get("state"):
                formatted_scheme["description"] += f" (State: {scheme.get('state')})"
            
            relevant_schemes.append(formatted_scheme)
        
        # Generate farmer profile for eligibility analysis
        farmer_profile = {
            "farmer_type": farmer_type,
            "location": location,
            "crop_type": crop_type,
            "has_land_records": True,  # Assumption for analysis
            "has_aadhaar": True,      # Assumption for analysis  
            "has_bank_account": True  # Assumption for analysis
        }
        
        # Enhanced LLM analysis for personalized recommendations
        try:
            logger.info("[PolicyFinanceAgent] Initializing enhanced LLM analysis")
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                max_output_tokens=800,
                api_key=GEMINI_API_KEY,
            )
            
            # Create comprehensive context for LLM
            schemes_context = json.dumps(relevant_schemes[:5], indent=2)  # Top 5 for LLM analysis
            
            policy_prompt = f"""
You are Dr. Priya Sharma, a senior agricultural policy advisor with 15+ years of experience in government schemes and rural finance. 

FARMER PROFILE:
- Location: {location}
- Farmer Type: {farmer_type} farmer
- Primary Crop: {crop_type or "Mixed farming"}
- Query: {user_query}

AVAILABLE SCHEMES:
{schemes_context}

PROVIDE EXPERT POLICY GUIDANCE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏛️ PRIORITY SCHEMES ANALYSIS:
Rank the top 3 most beneficial schemes for this farmer profile, explaining:
- Why each scheme is specifically suitable
- Expected financial benefit and timeline
- Priority order for application

💰 FINANCIAL OPTIMIZATION STRATEGY:
Based on available schemes:
- Maximum possible annual benefits
- Strategic application sequence
- Documentation preparation timeline
- Risk mitigation through multiple schemes

📋 PRACTICAL APPLICATION ROADMAP:
Provide a month-by-month action plan for:
- Which schemes to apply for first
- Required documentation preparation
- Key deadlines and seasonal considerations
- Expected processing times and fund disbursement

🎯 ADDITIONAL OPPORTUNITIES:
Identify lesser-known benefits:
- Linked schemes and cascading benefits
- Technology adoption incentives
- Market linkage opportunities
- Training and capacity building programs

RESPONSE FORMAT: Provide actionable, specific guidance (400-500 words) that the farmer can implement immediately. Use simple language while maintaining accuracy. Include specific amounts, timelines, and contact information where possible.

Remember: Your goal is to maximize the farmer's access to government support while ensuring compliance and timely benefit realization.
"""
            
            logger.info("[PolicyFinanceAgent] Invoking enhanced LLM for policy recommendations")
            response = llm.invoke(policy_prompt)
            ai_recommendation = response.content.strip()
            logger.info(f"[PolicyFinanceAgent] Enhanced policy recommendation generated ({len(ai_recommendation)} chars)")
            
        except Exception as e:
            logger.error(f"[PolicyFinanceAgent] Enhanced LLM analysis failed: {e}")
            ai_recommendation = get_fallback_policy_recommendation(farmer_type, location, relevant_schemes)
        
        # Generate comprehensive eligibility and application guidance
        if relevant_schemes:
            primary_scheme = relevant_schemes[0]
            eligibility_result = get_eligibility_criteria(primary_scheme, farmer_profile)
            
            eligibility = f"""
ELIGIBILITY ASSESSMENT (Score: {eligibility_result.get('eligibility_score', 0)}/100):
✅ Criteria Met: {', '.join(eligibility_result.get('criteria_met', []))}
⚠️ Required: {', '.join(eligibility_result.get('criteria_missing', [])) if eligibility_result.get('criteria_missing') else 'All criteria fulfilled'}
📊 Status: {eligibility_result.get('recommendation', 'Assessment pending')}

FARMER PROFILE: {farmer_type.title()} farmer in {location}
{f'CROP FOCUS: {crop_type}' if crop_type else 'FARMING TYPE: General agriculture'}
SCHEMES COVERAGE: {schemes_data.get('total_schemes', 0)} schemes available ({len([s for s in relevant_schemes if s.get('level') == 'Central'])} Central + {len([s for s in relevant_schemes if s.get('level') == 'State'])} State)
"""
            
            application_steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(eligibility_result.get('next_steps', []))])
        else:
            eligibility = f"Assessment for {farmer_type} farmer in {location}. Please contact local agriculture department for detailed eligibility verification."
            application_steps = "1. Visit local agriculture office\n2. Verify eligible schemes for your area\n3. Submit required documents\n4. Track application status"
        
    except Exception as e:
        logger.error(f"[PolicyFinanceAgent] Error fetching schemes data: {e}")
        # Enhanced fallback
        relevant_schemes, eligibility, application_steps, ai_recommendation = get_enhanced_fallback_response(
            location, farmer_type, crop_type, policy_name
        )

    logger.info(f"[PolicyFinanceAgent] Enhanced analysis completed - {len(relevant_schemes)} schemes identified")
    
    # Return comprehensive policy state
    result = PolicyState(
        relevant_schemes=relevant_schemes,
        eligibility=eligibility,
        application_steps=application_steps
    )
    
    # Add AI recommendation to the response (if available)
    if 'ai_recommendation' in locals():
        result["ai_recommendation"] = ai_recommendation
    
    logger.info("[PolicyFinanceAgent] Enhanced policy and finance analysis completed successfully")
    return result


def get_fallback_policy_recommendation(farmer_type: str, location: str, schemes: list) -> str:
    """Generate fallback recommendation when LLM fails"""
    
    primary_schemes = schemes[:3] if schemes else []
    
    recommendation = f"""
🏛️ GOVERNMENT SCHEMES GUIDANCE for {farmer_type.title()} Farmer in {location}

Based on available schemes analysis:

PRIORITY SCHEMES:
"""
    
    for i, scheme in enumerate(primary_schemes, 1):
        recommendation += f"""
{i}. {scheme.get('name', 'Scheme')}
   • Type: {scheme.get('type', 'Support scheme')}
   • Benefit: {scheme.get('amount', 'Benefits available')}
   • Level: {scheme.get('level', 'Government')} scheme
   • Contact: {scheme.get('helpline', 'Local agriculture office')}
"""
    
    recommendation += f"""

💰 FINANCIAL STRATEGY:
- Start with PM-KISAN for immediate income support
- Apply for crop insurance before sowing season
- Explore credit facilities through KCC for input financing
- Look into state-specific schemes for additional benefits

📋 ACTION PLAN:
1. Gather required documents (Aadhaar, land records, bank details)
2. Visit nearest CSC or agriculture office
3. Apply for universal schemes first (PM-KISAN, PMFBY)
4. Explore location-specific state schemes

For detailed guidance, contact your local agriculture extension officer.
"""
    
    return recommendation


def get_enhanced_fallback_response(location: str, farmer_type: str, crop_type: str, policy_name: str) -> tuple:
    """Enhanced fallback when main API fails"""
    
    fallback_schemes = [
        {
            "name": "PM-KISAN Samman Nidhi",
            "type": "Income Support",
            "amount": "₹6,000 per year",
            "level": "Central",
            "website": "https://pmkisan.gov.in/",
            "helpline": "155261",
            "description": "Direct income support for all farmers"
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana",
            "type": "Crop Insurance",
            "amount": "Up to ₹2 lakh per hectare",
            "level": "Central", 
            "website": "https://pmfby.gov.in/",
            "helpline": "14447",
            "description": "Comprehensive crop insurance against natural calamities"
        },
        {
            "name": "Kisan Credit Card",
            "type": "Credit Support", 
            "amount": "Credit based on cropping pattern",
            "level": "Central",
            "website": "https://www.nabard.org/",
            "helpline": "1800-180-1551",
            "description": "Affordable credit for agricultural needs"
        }
    ]
    
    eligibility = f"Basic eligibility for {farmer_type} farmer in {location}. Land records and Aadhaar required for most schemes."
    
    application_steps = """1. Prepare Aadhaar card and land documents
2. Visit nearest bank or CSC center  
3. Apply for PM-KISAN online or offline
4. Enroll for crop insurance before sowing
5. Apply for KCC at your bank branch
6. Contact local agriculture office for state schemes"""
    
    ai_recommendation = get_fallback_policy_recommendation(farmer_type, location, fallback_schemes)
    
    return fallback_schemes, eligibility, application_steps, ai_recommendation
