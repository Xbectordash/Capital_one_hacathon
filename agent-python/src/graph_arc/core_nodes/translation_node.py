"""
Translation Agent Node - Simple and Clean
Task: Read final decision + explanation, translate to local language
"""
from graph_arc.state import GlobalState
from utils.loggers import get_logger
from langchain_core.runnables import RunnableConfig
from config.model_conf import Configuration
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
import json
import re

def translation_language_agent(state: GlobalState, config: RunnableConfig) -> dict:
    """
    Simple translation: Read decision + explanation, translate to user language.
    """
    logger = get_logger("translation_language_agent")
    logger.info("[TranslationAgent] Starting translation")
    
    # Get user language
    user_language = state.get("language", "en").lower()
    logger.info(f"[TranslationAgent] User language: {user_language}")
    
    # Skip if English
    if user_language in ["en", "english"]:
        logger.info("[TranslationAgent] English - no translation needed")
        return {}
    
    # Get content to translate
    decision = state.get("decision", {})
    advice = decision.get("final_advice", "No advice available")
    explanation = decision.get("explanation", "No explanation available")
    
    logger.info(f"[TranslationAgent] Translating to {user_language}")
    
    try:
        # Initialize LLM
        configurable = Configuration.from_runnable_config(config)
        llm = ChatGoogleGenerativeAI(
            model=configurable.translation_model,
            temperature=0.2,
            max_output_tokens=3000,
            api_key=GEMINI_API_KEY,
        )
        
        # Language mapping
        lang_map = {
            "hi": "Hindi", "bn": "Bengali", "te": "Telugu", "ta": "Tamil",
            "gu": "Gujarati", "mr": "Marathi", "kn": "Kannada", "ml": "Malayalam",
            "pa": "Punjabi", "or": "Odia"
        }
        target_lang = lang_map.get(user_language, user_language)
        
        # Simple translation prompt
        prompt = f"""
        Translate this agricultural content to {target_lang}. Return JSON with 'advice' and 'explanation' fields.
        
        ADVICE: {advice}
        
        EXPLANATION: {explanation}
        """
        
        # Get translation
        response = llm.invoke(prompt)
        content = re.sub(r"```json|```", "", response.content).strip()
        
        try:
            result = json.loads(content)
            translated_advice = result.get("advice", advice)
            translated_explanation = result.get("explanation", explanation)
            
            logger.info("[TranslationAgent] Translation completed")
            
            return {
                "translation": {
                    "detected_language": "en",
                    "translated_query": state.get("raw_query", ""),
                    "translated_response": translated_advice,
                    "translated_explanation": translated_explanation
                }
            }
            
        except json.JSONDecodeError:
            logger.error("[TranslationAgent] JSON parse failed - using fallback")
            # Simple fallback
            if user_language == "hi":
                fallback_advice = "कृषि सलाह उपलब्ध है। स्थानीय कृषि कार्यालय से संपर्क करें।"
                fallback_explanation = "विस्तृत जानकारी अंग्रेजी में उपलब्ध है।"
            else:
                fallback_advice = f"Agricultural advice available in {target_lang}."
                fallback_explanation = f"Detailed information available in English."
            
            return {
                "translation": {
                    "detected_language": "en", 
                    "translated_query": state.get("raw_query", ""),
                    "translated_response": fallback_advice,
                    "translated_explanation": fallback_explanation
                }
            }
            
    except Exception as e:
        logger.error(f"[TranslationAgent] Translation failed: {e}")
        return {}
