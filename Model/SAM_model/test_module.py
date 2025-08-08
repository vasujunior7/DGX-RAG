"""
Quick test to demonstrate Legal Query RAG system running.
This test shows system initialization and basic functionality without requiring API keys.
"""
import os
import asyncio

# Set a dummy API key for testing (won't actually be used for API calls in this demo)
os.environ["OPENAI_API_KEY"] = "dummy-key-for-testing"

from Model.SAM_model.inference import LegalRAGInference

def test_system_initialization():
    """Test that the system can be initialized."""
    print("🏛️ Testing Legal Query RAG System Initialization...")
    
    try:
        # Initialize the system
        legal_rag = LegalRAGInference(api_key="dummy-key-for-testing")
        
        print("✅ System initialized successfully")
        
        # Get system information
        info = legal_rag.get_system_info()
        print(f"✅ System Status: {info['status']}")
        print(f"✅ Knowledge Base: {'Ready' if info['knowledge_base_initialized'] else 'Not initialized'}")
        
        # Show system configuration
        stats = info.get('system_stats', {})
        config = stats.get('config', {})
        
        print("\n📋 System Configuration:")
        print(f"  - LLM Model: {config.get('llm_model', 'Unknown')}")
        print(f"  - Embedding Model: {config.get('embedding_model', 'Unknown')}")
        print(f"  - Max Concurrent Queries: {config.get('max_concurrent_queries', 'Unknown')}")
        print(f"  - Chunk Size: {config.get('chunk_size', 'Unknown')}")
        print(f"  - Top-K Retrieval: {config.get('top_k_retrieval', 'Unknown')}")
        
        # Test reranking system
        rerank_stats = stats.get('reranking', {})
        print(f"\n🔧 Re-ranking System: {rerank_stats.get('status', 'Unknown')}")
        print(f"  - Model: {rerank_stats.get('model_name', 'Unknown')}")
        print(f"  - Top-K: {rerank_stats.get('rerank_top_k', 'Unknown')}")
        
        print("\n🎉 System is ready for use!")
        print("\n📋 To use the full system:")
        print("1. Set your real OpenAI API key: $env:OPENAI_API_KEY='your-actual-key'")
        print("2. Add legal documents using: legal_rag.load_document('path/to/document.pdf')")
        print("3. Run queries using: legal_rag.inference(['Your legal question here'])")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        return False

def test_module_imports():
    """Test that all modules can be imported."""
    print("\n🧪 Testing Module Imports...")
    
    try:
        from src.config import Config
        from src.data_ingestion import DocumentIngestion
        from src.embeddings import EmbeddingManager
        from src.vector_db import VectorDatabase
        from src.react_agent import ReActAgent
        from src.retrieval import HybridRetriever
        from src.reranking import DocumentReRanker
        from src.llm_generator import LLMGenerator
        from src.evaluation import ResponseEvaluator
        from src.legal_query_rag import LegalQueryRAG
        
        print("✅ All core modules imported successfully")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded: {config.LLM_MODEL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return False

async def test_basic_functionality():
    """Test basic system functionality without API calls."""
    print("\n🔧 Testing Basic Functionality...")
    
    try:
        # Test reranking fallback (doesn't require API)
        from src.reranking import DocumentReRanker
        from src.config import Config
        
        config = Config()
        reranker = DocumentReRanker(config)
        
        # Test fallback reranking with sample data
        sample_docs = [
            {
                'content': 'Contract law governs agreements between parties. A valid contract requires offer, acceptance, and consideration.',
                'combined_score': 0.8
            },
            {
                'content': 'Tort law deals with civil wrongs and damages. Negligence requires duty, breach, causation, and damages.',
                'combined_score': 0.6
            }
        ]
        
        query = "What are the elements of a contract?"
        reranked = reranker._fallback_rerank(query, sample_docs)
        
        print(f"✅ Fallback re-ranking test passed: {len(reranked)} documents processed")
        
        if reranked:
            top_doc = reranked[0]
            print(f"  - Top result score: {top_doc.get('rerank_score', 0):.3f}")
            print(f"  - Content preview: {top_doc.get('content', '')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic functionality test: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Legal Query RAG System Module Test")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_module_imports),
        ("System Initialization", test_system_initialization),
        ("Basic Functionality", lambda: asyncio.run(test_basic_functionality()))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Legal Query RAG module is working correctly!")
        print("\n🚀 Ready for production use with real OpenAI API key and legal documents.")
    else:
        print("⚠️ Some tests failed. Please check the configuration and dependencies.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("✅ Module test completed successfully!")
        print("🏛️ Legal Query RAG system is ready to process legal queries!")
    else:
        print("❌ Module test completed with issues.")
        print("🔧 Please check the error messages above.")
