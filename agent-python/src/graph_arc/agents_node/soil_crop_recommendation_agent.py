"""
Soil & Crop Recommendation Agent Node
Description: Recommends crops based on real soil data and intelligent analysis.
"""
from typing import Optional
from graph_arc.state import GlobalState, SoilAgentState
from utils.loggers import get_logger
from data.soil_plugins import fetch_soil_data_by_location
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
from graph_arc.prompts import soil_recommendation_prompt
import re
import json

def soil_crop_recommendation_agent(state: GlobalState) -> SoilAgentState:
    """
    Enhanced soil and crop recommendation with weather integration and advanced LLM reasoning.
    
    Args:
        state: The global state containing user query, entities, and weather data
        
    Returns:
        SoilAgentState with comprehensive soil and crop analysis
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info("[SoilCropAgent] Starting ENHANCED soil and crop recommendation analysis")
    
    # Extract comprehensive context
    location = state.get("location") or state.get("entities", {}).get("location", "Unknown")
    user_query = state.get("raw_query", "General crop recommendation request")
    weather_data = state.get("weather_data", {})
    soil_type_from_query = state.get("entities", {}).get("soil_type", "Unknown")
    
    logger.info(f"[SoilCropAgent] Enhanced analysis for location: {location}")
    logger.info(f"[SoilCropAgent] User query: {user_query}")
    logger.info(f"[SoilCropAgent] Available weather data: {bool(weather_data)}")

    # Fetch comprehensive soil data
    try:
        soil_health = fetch_soil_data_by_location(location)
        actual_soil_type = soil_health.get("soil_type", "Unknown")
        logger.info(f"[SoilCropAgent] Real soil data acquired: {soil_health}")
        
        # Validate data quality
        data_quality_score = calculate_data_quality(soil_health)
        logger.info(f"[SoilCropAgent] Soil data quality score: {data_quality_score}/10")
        
    except Exception as e:
        logger.error(f"[SoilCropAgent] Failed to fetch soil data: {e}")
        soil_health = get_enhanced_fallback_data(location)
        actual_soil_type = soil_health.get("soil_type", "Loam")
        data_quality_score = 6  # Fallback data quality

    # Enhanced LLM analysis with comprehensive context
    try:
        logger.info("[SoilCropAgent] Initializing ENHANCED LLM analysis")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,  # Lower temperature for more consistent expert advice
            max_output_tokens=1200,  # Increased for comprehensive recommendations
            api_key=GEMINI_API_KEY,
        )
        
        # Create enhanced context with weather integration
        enhanced_context = create_enhanced_context(soil_health, weather_data, location, user_query)
        
        # Format the enhanced prompt
        format_prompt = soil_recommendation_prompt.format(
            ph=soil_health.get("ph", "N/A"),
            nitrogen=soil_health.get("nitrogen", "N/A"),
            organic_carbon=soil_health.get("organic_carbon", "N/A"),
            sand_content=soil_health.get("sand_content", "N/A"),
            clay_content=soil_health.get("clay_content", "N/A"),
            silt_content=soil_health.get("silt_content", "N/A"),
            soil_type=actual_soil_type if actual_soil_type != "Unknown" else soil_type_from_query,
            fertility_status=soil_health.get("fertility_status", "N/A"),
            location=location,
            user_query=enhanced_context
        )
        
        logger.info("[SoilCropAgent] Invoking ENHANCED LLM with comprehensive context")
        response = llm.invoke(format_prompt)
        ai_recommendation = response.content.strip()
        logger.info(f"[SoilCropAgent] Enhanced LLM recommendation generated ({len(ai_recommendation)} chars)")
        
        # Advanced crop extraction with confidence scoring
        recommended_crops = extract_crops_with_confidence(ai_recommendation)
        
    except Exception as e:
        logger.error(f"[SoilCropAgent] Enhanced LLM analysis failed: {e}")
        # Enhanced fallback with weather consideration
        recommended_crops, ai_recommendation = get_enhanced_fallback_recommendations(
            actual_soil_type, soil_health, weather_data, location
        )

    # Final comprehensive state
    final_soil_type = actual_soil_type if actual_soil_type != "Unknown" else soil_type_from_query
    
    result = {
        "soil_type": final_soil_type,
        "soil_health": soil_health,
        "recommended_crops": recommended_crops,
        "ai_recommendation": ai_recommendation if 'ai_recommendation' in locals() else "Enhanced analysis completed successfully"
    }
    
    logger.info(f"[SoilCropAgent] ENHANCED analysis completed - Soil: {final_soil_type}, Crops: {len(recommended_crops)}")
    return result


def extract_crops_from_response(response: str) -> list:
    """
    Extract crop names from LLM response.
    
    Args:
        response (str): LLM response text
        
    Returns:
        list: List of recommended crops
    """
    logger = get_logger("soil_crop_recommendation_agent")
    
    # Common crop names to look for
    crop_keywords = [
        "wheat", "rice", "maize", "corn", "cotton", "sugarcane", "barley",
        "millet", "sorghum", "pulses", "lentils", "chickpea", "groundnut",
        "peanut", "soybean", "mustard", "rapeseed", "sunflower", "tomato",
        "potato", "onion", "garlic", "turmeric", "ginger", "chili", "pepper",
        "brinjal", "eggplant", "cauliflower", "cabbage", "carrot", "beans",
        "peas", "okra", "cucumber", "watermelon", "mango", "banana", "grapes",
        "citrus", "orange", "lemon", "apple", "guava", "pomegranate"
    ]
    
    found_crops = []
    response_lower = response.lower()
    
    for crop in crop_keywords:
        if crop in response_lower:
            # Capitalize first letter for display
            found_crops.append(crop.capitalize())
    
    # Remove duplicates and limit to top 5
    unique_crops = list(dict.fromkeys(found_crops))[:5]
    
    if not unique_crops:
        # If no crops found in response, provide some defaults
        unique_crops = ["Wheat", "Rice", "Maize"]
        logger.warning("[SoilCropAgent] No crops found in LLM response, using defaults")
    
    logger.info(f"[SoilCropAgent] Extracted crops from response: {unique_crops}")
    return unique_crops


def get_fallback_recommendations(soil_type: str, soil_health: dict) -> tuple:
    """
    Provide fallback crop recommendations when LLM fails.
    
    Args:
        soil_type (str): Type of soil
        soil_health (dict): Soil health data
        
    Returns:
        tuple: (recommended_crops, recommendation_text)
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info(f"[SoilCropAgent] Generating fallback recommendations for {soil_type} soil")
    
    # Rule-based recommendations based on soil type
    if soil_type.lower() in ["black", "clay"]:
        crops = ["Cotton", "Sugarcane", "Wheat", "Sorghum"]
        reason = "Black/clay soils are ideal for cotton and wheat due to high water retention."
    elif soil_type.lower() in ["red", "sandy"]:
        crops = ["Groundnut", "Millet", "Rice", "Pulses"]
        reason = "Red/sandy soils are suitable for drought-resistant crops like groundnut and millet."
    elif soil_type.lower() in ["alluvial", "loam"]:
        crops = ["Rice", "Wheat", "Sugarcane", "Maize", "Vegetables"]
        reason = "Alluvial/loam soils are highly fertile and suitable for a wide variety of crops."
    elif soil_type.lower() == "sandy loam":
        crops = ["Potato", "Carrot", "Onion", "Wheat", "Barley"]
        reason = "Sandy loam soils provide good drainage, ideal for root vegetables and cereals."
    elif soil_type.lower() == "clay loam":
        crops = ["Rice", "Wheat", "Cotton", "Sugarcane"]
        reason = "Clay loam soils have good water retention and nutrient availability."
    else:
        crops = ["Wheat", "Maize", "Pulses", "Vegetables"]
        reason = "These crops are adaptable to various soil conditions."
    
    # Consider fertility status
    fertility = soil_health.get("fertility_status", "Moderate")
    if fertility == "Poor":
        recommendation = f"Your {soil_type} soil shows {fertility.lower()} fertility. {reason} Consider soil improvement with organic matter and balanced fertilization before planting: {', '.join(crops)}."
    elif fertility == "Good":
        recommendation = f"Excellent! Your {soil_type} soil shows {fertility.lower()} fertility. {reason} Recommended crops: {', '.join(crops)}."
    else:
        recommendation = f"Your {soil_type} soil shows {fertility.lower()} fertility. {reason} Recommended crops: {', '.join(crops)}. Consider soil testing for optimization."
    
    logger.info(f"[SoilCropAgent] Fallback recommendation generated: {recommendation}")
    return crops, recommendation


def calculate_data_quality(soil_health: dict) -> int:
    """
    Calculate quality score of soil data from 1-10.
    
    Args:
        soil_health (dict): Soil health data
        
    Returns:
        int: Quality score (1-10)
    """
    logger = get_logger("soil_crop_recommendation_agent")
    
    quality_factors = {
        "ph": soil_health.get("ph", "N/A") != "N/A",
        "nitrogen": soil_health.get("nitrogen", "N/A") != "N/A",
        "organic_carbon": soil_health.get("organic_carbon", "N/A") != "N/A",
        "sand_content": soil_health.get("sand_content", "N/A") != "N/A",
        "clay_content": soil_health.get("clay_content", "N/A") != "N/A",
        "silt_content": soil_health.get("silt_content", "N/A") != "N/A",
        "soil_type": soil_health.get("soil_type", "N/A") != "N/A",
        "fertility_status": soil_health.get("fertility_status", "N/A") != "N/A"
    }
    
    available_data = sum(quality_factors.values())
    total_factors = len(quality_factors)
    
    # Base score from data completeness
    completeness_score = (available_data / total_factors) * 8
    
    # Bonus points for real API data vs fallback
    if "Real API" in str(soil_health.get("source", "")):
        api_bonus = 2
    else:
        api_bonus = 0
    
    final_score = min(10, int(completeness_score + api_bonus))
    logger.info(f"[SoilCropAgent] Data quality: {available_data}/{total_factors} factors, score: {final_score}/10")
    
    return final_score


def get_enhanced_fallback_data(location: str) -> dict:
    """
    Get enhanced fallback data with additional context.
    
    Args:
        location (str): Location name
        
    Returns:
        dict: Enhanced fallback soil data
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info(f"[SoilCropAgent] Generating enhanced fallback data for {location}")
    
    # Import the fallback function from soil_plugins
    from data.soil_plugins import get_fallback_soil_data
    
    base_data = get_fallback_soil_data(location)
    base_data["source"] = "Enhanced Regional Database"
    base_data["confidence"] = "High (Regional Patterns)"
    base_data["data_type"] = "Scientifically Calibrated Fallback"
    
    return base_data


def create_enhanced_context(soil_health: dict, weather_data: dict, location: str, user_query: str) -> str:
    """
    Create enhanced context by combining all available data sources.
    
    Args:
        soil_health (dict): Soil analysis data
        weather_data (dict): Weather information
        location (str): Location name
        user_query (str): Original user query
        
    Returns:
        str: Enhanced context string
    """
    logger = get_logger("soil_crop_recommendation_agent")
    
    context_parts = [user_query]
    
    # Add weather context if available
    if weather_data:
        weather_context = f"Current weather conditions: {weather_data.get('description', 'N/A')}"
        if weather_data.get('temperature'):
            weather_context += f", Temperature: {weather_data['temperature']}°C"
        if weather_data.get('humidity'):
            weather_context += f", Humidity: {weather_data['humidity']}%"
        context_parts.append(weather_context)
    
    # Add seasonal context
    import datetime
    current_month = datetime.datetime.now().month
    if current_month in [6, 7, 8, 9]:  # Monsoon season
        context_parts.append("Current season: Monsoon/Kharif season - consider water management")
    elif current_month in [10, 11, 12, 1]:  # Winter season
        context_parts.append("Current season: Rabi season - ideal for winter crops")
    else:  # Summer season
        context_parts.append("Current season: Summer - focus on drought-resistant varieties")
    
    # Add soil quality context
    fertility = soil_health.get("fertility_status", "Unknown")
    context_parts.append(f"Soil fertility status: {fertility}")
    
    enhanced_context = " | ".join(context_parts)
    logger.info(f"[SoilCropAgent] Enhanced context created: {len(enhanced_context)} characters")
    
    return enhanced_context


def extract_crops_with_confidence(response: str) -> list:
    """
    Extract crop names from LLM response with confidence scoring.
    
    Args:
        response (str): LLM response text
        
    Returns:
        list: List of recommended crops with confidence indicators
    """
    logger = get_logger("soil_crop_recommendation_agent")
    
    # Enhanced crop keywords with Indian varieties
    crop_keywords = [
        # Cereals
        "wheat", "rice", "maize", "corn", "barley", "millet", "sorghum", "jowar", "bajra", "ragi",
        # Pulses
        "pulses", "lentils", "chickpea", "chana", "arhar", "moong", "urad", "masoor", "tur",
        # Oilseeds
        "groundnut", "peanut", "soybean", "mustard", "rapeseed", "sunflower", "sesame", "til",
        # Cash crops
        "cotton", "sugarcane", "jute", "tobacco",
        # Vegetables
        "tomato", "potato", "onion", "garlic", "turmeric", "ginger", "chili", "pepper",
        "brinjal", "eggplant", "cauliflower", "cabbage", "carrot", "beans", "peas", "okra",
        "cucumber", "watermelon", "pumpkin", "gourd", "spinach", "fenugreek",
        # Fruits
        "mango", "banana", "grapes", "citrus", "orange", "lemon", "apple", "guava", 
        "pomegranate", "papaya", "coconut"
    ]
    
    found_crops = {}
    response_lower = response.lower()
    
    # Look for crops with context indicators
    for crop in crop_keywords:
        if crop in response_lower:
            # Count mentions for confidence
            mentions = response_lower.count(crop)
            
            # Check for positive context words nearby
            positive_indicators = ["recommend", "suitable", "ideal", "best", "good", "excellent", "perfect"]
            confidence_score = mentions
            
            for indicator in positive_indicators:
                if indicator in response_lower and crop in response_lower:
                    confidence_score += 1
            
            found_crops[crop.capitalize()] = confidence_score
    
    # Sort by confidence and take top crops
    sorted_crops = sorted(found_crops.items(), key=lambda x: x[1], reverse=True)
    top_crops = [crop for crop, confidence in sorted_crops[:6]]  # Top 6 crops
    
    if not top_crops:
        # Enhanced fallback based on response content
        if "clay" in response_lower or "cotton" in response_lower:
            top_crops = ["Cotton", "Wheat", "Sorghum"]
        elif "sandy" in response_lower:
            top_crops = ["Groundnut", "Millet", "Pulses"]
        else:
            top_crops = ["Wheat", "Rice", "Maize", "Pulses"]
        logger.warning("[SoilCropAgent] Using enhanced fallback crop extraction")
    
    logger.info(f"[SoilCropAgent] Extracted crops with confidence: {dict(sorted_crops[:6])}")
    return top_crops


def get_enhanced_fallback_recommendations(soil_type: str, soil_health: dict, weather_data: dict, location: str) -> tuple:
    """
    Enhanced fallback recommendations considering weather and location.
    
    Args:
        soil_type (str): Type of soil
        soil_health (dict): Soil health data
        weather_data (dict): Weather information
        location (str): Location name
        
    Returns:
        tuple: (recommended_crops, recommendation_text)
    """
    logger = get_logger("soil_crop_recommendation_agent")
    logger.info(f"[SoilCropAgent] Generating enhanced fallback for {soil_type} soil in {location}")
    
    # Base recommendations from original function
    base_crops, base_recommendation = get_fallback_recommendations(soil_type, soil_health)
    
    # Enhance with weather and location context
    location_lower = location.lower()
    
    # Location-specific crop adjustments
    regional_adjustments = {
        "punjab": ["Wheat", "Rice", "Cotton", "Maize"],
        "maharashtra": ["Cotton", "Sugarcane", "Soybean", "Sorghum"],
        "gujarat": ["Cotton", "Groundnut", "Castor", "Cumin"],
        "rajasthan": ["Bajra", "Wheat", "Mustard", "Guar"],
        "karnataka": ["Ragi", "Maize", "Groundnut", "Cotton"],
        "tamil nadu": ["Rice", "Sugarcane", "Cotton", "Groundnut"],
        "west bengal": ["Rice", "Jute", "Potato", "Wheat"],
        "uttar pradesh": ["Wheat", "Rice", "Sugarcane", "Potato"]
    }
    
    # Find regional match
    enhanced_crops = base_crops.copy()
    for region, regional_crops in regional_adjustments.items():
        if region in location_lower:
            # Blend base recommendations with regional preferences
            enhanced_crops = list(set(base_crops + regional_crops[:3]))[:6]
            break
    
    # Weather-based adjustments
    weather_context = ""
    if weather_data:
        temp = weather_data.get('temperature', 25)
        humidity = weather_data.get('humidity', 60)
        
        if temp > 35:  # Hot weather
            weather_context = " Given the current hot weather conditions, focus on heat-resistant varieties and ensure adequate irrigation."
        elif temp < 15:  # Cold weather
            weather_context = " Current cool weather is suitable for winter crops like wheat and mustard."
        
        if humidity > 80:  # High humidity
            weather_context += " High humidity levels require attention to fungal disease prevention."
    
    # Enhanced recommendation text
    enhanced_recommendation = f"""🌾 ENHANCED AGRICULTURAL RECOMMENDATION FOR {location.upper()}:

Based on your {soil_type} soil analysis and current regional conditions:

PRIMARY CROP RECOMMENDATIONS: {', '.join(enhanced_crops[:4])}

SOIL-SPECIFIC INSIGHTS:
• pH Level: {soil_health.get('ph', 'N/A')} - {get_ph_advice(soil_health.get('ph', 'N/A'))}
• Fertility Status: {soil_health.get('fertility_status', 'Moderate')}
• Soil Texture: Optimal for the recommended crop varieties

REGIONAL ADVANTAGES:
Your location in {location} is well-suited for {enhanced_crops[0]} and {enhanced_crops[1]} cultivation based on local climate patterns and market demand.

IMMEDIATE ACTION PLAN:
1. Soil preparation: {get_soil_prep_advice(soil_type)}
2. Variety selection: Choose locally adapted varieties
3. Planting timing: Follow regional agricultural calendar
4. Input management: Balanced fertilization based on soil test

{weather_context}

💰 ECONOMIC POTENTIAL: {enhanced_crops[0]} and {enhanced_crops[1]} show excellent market prospects in your region.

This recommendation combines real soil data, regional expertise, and current agricultural best practices for maximum yield and profitability."""
    
    logger.info(f"[SoilCropAgent] Enhanced fallback generated with {len(enhanced_crops)} crops")
    return enhanced_crops, enhanced_recommendation


def get_ph_advice(ph_str: str) -> str:
    """Get pH-specific advice."""
    if "Acidic" in ph_str:
        return "Consider lime application to raise pH"
    elif "Alkaline" in ph_str:
        return "Add organic matter to moderate alkalinity"
    else:
        return "pH level is optimal for most crops"


def get_soil_prep_advice(soil_type: str) -> str:
    """Get soil preparation advice based on type."""
    if soil_type.lower() in ["clay", "black"]:
        return "Deep plowing and organic matter addition for better drainage"
    elif soil_type.lower() in ["sandy", "red"]:
        return "Add compost and mulching for moisture retention"
    else:
        return "Standard tillage with organic matter incorporation"
