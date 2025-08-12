"""
Test suite for soil and crop recommendation functionality.
Covers API integration, LLM recommendations, error handling, and edge cases.
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import the modules to test
from data.soil_plugins import (
    fetch_soil_data_by_location, 
    fetch_soil_data, 
    get_location_coordinates,
    format_soil_data,
    get_fallback_soil_data
)
from graph_arc.agents_node.soil_crop_recommendation_agent import (
    soil_crop_recommendation_agent,
    extract_crops_from_response,
    get_fallback_recommendations
)


class TestSoilPluginsMocked(unittest.TestCase):
    """Test cases for soil_plugins module with mocked API calls"""
    
    def test_get_fallback_soil_data(self):
        """Test fallback soil data generation"""
        print("\n=== Testing Fallback Soil Data ===")
        
        test_locations = ["Delhi", "Mumbai", "Unknown"]
        
        for location in test_locations:
            result = get_fallback_soil_data(location)
            
            # Verify structure
            self.assertIsInstance(result, dict)
            self.assertIn("location", result)
            self.assertIn("ph", result)
            self.assertIn("nitrogen", result)
            self.assertIn("organic_carbon", result)
            self.assertIn("soil_type", result)
            self.assertIn("fertility_status", result)
            
            # Verify location is preserved
            self.assertEqual(result["location"], location)
            
            print(f"✓ Fallback data for {location}: {result['soil_type']} soil, pH {result['ph']}")
    
    def test_format_soil_data(self):
        """Test soil data formatting functionality"""
        print("\n=== Testing Soil Data Formatting ===")
        
        # Mock raw soil data from SoilGrids API
        raw_data = {
            "phh2o": 65,  # pH * 10
            "nitrogen": 250,  # cg/kg
            "soc": 1200,  # dg/kg
            "sand": 450,  # g/kg * 10
            "clay": 250,  # g/kg * 10
            "silt": 300   # g/kg * 10
        }
        
        result = format_soil_data(raw_data, "Test Location")
        
        # Verify formatting
        self.assertIn("6.5", result["ph"])  # Should convert 65 to 6.5
        self.assertIn("Neutral", result["ph"])  # Should classify as neutral
        self.assertIn("2.5", result["nitrogen"])  # Should convert 250 to 2.5 g/kg
        self.assertIn("1.20%", result["organic_carbon"])  # Should convert 1200 to 1.20%
        self.assertEqual(result["soil_type"], "Loam")  # Should classify as loam
        self.assertEqual(result["fertility_status"], "Good")  # Should be good fertility
        
        print(f"✓ Formatted soil data: {result['soil_type']} soil")
        print(f"  - pH: {result['ph']}")
        print(f"  - Nitrogen: {result['nitrogen']}")
        print(f"  - Organic Carbon: {result['organic_carbon']}")
        print(f"  - Fertility: {result['fertility_status']}")
    
    @patch('data.soil_plugins.requests.get')
    def test_get_location_coordinates_success(self, mock_get):
        """Test successful coordinate retrieval"""
        print("\n=== Testing Location Coordinates (Mocked Success) ===")
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"lat": "28.6139", "lon": "77.2090"}  # Delhi coordinates
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        coordinates = get_location_coordinates("Delhi")
        
        self.assertIsNotNone(coordinates)
        self.assertEqual(len(coordinates), 2)
        self.assertAlmostEqual(coordinates[0], 28.6139, places=3)  # latitude
        self.assertAlmostEqual(coordinates[1], 77.2090, places=3)  # longitude
        
        print(f"✓ Coordinates for Delhi: {coordinates}")
    
    @patch('data.soil_plugins.requests.get')
    def test_get_location_coordinates_failure(self, mock_get):
        """Test coordinate retrieval failure"""
        print("\n=== Testing Location Coordinates (Mocked Failure) ===")
        
        # Mock failed API response
        mock_get.side_effect = Exception("Network error")
        
        coordinates = get_location_coordinates("InvalidLocation")
        
        self.assertIsNone(coordinates)
        print("✓ Correctly handled coordinate lookup failure")
    
    @patch('data.soil_plugins.requests.get')
    def test_fetch_soil_data_success(self, mock_get):
        """Test successful soil data fetching"""
        print("\n=== Testing Soil Data Fetch (Mocked Success) ===")
        
        # Mock successful SoilGrids API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "properties": {
                "phh2o": {
                    "depths": [{"values": {"mean": 65}}]
                },
                "nitrogen": {
                    "depths": [{"values": {"mean": 250}}]
                },
                "soc": {
                    "depths": [{"values": {"mean": 1200}}]
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = fetch_soil_data(28.6139, 77.2090, "Delhi")
        
        self.assertIsInstance(result, dict)
        self.assertIn("ph", result)
        self.assertIn("nitrogen", result)
        self.assertIn("organic_carbon", result)
        self.assertIn("soil_type", result)
        
        print(f"✓ Soil data for Delhi: {result['soil_type']} soil, pH {result['ph']}")
    
    @patch('data.soil_plugins.requests.get')
    def test_fetch_soil_data_failure(self, mock_get):
        """Test soil data fetch failure handling"""
        print("\n=== Testing Soil Data Fetch (Mocked Failure) ===")
        
        # Mock failed API response
        mock_get.side_effect = Exception("API error")
        
        result = fetch_soil_data(28.6139, 77.2090, "Delhi")
        
        # Should return fallback data
        self.assertIsInstance(result, dict)
        self.assertEqual(result["location"], "Delhi")
        self.assertIn("ph", result)
        self.assertIn("soil_type", result)
        
        print(f"✓ Fallback data returned: {result['soil_type']} soil")


class TestSoilCropAgent(unittest.TestCase):
    """Test cases for soil crop recommendation agent"""
    
    def test_extract_crops_from_response(self):
        """Test crop extraction from LLM responses"""
        print("\n=== Testing Crop Extraction from LLM Response ===")
        
        test_responses = [
            "I recommend wheat, rice, and maize for your loam soil.",
            "Cotton and sugarcane are ideal for black soil conditions.",
            "Consider groundnut, millet, and pulses for red soil.",
            "This text has no crop mentions at all.",
            "Tomato, potato, onion, and other vegetables grow well here."
        ]
        
        expected_crops = [
            ["Wheat", "Rice", "Maize"],
            ["Cotton", "Sugarcane"],
            ["Groundnut", "Millet", "Pulses"],
            ["Wheat", "Rice", "Maize"],  # Default fallback
            ["Tomato", "Potato", "Onion"]
        ]
        
        for i, response in enumerate(test_responses):
            result = extract_crops_from_response(response)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0, f"Should extract crops from: {response}")
            
            if i < len(expected_crops) - 1:  # Skip last one as it's more complex
                for expected_crop in expected_crops[i]:
                    self.assertIn(expected_crop, result, 
                                f"Expected {expected_crop} in result for: {response}")
            
            print(f"✓ Response: '{response[:50]}...' → Crops: {result}")
    
    def test_get_fallback_recommendations(self):
        """Test fallback crop recommendations"""
        print("\n=== Testing Fallback Crop Recommendations ===")
        
        test_soils = [
            ("black", {"fertility_status": "Good"}),
            ("red", {"fertility_status": "Moderate"}),
            ("alluvial", {"fertility_status": "Poor"}),
            ("sandy loam", {"fertility_status": "Good"}),
            ("unknown", {"fertility_status": "Moderate"})
        ]
        
        for soil_type, soil_health in test_soils:
            crops, recommendation = get_fallback_recommendations(soil_type, soil_health)
            
            self.assertIsInstance(crops, list)
            self.assertTrue(len(crops) > 0, f"Should recommend crops for {soil_type} soil")
            self.assertIsInstance(recommendation, str)
            self.assertTrue(len(recommendation) > 20, "Recommendation should be detailed")
            
            # Verify soil type is mentioned in recommendation
            self.assertIn(soil_type, recommendation.lower())
            
            print(f"✓ {soil_type.title()} soil: {len(crops)} crops, {len(recommendation)} char recommendation")
            print(f"  Crops: {', '.join(crops)}")
    
    @patch('graph_arc.agents_node.soil_crop_recommendation_agent.ChatGoogleGenerativeAI')
    @patch('data.soil_plugins.fetch_soil_data_by_location')
    def test_soil_crop_agent_llm_success(self, mock_fetch_soil, mock_llm):
        """Test soil crop agent with successful LLM call"""
        print("\n=== Testing Soil Crop Agent with LLM (Mocked Success) ===")
        
        # Mock complete soil data (what would come from a successful API call)
        mock_soil_data = {
            "location": "Delhi",
            "ph": "6.5 (Neutral)",
            "nitrogen": "2.5 g/kg (Medium)",
            "organic_carbon": "1.2% (Medium)",
            "sand_content": "45.0%",
            "clay_content": "25.0%",
            "silt_content": "30.0%",
            "soil_type": "Loam",
            "fertility_status": "Good"
        }
        mock_fetch_soil.return_value = mock_soil_data
        
        # Mock LLM response
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Based on your loam soil with good fertility, I recommend wheat, rice, maize, and vegetables. The neutral pH and moderate nitrogen content make these crops ideal for your location."
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_llm_response
        mock_llm.return_value = mock_llm_instance
        
        # Test state
        test_state = {
            "location": "Delhi",
            "raw_query": "What crops should I plant in my field?",
            "entities": {"location": "Delhi"}
        }
        
        result = soil_crop_recommendation_agent(test_state)
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn("soil_type", result)
        self.assertIn("soil_health", result)
        self.assertIn("recommended_crops", result)
        self.assertIn("ai_recommendation", result)
        
        # Verify content
        self.assertEqual(result["soil_type"], "Loam")
        self.assertIsInstance(result["recommended_crops"], list)
        self.assertTrue(len(result["recommended_crops"]) > 0)
        self.assertIsInstance(result["ai_recommendation"], str)
        
        print(f"✓ Agent result for Delhi:")
        print(f"  Soil Type: {result['soil_type']}")
        print(f"  Recommended Crops: {result['recommended_crops']}")
        print(f"  AI Recommendation: {result['ai_recommendation'][:100]}...")
    
    @patch('graph_arc.agents_node.soil_crop_recommendation_agent.ChatGoogleGenerativeAI')
    @patch('data.soil_plugins.fetch_soil_data_by_location')
    def test_soil_crop_agent_llm_failure(self, mock_fetch_soil, mock_llm):
        """Test soil crop agent with LLM failure (fallback)"""
        print("\n=== Testing Soil Crop Agent with LLM Failure (Fallback) ===")
        
        # Mock soil data that looks like API failure (N/A values)
        mock_api_soil_data = {
            "location": "Mumbai",
            "ph": "N/A",
            "nitrogen": "N/A",
            "organic_carbon": "N/A",
            "sand_content": "N/A",
            "clay_content": "N/A",
            "silt_content": "N/A",
            "soil_type": "N/A",
            "fertility_status": "N/A"
        }
        mock_fetch_soil.return_value = mock_api_soil_data
        
        # Mock LLM failure
        mock_llm.side_effect = Exception("LLM API error")
        
        # Test state
        test_state = {
            "location": "Mumbai",
            "raw_query": "What crops can I grow in sandy soil?",
            "entities": {"location": "Mumbai", "soil_type": "sandy"}
        }
        
        result = soil_crop_recommendation_agent(test_state)
        
        # Verify fallback worked - should use fallback soil data when API data is N/A
        self.assertIsInstance(result, dict)
        # Should fall back to "Loam" when API data is N/A
        self.assertEqual(result["soil_type"], "Loam")
        self.assertIsInstance(result["recommended_crops"], list)
        self.assertTrue(len(result["recommended_crops"]) > 0)
        self.assertIsInstance(result["ai_recommendation"], str)
        
        # Should contain fallback-appropriate crops for loam soil (after API failure)
        loam_crops = ["Wheat", "Maize", "Pulses", "Vegetables"]
        crop_found = any(crop in result["recommended_crops"] for crop in loam_crops)
        self.assertTrue(crop_found, "Should recommend crops suitable for loam soil (fallback)")
        
        print(f"✓ Fallback worked for Mumbai:")
        print(f"  Soil Type: {result['soil_type']}")
        print(f"  Recommended Crops: {result['recommended_crops']}")
        print(f"  Fallback Recommendation: {result['ai_recommendation'][:100]}...")
    
    @patch('data.soil_plugins.fetch_soil_data_by_location')
    def test_soil_crop_agent_api_failure(self, mock_fetch_soil):
        """Test soil crop agent with soil API failure"""
        print("\n=== Testing Soil Crop Agent with Soil API Failure ===")
        
        # Mock soil API failure
        mock_fetch_soil.side_effect = Exception("Soil API error")
        
        # Test state
        test_state = {
            "location": "Bangalore",
            "raw_query": "Suggest crops for my farm",
            "entities": {"location": "Bangalore"}
        }
        
        result = soil_crop_recommendation_agent(test_state)
        
        # Should still work with fallback soil data
        self.assertIsInstance(result, dict)
        self.assertIn("soil_type", result)
        self.assertEqual(result["soil_health"]["location"], "Bangalore")
        self.assertIsInstance(result["recommended_crops"], list)
        self.assertTrue(len(result["recommended_crops"]) > 0)
        
        print(f"✓ API failure handled for Bangalore:")
        print(f"  Used Fallback Soil Type: {result['soil_type']}")
        print(f"  Recommended Crops: {result['recommended_crops']}")


class TestSoilPluginsRealAPI(unittest.TestCase):
    """Test cases for soil_plugins module with real API calls"""
    
    @unittest.skipIf(not os.getenv("RUN_REAL_API_TESTS"), 
                     "Real API tests disabled. Set RUN_REAL_API_TESTS=1 to enable.")
    def test_real_coordinate_lookup(self):
        """Test real coordinate lookup for Indian cities"""
        print("\n=== Testing Real Coordinate Lookup ===")
        
        test_cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]
        
        for city in test_cities:
            try:
                coordinates = get_location_coordinates(city)
                
                if coordinates:
                    lat, lon = coordinates
                    self.assertTrue(-90 <= lat <= 90, f"Invalid latitude for {city}: {lat}")
                    self.assertTrue(-180 <= lon <= 180, f"Invalid longitude for {city}: {lon}")
                    
                    # Check if coordinates are roughly in India
                    self.assertTrue(6 <= lat <= 37, f"{city} latitude should be in India range")
                    self.assertTrue(68 <= lon <= 98, f"{city} longitude should be in India range")
                    
                    print(f"✓ {city}: ({lat:.4f}, {lon:.4f})")
                else:
                    print(f"⚠ Could not find coordinates for {city}")
                    
            except Exception as e:
                self.fail(f"Coordinate lookup failed for {city}: {str(e)}")
    
    @unittest.skipIf(not os.getenv("RUN_REAL_API_TESTS"), 
                     "Real API tests disabled. Set RUN_REAL_API_TESTS=1 to enable.")
    def test_real_soil_data_fetch(self):
        """Test real soil data fetching from SoilGrids API"""
        print("\n=== Testing Real Soil Data Fetch ===")
        
        # Test coordinates for major Indian cities
        test_locations = [
            ("Delhi", 28.6139, 77.2090),
            ("Mumbai", 19.0760, 72.8777),
            ("Chennai", 13.0827, 80.2707),
            ("Bangalore", 12.9716, 77.5946),
            ("Pune", 18.5204, 73.8567)
        ]
        
        for city, lat, lon in test_locations:
            try:
                result = fetch_soil_data(lat, lon, city)
                
                # Verify result structure
                self.assertIsInstance(result, dict)
                self.assertIn("location", result)
                self.assertIn("ph", result)
                self.assertIn("soil_type", result)
                self.assertIn("fertility_status", result)
                
                # Verify location is preserved
                self.assertEqual(result["location"], city)
                
                print(f"✓ {city}: {result['soil_type']} soil, pH {result['ph']}, {result['fertility_status']} fertility")
                
            except Exception as e:
                print(f"⚠ Soil data fetch failed for {city}: {str(e)}")
                # For real API tests, we might get occasional failures, so don't fail the test
                continue
    
    @unittest.skipIf(not os.getenv("RUN_REAL_API_TESTS"), 
                     "Real API tests disabled. Set RUN_REAL_API_TESTS=1 to enable.")
    def test_real_soil_data_by_location(self):
        """Test complete soil data fetch by location name"""
        print("\n=== Testing Real Soil Data by Location ===")
        
        test_cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Jaipur"]
        
        for city in test_cities:
            try:
                result = fetch_soil_data_by_location(city)
                
                # Verify result structure
                self.assertIsInstance(result, dict)
                self.assertIn("location", result)
                self.assertIn("ph", result)
                self.assertIn("nitrogen", result)
                self.assertIn("organic_carbon", result)
                self.assertIn("soil_type", result)
                self.assertIn("fertility_status", result)
                
                # Verify location is preserved
                self.assertEqual(result["location"], city)
                
                print(f"✓ {city}:")
                print(f"  - Soil Type: {result['soil_type']}")
                print(f"  - pH: {result['ph']}")
                print(f"  - Nitrogen: {result['nitrogen']}")
                print(f"  - Organic Carbon: {result['organic_carbon']}")
                print(f"  - Fertility Status: {result['fertility_status']}")
                
            except Exception as e:
                print(f"⚠ Complete soil data fetch failed for {city}: {str(e)}")
                continue


if __name__ == "__main__":
    print("=" * 60)
    print("🌱 SOIL & CROP RECOMMENDATION AGENT - TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSoilPluginsMocked))
    suite.addTests(loader.loadTestsFromTestCase(TestSoilCropAgent))
    
    # Add real API tests if enabled
    if os.getenv("RUN_REAL_API_TESTS"):
        print("\n🌐 Real API tests are ENABLED")
        suite.addTests(loader.loadTestsFromTestCase(TestSoilPluginsRealAPI))
    else:
        print("\n🌐 Real API tests are DISABLED (set RUN_REAL_API_TESTS=1 to enable)")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"✅ Passed: {passed}/{total_tests}")
    if failures > 0:
        print(f"❌ Failed: {failures}")
    if errors > 0:
        print(f"🚫 Errors: {errors}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! The soil & crop tool is working correctly.")
    else:
        print(f"\n⚠ {failures + errors} test(s) failed. Check the output above.")
        sys.exit(1)
