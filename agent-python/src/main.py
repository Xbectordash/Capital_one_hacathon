
from graph_arc.graph import workflow

def main():
    # Example initial state
    initial_state = {
        "user_id": "user123",
        "raw_query": "What is the weather forecast for the next week, current soil moisture levels, market price trends for wheat, pest infestation alerts, and government subsidies available in Punjab?",
        "language": "en"
    }
    result = workflow.invoke(initial_state)
    print("Graph result:", result)

if __name__ == "__main__":
    main()
