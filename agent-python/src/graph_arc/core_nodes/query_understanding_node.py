from src.utils.loggers import get_logger
from src.graph_arc.state import GlobalState
import pickle
import string
import os

# Simple intent classifier using trained model
model = None
vectorizer = None
binarizer = None

def load_intent_model():
    """Load trained model once"""
    global model, vectorizer, binarizer
    if model is not None:
        return True
    
    try:
        # Get model directory - go up from current file to agent-python root, then to model
        current_dir = os.path.dirname(__file__)  # core_nodes
        graph_arc_dir = os.path.dirname(current_dir)  # graph_arc  
        src_dir = os.path.dirname(graph_arc_dir)  # src
        agent_python_dir = os.path.dirname(src_dir)  # agent-python
        model_dir = os.path.join(agent_python_dir, "model")
        
        with open(os.path.join(model_dir, "agricultural_multilabel_model.pkl"), 'rb') as f:
            model = pickle.load(f)
        
        with open(os.path.join(model_dir, "multilabel_binarizer.pkl"), 'rb') as f:
            binarizer = pickle.load(f)
            
        with open(os.path.join(model_dir, "multilabel_tfidf_vectorizer.pkl"), 'rb') as f:
            vectorizer = pickle.load(f)
        
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def clean_text(text):
    """Clean text for model"""
    if not text:
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(text.split())

def get_intents(query, threshold=0.3):
    """Get intents using trained model"""
    if not load_intent_model():
        return [], 0.0
    
    cleaned = clean_text(query)
    query_vector = vectorizer.transform([cleaned])
    prediction_probs = model.predict_proba(query_vector)
    
    intents = []
    max_prob = 0.0
    
    for i, class_name in enumerate(binarizer.classes_):
        prob = prediction_probs[i][0][1] if len(prediction_probs[i][0]) > 1 else prediction_probs[i][0][0]
        if prob > threshold:
            intents.append(class_name)
        max_prob = max(max_prob, prob)
    
    if not intents and len(binarizer.classes_) > 0:
        # Get highest probability intent
        best_idx = 0
        best_prob = 0
        for i, class_name in enumerate(binarizer.classes_):
            prob = prediction_probs[i][0][1] if len(prediction_probs[i][0]) > 1 else prediction_probs[i][0][0]
            if prob > best_prob:
                best_prob = prob
                best_idx = i
        intents = [binarizer.classes_[best_idx]]
        max_prob = best_prob
    
    return intents, max_prob

def understand_query(state: GlobalState, config=None) -> GlobalState:
    logger = get_logger("query_understanding_node")
    
    query = state.get("raw_query", "")
    logger.info(f"Using trained model for intent classification: {query}")
    
    # Get intents using trained model
    intents, confidence = get_intents(query)
    
    # Simple entity extraction
    entities = extract_entities(query)
    
    state["intents"] = intents
    state["entities"] = entities
    state["confidence_score"] = confidence
    
    logger.info(f"Predicted intents: {intents}, confidence: {confidence}")
    logger.info(f"Extracted entities: {entities}")
    
    return state

def extract_entities(query: str) -> dict:
    """Simple entity extraction for agricultural terms"""
    query_lower = query.lower()
    entities = {}
    
    # Common crops
    crops = ['rice', 'wheat', 'cotton', 'sugarcane', 'maize', 'corn', 'soybean', 'potato', 'tomato', 'onion']
    for crop in crops:
        if crop in query_lower:
            entities['commodity'] = crop.title()
            entities['crop'] = crop.title()
            break
    
    # Investment/savings amounts
    import re
    amount_pattern = r'(\d+)\s*lakh'
    amount_match = re.search(amount_pattern, query_lower)
    if amount_match:
        entities['investment'] = f"{amount_match.group(1)} lakh"
    
    # Fertilizer keywords
    fertilizer_keywords = ['fertilize', 'fertilizer', 'manure', 'urea', 'phosphate']
    if any(keyword in query_lower for keyword in fertilizer_keywords):
        entities['fertilizer_needed'] = True
    
    # Market/price keywords
    price_keywords = ['price', 'rate', 'cost', 'market', 'selling']
    if any(keyword in query_lower for keyword in price_keywords):
        entities['price_inquiry'] = True
    
    return entities
