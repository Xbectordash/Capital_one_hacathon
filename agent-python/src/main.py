from graph_arc.graph import workflow
import json

def main():
    # Example initial state
    initial_state = {
        "user_id": "user123",
        "raw_query": "What is the weather forecast for the next week, current soil moisture levels, market price trends for wheat, pest infestation alerts, and government subsidies available in Punjabm?",
        "language": "hi"
    }
    result = workflow.invoke(initial_state)
    
    # Debug: Print the result structure to understand what we're getting
    print("DEBUG - Full result keys:", result.keys())
    if "translation" in result:
        print("DEBUG - Translation content:", result["translation"])
    if "decision" in result:
        print("DEBUG - Decision content keys:", result["decision"].keys() if isinstance(result["decision"], dict) else "Not a dict")
    
    # Check if translation is available and user language is not English
    user_language = result.get('language', 'en').lower()
    has_translation = "translation" in result and result["translation"].get('translated_response')
    
    print(f"DEBUG - User language: {user_language}")
    print(f"DEBUG - Has translation: {has_translation}")
    
    # Determine final content to display
    if has_translation and user_language not in ['en', 'english']:
        # Show translated version
        translation = result["translation"]
        final_advice = translation.get('translated_response', 'कोई अनुवाद उपलब्ध नहीं')
        final_explanation = translation.get('translated_explanation', 'कोई विवरण उपलब्ध नहीं')
        header = "🌾 कृषि सलाहकार प्रणाली - अंतिम सिफारिश"
        advice_label = "💡 अंतिम सलाह:"
        explanation_label = "📋 विस्तृत विवरण:"
        show_explanation = True
    else:
        # Show English version
        decision = result.get("decision", {})
        final_advice = decision.get('final_advice', 'No advice available')
        final_explanation = decision.get('explanation', 'No explanation available')
        header = "🌾 AGRICULTURAL ADVISORY SYSTEM - FINAL RECOMMENDATION"
        advice_label = "💡 FINAL ADVICE:"
        explanation_label = "📋 EXPLANATION:"
        show_explanation = True
    
    # Display the final result
    print("\n" + "="*60)
    print(header)
    print("="*60)
    print(f"\n📍 Query: {result.get('raw_query', 'N/A')}")
    print(f"🌍 Location: {result.get('location', 'N/A')}")
    print(f"🗣️ Language: {result.get('language', 'N/A')}")
    print(f"🎯 Detected Intents: {', '.join(result.get('intents', []))}")
    print("\n" + "-"*40)
    print(advice_label)
    print("-"*40)
    print(final_advice)
    
    # Show explanation if available
    if show_explanation and final_explanation:
        print("\n" + "-"*40)
        print(explanation_label)
        print("-"*40)
        print(final_explanation)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
