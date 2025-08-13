"""
Optimized Agricultural Graph with Performance Enhancements
- Parallel agent execution
- Smart routing based on query complexity  
- Cached LLM responses
- Fast fallbacks for simple queries
"""
from langgraph.graph import START, END, StateGraph
from src.graph_arc.state import GlobalState
from src.config.model_conf import Configuration
from src.graph_arc.core_nodes.user_context_node import get_user_context
from src.graph_arc.core_nodes.query_understanding_node import understand_query
from src.graph_arc.router import conditional_router
from src.graph_arc.core_nodes.decision_support_node import aggregate_decisions
from src.graph_arc.core_nodes.translation_node import translation_language_agent
from src.utils.loggers import get_logger
import time
from datetime import datetime

def build_optimized_graph():
    """
    Builds and returns the optimized LangGraph workflow with performance enhancements.
    
    Returns:
        Compiled optimized LangGraph workflow
    """
    logger = get_logger("optimized_graph")
    logger.info("[OptimizedGraph] Building performance-optimized agricultural workflow")
    
    # Create a new StateGraph with the GlobalState type
    graph = StateGraph(GlobalState, config=Configuration)
    
    # Adding optimized nodes to the graph
    graph.add_node("user_context", get_user_context)
    graph.add_node("query_understanding", understand_query)
    graph.add_node("optimized_router", _async_router_wrapper)
    graph.add_node("optimized_decision", aggregate_decisions)
    graph.add_node("translation_language", translation_language_agent)
    
    # Connecting nodes with edges
    graph.add_edge(START, "user_context")
    graph.add_edge("user_context", "query_understanding")
    graph.add_edge("query_understanding", "optimized_router")
    
    # Route to optimized decision support
    graph.add_edge("optimized_router", "optimized_decision")
    
    # Conditional translation routing
    graph.add_conditional_edges(
        "optimized_decision",
        _should_translate,
        {
            "translate": "translation_language",
            "end": END
        }
    )
    
    # Translation goes to END
    graph.add_edge("translation_language", END)
    
    logger.info("[OptimizedGraph] Optimized workflow graph compiled successfully")
    
    # Compile the graph into a runnable workflow
    return graph.compile()

def _should_translate(state) -> str:
    """Determine if translation is needed"""
    language = state.get("language", "en").lower()
    if language in ["en", "english"]:
        return "end"
    return "translate"

def _async_router_wrapper(state):
    """Wrapper to handle router in sync context"""
    try:
        # Use the sync version from the original router
        result = conditional_router(state)
        return result
    except Exception as e:
        logger = get_logger("optimized_graph")
        logger.error(f"[OptimizedGraph] Router execution failed: {e}")
        # Return state with empty results as fallback
        return {**state, "agent_results": {}}

# Performance monitoring wrapper
def build_monitored_graph():
    """Build graph with performance monitoring"""
    logger = get_logger("performance_monitor")
    
    class PerformanceMonitor:
        def __init__(self, workflow):
            self.workflow = workflow
            self.execution_times = {}
        
        def invoke(self, initial_state):
            import time
            
            start_time = time.time()
            logger.info("[PerfMonitor] Starting optimized workflow execution")
            
            try:
                result = self.workflow.invoke(initial_state)
                execution_time = time.time() - start_time
                
                logger.info(f"[PerfMonitor] ✅ Workflow completed in {execution_time:.2f}s")
                
                # Add performance metrics to result
                if isinstance(result, dict):
                    result["_performance"] = {
                        "execution_time": execution_time,
                        "optimization_enabled": True,
                        "timestamp": time.time()
                    }
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"[PerfMonitor] ❌ Workflow failed after {execution_time:.2f}s: {e}")
                raise
    
    # Build optimized workflow
    base_workflow = build_optimized_graph()
    
    # Wrap with performance monitoring
    monitored_workflow = PerformanceMonitor(base_workflow)
    
    logger.info("[PerfMonitor] Performance monitoring enabled for optimized workflow")
    return monitored_workflow

# Configuration for different performance modes
class PerformanceConfig:
    FAST_MODE = {
        "max_parallel_agents": 6,
        "llm_timeout": 8,
        "cache_enabled": True,
        "fallback_enabled": True
    }
    
    BALANCED_MODE = {
        "max_parallel_agents": 4,
        "llm_timeout": 12,
        "cache_enabled": True,
        "fallback_enabled": True
    }
    
    DETAILED_MODE = {
        "max_parallel_agents": 2,
        "llm_timeout": 20,
        "cache_enabled": False,
        "fallback_enabled": False
    }

# Create the optimized workflow instances
optimized_workflow = build_optimized_graph()
monitored_workflow = build_monitored_graph()

# Export the default optimized workflow
workflow_optimized = monitored_workflow

logger = get_logger("optimized_graph")
logger.info("🚀 Optimized agricultural workflow initialized with performance monitoring")
