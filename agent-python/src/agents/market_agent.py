from .base import BaseAgent
from plugins.price_from_mandi import PriceFromMandi

class MarketAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm, name="MarketAgent")
        self.mandi = PriceFromMandi()  # 👈 Create instance of your price class

    def act(self, prompt: str) -> str:
        """
        Acts based on the prompt. If it includes a price-related query,
        fetch from mandi. Otherwise fallback to LLM.
        """

        # 👇 Simple keyword check — you can make it better using regex or classification
        if "price" in prompt.lower():
            # Try to extract info from prompt - in real case use NLP parser or tools
            # Example prompt: "Get price of Onion in Rahata, Ahmednagar, Maharashtra"

            try:
                # Very naive parsing, ideally you use LangChain tool calling or structured input
                words = prompt.split(" in ")
                commodity = words[0].split("price of")[-1].strip()
                location_parts = words[1].split(",")
                market = location_parts[0].strip()
                district = location_parts[1].strip()
                state = location_parts[2].strip()

                price = self.mandi.get_price(commodity, state, district, market)

                if price:
                    return f"The modal price of {commodity} in {market}, {district}, {state} is ₹{price}."
                else:
                    return f"Sorry, I couldn't find price data for {commodity} in {market}, {district}, {state}."

            except Exception as e:
                return f"Error parsing mandi price prompt: {e}"

        # Default to LLM for other market-related queries
        response = self.llm.llm.invoke(prompt)
        return f"[MarketAgent] {response}"
