from .base import BaseAgent

class FarmerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm, name="FarmerAgent")

    def act(self, prompt):
        # Example: Use LLM to answer a farming question
        response = self.llm.llm.invoke(prompt)
        return f"[FarmerAgent] {response}"
