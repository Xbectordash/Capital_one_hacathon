from langgraph.graph import StateGraph, END
from agents.market_agent import MarketAgent
from core.llm import LLM

# Define the state


# Node: Use MarketAgent to process prompt
def market_node(state):
	llm = LLM()  # Your LLM wrapper
	agent = MarketAgent(llm)
	result = agent.act(state["prompt"])
	state["result"] = result
	return state

# Build the graph
graph = StateGraph(dict)
graph.add_node("market", market_node)
graph.set_entry_point("market")
graph.add_edge("market", END)

def run_market_flow(prompt):
	compiled_graph = graph.compile()
	result_state = compiled_graph.invoke({"prompt": prompt})
	print("MarketAgent Result:", result_state["result"])

# if __name__ == "__main__":
# 	# Example prompt: "Get price of Onion in Rahata, Ahmednagar, Maharashtra"
# 	run_market_flow("Get price of Onion in Rahata, Ahmednagar, Maharashtra")
