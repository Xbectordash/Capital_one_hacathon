import unittest
import requests
import os
from data.weather_plugins import fetch_weather_data
from config.settings import WEATHER_API
from graph_arc.agents_node.weather_agent import weather_agent
from graph_arc.state import GlobalState


class TestWeatherPluginsRealAPI(unittest.TestCase):
    """Test cases for weather_plugins module with real API calls"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_locations = [
            "Delhi",
            "Bangalore", 
            "Mumbai",
            "Karnataka",
            "Punjab",
            "Chennai",
            "Kolkata"
        ]
        
        # Skip tests if API key is not available
        if not WEATHER_API:
            self.skipTest("WEATHER_API key is not set in environment variables")

    def test_api_response_status_code_for_locations(self):
        """Test API response status code 200 for different locations"""
        print("\n=== Testing API Status Codes for Different Locations ===")
        
        for location in self.test_locations:
            with self.subTest(location=location):
                print(f"\n📍 Testing location: {location}")
                
                # Construct API URL
                url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API}&units=metric"
                
                try:
                    # Make direct API call
                    response = requests.get(url, timeout=10)
                    
                    print(f"   Status Code: {response.status_code}")
                    
                    # Check status code
                    self.assertEqual(response.status_code, 200, 
                                   f"Expected status code 200 for {location}, got {response.status_code}")
                    
                    # Parse response
                    data = response.json()
                    
                    # Verify essential fields are present
                    self.assertIn('main', data, f"'main' field missing in response for {location}")
                    self.assertIn('weather', data, f"'weather' field missing in response for {location}")
                    self.assertIn('name', data, f"'name' field missing in response for {location}")
                    
                    print(f"   ✅ City Name: {data.get('name', 'N/A')}")
                    print(f"   ✅ Temperature: {data['main'].get('temp', 'N/A')}°C")
                    print(f"   ✅ Condition: {data['weather'][0].get('main', 'N/A')}")
                    print(f"   ✅ Humidity: {data['main'].get('humidity', 'N/A')}%")
                    
                except requests.exceptions.Timeout:
                    self.fail(f"API request timed out for location: {location}")
                except requests.exceptions.RequestException as e:
                    self.fail(f"API request failed for location {location}: {str(e)}")
                except Exception as e:
                    self.fail(f"Unexpected error for location {location}: {str(e)}")

    def test_fetch_weather_data_function_with_real_locations(self):
        """Test the fetch_weather_data function with real locations"""
        print("\n=== Testing fetch_weather_data Function ===")
        
        for location in self.test_locations[:3]:  # Test first 3 locations to avoid too many API calls
            with self.subTest(location=location):
                print(f"\n📍 Testing fetch_weather_data for: {location}")
                
                try:
                    # Use the actual function
                    forecast = fetch_weather_data(location)
                    
                    # Verify the returned forecast structure
                    required_keys = ['temperature', 'condition', 'humidity', 'wind_speed', 'precipitation']
                    
                    for key in required_keys:
                        self.assertIn(key, forecast, f"Missing key '{key}' in forecast for {location}")
                        self.assertIsNotNone(forecast[key], f"Key '{key}' is None for {location}")
                    
                    print(f"   ✅ Temperature: {forecast['temperature']}")
                    print(f"   ✅ Condition: {forecast['condition']}")
                    print(f"   ✅ Humidity: {forecast['humidity']}")
                    print(f"   ✅ Wind Speed: {forecast['wind_speed']}")
                    print(f"   ✅ Precipitation: {forecast['precipitation']}")
                    
                except ValueError as e:
                    self.fail(f"fetch_weather_data failed for {location}: {str(e)}")
                except Exception as e:
                    self.fail(f"Unexpected error in fetch_weather_data for {location}: {str(e)}")

    def test_api_response_for_invalid_location(self):
        """Test API response for invalid location"""
        print("\n=== Testing Invalid Location ===")
        
        invalid_location = "InvalidCityName12345"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={invalid_location}&appid={WEATHER_API}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status Code for invalid location: {response.status_code}")
            
            # For invalid locations, API typically returns 404
            self.assertEqual(response.status_code, 404, 
                           f"Expected status code 404 for invalid location, got {response.status_code}")
            
            print(f"   ✅ Correctly returned 404 for invalid location")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"API request failed for invalid location: {str(e)}")

    def test_api_key_authentication(self):
        """Test API key authentication"""
        print("\n=== Testing API Key Authentication ===")
        
        # Test with valid API key
        url_valid = f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={WEATHER_API}&units=metric"
        
        try:
            response_valid = requests.get(url_valid, timeout=10)
            print(f"   Status Code with valid API key: {response_valid.status_code}")
            self.assertEqual(response_valid.status_code, 200)
            print(f"   ✅ Valid API key works correctly")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"API request failed with valid key: {str(e)}")
        
        # Test with invalid API key
        url_invalid = f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=invalid_key&units=metric"
        
        try:
            response_invalid = requests.get(url_invalid, timeout=10)
            print(f"   Status Code with invalid API key: {response_invalid.status_code}")
            self.assertEqual(response_invalid.status_code, 401)
            print(f"   ✅ Invalid API key correctly rejected")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"API request failed with invalid key: {str(e)}")

    def test_weather_agent_llm_recommendations(self):
        """Test weather agent LLM recommendations for different weather conditions"""
        print("\n=== Testing Weather Agent LLM Recommendations ===")
        
        # Test different weather scenarios
        test_scenarios = [
            {
                "location": "Delhi",
                "query": "Should I spray pesticides on my wheat crop today?",
                "expected_keywords": ["spray", "pesticide", "wind", "weather"]
            },
            {
                "location": "Bangalore", 
                "query": "When should I irrigate my tomato plants?",
                "expected_keywords": ["irrigat", "water", "temperature", "humidity"]
            },
            {
                "location": "Punjab",
                "query": "Is it a good day for harvesting wheat?",
                "expected_keywords": ["harvest", "temperature", "humidity", "field"]
            }
        ]
        
        for scenario in test_scenarios:
            with self.subTest(location=scenario["location"]):
                print(f"\n📍 Testing weather agent for: {scenario['location']}")
                print(f"   Query: {scenario['query']}")
                
                try:
                    # Create test state
                    test_state = {
                        "location": scenario["location"],
                        "raw_query": scenario["query"],
                        "entities": {"location": scenario["location"]}
                    }
                    
                    # Call weather agent
                    result = weather_agent(test_state)
                    
                    # Verify the result structure
                    self.assertIsInstance(result, dict, f"Result should be a dictionary for {scenario['location']}")
                    self.assertIn('forecast', result, f"Missing 'forecast' in result for {scenario['location']}")
                    self.assertIn('recommendation', result, f"Missing 'recommendation' in result for {scenario['location']}")
                    self.assertIn('date_range', result, f"Missing 'date_range' in result for {scenario['location']}")
                    
                    # Verify forecast structure
                    forecast = result['forecast']
                    required_forecast_keys = ['temperature', 'condition', 'humidity', 'wind_speed', 'precipitation']
                    for key in required_forecast_keys:
                        self.assertIn(key, forecast, f"Missing '{key}' in forecast for {scenario['location']}")
                    
                    # Check recommendation quality
                    recommendation = result['recommendation']
                    self.assertIsInstance(recommendation, str, f"Recommendation should be string for {scenario['location']}")
                    self.assertTrue(len(recommendation) > 20, f"Recommendation too short for {scenario['location']}: {recommendation}")
                    
                    print(f"   ✅ Forecast: {forecast['temperature']}, {forecast['condition']}")
                    print(f"   ✅ LLM Recommendation: {recommendation}")
                    
                    # Check if recommendation contains relevant keywords
                    recommendation_lower = recommendation.lower()
                    relevant_keywords_found = sum(1 for keyword in scenario["expected_keywords"] 
                                                if keyword.lower() in recommendation_lower)
                    
                    print(f"   ✅ Relevant keywords found: {relevant_keywords_found}/{len(scenario['expected_keywords'])}")
                    
                    # Verify recommendation is contextual (contains at least one relevant keyword)
                    self.assertGreater(relevant_keywords_found, 0, 
                                     f"Recommendation should contain relevant agricultural keywords for {scenario['location']}")
                    
                except Exception as e:
                    self.fail(f"Weather agent failed for {scenario['location']}: {str(e)}")

    def test_weather_agent_error_handling(self):
        """Test weather agent error handling with invalid location"""
        print("\n=== Testing Weather Agent Error Handling ===")
        
        test_state = {
            "location": "InvalidCity12345",
            "raw_query": "What's the weather like?",
            "entities": {"location": "InvalidCity12345"}
        }
        
        try:
            result = weather_agent(test_state)
            
            # Should still return a result with N/A values
            self.assertIn('forecast', result)
            self.assertIn('recommendation', result)
            
            forecast = result['forecast']
            # Check if fallback values are used
            self.assertTrue(any(value == "N/A" for value in forecast.values()), 
                          "Should have N/A values for invalid location")
            
            print(f"   ✅ Error handled gracefully with fallback recommendation")
            print(f"   ✅ Fallback forecast: {forecast}")
            
        except Exception as e:
            self.fail(f"Weather agent should handle errors gracefully: {str(e)}")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
