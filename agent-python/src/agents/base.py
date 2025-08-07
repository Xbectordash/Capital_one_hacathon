# Base agent class
class BaseAgent:
    def __init__(self, llm, name="BaseAgent"):
        self.llm = llm
        self.name = name

    def act(self, prompt):
        raise NotImplementedError("Each agent must implement the act method.")
