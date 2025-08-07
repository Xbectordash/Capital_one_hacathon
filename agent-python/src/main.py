from core.llm import LLM
from agents.farmer_agent import FarmerAgent
from agents.market_agent import MarketAgent
from dotenv import load_dotenv
load_dotenv()

def main():
    llm = LLM()
    farmer = FarmerAgent(llm)
    market = MarketAgent(llm)

    farmer_prompt = "What are the best crops to plant in August?"
    market_prompt = "What is the current market price for wheat?"

    print(farmer.act(farmer_prompt))
    print(market.act(market_prompt))

if __name__ == "__main__":
    main()
