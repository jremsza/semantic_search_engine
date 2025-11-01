"""
Semantic search functionality using ChromaDB.
This module provides a clean interface for semantic search without Streamlit dependencies.
"""

import chromadb
from typing import List, Dict, Any, Optional


# --- Configuration ---
CHROMA_HOST = "localhost"
CHROMA_PORT = "8000"
COLLECTION_NAME = "semantic_search_engine"


def get_chromadb_client():
    """Get ChromaDB client and collection"""
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collection = client.get_collection(name=COLLECTION_NAME)
        return client, collection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to ChromaDB: {e}")


def semantic_search(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs semantic search using ChromaDB.
    
    Args:
        query: The search query string
        n_results: Number of results to return
        
    Returns:
        List of dictionaries containing search results with 'id', 'document', 'distance', and 'similarity'
    """
    try:
        client, collection = get_chromadb_client()
        
        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "distances", "metadatas"]
        )
        
        # Format results
        formatted_results = []
        if results and results.get("documents") and results["documents"][0]:
            for i, (doc_id, doc, distance) in enumerate(zip(
                results["ids"][0],
                results["documents"][0], 
                results["distances"][0]
            )):
                formatted_results.append({
                    'id': doc_id,
                    'document': doc,
                    'distance': distance,
                    'similarity': 1 - distance,
                    'metadata': results["metadatas"][0][i] if results.get("metadatas") and results["metadatas"][0] else None
                })
        
        return formatted_results
        
    except Exception as e:
        print(f"Error during semantic search: {e}")
        return []


def test_connection() -> bool:
    """
    Test if ChromaDB connection is working.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        get_chromadb_client()
        print("✅ ChromaDB connection successful")
        return True
    except Exception as e:
        print(f"❌ ChromaDB connection failed: {e}")
        print("Make sure ChromaDB is running: docker-compose up -d")
        return False


if __name__ == "__main__":
    # Test the semantic search function
    print("Testing semantic search...")
    
    if test_connection():
        query = "What is machine learning?"
        results = semantic_search(query, n_results=3)
        
        print(f"\nFound {len(results)} results for: '{query}'")
        print("\n" + "="*50)
        
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"ID: {result['id']}")
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Content: {result['document'][:200]}...")
            print("-" * 30)
