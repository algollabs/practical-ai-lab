import os
import qdrant_client
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SentenceSplitter
from shared.utils import init_settings

# Initialize Global Settings (LLM & Embeddings)
init_settings()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "practical_ai_policies"

def get_vector_store():
    """
    Creates and returns the QdrantVectorStore instance.
    
    We use a specific collection name to identify our data in Qdrant.
    """
    # Create a Qdrant client instance
    client = qdrant_client.QdrantClient(url=QDRANT_URL)
    
    # Create the VectorStore wrapper around Qdrant
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name=COLLECTION_NAME
    )
    return vector_store, client

def build_or_load_index():
    """
    Implements 'Smart Loading' strategy for the RAG pipeline.
    
    1. Connects to Qdrant.
    2. Checks if our collection already exists and has data.
    3. If YES: Load the index directly from the vector store (Zero Ingestion).
    4. If NO: Load PDFs, chunk them, index them, and upsert to Qdrant.
    
    Returns:
        VectorStoreIndex: The queryable index.
    """
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    vector_store, client = get_vector_store()
    
    # Smart Loading: Check if collection exists
    # Qdrant client `get_collections` returns an object with a list of collections
    try:
        collections = client.get_collections()
        collection_names = [c.name for c in collections.collections]
        exists = COLLECTION_NAME in collection_names
        
        # If exists, check if it's not empty (count > 0)
        if exists:
            count_result = client.count(collection_name=COLLECTION_NAME)
            if count_result.count == 0:
                exists = False # Exists but empty, so we treat as new
    except Exception as e:
        print(f"Error checking Qdrant status: {e}")
        exists = False

    if exists:
        print(f"✅ Collection '{COLLECTION_NAME}' found. Loading existing index...")
        # To load from an existing vector store, we create a StorageContext with it
        # and use VectorStoreIndex.from_vector_store
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index
    else:
        print(f"⚠️ Collection '{COLLECTION_NAME}' not found or empty. Starting ingestion...")
        
        # 1. Load Data
        if not os.path.exists(DATA_DIR):
            raise FileNotFoundError(f"Data directory not found at: {DATA_DIR}")
            
        print(f"Loading documents from {DATA_DIR}...")
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        print(f"Loaded {len(documents)} documents.")
        
        # 2. Chunking Strategy
        # We explicitly define a splitter to control chunk size/overlap.
        # Chunk size 1024 is a good balance for policy docs.
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
        
        # 3. Create Index (Ingestion)
        # This step automatically:
        # - Splits documents into nodes using the global Settings.transformations (or defaults)
        # - Computes embeddings using global Settings.embed_model
        # - Upserts vectors to Qdrant via storage_context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context,
            transformations=[splitter],
            show_progress=True
        )
        print("✅ Ingestion complete.")
        return index

def get_query_engine():
    """
    Returns a query engine configured for the workshop.
    """
    index = build_or_load_index()
    
    # retrieval_mode='embedding' is standard for dense vector retrieval
    # similarity_top_k=3 gives us the 3 most relevant chunks
    return index.as_query_engine(
        similarity_top_k=3,
        vector_store_query_mode="default" # standard dense retrieval
    )

if __name__ == "__main__":
    # Simple test to ensure pipeline works
    engine = get_query_engine()
    response = engine.query("What is the policy on working from home?")
    print("\n--- Test Response ---")
    print(response)

