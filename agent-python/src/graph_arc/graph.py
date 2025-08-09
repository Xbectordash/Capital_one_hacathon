from langgraph.graph import START, END
from langgraph.graph import StateGraph
from graph_arc.state import GlobalState
from config.model_conf import Configuration
from graph_arc.core_nodes.user_context_node import get_user_context
from graph_arc.core_nodes.query_understanding_node import understand_query


# Adding nodes to the graph
graph = StateGraph(GlobalState, config=Configuration)
graph.add_node("user_context", get_user_context)
graph.add_node("query_understanding", understand_query)

# Connecting nodes and edges
graph.add_edge(START, "user_context")
graph.add_edge("user_context", "query_understanding")
graph.add_edge("query_understanding", END)

workflow = graph.compile()

