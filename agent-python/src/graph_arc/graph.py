from langgraph.graph import START, END
from langgraph.graph import StateGraph
from src.graph_arc.state import GlobalState
from src.config.model_conf import Configuration
from src.graph_arc.core_nodes.user_context_node import get_user_context
from src.graph_arc.core_nodes.query_understanding_node import understand_query
from src.graph_arc.router import conditional_router
from src.graph_arc.core_nodes.decision_support_node import aggregate_decisions
from src.graph_arc.core_nodes.translation_node import translation_language_agent

# Import all agent nodes
from src.graph_arc.agents_node.soil_crop_recommendation_agent import soil_crop_recommendation_agent
from src.graph_arc.agents_node.weather_agent import weather_agent
from src.graph_arc.agents_node.market_price_agent import market_price_agent
from src.graph_arc.agents_node.crop_health_pest_agent import crop_health_pest_agent
from src.graph_arc.agents_node.government_schemes_agent import government_schemes_agent


def build_graph():
    """
    Builds and returns the LangGraph workflow.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create a new StateGraph with the GlobalState type
    graph = StateGraph(GlobalState, config=Configuration)
    
    # Adding core nodes to the graph
    graph.add_node("user_context", get_user_context)
    graph.add_node("query_understanding", understand_query)
    graph.add_node("conditional_router", conditional_router)
    
    # Adding decision and translation nodes
    graph.add_node("decision_support", aggregate_decisions)
    graph.add_node("translation_language", translation_language_agent)
    
    # Core flow - router processes all agents internally
    graph.add_edge(START, "user_context")
    graph.add_edge("user_context", "query_understanding")
    graph.add_edge("query_understanding", "conditional_router")
    
    # Router processes all agents and flows directly to decision support
    graph.add_edge("conditional_router", "decision_support")
    
    # After decision support, conditionally go to translation if needed
    def should_translate(state):
        language = state.get("language", "en").lower()
        print(f"🔍 Checking translation need for language: {language}")
        if language not in ["en", "english"]:
            print(f"✅ Translation needed for language: {language}")
            return "translation_language"
        else:
            print("❌ No translation needed - language is English")
            return "END"
    
    graph.add_conditional_edges(
        "decision_support",
        should_translate,
        {
            "translation_language": "translation_language",
            "END": END
        }
    )
    
    # Translation goes to END
    graph.add_edge("translation_language", END)
    
    # Compile the graph into a runnable workflow
    return graph.compile()

# Create the compiled workflow
workflow = build_graph()
