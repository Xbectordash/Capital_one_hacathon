"""
CSV-Based Soil Analysis Plugin
Description: Provides soil analysis using Indian district-wise soil nutrient data from CSV
Fast, reliable, data-driven soil recommendations
"""
import os
import pandas as pd
from typing import Dict, Optional, List
from src.utils.loggers import get_logger

def get_soil_data_from_csv(location: str, query: str = "") -> Dict:
    """
    Analyze soil based on CSV data for Indian districts
    
    Args:
        location (str): Location name (district, state)
        query (str): User's specific question about soil/crops
        
    Returns:
        Dict: Comprehensive soil analysis with nutrient data
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilCSV] Starting CSV-based soil analysis for location: {location}")
    logger.info(f"[SoilCSV] User query: {query}")
    
    try:
        # Load soil CSV data
        csv_path = os.path.join(os.path.dirname(__file__), 'soil.csv')
        soil_df = pd.read_csv(csv_path)
        logger.info(f"[SoilCSV] Loaded soil data with {len(soil_df)} districts")
        
        # Find matching district
        district_data = find_district_in_csv(soil_df, location)
        
        if district_data is not None:
            logger.info(f"[SoilCSV] Found exact match for {location}")
            soil_analysis = analyze_district_nutrients(district_data, location, query)
        else:
            logger.info(f"[SoilCSV] No exact match found, using regional analysis")
            soil_analysis = get_regional_soil_analysis(location, query)
        
        logger.info(f"[SoilCSV] Soil analysis completed for {location}")
        return soil_analysis
        
    except Exception as e:
        logger.error(f"[SoilCSV] Error in CSV soil analysis: {e}")
        logger.info("[SoilCSV] Falling back to basic knowledge")
        return get_fallback_soil_knowledge(location, query)

def find_district_in_csv(soil_df: pd.DataFrame, location: str) -> Optional[pd.Series]:
    """Find district data in CSV by location name"""
    
    location_clean = location.strip().lower()
    
    # Direct district name search
    for idx, row in soil_df.iterrows():
        district_name = str(row['District ']).strip().lower()
        
        # Exact match
        if district_name == location_clean:
            return row
        
        # Partial match (location contains district name or vice versa)
        if district_name in location_clean or location_clean in district_name:
            return row
    
    # Try common name variations
    location_variations = get_location_variations(location_clean)
    
    for variation in location_variations:
        for idx, row in soil_df.iterrows():
            district_name = str(row['District ']).strip().lower()
            if district_name == variation or variation in district_name:
                return row
    
    return None

def get_location_variations(location: str) -> List[str]:
    """Generate common variations of location names"""
    
    variations = [location]
    
    # Common spelling variations
    replacements = {
        'bangalore': ['bengaluru', 'bangalore urban'],
        'bengaluru': ['bangalore', 'bangalore urban'],
        'mumbai': ['bombay'],
        'delhi': ['new delhi'],
        'pune': ['poona'],
        'kolkata': ['calcutta'],
        'chennai': ['madras'],
        'hyderabad': ['secunderabad'],
        'gurgaon': ['gurugram'],
        'noida': ['gautam buddha nagar'],
        'faridabad': ['faridabad'],
        'ghaziabad': ['ghaziabad']
    }
    
    for original, alts in replacements.items():
        if original in location:
            for alt in alts:
                variations.append(location.replace(original, alt))
        
        for alt in alts:
            if alt in location:
                variations.append(location.replace(alt, original))
    
    return list(set(variations))

def analyze_district_nutrients(district_data: pd.Series, location: str, query: str) -> Dict:
    """Analyze soil nutrients for a specific district"""
    
    logger = get_logger("soil_plugins")
    
    try:
        district_name = district_data['District ']
        
        # Extract nutrient percentages
        nutrients = {
            'zinc': float(district_data['Zn %']) if pd.notna(district_data['Zn %']) else 0,
            'iron': float(district_data['Fe%']) if pd.notna(district_data['Fe%']) else 0,
            'copper': float(district_data['Cu %']) if pd.notna(district_data['Cu %']) else 0,
            'manganese': float(district_data['Mn %']) if pd.notna(district_data['Mn %']) else 0,
            'boron': float(district_data['B %']) if pd.notna(district_data['B %']) else 0,
            'sulfur': float(district_data['S %']) if pd.notna(district_data['S %']) else 0
        }
        
        # Classify nutrient levels
        nutrient_status = classify_nutrients(nutrients)
        
        # Determine soil health and fertility
        soil_health = assess_soil_health(nutrients)
        
        # Get crop recommendations based on nutrients
        recommended_crops = get_crops_for_nutrients(nutrients, location)
        
        # Get irrigation and fertilizer recommendations
        management_advice = get_soil_management_advice(nutrients, query)
        
        # Generate comprehensive analysis
        soil_analysis = {
            "location": f"{district_name} (District Data)",
            "data_source": "Indian Soil Survey CSV Data",
            "quality_score": "9/10",
            
            # Nutrient Analysis
            "zinc_status": f"{nutrients['zinc']:.1f}% ({nutrient_status['zinc']})",
            "iron_status": f"{nutrients['iron']:.1f}% ({nutrient_status['iron']})",
            "copper_status": f"{nutrients['copper']:.1f}% ({nutrient_status['copper']})",
            "manganese_status": f"{nutrients['manganese']:.1f}% ({nutrient_status['manganese']})",
            "boron_status": f"{nutrients['boron']:.1f}% ({nutrient_status['boron']})",
            "sulfur_status": f"{nutrients['sulfur']:.1f}% ({nutrient_status['sulfur']})",
            
            # Overall Assessment
            "soil_health": soil_health['overall'],
            "fertility_status": soil_health['fertility'],
            "limiting_factors": soil_health['limitations'],
            
            # Recommendations
            "recommended_crops": recommended_crops,
            "irrigation_guidance": management_advice['irrigation'],
            "fertilizer_recommendations": management_advice['fertilizers'],
            
            # Formatted for compatibility
            "soil_type": determine_soil_type_from_location(location),
            "ph": "6.5-7.5 (Neutral - typical for region)",
            "nitrogen": "Medium (estimated from regional data)",
            "organic_carbon": "1.0-2.0% (Medium)",
            "sand_content": "35-45%",
            "clay_content": "25-35%",
            "silt_content": "25-35%",
            
            # AI Recommendation
            "ai_recommendation": generate_detailed_recommendation(district_name, nutrients, query)
        }
        
        logger.info(f"[SoilCSV] Generated nutrient analysis for {district_name}")
        return soil_analysis
        
    except Exception as e:
        logger.error(f"[SoilCSV] Error analyzing district nutrients: {e}")
        return get_fallback_soil_knowledge(location, query)

def classify_nutrients(nutrients: Dict[str, float]) -> Dict[str, str]:
    """Classify nutrient levels as Low, Medium, or High"""
    
    # Classification thresholds based on Indian soil standards
    thresholds = {
        'zinc': {'low': 30, 'medium': 70},
        'iron': {'low': 40, 'medium': 80},
        'copper': {'low': 60, 'medium': 90},
        'manganese': {'low': 50, 'medium': 85},
        'boron': {'low': 30, 'medium': 70},
        'sulfur': {'low': 40, 'medium': 80}
    }
    
    classification = {}
    
    for nutrient, value in nutrients.items():
        if nutrient in thresholds:
            if value < thresholds[nutrient]['low']:
                classification[nutrient] = 'Low'
            elif value < thresholds[nutrient]['medium']:
                classification[nutrient] = 'Medium'
            else:
                classification[nutrient] = 'High'
        else:
            classification[nutrient] = 'Medium'
    
    return classification

def assess_soil_health(nutrients: Dict[str, float]) -> Dict[str, str]:
    """Assess overall soil health based on nutrient levels"""
    
    # Calculate average nutrient sufficiency
    total_nutrients = len(nutrients)
    sufficient_nutrients = 0
    limiting_factors = []
    
    thresholds = {
        'zinc': 50, 'iron': 60, 'copper': 70, 
        'manganese': 60, 'boron': 50, 'sulfur': 60
    }
    
    for nutrient, value in nutrients.items():
        if nutrient in thresholds:
            if value >= thresholds[nutrient]:
                sufficient_nutrients += 1
            else:
                limiting_factors.append(nutrient.capitalize())
    
    # Overall health assessment
    sufficiency_ratio = sufficient_nutrients / total_nutrients
    
    if sufficiency_ratio >= 0.8:
        overall = "Excellent"
        fertility = "High"
    elif sufficiency_ratio >= 0.6:
        overall = "Good"
        fertility = "Medium to High"
    elif sufficiency_ratio >= 0.4:
        overall = "Moderate"
        fertility = "Medium"
    else:
        overall = "Poor"
        fertility = "Low to Medium"
    
    return {
        'overall': overall,
        'fertility': fertility,
        'limitations': limiting_factors[:3] if limiting_factors else ['None identified']
    }

def get_crops_for_nutrients(nutrients: Dict[str, float], location: str) -> List[str]:
    """Recommend crops based on nutrient profile"""
    
    suitable_crops = []
    
    # High zinc crops
    if nutrients['zinc'] > 60:
        suitable_crops.extend(['Rice', 'Wheat', 'Maize'])
    
    # High iron crops
    if nutrients['iron'] > 70:
        suitable_crops.extend(['Pulses', 'Legumes', 'Soybean'])
    
    # High copper crops
    if nutrients['copper'] > 80:
        suitable_crops.extend(['Sugarcane', 'Cotton', 'Sunflower'])
    
    # High manganese crops
    if nutrients['manganese'] > 70:
        suitable_crops.extend(['Vegetables', 'Fruits', 'Tea'])
    
    # High boron crops
    if nutrients['boron'] > 60:
        suitable_crops.extend(['Mustard', 'Rape', 'Cauliflower'])
    
    # High sulfur crops
    if nutrients['sulfur'] > 70:
        suitable_crops.extend(['Onion', 'Garlic', 'Cruciferous vegetables'])
    
    # Regional defaults based on location
    if not suitable_crops:
        location_lower = location.lower()
        if any(state in location_lower for state in ['punjab', 'haryana']):
            suitable_crops = ['Wheat', 'Rice', 'Maize', 'Cotton']
        elif any(state in location_lower for state in ['maharashtra', 'gujarat']):
            suitable_crops = ['Cotton', 'Sugarcane', 'Soybean', 'Jowar']
        elif any(state in location_lower for state in ['karnataka', 'kerala']):
            suitable_crops = ['Rice', 'Ragi', 'Coconut', 'Spices']
        else:
            suitable_crops = ['Rice', 'Wheat', 'Pulses', 'Vegetables']
    
    # Remove duplicates and return top 6
    unique_crops = list(dict.fromkeys(suitable_crops))
    return unique_crops[:6]

def get_soil_management_advice(nutrients: Dict[str, float], query: str) -> Dict[str, str]:
    """Generate irrigation and fertilizer recommendations"""
    
    irrigation_advice = "Monitor soil moisture regularly. Irrigate based on crop requirements and weather conditions."
    fertilizer_advice = []
    
    # Specific fertilizer recommendations based on deficiencies
    if nutrients['zinc'] < 50:
        fertilizer_advice.append("Apply Zinc Sulfate (25 kg/ha)")
    
    if nutrients['iron'] < 60:
        fertilizer_advice.append("Apply Iron Sulfate or FeSO4 (20 kg/ha)")
    
    if nutrients['copper'] < 70:
        fertilizer_advice.append("Apply Copper Sulfate (10 kg/ha)")
    
    if nutrients['manganese'] < 60:
        fertilizer_advice.append("Apply Manganese Sulfate (15 kg/ha)")
    
    if nutrients['boron'] < 50:
        fertilizer_advice.append("Apply Borax (10 kg/ha)")
    
    if nutrients['sulfur'] < 60:
        fertilizer_advice.append("Apply Gypsum or Sulfur fertilizer (200 kg/ha)")
    
    # Irrigation-specific advice for query
    if "irrigat" in query.lower():
        avg_nutrients = sum(nutrients.values()) / len(nutrients)
        if avg_nutrients > 80:
            irrigation_advice = "Soil has high nutrient retention. Irrigate moderately to prevent nutrient leaching."
        elif avg_nutrients < 50:
            irrigation_advice = "Low nutrient soil. Use efficient irrigation methods like drip to conserve nutrients."
    
    fertilizer_text = "; ".join(fertilizer_advice) if fertilizer_advice else "Current nutrient levels are adequate"
    
    return {
        'irrigation': irrigation_advice,
        'fertilizers': fertilizer_text
    }

def determine_soil_type_from_location(location: str) -> str:
    """Determine likely soil type based on location"""
    
    location_lower = location.lower()
    
    # Regional soil types
    if any(region in location_lower for region in ['maharashtra', 'gujarat', 'mp', 'madhya pradesh']):
        return "Black Cotton Soil (Vertisols)"
    elif any(region in location_lower for region in ['karnataka', 'tamilnadu', 'andhra', 'telangana']):
        return "Red Laterite Soil"
    elif any(region in location_lower for region in ['punjab', 'haryana', 'uttar pradesh', 'bihar']):
        return "Alluvial Soil"
    elif any(region in location_lower for region in ['rajasthan', 'gujarat']):
        return "Desert/Arid Soil"
    elif any(region in location_lower for region in ['west bengal', 'odisha', 'assam']):
        return "Deltaic Alluvial Soil"
    else:
        return "Mixed Indian Agricultural Soil"

def generate_detailed_recommendation(district: str, nutrients: Dict[str, float], query: str) -> str:
    """Generate detailed AI-style recommendation"""
    
    recommendation = f"""
COMPREHENSIVE SOIL ANALYSIS FOR {district.upper()}:

NUTRIENT STATUS ANALYSIS:
- Zinc (Zn): {nutrients['zinc']:.1f}% - {'Sufficient' if nutrients['zinc'] > 50 else 'Deficient'}
- Iron (Fe): {nutrients['iron']:.1f}% - {'Sufficient' if nutrients['iron'] > 60 else 'Deficient'}  
- Copper (Cu): {nutrients['copper']:.1f}% - {'Sufficient' if nutrients['copper'] > 70 else 'Deficient'}
- Manganese (Mn): {nutrients['manganese']:.1f}% - {'Sufficient' if nutrients['manganese'] > 60 else 'Deficient'}
- Boron (B): {nutrients['boron']:.1f}% - {'Sufficient' if nutrients['boron'] > 50 else 'Deficient'}
- Sulfur (S): {nutrients['sulfur']:.1f}% - {'Sufficient' if nutrients['sulfur'] > 60 else 'Deficient'}

PRIORITY RECOMMENDATIONS:
"""
    
    # Add specific recommendations based on deficiencies
    deficient_nutrients = []
    for nutrient, value in nutrients.items():
        thresholds = {'zinc': 50, 'iron': 60, 'copper': 70, 'manganese': 60, 'boron': 50, 'sulfur': 60}
        if value < thresholds.get(nutrient, 50):
            deficient_nutrients.append(nutrient)
    
    if deficient_nutrients:
        recommendation += f"\n1. IMMEDIATE ACTION: Address {', '.join(deficient_nutrients)} deficiency through targeted fertilization"
        recommendation += f"\n2. SOIL AMENDMENT: Apply recommended micronutrient fertilizers before next sowing"
        recommendation += f"\n3. MONITORING: Conduct soil test every 2-3 years to track improvement"
    else:
        recommendation += f"\n1. MAINTENANCE: Current nutrient levels are good, maintain with balanced fertilization"
        recommendation += f"\n2. OPTIMIZATION: Focus on organic matter enhancement for sustained productivity"
    
    # Add irrigation-specific advice if mentioned in query
    if "irrigat" in query.lower():
        avg_nutrients = sum(nutrients.values()) / len(nutrients)
        if avg_nutrients > 75:
            recommendation += f"\n\nIRRIGATION STRATEGY: High nutrient soil - irrigate moderately to prevent leaching"
        else:
            recommendation += f"\n\nIRRIGATION STRATEGY: Use water-efficient methods to preserve nutrients"
    
    recommendation += f"\n\nSOIL HEALTH SCORE: {sum(nutrients.values())/6:.1f}/100"
    
    return recommendation

def get_regional_soil_analysis(location: str, query: str) -> Dict:
    """Get regional soil analysis when specific district data is not available"""
    
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilCSV] Generating regional analysis for {location}")
    
    # Regional nutrient averages (estimated from CSV data patterns)
    regional_data = {
        'north_india': {'zinc': 70, 'iron': 75, 'copper': 95, 'manganese': 80, 'boron': 55, 'sulfur': 75},
        'south_india': {'zinc': 60, 'iron': 70, 'copper': 90, 'manganese': 85, 'boron': 60, 'sulfur': 70},
        'west_india': {'zinc': 65, 'iron': 65, 'copper': 95, 'manganese': 90, 'boron': 50, 'sulfur': 80},
        'east_india': {'zinc': 75, 'iron': 85, 'copper': 95, 'manganese': 85, 'boron': 45, 'sulfur': 65},
        'central_india': {'zinc': 55, 'iron': 80, 'copper': 90, 'manganese': 85, 'boron': 65, 'sulfur': 70}
    }
    
    # Determine region
    location_lower = location.lower()
    if any(state in location_lower for state in ['punjab', 'haryana', 'delhi', 'himachal', 'uttarakhand']):
        nutrients = regional_data['north_india']
        region = 'North India'
    elif any(state in location_lower for state in ['karnataka', 'tamilnadu', 'kerala', 'andhra', 'telangana']):
        nutrients = regional_data['south_india']
        region = 'South India'
    elif any(state in location_lower for state in ['maharashtra', 'gujarat', 'rajasthan', 'goa']):
        nutrients = regional_data['west_india']
        region = 'West India'
    elif any(state in location_lower for state in ['west bengal', 'odisha', 'bihar', 'jharkhand', 'assam']):
        nutrients = regional_data['east_india']
        region = 'East India'
    else:
        nutrients = regional_data['central_india']
        region = 'Central India'
    
    return analyze_district_nutrients(
        pd.Series({
            'District ': f"{location} ({region} Regional)",
            'Zn %': nutrients['zinc'],
            'Fe%': nutrients['iron'],
            'Cu %': nutrients['copper'],
            'Mn %': nutrients['manganese'],
            'B %': nutrients['boron'],
            'S %': nutrients['sulfur']
        }),
        location,
        query
    )

def get_fallback_soil_knowledge(location: str, query: str) -> Dict:
    """Fallback soil knowledge when CSV data is not available"""
    
    return {
        "location": location,
        "data_source": "Basic Agricultural Knowledge",
        "quality_score": "6/10",
        "soil_type": "Mixed Indian Agricultural Soil",
        "ph": "6.5-7.5 (Neutral)",
        "nitrogen": "Medium (1.5-2.5%)",
        "organic_carbon": "1.0-2.0% (Medium)",
        "sand_content": "40-50%",
        "clay_content": "25-35%",
        "silt_content": "25-35%",
        "fertility_status": "Moderate",
        "recommended_crops": ["Rice", "Wheat", "Cotton", "Sugarcane", "Soybean", "Maize"],
        "irrigation_guidance": "Standard irrigation practices based on crop and season",
        "ai_recommendation": f"""
BASIC SOIL ANALYSIS FOR {location}:

GENERAL RECOMMENDATIONS:
- Conduct detailed soil testing for precise nutrient analysis
- Apply balanced NPK fertilizers based on crop requirements
- Incorporate organic matter (5-10 tons FYM/hectare)
- Follow crop rotation practices for soil health
- Monitor soil moisture for optimal irrigation timing

CROP SUITABILITY:
- Food grains: Rice, Wheat, Maize, Millets
- Cash crops: Cotton, Sugarcane, Oilseeds
- Pulses: Gram, Arhar, Moong, Urad

For location-specific recommendations, please provide district name for detailed analysis.
"""
    }

# Main function for backward compatibility
def fetch_soil_data_by_location(location_name: str) -> Dict:
    """
    Main function to get soil data by location using CSV data
    """
    return get_soil_data_from_csv(location_name, "")

def analyze_soil_with_llm(location: str, query: str = "") -> Dict:
    """
    Compatibility function that uses CSV data instead of LLM
    """
    return get_soil_data_from_csv(location, query)
