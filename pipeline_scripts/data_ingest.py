import pickle
import chromadb
from tqdm import tqdm

# --- Configuration ---
INPUT_PATH = "data/embeddings.pkl"
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = 'semantic_search_engine'

# --- Main ---
def load_embeddings_data(file_path):
    """
    Load embeddings data from pickle file
    """
    try:
        print(f"Loading embeddings from {file_path}...")
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        
        # Validate required keys
        required_keys = ['ids', 'embeddings', 'documents']
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Missing required key '{key}' in pickle file")
        
        ids = data['ids']
        embeddings = data['embeddings']
        documents = data['documents']
        
        # Validate data consistency
        if not (len(ids) == len(embeddings) == len(documents)):
            raise ValueError("Inconsistent data lengths: ids, embeddings, and documents must have the same length")
        
        print(f"Loaded {len(ids)} documents and embeddings.")
        return ids, embeddings, documents
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        raise
    except Exception as e:
        print(f"Error loading embeddings data: {e}")
        raise

def data_ingest():
    """
    Loads data from a pickle file into ChromaDB collection
    """
    # 1. Load the data from the pickle file
    try:
        ids, embeddings, documents = load_embeddings_data(INPUT_PATH)
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    # 2. Connect to ChromaDB
    print(f"Connecting to DB instance at {CHROMA_HOST}:{CHROMA_PORT}...")
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        # Check connection
        client.heartbeat()
        print("Connection to ChromaDB established.")
    except Exception as e:
        print(f"Failed to establish a connection to ChromaDB: {e}")
        return

    try:
        # 3. Create or get the collection
        # A collection is like a table in a traditional database.
        print(f"Creating or getting collection {COLLECTION_NAME}...")
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Collection {COLLECTION_NAME} created or retrieved.")
        
        # 4. Add the data to the collection
        # ChromaDB's .add() method is highly optimized for this.
        # We convert embeddings to a list as it's the expected format.

        print(f"Adding {len(ids)} documents to {COLLECTION_NAME}...(This may take a while)")
        
        # Add the data in batches to be memory-efficient and provide progress.
        batch_size = 100

        for i in tqdm(range(0, len(ids), batch_size), desc="Adding documents to ChromaDB"):
            collection.add(
                ids=ids[i:i+batch_size],
                documents=documents[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size]
            )
        
        print(f"Documents added to {COLLECTION_NAME}.")
        
        # 5. Get final count and close the connection
        count = collection.count()
        print(f"--------------------------------")
        print(f"Successfully added {count} documents to the '{COLLECTION_NAME}' collection.")
        print(f"--------------------------------")
        
        print("Done!")
        print("-" * 50)
        print("Data ingestion completed successfully.")
        print("-" * 50)
        
    except Exception as e:
        print(f"Failed to ingest data: {e}")
        return
    finally:
        # Note: ChromaDB HttpClient doesn't require explicit closing
        print("Connection handling complete.")

if __name__ == "__main__":
    data_ingest()   
       

