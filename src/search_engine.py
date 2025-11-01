import streamlit as st
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.semantic_search import semantic_search, test_connection, get_chromadb_client
from src.baseline import search_baseline

# --- Configuration ---
st.set_page_config(page_title="Data Science Q&A", page_icon="🧠", layout="wide")


def fetch_documents_by_ids(doc_ids: list) -> dict:
    """
    Fetch document text by IDs from ChromaDB.
    
    Args:
        doc_ids: List of document IDs to fetch
        
    Returns:
        Dictionary mapping document ID to document text
    """
    try:
        client, collection = get_chromadb_client()
        retrieved = collection.get(ids=doc_ids, include=['documents'])
        
        doc_dict = {}
        if retrieved.get('ids') and retrieved.get('documents'):
            for doc_id, doc_text in zip(retrieved['ids'], retrieved['documents']):
                doc_dict[doc_id] = doc_text
        return doc_dict
    except Exception as e:
        st.error(f"Error fetching documents: {e}")
        return {}

# --- Streamlit App Code ---
# Test connection and set session state
if test_connection():
    st.session_state.db_connected = True
else:
    st.error("Failed to connect to ChromaDB", icon="🚨")
    st.warning("Please ensure the ChromaDB Docker container is running.")
    st.session_state.db_connected = False

# Check if baseline model is available
if 'baseline_available' not in st.session_state:
    # Try to import and check if baseline model is loaded
    try:
        from src.baseline import vectorizer
        st.session_state.baseline_available = vectorizer is not None
    except:
        st.session_state.baseline_available = False

# --- UI Elements ---
st.title("🧠 Data Science Q&A System")
st.markdown(
    "Ask a question about data science, and the system will retrieve the most relevant documents using both TF-IDF baseline and semantic search models."
)

# Sidebar for settings
with st.sidebar:
    st.header("Search Settings")
    n_results = st.slider("Number of results", 1, 10, 5)
    show_full_text = st.checkbox("Show full text (not truncated)", value=True)
    
    # Model status indicators
    st.header("Model Status")
    if st.session_state.db_connected:
        st.success("✅ Semantic Search (ChromaDB) - Connected")
    else:
        st.error("❌ Semantic Search (ChromaDB) - Not Connected")
    
    if st.session_state.baseline_available:
        st.success("✅ Baseline (TF-IDF) - Available")
    else:
        st.warning("⚠️ Baseline (TF-IDF) - Not Available")

query = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is LSTM?",
    disabled=not st.session_state.db_connected # Disable input if DB is not connected
)

if st.button("Search", type="primary", disabled=not st.session_state.db_connected):
    if query:
        with st.spinner("Searching with both models..."):
            # Run both searches in parallel
            semantic_results = []
            baseline_results = []
            
            # Semantic search
            if st.session_state.db_connected:
                semantic_results = semantic_search(query, n_results=n_results)
            
            # Baseline search
            if st.session_state.baseline_available:
                baseline_results_raw = search_baseline(query, n_results=n_results)
                # Fetch document text for baseline results
                if baseline_results_raw:
                    baseline_ids = [r['id'] for r in baseline_results_raw]
                    doc_texts = fetch_documents_by_ids(baseline_ids)
                    
                    # Format baseline results to match semantic results structure
                    baseline_results = []
                    for result in baseline_results_raw:
                        doc_id = result['id']
                        baseline_results.append({
                            'id': doc_id,
                            'score': result['score'],
                            'document': doc_texts.get(doc_id, "Document text not available"),
                            'similarity': result['score']  # Use score as similarity for baseline
                        })
            
            # --- Display Results Side-by-Side ---
            if semantic_results or baseline_results:
                # Create two columns for side-by-side display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"🔍 Semantic Search ({len(semantic_results)} results)")
                    if semantic_results:
                        for i, result in enumerate(semantic_results):
                            with st.container():
                                st.markdown(f"**Result {i+1}** - ID: `{result['id']}`")
                                st.metric("Similarity", f"{result['similarity']:.4f}")
                                
                                # Display document content
                                if show_full_text:
                                    st.write(result['document'])
                                else:
                                    truncated = result['document'][:500] + "..." if len(result['document']) > 500 else result['document']
                                    st.write(truncated)
                                    if len(result['document']) > 500:
                                        with st.expander("Show full text"):
                                            st.write(result['document'])
                                st.divider()
                    else:
                        st.warning("No results from semantic search.")
                
                with col2:
                    st.subheader(f"📊 Baseline (TF-IDF) ({len(baseline_results)} results)")
                    if baseline_results:
                        for i, result in enumerate(baseline_results):
                            with st.container():
                                st.markdown(f"**Result {i+1}** - ID: `{result['id']}`")
                                st.metric("Similarity", f"{result['similarity']:.4f}")
                                
                                # Display document content
                                if show_full_text:
                                    st.write(result['document'])
                                else:
                                    truncated = result['document'][:500] + "..." if len(result['document']) > 500 else result['document']
                                    st.write(truncated)
                                    if len(result['document']) > 500:
                                        with st.expander("Show full text"):
                                            st.write(result['document'])
                                st.divider()
                    else:
                        if st.session_state.baseline_available:
                            st.warning("No results from baseline search.")
                        else:
                            st.info("Baseline model not available. Please run 'wsl_scripts/build_baseline.py' to build the model.")
            else:
                st.warning("No relevant documents found from either model.")
    else:
        st.warning("Please enter a question.")