from utils.loggers import get_logger
from graph_arc.state import GlobalState
from langchain_core.runnables import RunnableConfig
from config.model_conf import Configuration
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
from graph_arc.prompts import understand_query_prompt
import json
import re

# """
# Query Understanding Node
# Description: Extracts intent, entities, and multi-intent from user query.
# """


def understand_query(state: GlobalState, config: RunnableConfig) -> GlobalState:
    logger = get_logger("query_understanding_node")
    configurable = Configuration.from_runnable_config(config)

    llm = ChatGoogleGenerativeAI(
        model=configurable.query_understanding_model,
        temperature=0.2,
        max_output_tokens=1000,
        api_key=GEMINI_API_KEY,
    )
    logger.info("Invoking Gemini LLM for query understanding")

    format_prompt = understand_query_prompt.format(raw_query=state["raw_query"])
    response = llm.invoke(format_prompt)
    raw_content = response.content
    logger.info(f"[QueryUnderstandingNode] Raw LLM response: {raw_content}")

    # Remove ```json and ``` if present
    cleaned_content = re.sub(r"```json|```", "", raw_content).strip()

    try:
        parsed = json.loads(cleaned_content)
        state["intents"] = parsed.get("intents", [])
        state["entities"] = parsed.get("entities", {})
        state["confidence_score"] = parsed.get("confidence_score", 0.0)
    except Exception as e:
        logger.error(f"Failed to parse LLM JSON response: {e}")
        # fallback - keep state as is or set empty values
        state["intents"] = []
        state["entities"] = {}
        state["confidence_score"] = 0.0

    return state
