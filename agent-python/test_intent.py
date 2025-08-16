#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.graph_arc.core_nodes.query_understanding_node import get_intents

# Test the problematic query
query = "mai rice ke liye fertilizer use karna chahta hu or uske rates kya hai?"
print(f"Testing query: {query}")

# Test with different thresholds
for threshold in [0.1, 0.2, 0.3, 0.4]:
    intents, confidence = get_intents(query, threshold=threshold)
    print(f"Threshold {threshold}: Intents: {intents}, Confidence: {confidence}")

# Test individual parts
print("\nTesting individual parts:")
intents1, conf1 = get_intents("rice fertilizer", threshold=0.2)
print(f"'rice fertilizer': {intents1}, {conf1}")

intents2, conf2 = get_intents("rates price", threshold=0.2) 
print(f"'rates price': {intents2}, {conf2}")

intents3, conf3 = get_intents("fertilizer soil", threshold=0.2)
print(f"'fertilizer soil': {intents3}, {conf3}")
