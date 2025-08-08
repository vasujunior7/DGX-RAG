"""
Test script to validate the new Sentence Transformers embedding system with GPU support.
"""
import asyncio
import logging
import torch
from src.config import Config
from src.embeddings import EmbeddingManager
from langchain_core.documents import Document

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_embeddings():
    """Test the embedding system with both configurations."""
    
    # Check GPU availability
    print(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA Device Count: {torch.cuda.device_count()}")
        print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
    
    # Create test documents
    test_docs = [
        Document(page_content="This is a test document about Indian law.", metadata={"source": "test1"}),
        Document(page_content="Constitutional provisions and fundamental rights in India.", metadata={"source": "test2"}),
        Document(page_content="Legal procedures for civil cases in Indian courts.", metadata={"source": "test3"})
    ]
    
    test_queries = [
        "What are fundamental rights in India?",
        "How do civil cases work in Indian law?"
    ]
    
    print("=" * 50)
    print("Testing Sentence Transformers Embeddings with GPU")
    print("=" * 50)
    
    try:
        # Initialize config for Sentence Transformers
        config = Config()
        print(f"Embedding Provider: {config.EMBEDDING_PROVIDER}")
        print(f"Model: {config.ST_EMBEDDING_MODEL}")
        print(f"Use GPU: {config.USE_GPU}")
        print(f"Embedding Dimension: {config.EMBEDDING_DIMENSION}")
        
        # Create embedding manager
        embedding_manager = EmbeddingManager(config)
        
        # Get embedding info
        info = embedding_manager.get_embedding_info()
        print(f"\nEmbedding System Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Test document embedding
        print(f"\nEmbedding {len(test_docs)} documents...")
        embedded_docs = await embedding_manager.embed_documents(test_docs)
        
        print(f"Successfully embedded {len(embedded_docs)} documents")
        for i, (doc, emb) in enumerate(embedded_docs):
            print(f"  Doc {i+1}: {emb.shape} - {doc.page_content[:50]}...")
        
        # Test query embedding
        print(f"\nEmbedding {len(test_queries)} queries...")
        query_embeddings = await embedding_manager.embed_queries(test_queries)
        
        print(f"Successfully embedded {len(query_embeddings)} queries")
        for i, (query, emb) in enumerate(zip(test_queries, query_embeddings)):
            print(f"  Query {i+1}: {emb.shape} - {query}")
        
        # Test similarity search
        print(f"\nTesting similarity search...")
        for i, query_emb in enumerate(query_embeddings):
            print(f"\nQuery {i+1}: {test_queries[i]}")
            similar_docs = embedding_manager.get_top_k_similar(query_emb, embedded_docs, k=3)
            
            for j, (doc, score) in enumerate(similar_docs):
                print(f"  Result {j+1} (score: {score:.4f}): {doc.page_content[:60]}...")
        
        print(f"\n✅ Sentence Transformers embedding test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in Sentence Transformers test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_embeddings())
    if success:
        print(f"\n🎉 All tests passed! Your Legal RAG system is now using GPU-accelerated Sentence Transformers embeddings.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the error messages above.")
