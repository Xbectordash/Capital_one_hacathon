"""
Soil Data Plugin
Description: Fetches soil data from various APIs and provides soil analysis functionality.
"""
import os
import requests
from typing import Dict, Optional
from src.utils.loggers import get_logger
from src.config.settings import GEMINI_API_KEY

def fetch_soil_data(latitude: float, longitude: float, location_name: str = "Unknown") -> Dict:
    """
    Fetch soil data for given coordinates using SoilGrids API and other sources.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate  
        location_name (str): Name of the location for logging purposes
        
    Returns:
        Dict: A dictionary containing soil details (pH, nutrients, organic matter, etc.)
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilPlugins] Fetching soil data for location: {location_name} ({latitude}, {longitude})")
    
    try:
        # Using SoilGrids API for soil data
        # This is a free, open-source global soil information system
        properties = ["phh2o", "nitrogen", "soc", "sand", "clay", "silt"]
        depths = ["0-5cm", "5-15cm"]
        
        soil_data = {}
        
        # Fetch soil properties from SoilGrids
        for prop in properties:
            try:
                url = f"https://rest.isric.org/soilgrids/v2.0/properties/query"
                params = {
                    "lon": longitude,
                    "lat": latitude,
                    "property": prop,
                    "depth": "0-5cm",
                    "value": "mean"
                }
                
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                # Correct SoilGrids API structure: properties.layers[0].depths[0].values.mean
                if (data.get("properties") and 
                    data["properties"].get("layers") and 
                    len(data["properties"]["layers"]) > 0):
                    
                    layer = data["properties"]["layers"][0]
                    if (layer.get("depths") and 
                        len(layer["depths"]) > 0 and
                        layer["depths"][0].get("values") and
                        layer["depths"][0]["values"].get("mean") is not None):
                        
                        value = layer["depths"][0]["values"]["mean"]
                        soil_data[prop] = value
                        logger.info(f"[SoilPlugins] Fetched {prop}: {value}")
                    else:
                        logger.warning(f"[SoilPlugins] No data available for {prop} at this location")
                        soil_data[prop] = None
                else:
                    logger.warning(f"[SoilPlugins] Invalid response structure for {prop}")
                    soil_data[prop] = None
                
            except Exception as e:
                logger.warning(f"[SoilPlugins] Failed to fetch {prop}: {e}")
                soil_data[prop] = None
        
        # Format the soil data for better readability
        formatted_soil_data = format_soil_data(soil_data, location_name)
        
        # Check if we got any real data - if all values are None, use fallback
        has_real_data = any(soil_data.get(prop) is not None for prop in properties)
        
        if has_real_data:
            logger.info(f"[SoilPlugins] Soil data fetched successfully: {formatted_soil_data}")
            return formatted_soil_data
        else:
            logger.warning(f"[SoilPlugins] No real data available for {location_name}, using region-specific fallback")
            return get_fallback_soil_data(location_name)
        
    except Exception as e:
        logger.error(f"[SoilPlugins] Error fetching soil data: {e}")
        # Return fallback soil data
        return get_fallback_soil_data(location_name)


def format_soil_data(raw_data: Dict, location: str) -> Dict:
    """
    Format raw soil data into readable format.
    
    Args:
        raw_data (Dict): Raw soil data from API
        location (str): Location name
        
    Returns:
        Dict: Formatted soil data
    """
    logger = get_logger("soil_plugins")
    
    formatted = {
        "location": location,
        "ph": "N/A",
        "nitrogen": "N/A", 
        "organic_carbon": "N/A",
        "sand_content": "N/A",
        "clay_content": "N/A",
        "silt_content": "N/A",
        "soil_type": "N/A",
        "fertility_status": "N/A"
    }
    
    try:
        # pH conversion (SoilGrids pH is in pH*10)
        if raw_data.get("phh2o") is not None:
            ph_value = raw_data["phh2o"] / 10
            formatted["ph"] = f"{ph_value:.1f}"
            
            # Classify pH
            if ph_value < 6.0:
                ph_status = "Acidic"
            elif ph_value > 7.5:
                ph_status = "Alkaline"
            else:
                ph_status = "Neutral"
            formatted["ph"] += f" ({ph_status})"
        
        # Nitrogen (convert from cg/kg to more readable format)
        if raw_data.get("nitrogen") is not None:
            n_value = raw_data["nitrogen"] / 100  # Convert cg/kg to g/kg
            formatted["nitrogen"] = f"{n_value:.1f} g/kg"
            
            # Classify nitrogen levels
            if n_value < 2.0:
                n_status = "Low"
            elif n_value > 4.0:
                n_status = "High"
            else:
                n_status = "Medium"
            formatted["nitrogen"] += f" ({n_status})"
        
        # Organic Carbon (convert from dg/kg to percentage)
        if raw_data.get("soc") is not None:
            oc_value = raw_data["soc"] / 1000  # Convert dg/kg to %
            formatted["organic_carbon"] = f"{oc_value:.2f}%"
            
            # Classify organic carbon levels
            if oc_value < 1.0:
                oc_status = "Low"
            elif oc_value > 2.0:
                oc_status = "High"
            else:
                oc_status = "Medium"
            formatted["organic_carbon"] += f" ({oc_status})"
        
        # Soil texture components - handle None values gracefully
        sand = raw_data.get("sand", 0) / 10 if raw_data.get("sand") is not None else 0  # Convert to %
        clay = raw_data.get("clay", 0) / 10 if raw_data.get("clay") is not None else 0
        silt = raw_data.get("silt", 0) / 10 if raw_data.get("silt") is not None else 0
        
        if sand > 0:
            formatted["sand_content"] = f"{sand:.1f}%"
        if clay > 0:
            formatted["clay_content"] = f"{clay:.1f}%"
        if silt > 0:
            formatted["silt_content"] = f"{silt:.1f}%"
        
        # Determine soil type based on texture
        if sand > 0 and clay > 0 and silt > 0:
            if sand > 70:
                formatted["soil_type"] = "Sandy"
            elif clay > 40:
                formatted["soil_type"] = "Clay"
            elif silt > 40:
                formatted["soil_type"] = "Silty"
            elif sand > 45 and clay < 20:
                formatted["soil_type"] = "Sandy Loam"
            elif clay > 25 and clay < 40:
                formatted["soil_type"] = "Clay Loam"
            else:
                formatted["soil_type"] = "Loam"
        
        # Overall fertility assessment
        ph_good = False
        n_good = False
        oc_good = False
        
        if raw_data.get("phh2o") is not None:
            ph_good = 6.0 <= (raw_data["phh2o"] / 10) <= 7.5
        if raw_data.get("nitrogen") is not None:
            n_good = (raw_data["nitrogen"] / 100) >= 2.0
        if raw_data.get("soc") is not None:
            oc_good = (raw_data["soc"] / 1000) >= 1.0
        
        # Only calculate fertility if we have some data
        if raw_data.get("phh2o") is not None or raw_data.get("nitrogen") is not None or raw_data.get("soc") is not None:
            fertility_score = sum([ph_good, n_good, oc_good])
            if fertility_score >= 2:
                formatted["fertility_status"] = "Good"
            elif fertility_score == 1:
                formatted["fertility_status"] = "Moderate"
            else:
                formatted["fertility_status"] = "Poor"
        
        logger.info(f"[SoilPlugins] Formatted soil data successfully")
        
    except Exception as e:
        logger.error(f"[SoilPlugins] Error formatting soil data: {e}")
    
    return formatted


def get_fallback_soil_data(location: str) -> Dict:
    """
    Provide fallback soil data when API calls fail.
    Uses region-specific typical soil characteristics for India.
    
    Args:
        location (str): Location name
        
    Returns:
        Dict: Fallback soil data
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilPlugins] Providing fallback soil data for {location}")
    
    # Region-specific soil data for India
    location_lower = location.lower()
    
    if any(city in location_lower for city in ['delhi', 'ncr', 'gurgaon', 'noida']):
        # North India - Delhi region (alluvial soil)
        return {
            "location": location,
            "ph": "7.8 (Alkaline)",
            "nitrogen": "2.1 g/kg (Medium)",
            "organic_carbon": "0.8% (Low)",
            "sand_content": "52.0%",
            "clay_content": "18.0%", 
            "silt_content": "30.0%",
            "soil_type": "Sandy Loam",
            "fertility_status": "Moderate"
        }
    elif any(city in location_lower for city in ['mumbai', 'pune', 'nashik', 'aurangabad']):
        # Maharashtra - black soil (regur)
        return {
            "location": location,
            "ph": "7.5 (Alkaline)",
            "nitrogen": "2.8 g/kg (Medium)",
            "organic_carbon": "1.4% (Medium)",
            "sand_content": "25.0%",
            "clay_content": "48.0%", 
            "silt_content": "27.0%",
            "soil_type": "Clay",
            "fertility_status": "Good"
        }
    elif any(city in location_lower for city in ['bangalore', 'mysore', 'tumkur', 'hassan']):
        # Karnataka - red soil
        return {
            "location": location,
            "ph": "6.2 (Slightly Acidic)",
            "nitrogen": "1.9 g/kg (Low)",
            "organic_carbon": "1.1% (Medium)",
            "sand_content": "65.0%",
            "clay_content": "15.0%", 
            "silt_content": "20.0%",
            "soil_type": "Sandy",
            "fertility_status": "Moderate"
        }
    elif any(city in location_lower for city in ['chennai', 'coimbatore', 'madurai', 'salem']):
        # Tamil Nadu - red and black soil mix
        return {
            "location": location,
            "ph": "6.8 (Neutral)",
            "nitrogen": "2.3 g/kg (Medium)",
            "organic_carbon": "1.3% (Medium)",
            "sand_content": "42.0%",
            "clay_content": "35.0%", 
            "silt_content": "23.0%",
            "soil_type": "Clay Loam",
            "fertility_status": "Good"
        }
    elif any(city in location_lower for city in ['kolkata', 'howrah', 'durgapur', 'asansol']):
        # West Bengal - alluvial soil
        return {
            "location": location,
            "ph": "7.2 (Neutral)",
            "nitrogen": "3.1 g/kg (High)",
            "organic_carbon": "1.8% (High)",
            "sand_content": "38.0%",
            "clay_content": "28.0%", 
            "silt_content": "34.0%",
            "soil_type": "Loam",
            "fertility_status": "Good"
        }
    else:
        # Generic Indian agricultural soil
        return {
            "location": location,
            "ph": "6.8 (Neutral)",
            "nitrogen": "2.5 g/kg (Medium)",
            "organic_carbon": "1.2% (Medium)",
            "sand_content": "45.0%",
            "clay_content": "25.0%", 
            "silt_content": "30.0%",
            "soil_type": "Loam",
            "fertility_status": "Moderate"
        }


def get_agricultural_coordinates(location_name: str) -> Optional[tuple]:
    """
    Get coordinates for agricultural areas near a location, not city centers.
    SoilGrids has better coverage for rural/agricultural areas.
    
    Args:
        location_name (str): Name of the location
        
    Returns:
        Optional[tuple]: (latitude, longitude) for agricultural area or None if not found
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilPlugins] Getting agricultural coordinates for location: {location_name}")
    
    # Known agricultural coordinates for major Indian regions
    # These are rural areas with good SoilGrids coverage
    agricultural_coords = {
        'delhi': [(28.4595, 77.0266), (28.7000, 77.3000), (28.5000, 77.1000)],  # Delhi NCR agricultural areas
        'mumbai': [(19.7515, 75.7139), (19.2000, 72.9000), (19.5000, 73.0000)],  # Maharashtra agricultural
        'bangalore': [(15.3173, 75.7139), (12.5000, 77.2000), (13.2000, 77.8000)],  # Karnataka agricultural    
        'chennai': [(11.1271, 78.6569), (11.5000, 79.0000), (12.2000, 79.5000)],  # Tamil Nadu agricultural
        'kolkata': [(23.3441, 87.8619), (23.0000, 88.0000), (22.8000, 88.5000)],  # West Bengal agricultural
        'hyderabad': [(17.2000, 78.8000), (17.5000, 78.2000), (16.8000, 79.2000)],  # Telangana agricultural
        'pune': [(19.7515, 75.7139), (18.8000, 73.5000), (19.2000, 74.0000)],  # Maharashtra Pune region
        'ahmedabad': [(23.5000, 72.0000), (23.8000, 72.5000), (22.8000, 72.2000)],  # Gujarat agricultural
        'jaipur': [(26.5000, 75.5000), (27.2000, 76.0000), (26.8000, 75.2000)],  # Rajasthan agricultural
        'lucknow': [(26.5000, 80.5000), (26.8000, 81.0000), (27.2000, 80.2000)],  # UP agricultural
        'chandigarh': [(30.9010, 75.8573), (30.5000, 76.2000), (31.2000, 75.5000)],  # Punjab agricultural
        'bhopal': [(23.0000, 77.5000), (23.5000, 77.8000), (22.8000, 77.2000)],  # MP agricultural
        'patna': [(25.5000, 85.0000), (25.8000, 85.5000), (25.2000, 84.8000)],  # Bihar agricultural
        'thiruvananthapuram': [(8.5000, 77.0000), (8.8000, 76.8000), (8.2000, 77.2000)],  # Kerala agricultural
        'guwahati': [(26.0000, 91.5000), (26.2000, 91.8000), (25.8000, 91.2000)],  # Assam agricultural
        'bhubaneswar': [(20.5000, 85.8000), (20.2000, 86.0000), (20.8000, 85.5000)],  # Odisha agricultural
    }
    
    location_lower = location_name.lower()
    
    # Find matching agricultural coordinates
    for key, coords_list in agricultural_coords.items():
        if key in location_lower:
            logger.info(f"[SoilPlugins] Found agricultural coordinates for {location_name}")
            return coords_list[0]  # Return first (best) coordinate
    
    # If no specific agricultural coordinates, try to get city coordinates
    # and offset them to nearby rural areas
    city_coords = get_location_coordinates(location_name)
    if city_coords:
        lat, lon = city_coords
        
        # Create agricultural offsets (move away from city center)
        agricultural_offsets = [
            (lat + 0.2, lon + 0.2),  # Northeast rural area
            (lat - 0.2, lon - 0.2),  # Southwest rural area  
            (lat + 0.3, lon - 0.1),  # North rural area
            (lat - 0.1, lon + 0.3),  # East rural area
        ]
        
        logger.info(f"[SoilPlugins] Using offset agricultural coordinates for {location_name}")
        return agricultural_offsets[0]  # Return first offset
    
    return None


def get_location_coordinates(location_name: str) -> Optional[tuple]:
    """
    Get coordinates for a location using a geocoding service.
    
    Args:
        location_name (str): Name of the location
        
    Returns:
        Optional[tuple]: (latitude, longitude) or None if not found
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilPlugins] Getting coordinates for location: {location_name}")
    
    try:
        # Using OpenStreetMap's Nominatim service (free, no API key required)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_name + ", India",  # Add India for better results
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "FarmMate-SoilPlugin/1.0"  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            logger.info(f"[SoilPlugins] Found coordinates for {location_name}: ({lat}, {lon})")
            return (lat, lon)
        else:
            logger.warning(f"[SoilPlugins] No coordinates found for {location_name}")
            return None
            
    except Exception as e:
        logger.error(f"[SoilPlugins] Error getting coordinates for {location_name}: {e}")
        return None


def fetch_soil_data_by_location(location_name: str) -> Dict:
    """
    Fetch soil data for a location by name.
    First tries agricultural coordinates, then city coordinates.
    
    Args:
        location_name (str): Name of the location
        
    Returns:
        Dict: Soil data for the location
    """
    logger = get_logger("soil_plugins")
    logger.info(f"[SoilPlugins] Fetching soil data for location: {location_name}")
    
    # Try agricultural coordinates first (better SoilGrids coverage)
    agricultural_coords = get_agricultural_coordinates(location_name)
    
    if agricultural_coords:
        lat, lon = agricultural_coords
        logger.info(f"[SoilPlugins] Using agricultural coordinates: ({lat}, {lon})")
        soil_data = fetch_soil_data(lat, lon, location_name)
        
        # Check if we got real data (not all N/A)
        if any(value != "N/A" for key, value in soil_data.items() if key != "location"):
            logger.info(f"[SoilPlugins] Successfully got real soil data from agricultural coordinates")
            return soil_data
        else:
            logger.warning(f"[SoilPlugins] Agricultural coordinates didn't yield data, trying city coordinates")
    
    # Try city coordinates as backup
    city_coords = get_location_coordinates(location_name)
    if city_coords:
        lat, lon = city_coords
        logger.info(f"[SoilPlugins] Using city coordinates: ({lat}, {lon})")
        soil_data = fetch_soil_data(lat, lon, location_name)
        
        # Check if we got real data
        if any(value != "N/A" for key, value in soil_data.items() if key != "location"):
            logger.info(f"[SoilPlugins] Successfully got real soil data from city coordinates")
            return soil_data
    
    # If no real data available, use fallback
    logger.warning(f"[SoilPlugins] No real API data available for {location_name}, using region-specific fallback")
    return get_fallback_soil_data(location_name)
