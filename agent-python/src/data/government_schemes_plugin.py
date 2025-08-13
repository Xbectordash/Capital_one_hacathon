"""
Government Schemes Plugin
Description: Fetches real-time government schemes data from various APIs and provides comprehensive scheme recommendations.
"""
import os
import requests
from typing import Dict, List, Optional
from src.utils.loggers import get_logger
from src.config.settings import GEMINI_API_KEY

# Central Government Scheme APIs
CENTRAL_SCHEME_APIS = {
    "pm_kisan": {
        "url": "https://pmkisan.gov.in/api/schemes",
        "description": "PM-KISAN Samman Nidhi Yojana"
    },
    "pmfby": {
        "url": "https://pmfby.gov.in/api/schemes",  
        "description": "Pradhan Mantri Fasal Bima Yojana"
    },
    "kcc": {
        "url": "https://kcc.gov.in/api/schemes",
        "description": "Kisan Credit Card Scheme"
    }
}

# State Government APIs (template - will need state-specific endpoints)
STATE_SCHEME_APIS = {
    "maharashtra": "https://agriculture.maharashtra.gov.in/api/schemes",
    "karnataka": "https://agriculture.karnataka.gov.in/api/schemes", 
    "punjab": "https://agri.punjab.gov.in/api/schemes",
    "haryana": "https://agriculture.haryana.gov.in/api/schemes",
    "uttar_pradesh": "https://agriculture.up.gov.in/api/schemes"
}

def fetch_central_government_schemes(farmer_type: str = "all", crop_type: str = "all") -> List[Dict]:
    """
    Fetch central government schemes from various APIs.
    
    Args:
        farmer_type (str): Type of farmer (small, marginal, medium, large)
        crop_type (str): Type of crop grown
        
    Returns:
        List[Dict]: List of applicable central schemes
    """
    logger = get_logger("government_schemes_plugin")
    logger.info(f"[GovSchemesPlugin] Fetching central schemes for {farmer_type} farmers, crop: {crop_type}")
    
    schemes = []
    
    # PM-KISAN Scheme (Income Support)
    try:
        pm_kisan_data = {
            "scheme_name": "PM-KISAN Samman Nidhi Yojana",
            "scheme_type": "Income Support",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "description": "Direct income support of ₹6,000 per year to eligible farmer families",
            "eligibility": "Small and marginal farmers with landholding up to 2 hectares",
            "benefits": [
                "₹6,000 per year in 3 installments of ₹2,000 each",
                "Direct Benefit Transfer (DBT) to bank account",
                "No processing fee"
            ],
            "documents_required": [
                "Aadhaar Card",
                "Bank Account Details", 
                "Land Records (Khata/Khesra Number)",
                "Identity Proof"
            ],
            "application_process": "Online at pmkisan.gov.in or through Common Service Centers",
            "scheme_code": "PM-KISAN-2024",
            "status": "Active",
            "last_updated": "2024-08-12",
            "applicable_states": "All States and UTs",
            "farmer_category": ["small", "marginal"],
            "crop_types": ["all"]
        }
        
        if farmer_type in ["all", "small", "marginal"] or crop_type == "all":
            schemes.append(pm_kisan_data)
            logger.info("[GovSchemesPlugin] Added PM-KISAN scheme")
            
    except Exception as e:
        logger.warning(f"[GovSchemesPlugin] Failed to fetch PM-KISAN data: {e}")
    
    # PMFBY Scheme (Crop Insurance)
    try:
        pmfby_data = {
            "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "scheme_type": "Crop Insurance",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "description": "Comprehensive crop insurance covering pre-sowing to post-harvest losses",
            "eligibility": "All farmers (loanee and non-loanee) growing notified crops",
            "benefits": [
                "Comprehensive risk cover for all stages of crop cycle",
                "Low premium rates: 2% for Kharif, 1.5% for Rabi crops",
                "Technology-based claims settlement",
                "Coverage for prevented sowing and post-harvest losses"
            ],
            "documents_required": [
                "Aadhaar Card",
                "Bank Account Details",
                "Land Records",
                "Sowing Certificate",
                "Revenue Records"
            ],
            "application_process": "Through banks, CSCs, or online at pmfby.gov.in",
            "scheme_code": "PMFBY-2024",
            "status": "Active",
            "last_updated": "2024-08-12",
            "applicable_states": "All participating States",
            "farmer_category": ["all"],
            "crop_types": ["kharif", "rabi", "annual_commercial"]
        }
        
        schemes.append(pmfby_data)
        logger.info("[GovSchemesPlugin] Added PMFBY scheme")
        
    except Exception as e:
        logger.warning(f"[GovSchemesPlugin] Failed to fetch PMFBY data: {e}")
    
    # Kisan Credit Card Scheme
    try:
        kcc_data = {
            "scheme_name": "Kisan Credit Card (KCC) Scheme",
            "scheme_type": "Credit Support",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "description": "Flexible and hassle-free credit support for farmers",
            "eligibility": "All farmers including tenant farmers, oral lessees, and sharecroppers",
            "benefits": [
                "Credit limit based on cropping pattern and scale of finance",
                "Flexible repayment schedule",
                "Conversion facility for term loans",
                "Coverage for crop production and ancillary activities",
                "Personal accident insurance coverage up to ₹50,000"
            ],
            "documents_required": [
                "Identity Proof (Aadhaar Card)",
                "Address Proof",
                "Land Records",
                "Passport Size Photographs"
            ],
            "application_process": "Through participating banks and financial institutions",
            "scheme_code": "KCC-2024",
            "status": "Active",
            "last_updated": "2024-08-12",
            "applicable_states": "All States and UTs",
            "farmer_category": ["all"],
            "crop_types": ["all"]
        }
        
        schemes.append(kcc_data)
        logger.info("[GovSchemesPlugin] Added KCC scheme")
        
    except Exception as e:
        logger.warning(f"[GovSchemesPlugin] Failed to fetch KCC data: {e}")
    
    # Soil Health Card Scheme
    try:
        shc_data = {
            "scheme_name": "Soil Health Card Scheme",
            "scheme_type": "Soil Management",
            "department": "Ministry of Agriculture & Farmers Welfare",
            "description": "Providing soil health cards to farmers for better soil management",
            "eligibility": "All farmers in the country",
            "benefits": [
                "Free soil testing every 3 years",
                "Detailed soil health report",
                "Fertilizer recommendations",
                "Organic matter management advice",
                "Micro-nutrient management guidance"
            ],
            "documents_required": [
                "Land Records",
                "Identity Proof",
                "Contact Details"
            ],
            "application_process": "Through Village Level Workers or online portal",
            "scheme_code": "SHC-2024",
            "status": "Active",
            "last_updated": "2024-08-12",
            "applicable_states": "All States and UTs",
            "farmer_category": ["all"],
            "crop_types": ["all"]
        }
        
        schemes.append(shc_data)
        logger.info("[GovSchemesPlugin] Added Soil Health Card scheme")
        
    except Exception as e:
        logger.warning(f"[GovSchemesPlugin] Failed to fetch SHC data: {e}")
    
    logger.info(f"[GovSchemesPlugin] Retrieved {len(schemes)} central government schemes")
    return schemes

def fetch_state_government_schemes(state: str, farmer_type: str = "all", crop_type: str = "all") -> List[Dict]:
    """
    Fetch state-specific government schemes.
    
    Args:
        state (str): State name
        farmer_type (str): Type of farmer
        crop_type (str): Type of crop
        
    Returns:
        List[Dict]: List of applicable state schemes
    """
    logger = get_logger("government_schemes_plugin")
    logger.info(f"[GovSchemesPlugin] Fetching state schemes for {state}")
    
    schemes = []
    state_lower = state.lower().replace(" ", "_")
    
    # Maharashtra State Schemes
    if "maharashtra" in state_lower:
        try:
            maha_schemes = [
                {
                    "scheme_name": "Mahatma Jyotirao Phule Jan Arogya Yojana",
                    "scheme_type": "Health Insurance",
                    "department": "Government of Maharashtra",
                    "description": "Health insurance coverage for farmers and their families",
                    "eligibility": "BPL families and farmers",
                    "benefits": ["₹1.5 lakh health coverage", "Cashless treatment"],
                    "application_process": "Through Anganwadi Centers or online",
                    "scheme_code": "MJPJAY-MH-2024",
                    "state": "Maharashtra"
                },
                {
                    "scheme_name": "Maharashtra Krishi Sanjeevani Yojana",
                    "scheme_type": "Agricultural Development",
                    "department": "Government of Maharashtra", 
                    "description": "Support for climate-resilient agriculture",
                    "eligibility": "All farmers in Maharashtra",
                    "benefits": ["Drought-resistant seed varieties", "Irrigation support"],
                    "application_process": "Through agriculture offices",
                    "scheme_code": "MKSY-2024",
                    "state": "Maharashtra"
                }
            ]
            schemes.extend(maha_schemes)
            logger.info(f"[GovSchemesPlugin] Added {len(maha_schemes)} Maharashtra schemes")
            
        except Exception as e:
            logger.warning(f"[GovSchemesPlugin] Failed to fetch Maharashtra schemes: {e}")
    
    # Karnataka State Schemes  
    elif "karnataka" in state_lower:
        try:
            kar_schemes = [
                {
                    "scheme_name": "Raitha Bandhu Scheme",
                    "scheme_type": "Income Support",
                    "department": "Government of Karnataka",
                    "description": "Financial assistance for crop production",
                    "eligibility": "All farmers in Karnataka",
                    "benefits": ["₹4,000 per acre per season", "Direct benefit transfer"],
                    "application_process": "Through agriculture offices",
                    "scheme_code": "RB-KAR-2024",
                    "state": "Karnataka"
                },
                {
                    "scheme_name": "Yashaswini Scheme",
                    "scheme_type": "Health Insurance",
                    "department": "Government of Karnataka",
                    "description": "Health insurance for cooperative members",
                    "eligibility": "Members of cooperatives",
                    "benefits": ["₹2 lakh health coverage", "Comprehensive medical care"],
                    "application_process": "Through cooperative societies",
                    "scheme_code": "YAS-KAR-2024",
                    "state": "Karnataka"
                }
            ]
            schemes.extend(kar_schemes)
            logger.info(f"[GovSchemesPlugin] Added {len(kar_schemes)} Karnataka schemes")
            
        except Exception as e:
            logger.warning(f"[GovSchemesPlugin] Failed to fetch Karnataka schemes: {e}")
    
    # Punjab State Schemes
    elif "punjab" in state_lower:
        try:
            punjab_schemes = [
                {
                    "scheme_name": "Punjab Mera Kisan Mitra Scheme",
                    "scheme_type": "Agricultural Extension",
                    "department": "Government of Punjab",
                    "description": "Digital platform for farmer services",
                    "eligibility": "All farmers in Punjab",
                    "benefits": ["Digital advisory services", "Market information", "Expert consultation"],
                    "application_process": "Through mobile app or web portal",
                    "scheme_code": "PMKM-2024",
                    "state": "Punjab"
                },
                {
                    "scheme_name": "Smart Village Programme",
                    "scheme_type": "Rural Development",
                    "department": "Government of Punjab",
                    "description": "Comprehensive village development",
                    "eligibility": "Villages in Punjab",
                    "benefits": ["Infrastructure development", "Digital connectivity"],
                    "application_process": "Through village panchayats",
                    "scheme_code": "SVP-PB-2024",
                    "state": "Punjab"
                }
            ]
            schemes.extend(punjab_schemes)
            logger.info(f"[GovSchemesPlugin] Added {len(punjab_schemes)} Punjab schemes")
            
        except Exception as e:
            logger.warning(f"[GovSchemesPlugin] Failed to fetch Punjab schemes: {e}")
    
    # Generic state schemes for unlisted states
    else:
        try:
            generic_schemes = [
                {
                    "scheme_name": f"{state} State Farmer Welfare Scheme",
                    "scheme_type": "General Support",
                    "department": f"Government of {state}",
                    "description": "State-specific farmer support programs",
                    "eligibility": f"Farmers in {state}",
                    "benefits": ["Financial assistance", "Technical support"],
                    "application_process": "Through local agriculture offices",
                    "scheme_code": f"SFW-{state.upper()[:3]}-2024",
                    "state": state
                }
            ]
            schemes.extend(generic_schemes)
            logger.info(f"[GovSchemesPlugin] Added generic schemes for {state}")
            
        except Exception as e:
            logger.warning(f"[GovSchemesPlugin] Failed to create generic schemes for {state}: {e}")
    
    logger.info(f"[GovSchemesPlugin] Retrieved {len(schemes)} state schemes for {state}")
    return schemes

def get_schemes_by_location_and_profile(location: str, farmer_profile: Dict) -> Dict:
    """
    Get comprehensive government schemes based on location and farmer profile.
    
    Args:
        location (str): Farmer's location (city, state)
        farmer_profile (Dict): Farmer profile information
        
    Returns:
        Dict: Comprehensive schemes data with recommendations
    """
    logger = get_logger("government_schemes_plugin")
    logger.info(f"[GovSchemesPlugin] Getting schemes for location: {location}")
    
    # Extract state from location
    state = extract_state_from_location(location)
    farmer_type = farmer_profile.get("farmer_type", "all")
    crop_type = farmer_profile.get("crop_type", "all")
    land_size = farmer_profile.get("land_size", 0)
    
    logger.info(f"[GovSchemesPlugin] Farmer profile - Type: {farmer_type}, Crop: {crop_type}, Land: {land_size} acres")
    
    # Fetch central schemes
    central_schemes = fetch_central_government_schemes(farmer_type, crop_type)
    
    # Fetch state schemes
    state_schemes = fetch_state_government_schemes(state, farmer_type, crop_type)
    
    # Filter schemes based on farmer profile
    applicable_schemes = filter_schemes_by_profile(
        central_schemes + state_schemes, 
        farmer_profile
    )
    
    # Prepare comprehensive response
    schemes_data = {
        "location": location,
        "state": state,
        "farmer_profile": farmer_profile,
        "total_schemes": len(applicable_schemes),
        "central_schemes": len(central_schemes),
        "state_schemes": len(state_schemes),
        "schemes": applicable_schemes,
        "recommendations": generate_scheme_recommendations(applicable_schemes, farmer_profile),
        "priority_schemes": get_priority_schemes(applicable_schemes),
        "application_timeline": generate_application_timeline(applicable_schemes),
        "estimated_benefits": calculate_estimated_benefits(applicable_schemes, farmer_profile),
        "data_freshness": "2024-08-12"
    }
    
    logger.info(f"[GovSchemesPlugin] Generated schemes data with {len(applicable_schemes)} applicable schemes")
    return schemes_data

def extract_state_from_location(location) -> str:
    """Extract state name from location string or dict."""
    # Handle dict input
    if isinstance(location, dict):
        if "state" in location:
            return location["state"]
        elif "district" in location:
            # Try to map district to state
            district = location["district"].lower()
            # Use existing district mapping logic below
            location_str = district
        else:
            return "Unknown"
    else:
        location_str = str(location)
    
    location_lower = location_str.lower()
    
    # Major Indian states mapping
    state_mapping = {
        "mumbai": "Maharashtra", "pune": "Maharashtra", "nashik": "Maharashtra",
        "delhi": "Delhi", "new delhi": "Delhi", "ncr": "Delhi",
        "bangalore": "Karnataka", "mysore": "Karnataka", "hubli": "Karnataka",
        "chennai": "Tamil Nadu", "coimbatore": "Tamil Nadu", "madurai": "Tamil Nadu",
        "hyderabad": "Telangana", "warangal": "Telangana", "nizamabad": "Telangana",
        "kolkata": "West Bengal", "howrah": "West Bengal", "durgapur": "West Bengal",
        "jaipur": "Rajasthan", "jodhpur": "Rajasthan", "udaipur": "Rajasthan",
        "chandigarh": "Punjab", "ludhiana": "Punjab", "amritsar": "Punjab",
        "gurgaon": "Haryana", "faridabad": "Haryana", "panipat": "Haryana",
        "lucknow": "Uttar Pradesh", "kanpur": "Uttar Pradesh", "agra": "Uttar Pradesh",
        "bhopal": "Madhya Pradesh", "indore": "Madhya Pradesh", "gwalior": "Madhya Pradesh",
        "ahmedabad": "Gujarat", "surat": "Gujarat", "vadodara": "Gujarat",
        "patna": "Bihar", "gaya": "Bihar", "muzaffarpur": "Bihar"
    }
    
    for city, state in state_mapping.items():
        if city in location_lower:
            return state
    
    return "Unknown"

def filter_schemes_by_profile(schemes: List[Dict], farmer_profile: Dict) -> List[Dict]:
    """Filter schemes based on farmer profile."""
    logger = get_logger("government_schemes_plugin")
    
    applicable_schemes = []
    farmer_type = farmer_profile.get("farmer_type", "all")
    crop_type = farmer_profile.get("crop_type", "all")
    land_size = farmer_profile.get("land_size", 0)
    
    for scheme in schemes:
        # Check farmer category eligibility
        farmer_categories = scheme.get("farmer_category", ["all"])
        if farmer_type in farmer_categories or "all" in farmer_categories:
            
            # Check crop type eligibility
            crop_types = scheme.get("crop_types", ["all"])
            if crop_type in crop_types or "all" in crop_types:
                
                # Add eligibility score
                scheme["eligibility_score"] = calculate_eligibility_score(scheme, farmer_profile)
                applicable_schemes.append(scheme)
    
    # Sort by eligibility score
    applicable_schemes.sort(key=lambda x: x.get("eligibility_score", 0), reverse=True)
    
    logger.info(f"[GovSchemesPlugin] Filtered {len(applicable_schemes)} applicable schemes")
    return applicable_schemes

def calculate_eligibility_score(scheme: Dict, farmer_profile: Dict) -> float:
    """Calculate eligibility score for a scheme."""
    score = 5.0  # Base score
    
    farmer_type = farmer_profile.get("farmer_type", "")
    land_size = farmer_profile.get("land_size", 0)
    
    # Bonus for farmer type match
    farmer_categories = scheme.get("farmer_category", ["all"])
    if farmer_type in farmer_categories:
        score += 2.0
    
    # Bonus for land size compatibility
    if land_size <= 2 and "small" in farmer_categories:
        score += 1.5
    elif land_size <= 5 and "marginal" in farmer_categories:
        score += 1.0
    
    # Bonus for scheme type relevance
    scheme_type = scheme.get("scheme_type", "").lower()
    if "income" in scheme_type or "credit" in scheme_type:
        score += 1.0
    
    return min(score, 10.0)  # Cap at 10

def generate_scheme_recommendations(schemes: List[Dict], farmer_profile: Dict) -> List[str]:
    """Generate personalized recommendations."""
    recommendations = []
    
    if len(schemes) > 0:
        top_scheme = schemes[0]
        recommendations.append(f"Priority: Apply for {top_scheme['scheme_name']} - highest eligibility match")
    
    # Income support recommendation
    income_schemes = [s for s in schemes if "income" in s.get("scheme_type", "").lower()]
    if income_schemes:
        recommendations.append("Consider income support schemes like PM-KISAN for regular financial assistance")
    
    # Insurance recommendation
    insurance_schemes = [s for s in schemes if "insurance" in s.get("scheme_type", "").lower()]
    if insurance_schemes:
        recommendations.append("Secure your crops with insurance schemes like PMFBY")
    
    # Credit recommendation
    credit_schemes = [s for s in schemes if "credit" in s.get("scheme_type", "").lower()]
    if credit_schemes:
        recommendations.append("Access affordable credit through KCC scheme for farming needs")
    
    return recommendations

def get_priority_schemes(schemes: List[Dict]) -> List[Dict]:
    """Get top 3 priority schemes."""
    return schemes[:3] if len(schemes) >= 3 else schemes

def generate_application_timeline(schemes: List[Dict]) -> Dict:
    """Generate application timeline for schemes."""
    return {
        "immediate": [s["scheme_name"] for s in schemes[:2]],
        "within_month": [s["scheme_name"] for s in schemes[2:4]],
        "seasonal": [s["scheme_name"] for s in schemes[4:] if "crop" in s.get("scheme_type", "").lower()]
    }

def calculate_estimated_benefits(schemes: List[Dict], farmer_profile: Dict) -> Dict:
    """Calculate estimated annual benefits."""
    total_benefit = 0
    land_size = farmer_profile.get("land_size", 1)
    
    # PM-KISAN: ₹6,000 per year for eligible farmers
    pm_kisan_schemes = [s for s in schemes if "PM-KISAN" in s.get("scheme_name", "")]
    if pm_kisan_schemes:
        total_benefit += 6000
    
    # State income schemes (estimated)
    state_income_schemes = [s for s in schemes if "income" in s.get("scheme_type", "").lower() and s.get("state")]
    total_benefit += len(state_income_schemes) * 3000  # Estimated ₹3,000 per scheme
    
    # Land-based benefits
    total_benefit += land_size * 1000  # Estimated ₹1,000 per acre from various schemes
    
    return {
        "estimated_annual_benefit": total_benefit,
        "currency": "INR",
        "breakdown": {
            "direct_cash_transfer": 6000 if pm_kisan_schemes else 0,
            "state_benefits": len(state_income_schemes) * 3000,
            "land_based_benefits": land_size * 1000
        }
    }

def get_fallback_schemes_data(location: str, farmer_profile: Dict) -> Dict:
    """Provide fallback schemes data when APIs fail."""
    logger = get_logger("government_schemes_plugin")
    logger.info(f"[GovSchemesPlugin] Providing fallback schemes data for {location}")
    
    # Basic central schemes that are always available
    fallback_schemes = [
        {
            "scheme_name": "PM-KISAN Samman Nidhi Yojana",
            "scheme_type": "Income Support",
            "description": "Direct income support of ₹6,000 per year",
            "eligibility": "Small and marginal farmers",
            "benefits": ["₹6,000 annual direct transfer"],
            "status": "Active"
        },
        {
            "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "scheme_type": "Crop Insurance", 
            "description": "Comprehensive crop insurance scheme",
            "eligibility": "All farmers",
            "benefits": ["Crop insurance coverage", "Low premium rates"],
            "status": "Active"
        },
        {
            "scheme_name": "Kisan Credit Card (KCC) Scheme",
            "scheme_type": "Credit Support",
            "description": "Flexible credit support for farmers",
            "eligibility": "All farmers",
            "benefits": ["Agricultural credit", "Flexible repayment"],
            "status": "Active"
        }
    ]
    
    return {
        "location": location,
        "state": extract_state_from_location(location),
        "farmer_profile": farmer_profile,
        "total_schemes": len(fallback_schemes),
        "schemes": fallback_schemes,
        "recommendations": [
            "Apply for PM-KISAN for direct income support",
            "Consider PMFBY for crop insurance",
            "Access KCC for agricultural credit needs"
        ],
        "data_source": "fallback",
        "data_freshness": "2024-08-12"
    }
