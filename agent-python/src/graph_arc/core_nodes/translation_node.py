"""
Translation Agent Node - Simple and Clean
Task: Read final decision + explanation, translate to local language
"""
from src.graph_arc.state import GlobalState
from src.utils.loggers import get_logger
from langchain_core.runnables import RunnableConfig
from src.config.model_conf import Configuration
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GEMINI_API_KEY
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
    print(f"🗣️ Translation starting for language: {user_language}")
    
    # Skip if English
    if user_language in ["en", "english"]:
        logger.info("[TranslationAgent] English - no translation needed")
        print("❌ No translation needed for English")
        return {}
    
    # Get content to translate
    decision = state.get("decision", {})
    advice = decision.get("final_advice", "No advice available")
    explanation = decision.get("explanation", "No explanation available")
    
    logger.info(f"[TranslationAgent] Translating to {user_language}")
    print(f"🔄 Translating advice: {advice[:100]}...")
    
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
        
        # Enhanced translation prompt
        prompt = f"""
        You are an expert agricultural translator. Translate the following agricultural advice and explanation into {target_lang}. 
        Maintain technical accuracy and farming terminology. Return ONLY a JSON object with 'advice' and 'explanation' fields.
        
        ADVICE TO TRANSLATE: {advice}
        
        EXPLANATION TO TRANSLATE: {explanation}
        
        Return format:
        {{
            "advice": "translated advice in {target_lang}",
            "explanation": "translated explanation in {target_lang}"
        }}
        """
        
        # Get translation
        response = llm.invoke(prompt)
        content = re.sub(r"```json|```", "", response.content).strip()
        
        print(f"🤖 Translation response received: {content[:200]}...")
        
        try:
            result = json.loads(content)
            translated_advice = result.get("advice", advice)
            translated_explanation = result.get("explanation", explanation)
            
            logger.info("[TranslationAgent] Translation completed successfully")
            print(f"✅ Translation completed for {target_lang}")
            print(f"📝 Translated advice: {translated_advice[:100]}...")
            
            # Return updated state with translation
            return {
                "translation": {
                    "detected_language": "en",
                    "target_language": user_language,
                    "translated_query": state.get("raw_query", ""),
                    "translated_response": translated_advice,
                    "translated_explanation": translated_explanation,
                    "original_advice": advice,
                    "original_explanation": explanation
                },
                # Also update decision with translated content
                "decision": {
                    **decision,
                    "final_advice": translated_advice,
                    "explanation": translated_explanation,
                    "original_advice": advice,
                    "original_explanation": explanation
                }
            }
            
        except json.JSONDecodeError:
            logger.error("[TranslationAgent] JSON parse failed - using enhanced fallback")
            print("❌ JSON parsing failed, using fallback translation")
            
            # Enhanced fallback with better Hindi translations
            fallback_translations = {
                "hi": {
                    "advice": f"कृषि सलाह: {advice}",
                    "explanation": f"विवरण: {explanation}",
                    "default_advice": "आपके खेती संबंधी प्रश्न के लिए विशेषज्ञ सलाह उपलब्ध है। कृपया स्थानीय कृषि कार्यालय से संपर्क करें।",
                    "default_explanation": "विस्तृत जानकारी के लिए कृषि विशेषज्ञ से सलाह लें।"
                },
                "pa": {
                    "advice": f"ਖੇਤੀ ਸਲਾਹ: {advice}",
                    "explanation": f"ਵਿਆਖਿਆ: {explanation}",
                    "default_advice": "ਤੁਹਾਡੇ ਖੇਤੀ ਸਬੰਧੀ ਸਵਾਲ ਲਈ ਮਾਹਰ ਸਲਾਹ ਉਪਲਬਧ ਹੈ।",
                    "default_explanation": "ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਲਈ ਖੇਤੀ ਮਾਹਰ ਨਾਲ ਸਲਾਹ ਕਰੋ।"
                },
                "gu": {
                    "advice": f"કૃષિ સલાહ: {advice}",
                    "explanation": f"સમજૂતી: {explanation}",
                    "default_advice": "તમારા ખેતી સંબંધિત પ્રશ્ન માટે નિષ્ણાત સલાહ ઉપલબ્ધ છે।",
                    "default_explanation": "વિગતવાર માહિતી માટે કૃષિ નિષ્ણાત સાથે સલાહ કરો।"
                }
            }
            
            fallback = fallback_translations.get(user_language, {
                "advice": f"Agricultural advice in {target_lang}: {advice}",
                "explanation": f"Explanation in {target_lang}: {explanation}",
                "default_advice": f"Expert agricultural advice available in {target_lang}.",
                "default_explanation": f"Detailed information available in {target_lang}."
            })
            
            final_advice = fallback.get("advice", fallback["default_advice"])
            final_explanation = fallback.get("explanation", fallback["default_explanation"])
            
            return {
                "translation": {
                    "detected_language": "en",
                    "target_language": user_language,
                    "translated_query": state.get("raw_query", ""),
                    "translated_response": final_advice,
                    "translated_explanation": final_explanation,
                    "original_advice": advice,
                    "original_explanation": explanation,
                    "fallback_used": True
                },
                "decision": {
                    **decision,
                    "final_advice": final_advice,
                    "explanation": final_explanation,
                    "original_advice": advice,
                    "original_explanation": explanation
                }
            }
            
    except Exception as e:
        logger.error(f"[TranslationAgent] Translation failed: {e}")
        print(f"💥 Translation error: {e}")
        return {}
