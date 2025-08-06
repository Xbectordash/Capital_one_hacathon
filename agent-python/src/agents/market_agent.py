from .base import BaseAgent

class MarketAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm, name="MarketAgent")

    def act(self, prompt):
        # Example: Use LLM to answer a market question
        response = self.llm.llm.invoke(prompt)
        return f"[MarketAgent] {response}"
