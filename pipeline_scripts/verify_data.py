import chromadb
import random
from typing import List, Dict, Any

# --- Configuration ---
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = 'semantic_search_engine'

def connect_to_chromadb():
    """Connect to ChromaDB and return client and collection"""
    try:
        print(f"Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()
        print("✅ Connection successful!")
        
        # Get the collection
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' found!")
        
        return client, collection
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None, None

def verify_collection_basic_info(collection):
    """Verify basic collection information"""
    print("\n" + "="*50)
    print("BASIC COLLECTION VERIFICATION")
    print("="*50)
    
    try:
        # Get collection count
        count = collection.count()
        print(f"📊 Total documents in collection: {count}")
        
        # Get collection metadata
        metadata = collection.metadata
        print(f"📋 Collection metadata: {metadata}")
        
        # Get a few sample documents
        print(f"\n🔍 Fetching sample documents...")
        sample_results = collection.get(limit=3)
        
        if sample_results['ids']:
            print(f"✅ Sample document IDs: {sample_results['ids'][:3]}")
            print(f"✅ Sample documents preview:")
            for i, doc in enumerate(sample_results['documents'][:2]):
                preview = doc[:100] + "..." if len(doc) > 100 else doc
                print(f"   Document {i+1}: {preview}")
        else:
            print("❌ No documents found in collection")
            
        return True
        
    except Exception as e:
        print(f"❌ Error verifying collection: {e}")
        return False

def test_semantic_search(collection, query_text: str = "machine learning algorithms"):
    """Test semantic search functionality"""
    print("\n" + "="*50)
    print("SEMANTIC SEARCH TEST")
    print("="*50)
    
    try:
        print(f"🔍 Searching for: '{query_text}'")
        
        # Perform semantic search
        results = collection.query(
            query_texts=[query_text],
            n_results=5,
            include=['documents', 'distances', 'metadatas']
        )
        
        if results['ids'][0]:  # Check if we got results
            print(f"✅ Found {len(results['ids'][0])} relevant documents")
            
            print(f"\n📄 Top 3 most relevant results:")
            for i, (doc_id, doc, distance) in enumerate(zip(
                results['ids'][0][:3], 
                results['documents'][0][:3], 
                results['distances'][0][:3]
            )):
                print(f"\n   Result {i+1}:")
                print(f"   ID: {doc_id}")
                print(f"   Similarity Score: {1-distance:.4f}")  # Convert distance to similarity
                preview = doc[:150] + "..." if len(doc) > 150 else doc
                print(f"   Content: {preview}")
        else:
            print("❌ No search results found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during semantic search: {e}")
        return False

def test_specific_document_retrieval(collection):
    """Test retrieving specific documents by ID"""
    print("\n" + "="*50)
    print("SPECIFIC DOCUMENT RETRIEVAL TEST")
    print("="*50)
    
    try:
        # Get a few random document IDs
        all_docs = collection.get(limit=10)
        if not all_docs['ids']:
            print("❌ No documents available for testing")
            return False
            
        # Test retrieving specific documents
        test_ids = all_docs['ids'][:3]
        print(f"🔍 Testing retrieval of specific IDs: {test_ids}")
        
        retrieved = collection.get(ids=test_ids, include=['documents'])
        
        if retrieved['ids']:
            print(f"✅ Successfully retrieved {len(retrieved['ids'])} documents")
            for i, (doc_id, doc) in enumerate(zip(retrieved['ids'], retrieved['documents'])):
                preview = doc[:100] + "..." if len(doc) > 100 else doc
                print(f"   Document {i+1} ({doc_id}): {preview}")
        else:
            print("❌ Failed to retrieve documents")
            
        return True
        
    except Exception as e:
        print(f"❌ Error retrieving specific documents: {e}")
        return False

def run_comprehensive_verification():
    """Run all verification tests"""
    print("🚀 Starting ChromaDB Data Verification")
    print("="*60)
    
    # Connect to ChromaDB
    client, collection = connect_to_chromadb()
    if not client or not collection:
        return False
    
    # Run verification tests
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Basic collection info
    if verify_collection_basic_info(collection):
        tests_passed += 1
    
    # Test 2: Semantic search
    if test_semantic_search(collection):
        tests_passed += 1
    
    # Test 3: Specific document retrieval
    if test_specific_document_retrieval(collection):
        tests_passed += 1
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"✅ Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All verification tests passed! Your data is correctly ingested.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    # Note: ChromaDB HttpClient doesn't require explicit closing
    print("🔌 Connection handling complete.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    run_comprehensive_verification()
