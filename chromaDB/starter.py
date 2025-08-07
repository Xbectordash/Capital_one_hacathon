"""
Starter script for using ChromaDB with the helper functions.
"""
from chromadb_helper import create_collection, get_collection, add_document

if __name__ == "__main__":
    # Create or get a collection
    collection = create_collection("my_collection")
    # Add a document
    doc = {"id": "1", "content": "Hello, ChromaDB!"}
    add_document(collection, doc)
    print("Document added to ChromaDB.")
