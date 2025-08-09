"""
Decision Support Node
Description: Aggregates outputs from all agent nodes for final advice.
"""

def aggregate_decisions(agent_outputs: dict) -> str:
    """
    Returns aggregated decision/advice from agent outputs.
    """
    # Placeholder: Aggregate logic
    return f"Final advice: {', '.join(str(v) for v in agent_outputs.values())}"
