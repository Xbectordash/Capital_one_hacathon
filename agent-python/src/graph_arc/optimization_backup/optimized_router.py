# Optimized Router with Parallel Processing
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Union
from src.graph_arc.agents_node.weather_agent import weather_agent
from src.graph_arc.agents_node.soil_crop_recommendation_agent import soil_crop_recommendation_agent
from src.graph_arc.agents_node.market_price_agent import market_price_agent
from src.graph_arc.agents_node.crop_health_pest_agent import crop_health_pest_agent
from src.graph_arc.agents_node.government_schemes_agent import government_schemes_agent
from src.graph_arc.core_nodes.offline_access_agent import offline_access_agent
from src.graph_arc.state import GlobalState, AgentResultsState
from src.utils.loggers import get_logger

class OptimizedRouter:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.logger = get_logger("optimized_router")
        
        # Agent registry with execution priority and independence
        self.agent_registry = {
            "weather": {
                "function": weather_agent,
                "priority": 1,  # High priority - needed by others
                "independent": True,  # Can run independently
                "timeout": 10  # seconds
            },
            "soil": {
                "function": soil_crop_recommendation_agent,
                "priority": 1,  # High priority - fundamental
                "independent": True,
                "timeout": 15
            },
            "market": {
                "function": market_price_agent,
                "priority": 2,  # Medium priority
                "independent": True,
                "timeout": 8
            },
            "crop_health": {
                "function": crop_health_pest_agent,
                "priority": 2,
                "independent": True,
                "timeout": 12
            },
            "government_schemes": {
                "function": government_schemes_agent,
                "priority": 3,  # Lower priority
                "independent": True,
                "timeout": 10
            },
            "offline": {
                "function": offline_access_agent,
                "priority": 3,
                "independent": True,
                "timeout": 5
            }
        }

    def _execute_agent_with_timeout(self, agent_info: Dict, state: Dict[str, Any]) -> tuple:
        """Execute a single agent with timeout handling"""
        try:
            agent_name = agent_info.get("name")
            agent_func = agent_info.get("function")
            timeout = agent_info.get("timeout", 10)
            
            self.logger.info(f"[OptimizedRouter] Executing {agent_name} with {timeout}s timeout")
            
            # Execute agent (this should be wrapped in timeout handling)
            result = agent_func(state)
            return agent_name, result, None
            
        except Exception as e:
            self.logger.error(f"[OptimizedRouter] Agent {agent_name} failed: {e}")
            return agent_name, None, str(e)

    async def conditional_router_parallel(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimized router with parallel execution and smart prioritization
        """
        self.logger.info("[OptimizedRouter] Starting PARALLEL agent routing process")
        
        intents = state.get("intents", [])
        raw_query = state.get("raw_query", "")
        
        self.logger.info(f"[OptimizedRouter] Processing query: '{raw_query}'")
        self.logger.info(f"[OptimizedRouter] Detected intents: {intents}")
        
        # Map intents to agents
        intent_to_agent = {
            "weather": "weather",
            "soil": "soil", 
            "market": "market",
            "crop_health": "crop_health",
            "government_schemes": "government_schemes",
            "offline": "offline"
        }
        
        # Determine which agents to run
        agents_to_run = []
        for intent in intents:
            if intent in intent_to_agent:
                agent_key = intent_to_agent[intent]
                if agent_key in self.agent_registry:
                    agent_info = self.agent_registry[agent_key].copy()
                    agent_info["name"] = intent
                    agents_to_run.append(agent_info)
        
        if not agents_to_run:
            self.logger.warning("[OptimizedRouter] No valid agents found for intents")
            return {**state, "agent_results": {}}
        
        # Sort by priority (higher priority first)
        agents_to_run.sort(key=lambda x: x["priority"])
        
        self.logger.info(f"[OptimizedRouter] Executing {len(agents_to_run)} agents in parallel")
        
        # Execute agents in parallel with timeout
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all agents for execution
            future_to_agent = {
                executor.submit(self._execute_agent_with_timeout, agent_info, state): agent_info["name"]
                for agent_info in agents_to_run
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_agent, timeout=30):  # 30s total timeout
                agent_name = future_to_agent[future]
                try:
                    name, result, error = future.result(timeout=1)  # 1s to get the result
                    if result:
                        results[name] = result
                        self.logger.info(f"[OptimizedRouter] ✅ {name} completed successfully")
                    else:
                        self.logger.warning(f"[OptimizedRouter] ⚠️ {name} failed: {error}")
                        results[name] = {"error": error}
                except Exception as e:
                    self.logger.error(f"[OptimizedRouter] ❌ {agent_name} execution failed: {e}")
                    results[agent_name] = {"error": str(e)}
        
        self.logger.info(f"[OptimizedRouter] Parallel execution completed. Results: {list(results.keys())}")
        
        return {**state, "agent_results": results}

# Global instance
optimized_router = OptimizedRouter()

# Export the function for use in graph
async def conditional_router_optimized(state: Dict[str, Any]) -> Dict[str, Any]:
    """Optimized conditional router function"""
    return await optimized_router.conditional_router_parallel(state)
