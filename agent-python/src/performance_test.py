"""
Performance Test Script for Optimized Agricultural AI
Compares performance between standard and optimized workflows
"""
import time
import asyncio
import statistics
from typing import List, Dict
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.loggers import get_logger

# Test queries for performance comparison
TEST_QUERIES = [
    {
        "raw_query": "Should I irrigate today?",
        "location": "Satara",
        "language": "en"
    },
    {
        "raw_query": "What crops should I plant?",
        "location": "Pune",
        "language": "en"
    },
    {
        "raw_query": "Current market prices for wheat",
        "location": "Mumbai",
        "language": "en"
    },
    {
        "raw_query": "Weather forecast and farming advice",
        "location": "Nashik",
        "language": "en"
    },
    {
        "raw_query": "Soil health and fertilizer recommendations",
        "location": "Kolhapur",
        "language": "en"
    }
]

class PerformanceTester:
    def __init__(self):
        self.logger = get_logger("performance_tester")
        self.results = {"standard": [], "optimized": []}
    
    def test_workflow(self, workflow, query_data: Dict, workflow_type: str) -> Dict:
        """Test a single workflow execution"""
        start_time = time.time()
        
        try:
            result = workflow.invoke(query_data)
            execution_time = time.time() - start_time
            
            # Extract performance metrics if available
            perf_metrics = result.get("_performance", {}) if isinstance(result, dict) else {}
            
            return {
                "success": True,
                "execution_time": execution_time,
                "query": query_data["raw_query"],
                "location": query_data["location"],
                "workflow_type": workflow_type,
                "metrics": perf_metrics
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"[PerfTest] {workflow_type} workflow failed: {e}")
            
            return {
                "success": False,
                "execution_time": execution_time,
                "query": query_data["raw_query"],
                "location": query_data["location"],
                "workflow_type": workflow_type,
                "error": str(e)
            }
    
    def run_performance_comparison(self, iterations: int = 3):
        """Run performance comparison between workflows"""
        self.logger.info(f"[PerfTest] Starting performance comparison with {iterations} iterations")
        
        try:
            # Import workflows
            from src.graph_arc.graph import workflow as standard_workflow
            from src.graph_arc.optimized_graph import workflow_optimized as optimized_workflow
            
            self.logger.info("[PerfTest] Both workflows imported successfully")
            
        except ImportError as e:
            self.logger.error(f"[PerfTest] Failed to import workflows: {e}")
            return
        
        all_results = []
        
        for iteration in range(iterations):
            self.logger.info(f"[PerfTest] === Iteration {iteration + 1}/{iterations} ===")
            
            for query_data in TEST_QUERIES:
                query = query_data["raw_query"]
                location = query_data["location"]
                
                self.logger.info(f"[PerfTest] Testing: '{query}' at {location}")
                
                # Test standard workflow
                self.logger.info("[PerfTest] Running standard workflow...")
                standard_result = self.test_workflow(standard_workflow, query_data, "standard")
                all_results.append(standard_result)
                
                # Small delay between tests
                time.sleep(1)
                
                # Test optimized workflow
                self.logger.info("[PerfTest] Running optimized workflow...")
                optimized_result = self.test_workflow(optimized_workflow, query_data, "optimized")
                all_results.append(optimized_result)
                
                # Print comparison for this query
                if standard_result["success"] and optimized_result["success"]:
                    improvement = ((standard_result["execution_time"] - optimized_result["execution_time"]) / 
                                 standard_result["execution_time"]) * 100
                    
                    self.logger.info(f"[PerfTest] ⚡ Performance improvement: {improvement:.1f}% " +
                                   f"({standard_result['execution_time']:.2f}s → {optimized_result['execution_time']:.2f}s)")
                
                # Delay between different queries
                time.sleep(2)
        
        # Analyze results
        self.analyze_results(all_results)
    
    def analyze_results(self, results: List[Dict]):
        """Analyze and report performance results"""
        self.logger.info("[PerfTest] === PERFORMANCE ANALYSIS ===")
        
        # Separate results by workflow type
        standard_times = [r["execution_time"] for r in results if r["workflow_type"] == "standard" and r["success"]]
        optimized_times = [r["execution_time"] for r in results if r["workflow_type"] == "optimized" and r["success"]]
        
        if not standard_times or not optimized_times:
            self.logger.error("[PerfTest] Insufficient data for analysis")
            return
        
        # Calculate statistics
        standard_stats = {
            "mean": statistics.mean(standard_times),
            "median": statistics.median(standard_times),
            "min": min(standard_times),
            "max": max(standard_times),
            "count": len(standard_times)
        }
        
        optimized_stats = {
            "mean": statistics.mean(optimized_times),
            "median": statistics.median(optimized_times),
            "min": min(optimized_times),
            "max": max(optimized_times),
            "count": len(optimized_times)
        }
        
        # Calculate improvements
        mean_improvement = ((standard_stats["mean"] - optimized_stats["mean"]) / standard_stats["mean"]) * 100
        median_improvement = ((standard_stats["median"] - optimized_stats["median"]) / standard_stats["median"]) * 100
        
        # Report results
        self.logger.info(f"[PerfTest] 📊 STANDARD WORKFLOW:")
        self.logger.info(f"[PerfTest]   Mean: {standard_stats['mean']:.2f}s")
        self.logger.info(f"[PerfTest]   Median: {standard_stats['median']:.2f}s")
        self.logger.info(f"[PerfTest]   Range: {standard_stats['min']:.2f}s - {standard_stats['max']:.2f}s")
        
        self.logger.info(f"[PerfTest] 🚀 OPTIMIZED WORKFLOW:")
        self.logger.info(f"[PerfTest]   Mean: {optimized_stats['mean']:.2f}s")
        self.logger.info(f"[PerfTest]   Median: {optimized_stats['median']:.2f}s")
        self.logger.info(f"[PerfTest]   Range: {optimized_stats['min']:.2f}s - {optimized_stats['max']:.2f}s")
        
        self.logger.info(f"[PerfTest] ⚡ PERFORMANCE IMPROVEMENTS:")
        self.logger.info(f"[PerfTest]   Mean improvement: {mean_improvement:.1f}%")
        self.logger.info(f"[PerfTest]   Median improvement: {median_improvement:.1f}%")
        
        # Success rates
        standard_success = len([r for r in results if r["workflow_type"] == "standard" and r["success"]])
        optimized_success = len([r for r in results if r["workflow_type"] == "optimized" and r["success"]])
        total_tests = len([r for r in results if r["workflow_type"] == "standard"])
        
        self.logger.info(f"[PerfTest] 📈 SUCCESS RATES:")
        self.logger.info(f"[PerfTest]   Standard: {standard_success}/{total_tests} ({(standard_success/total_tests)*100:.1f}%)")
        self.logger.info(f"[PerfTest]   Optimized: {optimized_success}/{total_tests} ({(optimized_success/total_tests)*100:.1f}%)")
        
        # Performance recommendation
        if mean_improvement > 20:
            self.logger.info(f"[PerfTest] 🎉 EXCELLENT: {mean_improvement:.1f}% performance improvement achieved!")
        elif mean_improvement > 10:
            self.logger.info(f"[PerfTest] ✅ GOOD: {mean_improvement:.1f}% performance improvement")
        elif mean_improvement > 0:
            self.logger.info(f"[PerfTest] 👍 MODEST: {mean_improvement:.1f}% performance improvement")
        else:
            self.logger.warning(f"[PerfTest] ⚠️ REGRESSION: {abs(mean_improvement):.1f}% performance degradation")

def main():
    """Run performance tests"""
    tester = PerformanceTester()
    
    print("🧪 Starting Agricultural AI Performance Tests...")
    print("This will compare standard vs optimized workflows")
    print("=" * 60)
    
    # Run comparison with 2 iterations (adjust as needed)
    tester.run_performance_comparison(iterations=2)
    
    print("=" * 60)
    print("🎯 Performance testing completed!")

if __name__ == "__main__":
    main()
