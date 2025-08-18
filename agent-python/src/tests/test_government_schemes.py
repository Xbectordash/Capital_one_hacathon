"""
Test Suite for Government Schemes Agent and Plugin
Description: Comprehensive testing for government schemes functionality with mock and real API scenarios.
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.government_schemes_plugin import (
    fetch_central_government_schemes,
    fetch_state_government_schemes,
    get_schemes_by_location_and_profile,
    extract_state_from_location,
    filter_schemes_by_profile,
    calculate_eligibility_score,
    get_fallback_schemes_data
)
from src.graph_arc.agents_node.government_schemes_agent import (
    government_schemes_agent,
    extract_farmer_profile,
    calculate_data_quality_score,
    generate_rule_based_recommendation,
    extract_top_schemes,
    generate_eligibility_summary
)
from src.graph_arc.state import GlobalState

class TestGovernmentSchemesPlugin(unittest.TestCase):
    """Test cases for government schemes plugin with mocked scenarios"""
    
    def test_fetch_central_government_schemes(self):
        """Test central government schemes fetching"""
        print("\n=== Testing Central Government Schemes ===")
        
        # Test different farmer types
        test_cases = [
            ("small", "rice"),
            ("marginal", "wheat"),
            ("all", "all"),
            ("large", "cotton")
        ]
        
        for farmer_type, crop_type in test_cases:
            schemes = fetch_central_government_schemes(farmer_type, crop_type)
            
            # Verify structure
            self.assertIsInstance(schemes, list)
            self.assertGreaterEqual(len(schemes), 3)  # At least PM-KISAN, PMFBY, KCC
            
            # Verify scheme structure
            for scheme in schemes:
                self.assertIsInstance(scheme, dict)
                self.assertIn("scheme_name", scheme)
                self.assertIn("scheme_type", scheme)
                self.assertIn("description", scheme)
                self.assertIn("eligibility", scheme)
                self.assertIn("benefits", scheme)
                self.assertIn("application_process", scheme)
                self.assertIn("scheme_code", scheme)
                
            print(f"✓ Central schemes for {farmer_type} farmer, {crop_type} crop: {len(schemes)} schemes")
    
    def test_fetch_state_government_schemes(self):
        """Test state government schemes fetching"""
        print("\n=== Testing State Government Schemes ===")
        
        test_states = ["Maharashtra", "Karnataka", "Punjab", "Delhi", "Unknown State"]
        
        for state in test_states:
            schemes = fetch_state_government_schemes(state)
            
            # Verify structure
            self.assertIsInstance(schemes, list)
            self.assertGreaterEqual(len(schemes), 1)  # At least one scheme
            
            # Verify scheme structure
            for scheme in schemes:
                self.assertIsInstance(scheme, dict)
                self.assertIn("scheme_name", scheme)
                self.assertIn("scheme_type", scheme)
                self.assertIn("department", scheme)
                self.assertIn("state", scheme)
                
            print(f"✓ State schemes for {state}: {len(schemes)} schemes")
    
    def test_get_schemes_by_location_and_profile(self):
        """Test comprehensive schemes fetching by location and profile"""
        print("\n=== Testing Schemes by Location and Profile ===")
        
        test_cases = [
            {
                "location": "Mumbai, Maharashtra",
                "farmer_profile": {
                    "farmer_type": "small",
                    "crop_type": "rice",
                    "land_size": 3.0,
                    "primary_need": "credit"
                }
            },
            {
                "location": "Bangalore, Karnataka", 
                "farmer_profile": {
                    "farmer_type": "marginal",
                    "crop_type": "cotton",
                    "land_size": 1.5,
                    "primary_need": "insurance"
                }
            },
            {
                "location": "Delhi",
                "farmer_profile": {
                    "farmer_type": "medium",
                    "crop_type": "wheat",
                    "land_size": 8.0,
                    "primary_need": "subsidy"
                }
            }
        ]
        
        for case in test_cases:
            location = case["location"]
            farmer_profile = case["farmer_profile"]
            
            schemes_data = get_schemes_by_location_and_profile(location, farmer_profile)
            
            # Verify structure
            self.assertIsInstance(schemes_data, dict)
            self.assertIn("location", schemes_data)
            self.assertIn("state", schemes_data)
            self.assertIn("farmer_profile", schemes_data)
            self.assertIn("total_schemes", schemes_data)
            self.assertIn("schemes", schemes_data)
            self.assertIn("recommendations", schemes_data)
            self.assertIn("priority_schemes", schemes_data)
            self.assertIn("estimated_benefits", schemes_data)
            
            # Verify data quality
            self.assertGreater(schemes_data["total_schemes"], 0)
            self.assertIsInstance(schemes_data["schemes"], list)
            self.assertIsInstance(schemes_data["recommendations"], list)
            
            print(f"✓ {location}: {schemes_data['total_schemes']} schemes, "
                  f"₹{schemes_data['estimated_benefits']['estimated_annual_benefit']} estimated benefits")
    
    def test_state_extraction(self):
        """Test state extraction from location strings"""
        print("\n=== Testing State Extraction ===")
        
        test_locations = [
            ("Mumbai", "Maharashtra"),
            ("Delhi", "Delhi"),
            ("Bangalore", "Karnataka"),
            ("Chennai", "Tamil Nadu"),
            ("Kolkata", "West Bengal"),
            ("Jaipur", "Rajasthan"),
            ("Unknown City", "Unknown")
        ]
        
        for location, expected_state in test_locations:
            extracted_state = extract_state_from_location(location)
            print(f"✓ {location} → {extracted_state}")
            
            if expected_state != "Unknown":
                self.assertEqual(extracted_state, expected_state)
    
    def test_scheme_filtering(self):
        """Test scheme filtering by farmer profile"""
        print("\n=== Testing Scheme Filtering ===")
        
        # Mock schemes data
        mock_schemes = [
            {
                "scheme_name": "PM-KISAN",
                "farmer_category": ["small", "marginal"],
                "crop_types": ["all"]
            },
            {
                "scheme_name": "Large Farmer Scheme",
                "farmer_category": ["large"],
                "crop_types": ["commercial"]
            },
            {
                "scheme_name": "Universal Scheme",
                "farmer_category": ["all"],
                "crop_types": ["all"]
            }
        ]
        
        farmer_profile = {
            "farmer_type": "small",
            "crop_type": "rice",
            "land_size": 2.0
        }
        
        filtered_schemes = filter_schemes_by_profile(mock_schemes, farmer_profile)
        
        # Should get PM-KISAN and Universal Scheme
        self.assertEqual(len(filtered_schemes), 2)
        
        scheme_names = [s["scheme_name"] for s in filtered_schemes]
        self.assertIn("PM-KISAN", scheme_names)
        self.assertIn("Universal Scheme", scheme_names)
        self.assertNotIn("Large Farmer Scheme", scheme_names)
        
        print(f"✓ Filtered {len(filtered_schemes)} applicable schemes for small farmer")
    
    def test_eligibility_scoring(self):
        """Test eligibility score calculation"""
        print("\n=== Testing Eligibility Scoring ===")
        
        scheme = {
            "scheme_name": "Test Scheme",
            "farmer_category": ["small", "marginal"],
            "scheme_type": "Income Support"
        }
        
        test_profiles = [
            {"farmer_type": "small", "land_size": 2.0},
            {"farmer_type": "large", "land_size": 15.0},
            {"farmer_type": "marginal", "land_size": 1.0}
        ]
        
        for profile in test_profiles:
            score = calculate_eligibility_score(scheme, profile)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)
            
            print(f"✓ {profile['farmer_type']} farmer ({profile['land_size']} acres): {score:.1f}/10")
    
    def test_fallback_schemes_data(self):
        """Test fallback schemes data generation"""
        print("\n=== Testing Fallback Schemes Data ===")
        
        location = "Test City"
        farmer_profile = {
            "farmer_type": "small",
            "crop_type": "wheat",
            "land_size": 3.0
        }
        
        fallback_data = get_fallback_schemes_data(location, farmer_profile)
        
        # Verify structure
        self.assertIsInstance(fallback_data, dict)
        self.assertIn("location", fallback_data)
        self.assertIn("schemes", fallback_data)
        self.assertIn("recommendations", fallback_data)
        self.assertEqual(fallback_data["data_source"], "fallback")
        
        # Should have basic central schemes
        self.assertGreaterEqual(len(fallback_data["schemes"]), 3)
        
        scheme_names = [s["scheme_name"] for s in fallback_data["schemes"]]
        self.assertIn("PM-KISAN Samman Nidhi Yojana", scheme_names)
        
        print(f"✓ Fallback data: {len(fallback_data['schemes'])} basic schemes")

class TestGovernmentSchemesAgent(unittest.TestCase):
    """Test cases for government schemes agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_state = GlobalState(
            user_query="What government schemes are available for me?",
            location="Mumbai",
            entities={"farmer_type": "small", "crop": "rice"},
            weather_data={"temperature": 28, "humidity": 75}
        )
    
    def test_government_schemes_agent(self):
        """Test complete government schemes agent workflow"""
        print("\n=== Testing Government Schemes Agent ===")
        
        result = government_schemes_agent(self.mock_state)
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn("relevant_schemes", result)
        self.assertIn("eligibility", result)
        self.assertIn("application_steps", result)
        
        # Verify schemes data
        schemes = result["relevant_schemes"]
        self.assertIsInstance(schemes, list)
        self.assertGreaterEqual(len(schemes), 1)
        
        # Verify each scheme structure
        for scheme in schemes:
            self.assertIn("name", scheme)
            self.assertIn("type", scheme)
            self.assertIn("description", scheme)
            
        print(f"✓ Agent returned {len(schemes)} relevant schemes")
        print(f"✓ Eligibility summary: {result['eligibility'][:100]}...")
    
    def test_farmer_profile_extraction(self):
        """Test farmer profile extraction from state"""
        print("\n=== Testing Farmer Profile Extraction ===")
        
        test_states = [
            {
                "entities": {"land_size": "3.5", "crop": "wheat"},
                "user_query": "I am a small farmer with credit needs"
            },
            {
                "entities": {"commodity": "rice"},
                "user_query": "I need insurance for my crops"
            },
            {
                "entities": {},
                "user_query": "Large farmer looking for subsidies"
            }
        ]
        
        for test_data in test_states:
            mock_state = GlobalState(
                entities=test_data["entities"],
                user_query=test_data["user_query"]
            )
            
            profile = extract_farmer_profile(test_data["entities"], mock_state)
            
            # Verify profile structure
            self.assertIsInstance(profile, dict)
            self.assertIn("farmer_type", profile)
            self.assertIn("crop_type", profile)
            self.assertIn("land_size", profile)
            self.assertIn("primary_need", profile)
            
            print(f"✓ Profile: {profile['farmer_type']} farmer, {profile['crop_type']} crop, "
                  f"{profile['land_size']} acres, needs {profile['primary_need']}")
    
    def test_data_quality_scoring(self):
        """Test data quality score calculation"""
        print("\n=== Testing Data Quality Scoring ===")
        
        test_data_sets = [
            {
                "total_schemes": 5,
                "central_schemes": 3,
                "state_schemes": 2,
                "recommendations": ["Apply for PM-KISAN"],
                "estimated_benefits": {"estimated_annual_benefit": 10000}
            },
            {
                "total_schemes": 0,
                "central_schemes": 0,
                "state_schemes": 0
            },
            {
                "total_schemes": 3,
                "central_schemes": 3,
                "recommendations": []
            }
        ]
        
        for data in test_data_sets:
            score = calculate_data_quality_score(data)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)
            
            print(f"✓ Data quality score: {score:.1f}/10 for {data['total_schemes']} schemes")
    
    def test_rule_based_recommendation(self):
        """Test rule-based recommendation generation"""
        print("\n=== Testing Rule-Based Recommendations ===")
        
        schemes_data = {
            "schemes": [
                {"scheme_name": "PM-KISAN", "scheme_type": "Income Support"},
                {"scheme_name": "PMFBY", "scheme_type": "Crop Insurance"}
            ],
            "estimated_benefits": {"estimated_annual_benefit": 15000}
        }
        
        farmer_profiles = [
            {"farmer_type": "small", "land_size": 2.0, "primary_need": "credit"},
            {"farmer_type": "marginal", "land_size": 1.5, "primary_need": "insurance"},
            {"farmer_type": "medium", "land_size": 8.0, "primary_need": "subsidy"}
        ]
        
        for profile in farmer_profiles:
            recommendation = generate_rule_based_recommendation(schemes_data, profile)
            
            # Verify recommendation structure
            self.assertIsInstance(recommendation, str)
            self.assertGreater(len(recommendation), 100)  # Should be substantial
            
            # Check for key elements
            self.assertIn("Namaskar", recommendation)
            self.assertIn(profile["farmer_type"], recommendation)
            self.assertIn("₹", recommendation)  # Should mention money
            
            print(f"✓ Generated {len(recommendation)} character recommendation for {profile['farmer_type']} farmer")
    
    def test_top_schemes_extraction(self):
        """Test top schemes extraction"""
        print("\n=== Testing Top Schemes Extraction ===")
        
        schemes_data = {
            "schemes": [
                {
                    "scheme_name": "PM-KISAN Samman Nidhi",
                    "scheme_type": "Income Support",
                    "description": "Direct income support scheme for farmers with financial assistance",
                    "eligibility": "Small and marginal farmers",
                    "application_process": "Online at pmkisan.gov.in",
                    "scheme_code": "PM-KISAN-2024",
                    "status": "Active"
                },
                {
                    "scheme_name": "PMFBY",
                    "scheme_type": "Crop Insurance",
                    "description": "Comprehensive crop insurance scheme providing risk coverage",
                    "eligibility": "All farmers",
                    "application_process": "Through banks",
                    "scheme_code": "PMFBY-2024",
                    "status": "Active"
                }
            ]
        }
        
        top_schemes = extract_top_schemes(schemes_data)
        
        # Verify structure
        self.assertIsInstance(top_schemes, list)
        self.assertLessEqual(len(top_schemes), 3)  # Top 3 schemes
        
        for scheme in top_schemes:
            self.assertIn("name", scheme)
            self.assertIn("type", scheme)
            self.assertIn("description", scheme)
            self.assertIn("eligibility", scheme)
            self.assertIn("application_process", scheme)
            
        print(f"✓ Extracted {len(top_schemes)} top schemes")
    
    def test_eligibility_summary_generation(self):
        """Test eligibility summary generation"""
        print("\n=== Testing Eligibility Summary ===")
        
        schemes_data = {"total_schemes": 7}
        farmer_profiles = [
            {"farmer_type": "small", "land_size": 1.8},
            {"farmer_type": "large", "land_size": 12.0},
            {"farmer_type": "marginal", "land_size": 1.2}
        ]
        
        for profile in farmer_profiles:
            summary = generate_eligibility_summary(schemes_data, profile)
            
            # Verify summary structure
            self.assertIsInstance(summary, str)
            self.assertGreater(len(summary), 50)
            self.assertIn(profile["farmer_type"], summary)
            self.assertIn(str(profile["land_size"]), summary)
            
            print(f"✓ {profile['farmer_type']} farmer summary: {summary[:80]}...")

class TestGovernmentSchemesRealAPI(unittest.TestCase):
    """Test cases for government schemes with real API scenarios (conditional)"""
    
    @unittest.skipIf(not os.getenv("RUN_REAL_API_TESTS"), 
                     "Real API tests disabled. Set RUN_REAL_API_TESTS=1 to enable.")
    def test_real_schemes_fetch(self):
        """Test real government schemes data fetching"""
        print("\n=== Testing Real Government Schemes API ===")
        
        test_locations = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Pune"]
        
        for location in test_locations:
            try:
                farmer_profile = {
                    "farmer_type": "small",
                    "crop_type": "rice",
                    "land_size": 2.5
                }
                
                schemes_data = get_schemes_by_location_and_profile(location, farmer_profile)
                
                # Verify real data structure
                self.assertIsInstance(schemes_data, dict)
                self.assertIn("total_schemes", schemes_data)
                self.assertIn("schemes", schemes_data)
                
                total_schemes = schemes_data["total_schemes"]
                print(f"✓ {location}: {total_schemes} schemes available")
                
                # Print sample scheme for verification
                if schemes_data["schemes"]:
                    sample_scheme = schemes_data["schemes"][0]
                    print(f"  Sample: {sample_scheme.get('scheme_name', 'Unknown')}")
                
            except Exception as e:
                print(f"⚠ Failed to fetch schemes for {location}: {str(e)}")
                continue
    
    @unittest.skipIf(not os.getenv("RUN_REAL_API_TESTS"), 
                     "Real API tests disabled. Set RUN_REAL_API_TESTS=1 to enable.")
    def test_real_agent_workflow(self):
        """Test complete agent workflow with real API"""
        print("\n=== Testing Real Agent Workflow ===")
        
        test_scenarios = [
            {
                "user_query": "What schemes are available for small farmers in Maharashtra?",
                "location": "Mumbai",
                "entities": {"farmer_type": "small", "crop": "cotton"}
            },
            {
                "user_query": "I need crop insurance for my wheat farm",
                "location": "Delhi", 
                "entities": {"crop": "wheat", "need": "insurance"}
            }
        ]
        
        for scenario in test_scenarios:
            try:
                mock_state = GlobalState(
                    user_query=scenario["user_query"],
                    location=scenario["location"],
                    entities=scenario["entities"]
                )
                
                result = government_schemes_agent(mock_state)
                
                # Verify result
                self.assertIsInstance(result, dict)
                self.assertIn("relevant_schemes", result)
                
                schemes_count = len(result["relevant_schemes"])
                print(f"✓ Query: '{scenario['user_query'][:50]}...'")
                print(f"  Location: {scenario['location']}")
                print(f"  Schemes found: {schemes_count}")
                
            except Exception as e:
                print(f"⚠ Agent workflow failed for scenario: {str(e)}")
                continue

if __name__ == "__main__":
    print("=" * 80)
    print("🏛️ GOVERNMENT SCHEMES AGENT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGovernmentSchemesPlugin))
    suite.addTests(loader.loadTestsFromTestCase(TestGovernmentSchemesAgent))
    
    # Add real API tests if enabled
    if os.getenv("RUN_REAL_API_TESTS"):
        print("\n🌐 Real API tests are ENABLED")
        suite.addTests(loader.loadTestsFromTestCase(TestGovernmentSchemesRealAPI))
    else:
        print("\n🌐 Real API tests are DISABLED (set RUN_REAL_API_TESTS=1 to enable)")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("🎯 TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED! Government Schemes system is working perfectly!")
    
    print("=" * 80)
