import chromadb

# Quick verification script
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = 'semantic_search_engine'

def quick_verify():
    """Quick verification of ChromaDB data"""
    try:
        # Connect
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collection = client.get_collection(name=COLLECTION_NAME)
        
        # Get basic info
        count = collection.count()
        print(f"📊 Documents in collection: {count}")
        
        # Test a simple search
        results = collection.query(
            query_texts=["data science"],
            n_results=3,
            include=['documents']
        )
        
        print(f"🔍 Search test - found {len(results['ids'][0])} results")
        if results['documents'][0]:
            print(f"📄 Sample result: {results['documents'][0][0][:100]}...")
        
        print("✅ Verification successful!")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    quick_verify()
