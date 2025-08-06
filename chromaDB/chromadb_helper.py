"""
Helper functions for interacting with ChromaDB.
"""

import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client
client = chromadb.Client(Settings())

def create_collection(name):
    """Create a new collection in ChromaDB."""
    return client.create_collection(name)

def get_collection(name):
    """Get an existing collection by name."""
    return client.get_collection(name)

# Example: Add a document to a collection
def add_document(collection, document, metadata=None):
    """Add a document to a ChromaDB collection."""
    return collection.add(document, metadata=metadata)
