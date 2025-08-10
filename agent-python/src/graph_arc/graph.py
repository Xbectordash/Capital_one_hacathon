from langgraph.graph import START, END
from langgraph.graph import StateGraph
from graph_arc.state import GlobalState
from config.model_conf import Configuration
from graph_arc.core_nodes.user_context_node import get_user_context
from graph_arc.core_nodes.query_understanding_node import understand_query
from graph_arc.router import conditional_router
from graph_arc.core_nodes.decision_support_node import aggregate_decisions
from graph_arc.core_nodes.translation_node import translation_language_agent


def build_graph():
    """
    Builds and returns the LangGraph workflow.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create a new StateGraph with the GlobalState type
    graph = StateGraph(GlobalState, config=Configuration)
    
    # Adding nodes to the graph
    graph.add_node("user_context", get_user_context)
    graph.add_node("query_understanding", understand_query)
    graph.add_node("conditional_router", conditional_router)
    graph.add_node("decision_support", aggregate_decisions)
    graph.add_node("translation_language", translation_language_agent)
    
    # Connecting nodes with edges
    graph.add_edge(START, "user_context")
    graph.add_edge("user_context", "query_understanding")
    graph.add_edge("query_understanding", "conditional_router")
    
    # First go to decision support (always needed)
    graph.add_edge("conditional_router", "decision_support")
    
    # After decision support, conditionally go to translation if needed
    graph.add_conditional_edges(
        "decision_support",
        lambda state: ["translation_language"] if state.get("language", "en").lower() not in ["en", "english"] else ["END"],
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
