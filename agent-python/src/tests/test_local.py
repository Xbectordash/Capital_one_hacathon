#!/usr/bin/env python3
"""
Test script to verify the optimized graph works without async errors
"""
import os
import sys
import asyncio
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_standard_graph():
    """Test the standard graph with a simple agricultural query"""
    
    print("🧪 Testing Standard Graph Locally")
    print("=" * 50)
    
    try:
        # Import the standard graph
        from src.graph_arc.graph import workflow
        
        print("✅ Successfully imported standard graph")
        
        # Test query
        test_query = {
            "user_id": "test_user",
            "raw_query": "What crops are best for sandy soil in Maharashtra?",
            "language": "en",
            "location": "Maharashtra, India",
            "confidence_score": 0.9
        }
        
        print(f"🌾 Testing query: {test_query['raw_query']}")
        print(f"📍 Location: {test_query['location']}")
        print(f"🌐 Language: {test_query['language']}")
        print()
        
        # Execute the workflow synchronously (avoid async issues)
        start_time = datetime.now()
        print(f"⏰ Started at: {start_time.strftime('%H:%M:%S')}")
        
        result = workflow.invoke(test_query)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"⏰ Completed at: {end_time.strftime('%H:%M:%S')}")
        print(f"⚡ Duration: {duration:.2f} seconds")
        print()
        
        # Display results
        if result:
            print("✅ SUCCESS: Workflow completed without errors!")
            print("=" * 50)
            
            if 'response' in result:
                print("🤖 AI Response:")
                print(result['response'])
                print()
            
            if 'agents_used' in result:
                print(f"🔧 Agents Used: {', '.join(result['agents_used'])}")
            
            if 'performance_metrics' in result:
                metrics = result['performance_metrics']
                print(f"📊 Performance Metrics:")
                for key, value in metrics.items():
                    print(f"  - {key}: {value}")
            
            print("=" * 50)
            return True
        else:
            print("❌ FAILED: No result returned")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Error Type: {type(e).__name__}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return False

def test_sync_functions():
    """Test sync functions without async context"""
    print("\n🔧 Testing Individual Components")
    print("=" * 50)
    
    try:
        # Test imports
        from src.graph_arc.router import conditional_router
        from src.graph_arc.core_nodes.decision_support_node import aggregate_decisions
        from src.config.model_conf import Configuration
        from langchain_core.runnables import RunnableConfig
        print("✅ Successfully imported sync functions")
        
        # Test basic routing
        test_state = {
            "query": "What crops are best for sandy soil?",
            "language": "en",
            "location": "Maharashtra, India"
        }
        
        route_result = conditional_router(test_state)
        print(f"✅ Router test passed: {route_result}")
        
        # Test decision aggregation with proper parameters
        test_state_with_results = {
            "query": "What crops are best for sandy soil?",
            "language": "en", 
            "location": "Maharashtra, India",
            "agent_results": {
                "weather_agent": {"recommendation": "Use drought-resistant crops"},
                "soil_agent": {"recommendation": "Apply organic fertilizers"},
                "crop_agent": {"recommendation": "Implement drip irrigation"}
            }
        }
        
        # Create a basic config for testing
        config = RunnableConfig()
        
        aggregated = aggregate_decisions(test_state_with_results, config)
        print(f"✅ Decision aggregation test passed: {type(aggregated).__name__} returned")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Local Tests for Agricultural AI")
    print("=" * 70)
    
    # Test sync functions first
    sync_success = test_sync_functions()
    
    if sync_success:
        print("\n🎯 Sync tests passed, proceeding with workflow test...")
        # Test workflow
        workflow_success = test_standard_graph()
        
        if workflow_success:
            print("\n🎉 ALL TESTS PASSED! The AI agent is working correctly.")
            print("✅ Ready to deploy to Docker")
        else:
            print("\n💥 Workflow test failed. Need to fix workflow issues.")
    else:
        print("\n💥 Sync function tests failed. Need to fix basic components.")
