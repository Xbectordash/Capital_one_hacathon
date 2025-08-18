#!/usr/bin/env python3
"""
Multi-Label Agricultural Intent Classification Tester
=====================================================
This script tests the multi-label agricultural intent classification model 
that can predict multiple intents for a single query.

Usage: python test_multilabel_model.py
"""

import pickle
import string
import numpy as np

def clean_text(text):
    """Clean and preprocess text"""
    if not text:
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    return text

def predict_multilabel(query, model, vectorizer, binarizer, threshold=0.3):
    """Predict multiple intents for a query"""
    cleaned_query = clean_text(query)
    query_vector = vectorizer.transform([cleaned_query])
    
    # Get prediction probabilities
    prediction_probs = model.predict_proba(query_vector)
    
    # Extract probabilities for each class
    class_probs = []
    for i, class_name in enumerate(binarizer.classes_):
        prob = prediction_probs[i][0][1] if len(prediction_probs[i][0]) > 1 else prediction_probs[i][0][0]
        class_probs.append((class_name, prob))
    
    # Sort by probability
    class_probs.sort(key=lambda x: x[1], reverse=True)
    
    # Get predictions above threshold
    predicted_intents = []
    for intent, prob in class_probs:
        if prob > threshold:
            predicted_intents.append(intent)
    
    # If no intent above threshold, take the highest one
    if not predicted_intents:
        predicted_intents = [class_probs[0][0]]
    
    return predicted_intents, class_probs

def load_multilabel_model():
    """Load the multi-label model components"""
    try:
        print("📂 Loading multi-label model...")
        
        # Fixed paths to point to model directory
        with open('../model/agricultural_multilabel_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("✅ Multi-label model loaded")
        
        with open('../model/multilabel_binarizer.pkl', 'rb') as f:
            binarizer = pickle.load(f)
        print("✅ Multi-label binarizer loaded")
        
        with open('../model/multilabel_tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        print("✅ TF-IDF vectorizer loaded")
        
        return model, vectorizer, binarizer
        
    except FileNotFoundError as e:
        print(f"❌ Error: Model file not found - {e}")
        return None, None, None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None

def test_multilabel_model():
    """Test the multi-label model with sample queries"""
    print("🌾 MULTI-LABEL AGRICULTURAL INTENT CLASSIFIER")
    print("="*60)
    
    # Load model
    model, vectorizer, binarizer = load_multilabel_model()
    if model is None:
        return
    
    print(f"\n📊 Model Info:")
    print(f"Available intent classes: {list(binarizer.classes_)}")
    print(f"Number of classes: {len(binarizer.classes_)}")
    
    # Test queries that should have multiple intents
    test_queries = [
        "Will rain affect my soil quality?",
        "Government weather advisory for crop protection",
        "Market prices during drought season",
        "Soil testing before rainy season planting", 
        "Weather forecast for fertilizer application",
        "Pest control in wet soil conditions",
        "Government subsidy for drought-resistant crops",
        "Market demand for organic crops in rainy season",
        "Soil health monitoring during monsoon"
    ]
    
    print(f"\n🧪 TESTING WITH {len(test_queries)} MULTI-INTENT QUERIES:")
    print("="*70)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        
        # Test with different thresholds
        predicted_intents_low, all_scores = predict_multilabel(
            query, model, vectorizer, binarizer, threshold=0.2
        )
        predicted_intents_high, _ = predict_multilabel(
            query, model, vectorizer, binarizer, threshold=0.4
        )
        
        print(f"   Multi-Label (threshold 0.2): {predicted_intents_low}")
        print(f"   Multi-Label (threshold 0.4): {predicted_intents_high}")
        
        # Show top scores
        top_scores = all_scores[:4]
        scores_str = ", ".join([f"{intent}: {score:.2f}" for intent, score in top_scores])
        print(f"   All Scores: {scores_str}")
    
    # Interactive mode
    print(f"\n🌱 INTERACTIVE MODE")
    print("Enter your agricultural queries (type 'quit' to exit):")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n🌾 Your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q', '']:
                print("👋 Goodbye!")
                break
            
            predicted_intents, all_scores = predict_multilabel(
                query, model, vectorizer, binarizer, threshold=0.25
            )
            
            print(f"🎯 Predicted Intents: {predicted_intents}")
            
            # Show confidence scores
            print(f"📊 Confidence Scores:")
            for intent, score in all_scores[:5]:
                print(f"   {intent}: {score:.3f} ({score*100:.1f}%)")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multilabel_model()
