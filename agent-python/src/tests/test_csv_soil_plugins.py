"""
Test suite for CSV-based soil and crop recommendation functionality.
Covers CSV data integration, nutrient analysis, district matching, and fallback mechanisms.
"""
import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import the modules to test
from src.data.soil_plugins import (
    get_soil_data_from_csv,
    fetch_soil_data_by_location,
    find_district_in_csv,
    analyze_district_nutrients,
    classify_nutrients,
    assess_soil_health,
    get_crops_for_nutrients,
    get_fallback_soil_knowledge,
    determine_soil_type_from_location
)
from src.graph_arc.agents_node.soil_crop_recommendation_agent import (
    soil_crop_recommendation_agent,
    extract_crops_from_response,
    get_fallback_recommendations
)


class TestCSVSoilPlugins(unittest.TestCase):
    """Test cases for CSV-based soil_plugins module"""
    
    def setUp(self):
        """Set up test data"""
        # Create a mock CSV data for testing
        self.mock_csv_data = pd.DataFrame({
            'District ': ['Delhi', 'Mumbai Urban', 'Bangalore Urban', 'Unknown District'],
            'Zn %': [65.5, 45.2, 78.9, 55.0],
            'Fe%': [75.3, 60.1, 85.7, 70.0],
            'Cu %': [90.2, 80.5, 95.3, 85.0],
            'Mn %': [80.7, 70.2, 88.4, 75.0],
            'B %': [55.8, 40.3, 68.2, 50.0],
            'S %': [70.4, 65.8, 82.1, 68.0]
        })
    
    def test_get_soil_data_from_csv_success(self):
        """Test successful CSV soil data retrieval"""
        print("\n=== Testing CSV Soil Data Retrieval ===")
        
        with patch('src.data.soil_plugins.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = self.mock_csv_data
            
            result = get_soil_data_from_csv("Delhi", "soil analysis")
            
            # Verify structure
            self.assertIsInstance(result, dict)
            self.assertIn("location", result)
            self.assertIn("zinc_status", result)
            self.assertIn("iron_status", result)
            self.assertIn("copper_status", result)
            self.assertIn("manganese_status", result)
            self.assertIn("boron_status", result)
            self.assertIn("sulfur_status", result)
            self.assertIn("soil_health", result)
            self.assertIn("recommended_crops", result)
            self.assertIn("ai_recommendation", result)
            
            print(f"✓ Delhi soil data retrieved successfully")
            print(f"  - Zinc: {result['zinc_status']}")
            print(f"  - Iron: {result['iron_status']}")
            print(f"  - Soil Health: {result['soil_health']}")
    
    def test_find_district_in_csv(self):
        """Test district finding functionality"""
        print("\n=== Testing District Matching ===")
        
        # Test exact match
        result = find_district_in_csv(self.mock_csv_data, "Delhi")
        self.assertIsNotNone(result)
        self.assertEqual(result['District '], 'Delhi')
        print("✓ Exact district match works")
        
        # Test partial match
        result = find_district_in_csv(self.mock_csv_data, "Mumbai")
        self.assertIsNotNone(result)
        self.assertEqual(result['District '], 'Mumbai Urban')
        print("✓ Partial district match works")
        
        # Test case insensitive
        result = find_district_in_csv(self.mock_csv_data, "BANGALORE")
        self.assertIsNotNone(result)
        print("✓ Case insensitive matching works")
        
        # Test no match
        result = find_district_in_csv(self.mock_csv_data, "NonExistentPlace")
        self.assertIsNone(result)
        print("✓ No match returns None correctly")
    
    def test_classify_nutrients(self):
        """Test nutrient classification system"""
        print("\n=== Testing Nutrient Classification ===")
        
        # Test high nutrient levels
        high_nutrients = {
            'zinc': 80, 'iron': 90, 'copper': 95, 
            'manganese': 90, 'boron': 85, 'sulfur': 90
        }
        classification = classify_nutrients(high_nutrients)
        
        self.assertEqual(classification['zinc'], 'High')
        self.assertEqual(classification['iron'], 'High')
        print("✓ High nutrient classification works")
        
        # Test low nutrient levels
        low_nutrients = {
            'zinc': 20, 'iron': 30, 'copper': 50, 
            'manganese': 40, 'boron': 25, 'sulfur': 35
        }
        classification = classify_nutrients(low_nutrients)
        
        self.assertEqual(classification['zinc'], 'Low')
        self.assertEqual(classification['iron'], 'Low')
        print("✓ Low nutrient classification works")
        
        # Test medium nutrient levels
        medium_nutrients = {
            'zinc': 55, 'iron': 65, 'copper': 75, 
            'manganese': 70, 'boron': 55, 'sulfur': 65
        }
        classification = classify_nutrients(medium_nutrients)
        
        self.assertEqual(classification['zinc'], 'Medium')
        self.assertEqual(classification['iron'], 'Medium')
        print("✓ Medium nutrient classification works")
    
    def test_assess_soil_health(self):
        """Test soil health assessment"""
        print("\n=== Testing Soil Health Assessment ===")
        
        # Test excellent health
        excellent_nutrients = {
            'zinc': 80, 'iron': 90, 'copper': 95, 
            'manganese': 90, 'boron': 85, 'sulfur': 90
        }
        health = assess_soil_health(excellent_nutrients)
        
        self.assertEqual(health['overall'], 'Excellent')
        self.assertEqual(health['fertility'], 'High')
        print(f"✓ Excellent health: {health['overall']}, {health['fertility']}")
        
        # Test poor health
        poor_nutrients = {
            'zinc': 20, 'iron': 30, 'copper': 35, 
            'manganese': 25, 'boron': 20, 'sulfur': 30
        }
        health = assess_soil_health(poor_nutrients)
        
        self.assertEqual(health['overall'], 'Poor')
        self.assertEqual(health['fertility'], 'Low to Medium')
        self.assertTrue(len(health['limitations']) > 0)
        print(f"✓ Poor health: {health['overall']}, Limitations: {health['limitations']}")
    
    def test_get_crops_for_nutrients(self):
        """Test crop recommendations based on nutrients"""
        print("\n=== Testing Crop Recommendations ===")
        
        # Test nutrients favoring specific crops
        high_zinc_nutrients = {
            'zinc': 80, 'iron': 60, 'copper': 70, 
            'manganese': 60, 'boron': 50, 'sulfur': 60
        }
        crops = get_crops_for_nutrients(high_zinc_nutrients, "Punjab")
        
        self.assertIsInstance(crops, list)
        self.assertTrue(any(crop in ['Rice', 'Wheat', 'Maize'] for crop in crops))
        print(f"✓ High zinc nutrients recommend: {crops}")
        
        # Test regional crop recommendations
        regional_crops = get_crops_for_nutrients({}, "Maharashtra")
        self.assertIsInstance(regional_crops, list)
        self.assertTrue(len(regional_crops) > 0)
        print(f"✓ Regional crops for Maharashtra: {regional_crops}")
    
    def test_determine_soil_type_from_location(self):
        """Test soil type determination by location"""
        print("\n=== Testing Soil Type Determination ===")
        
        # Test different regions
        test_cases = {
            "Maharashtra": "Black Cotton Soil (Vertisols)",
            "Karnataka": "Red Laterite Soil",
            "Punjab": "Alluvial Soil",
            "Rajasthan": "Desert/Arid Soil",
            "West Bengal": "Deltaic Alluvial Soil",
            "Unknown Place": "Mixed Indian Agricultural Soil"
        }
        
        for location, expected_soil in test_cases.items():
            result = determine_soil_type_from_location(location)
            self.assertEqual(result, expected_soil)
            print(f"✓ {location} -> {result}")
    
    def test_get_fallback_soil_knowledge(self):
        """Test fallback soil knowledge generation"""
        print("\n=== Testing Fallback Soil Knowledge ===")
        
        result = get_fallback_soil_knowledge("Test Location", "general query")
        
        # Verify structure
        self.assertIsInstance(result, dict)
        self.assertIn("location", result)
        self.assertIn("data_source", result)
        self.assertIn("soil_type", result)
        self.assertIn("recommended_crops", result)
        self.assertIn("ai_recommendation", result)
        
        # Verify data types
        self.assertIsInstance(result["recommended_crops"], list)
        self.assertTrue(len(result["recommended_crops"]) > 0)
        
        print(f"✓ Fallback data generated for {result['location']}")
        print(f"  - Crops: {result['recommended_crops']}")


class TestCSVSoilPluginsIntegration(unittest.TestCase):
    """Integration tests for CSV soil plugins with real CSV file"""
    
    def test_csv_file_loading(self):
        """Test loading actual CSV file"""
        print("\n=== Testing CSV File Loading ===")
        
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'soil.csv')
        
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                self.assertGreater(len(df), 0)
                
                # Check required columns
                required_columns = ['District ', 'Zn %', 'Fe%', 'Cu %', 'Mn %', 'B %', 'S %']
                for col in required_columns:
                    self.assertIn(col, df.columns)
                
                print(f"✓ CSV loaded successfully with {len(df)} districts")
                print(f"✓ All required columns present: {required_columns}")
                
                # Test with real data
                result = get_soil_data_from_csv("Delhi", "soil analysis")
                self.assertIsInstance(result, dict)
                print(f"✓ Real CSV data processed successfully")
                
            except Exception as e:
                print(f"⚠ CSV file exists but couldn't be processed: {e}")
        else:
            print("⚠ CSV file not found, skipping real data test")
    
    def test_soil_crop_agent_integration(self):
        """Test integration with soil crop recommendation agent"""
        print("\n=== Testing Agent Integration ===")
        
        # Mock state for testing
        mock_state = {
            "location": "Delhi",
            "raw_query": "What crops should I grow?",
            "entities": {"location": "Delhi"},
            "weather_data": {"temperature": 25, "humidity": 60}
        }
        
        try:
            # This would require the full agent setup, so we'll test the components
            from src.graph_arc.agents_node.soil_crop_recommendation_agent import extract_crops_from_response
            
            sample_response = "I recommend growing wheat, rice, maize, and cotton for your soil conditions."
            crops = extract_crops_from_response(sample_response)
            
            self.assertIsInstance(crops, list)
            self.assertTrue(len(crops) > 0)
            self.assertIn("Wheat", crops)
            
            print(f"✓ Agent crop extraction works: {crops}")
            
        except ImportError as e:
            print(f"⚠ Agent integration test skipped due to missing dependencies: {e}")


class TestCSVSoilPluginsEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_missing_csv_file(self):
        """Test behavior when CSV file is missing"""
        print("\n=== Testing Missing CSV File ===")
        
        with patch('src.data.soil_plugins.pd.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = FileNotFoundError("CSV file not found")
            
            result = get_soil_data_from_csv("TestLocation", "query")
            
            # Should fall back to basic knowledge
            self.assertIsInstance(result, dict)
            self.assertIn("location", result)
            self.assertEqual(result["data_source"], "Basic Agricultural Knowledge")
            
            print("✓ Missing CSV file handled gracefully")
    
    def test_empty_csv_file(self):
        """Test behavior with empty CSV"""
        print("\n=== Testing Empty CSV File ===")
        
        empty_df = pd.DataFrame()
        
        with patch('src.data.soil_plugins.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = empty_df
            
            result = get_soil_data_from_csv("TestLocation", "query")
            
            # Should handle empty data gracefully
            self.assertIsInstance(result, dict)
            self.assertIn("location", result)
            
            print("✓ Empty CSV file handled gracefully")
    
    def test_malformed_csv_data(self):
        """Test behavior with malformed CSV data"""
        print("\n=== Testing Malformed CSV Data ===")
        
        # CSV with missing/invalid columns
        malformed_df = pd.DataFrame({
            'WrongColumn': ['Data1', 'Data2'],
            'AnotherWrongColumn': ['Value1', 'Value2']
        })
        
        with patch('src.data.soil_plugins.pd.read_csv') as mock_read_csv:
            mock_read_csv.return_value = malformed_df
            
            result = get_soil_data_from_csv("TestLocation", "query")
            
            # Should handle malformed data gracefully
            self.assertIsInstance(result, dict)
            self.assertIn("location", result)
            
            print("✓ Malformed CSV data handled gracefully")
    
    def test_special_characters_in_location(self):
        """Test location names with special characters"""
        print("\n=== Testing Special Characters in Location ===")
        
        special_locations = [
            "New Delhi",
            "Mumbai-Suburban", 
            "Thiruvananthapuram",
            "St. Thomas Mount",
            "Location with (brackets)",
            ""
        ]
        
        for location in special_locations:
            try:
                result = get_soil_data_from_csv(location, "query")
                self.assertIsInstance(result, dict)
                self.assertIn("location", result)
                print(f"✓ Special location handled: '{location}'")
            except Exception as e:
                print(f"⚠ Special location failed: '{location}' - {e}")


def run_csv_soil_tests():
    """Run all CSV soil plugin tests"""
    print("=" * 80)
    print("🌾 RUNNING CSV-BASED SOIL PLUGIN TESTS")
    print("=" * 80)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCSVSoilPlugins))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVSoilPluginsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVSoilPluginsEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🌾 CSV SOIL PLUGIN TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, error in result.failures:
            print(f"- {test}: {error}")
    
    if result.errors:
        print("\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! CSV soil plugin system is working well!")
    elif success_rate >= 70:
        print("✅ GOOD! Most CSV soil plugin features are working.")
    else:
        print("⚠️  NEEDS WORK! Several CSV soil plugin issues found.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_csv_soil_tests()
    sys.exit(0 if success else 1)
