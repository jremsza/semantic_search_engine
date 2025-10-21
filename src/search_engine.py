import streamlit as st
import chromadb

# --- Configuration ---
st.set_page_config(page_title="Data Science Q&A", page_icon="🧠")

CHROMA_HOST = "localhost"
CHROMA_PORT = "8000"
COLLECTION_NAME = "semantic_search_engine"

# --- ChromaDB Connection ---
# Use a try-except block to handle connection errors gracefully
try:
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = client.get_collection(name=COLLECTION_NAME)
    st.session_state.db_connected = True
except Exception as e:
    st.error(f"Failed to connect to ChromaDB: {e}", icon="🚨")
    st.warning("Please ensure the ChromaDB Docker container is running.")
    st.session_state.db_connected = False

# --- UI Elements ---
st.title("🧠 Data Science Q&A System")
st.markdown(
    "Ask a question about machine learning, and the system will retrieve the most relevant paragraphs."
)

# Sidebar for settings
with st.sidebar:
    st.header("Search Settings")
    n_results = st.slider("Number of results", 1, 10, 5)
    show_full_text = st.checkbox("Show full text (not truncated)", value=True)

query = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is masked attention?",
    disabled=not st.session_state.db_connected # Disable input if DB is not connected
)

if st.button("Search", type="primary", disabled=not st.session_state.db_connected):
    if query:
        with st.spinner("Searching for answers..."):
            # --- Query ChromaDB Directly ---
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "distances", "metadatas"]
            )

            # --- Display Results ---
            st.subheader(f"Results ({len(results['documents'][0])} found)")
            if results and results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i]
                    doc_id = results["ids"][0][i]
                    
                    # Display result header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Result {i+1}** - ID: {doc_id}")
                    with col2:
                        st.metric("Similarity", f"{1-distance:.3f}")
                    
                    # Display document content
                    if show_full_text:
                        st.write(doc)
                    else:
                        # Show truncated version
                        truncated = doc[:500] + "..." if len(doc) > 500 else doc
                        st.write(truncated)
                        if len(doc) > 500:
                            with st.expander("Show full text"):
                                st.write(doc)
                    
                    st.divider()
            else:
                st.warning("No relevant documents found.")
    else:
        st.warning("Please enter a question.")