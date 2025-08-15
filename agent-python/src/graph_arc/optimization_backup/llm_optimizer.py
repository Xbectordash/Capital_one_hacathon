# LLM Optimization Module
import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GEMINI_API_KEY
from src.utils.loggers import get_logger
from concurrent.futures import ThreadPoolExecutor
import time

class LLMOptimizer:
    """Optimized LLM handling with batching, caching, and smart prompt management"""
    
    def __init__(self):
        self.logger = get_logger("llm_optimizer")
        self.response_cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes cache TTL
        
        # Pre-initialized LLM instances for different use cases
        self.llm_instances = {
            "fast": ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.1,
                max_output_tokens=800,
                api_key=GEMINI_API_KEY,
            ),
            "detailed": ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.3,
                max_output_tokens=1500,
                api_key=GEMINI_API_KEY,
            ),
            "decision": ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.2,
                max_output_tokens=1200,
                api_key=GEMINI_API_KEY,
            )
        }

    def _get_cache_key(self, prompt: str, model_type: str) -> str:
        """Generate cache key for prompt"""
        import hashlib
        return hashlib.md5(f"{model_type}:{prompt}".encode()).hexdigest()

    def _is_cache_valid(self, cached_time: float) -> bool:
        """Check if cache entry is still valid"""
        return (time.time() - cached_time) < self.cache_ttl

    async def get_llm_response_cached(self, prompt: str, model_type: str = "fast") -> str:
        """Get LLM response with caching"""
        cache_key = self._get_cache_key(prompt, model_type)
        
        # Check cache first
        if cache_key in self.response_cache:
            cached_data, cached_time = self.response_cache[cache_key]
            if self._is_cache_valid(cached_time):
                self.logger.info(f"[LLMOptimizer] Cache hit for {model_type} model")
                return cached_data
        
        # Cache miss - make LLM call
        try:
            llm = self.llm_instances[model_type]
            response = llm.invoke(prompt)
            result = response.content.strip()
            
            # Cache the response
            self.response_cache[cache_key] = (result, time.time())
            
            self.logger.info(f"[LLMOptimizer] {model_type} LLM call completed and cached")
            return result
            
        except Exception as e:
            self.logger.error(f"[LLMOptimizer] LLM call failed: {e}")
            return f"Error generating response: {str(e)}"

    async def batch_llm_calls(self, prompts_with_types: List[Tuple[str, str]]) -> List[str]:
        """Execute multiple LLM calls in parallel"""
        self.logger.info(f"[LLMOptimizer] Executing {len(prompts_with_types)} LLM calls in batch")
        
        tasks = []
        for prompt, model_type in prompts_with_types:
            task = self.get_llm_response_cached(prompt, model_type)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"[LLMOptimizer] Batch call {i} failed: {result}")
                processed_results.append(f"Error: {str(result)}")
            else:
                processed_results.append(result)
        
        return processed_results

    def get_optimized_prompt(self, agent_type: str, data: Dict[str, Any]) -> str:
        """Get optimized, concise prompts for each agent type"""
        
        base_context = f"Location: {data.get('location', 'Unknown')}, Query: {data.get('raw_query', '')}"
        
        optimized_prompts = {
            "weather": f"""Weather Analysis Request:
{base_context}
Weather Data: {json.dumps(data.get('weather_forecast', {}), indent=1)}

Provide concise weather-based agricultural advice in 2-3 sentences. Focus on:
- Irrigation needs
- Field operation timing
- Crop protection measures

Response format: Direct recommendation without explanations.""",

            "soil": f"""Soil & Crop Recommendation:
{base_context}
Soil Data: {json.dumps(data.get('soil_health', {}), indent=1)}

Provide top 3 crop recommendations with brief rationale. Format:
1. Crop A - reason
2. Crop B - reason  
3. Crop C - reason

Keep response under 150 words.""",

            "market": f"""Market Analysis:
{base_context}
Crop: {data.get('crop', 'general')}

Provide brief market advice: current prices, selling timing, profit potential.
Response in 2-3 sentences max.""",

            "decision": f"""Agricultural Decision Support:
{base_context}
Agent Results: {json.dumps(data.get('agent_results', {}), indent=1)}

Synthesize agent outputs into ONE clear, actionable recommendation. 
Include: What to do today, why, and expected outcome.
Maximum 100 words. JSON format:
{{"final_advice": "...", "explanation": "...", "confidence_score": 0.8}}"""
        }
        
        return optimized_prompts.get(agent_type, f"Analyze this agricultural query: {base_context}")

    def clear_cache(self):
        """Clear the response cache"""
        self.response_cache.clear()
        self.logger.info("[LLMOptimizer] Cache cleared")

# Global instance
llm_optimizer = LLMOptimizer()

# Export functions
async def get_optimized_llm_response(prompt: str, model_type: str = "fast") -> str:
    return await llm_optimizer.get_llm_response_cached(prompt, model_type)

async def batch_llm_requests(prompts_with_types: List[Tuple[str, str]]) -> List[str]:
    return await llm_optimizer.batch_llm_calls(prompts_with_types)

def get_agent_prompt(agent_type: str, data: Dict[str, Any]) -> str:
    return llm_optimizer.get_optimized_prompt(agent_type, data)
