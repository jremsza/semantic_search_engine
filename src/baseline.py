import os
import joblib
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
# 1. Load the pre-built model components
# Get the project root (parent of src directory)
try:
    PROJECT_ROOT = Path(__file__).parent.parent
    MODEL_DIR = PROJECT_ROOT / 'models'
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"MODEL_DIR: {MODEL_DIR}")
except Exception as e:
    print(f"Error setting up paths: {e}")
    PROJECT_ROOT = None
    MODEL_DIR = None

try:
    if MODEL_DIR is None:
        raise FileNotFoundError("MODEL_DIR is None - path setup failed")
    
    vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.joblib")
    tfidf_matrix = joblib.load(MODEL_DIR / "tfidf_matrix.joblib")
    doc_ids = joblib.load(MODEL_DIR / "tfidf_ids.joblib")
    print("Loaded model components successfully.")
except (FileNotFoundError, TypeError) as e:
    print(f"Error: Model components not found in {MODEL_DIR} directory. Please run 'wsl_scripts/build_baseline.py' to build the baseline model.")
    print(f"Error details: {e}")
    vectorizer, tfidf_matrix, doc_ids = None, None, None


def search_baseline(query: str, n_results: int = 5) -> list[dict]:
    """
    Performs a TF-IDF search on the pre-built index.
    
    Args:
        query: The search query string.
        n_results: The number of top results to return.
        
    Returns:
        A list of dictionaries, each containing 'id' and 'score'.
    """
    if vectorizer is None:
        return []
        
    # 1. Transform the query into a TF-IDF vector
    query_vector = vectorizer.transform([query])
    print(f"Query vector shape: {query_vector.shape}")
    print(f"Query vector: {query_vector.toarray()}")
            
    # 2. Compute the cosine similarity between the query and the corpus
    scores = cosine_similarity(tfidf_matrix, query_vector).flatten()
    print(f"Cosine similarities: {scores}")

    # 3. Get the indices of the top-n results
    top_n_indices = scores.argsort()[-n_results:][::-1]
    print(f"Top {n_results} indices: {top_n_indices}")

    #4. Format the results
    results = []
    for idx in top_n_indices:
        results.append({
        'id': doc_ids[idx],
        'score': scores[idx]
        })
    return results
    
if __name__ == "__main__":
    print("Testing the baseline model...")
    print("-" * 60)
    test_query = "what is ridge regression?"
    print(f"Testing query: '{test_query}'")
    results = search_baseline(test_query, n_results=3)

    if results:
        print(f"Results for '{test_query}':")
        for result in results:
            print(f"  ID: {result['id']}, Score: {result['score']:.4f}")
    else:
        print("No results found.")
    print("-" * 60)
    print("Test complete.")
    print("-" * 60)