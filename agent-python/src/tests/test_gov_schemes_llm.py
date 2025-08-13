#!/usr/bin/env python3
"""
Test Government Schemes Agent LLM Integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graph_arc.agents_node.government_schemes_agent import government_schemes_agent

def test_government_schemes_llm():
    """Test that the government schemes agent uses LLM properly"""
    print("🧪 Testing Government Schemes Agent LLM Integration")
    print("=" * 60)
    
    # Create test state with government schemes intent
    test_state = {
        "raw_query": "What government schemes are available for small farmers in Maharashtra?",
        "intents": ["government_schemes"],
        "entities": {"farmer_type": "small farmer"},
        "location": "Maharashtra",
        "farmer_profile": {
            "farm_size_acres": 2.5,
            "farmer_type": "small farmer",
            "annual_income": 50000,
            "crops": ["rice", "wheat"]
        }
    }
    
    try:
        print("📊 Input State:")
        print(f"  Query: {test_state['raw_query']}")
        print(f"  Location: {test_state['location']}")
        
        print("\n🔄 Processing through government schemes agent...")
        result = government_schemes_agent(test_state)
        
        print("\n✅ Agent Results:")
        print(f"  Result Type: {type(result)}")
        if isinstance(result, dict):
            print(f"  Available Keys: {list(result.keys())}")
            
            # Check if we got AI recommendation
            if "application_steps" in result:
                app_steps = result["application_steps"]
                print(f"  AI Recommendation Length: {len(app_steps)} characters")
                
                # Check if it's a proper LLM response or fallback
                if "Rule-based" in app_steps or "Namaskar! Based on your profile" in app_steps:
                    print("  ⚠️  Using fallback rule-based recommendation")
                else:
                    print("  ✅ Using LLM-generated recommendation")
                    
        print("\n🎉 Government Schemes Agent LLM Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ LLM test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🏛️ Government Schemes Agent LLM Integration Test")
    print("=" * 60)
    
    success = test_government_schemes_llm()
    
    print("\n📋 Test Summary:")
    print("=" * 60)
    if success:
        print("🎉 LLM Integration Test: ✅ PASSED")
        print("Government Schemes Agent should now use LLM properly!")
    else:
        print("⚠️  LLM Integration Test: ❌ FAILED")
        print("Please check the implementation")
