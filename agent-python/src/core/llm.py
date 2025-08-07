import os
from langchain_google_genai import ChatGoogleGenerativeAI


class LLM:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY not found. Please set it in your .env file."
            )
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.2,
            max_output_tokens=1024,
            top_p=0.95,
            top_k=40,
            api_key=api_key,
        )
        print(f"Initialized LLM with model: {model_name}")
        self.llm = llm
