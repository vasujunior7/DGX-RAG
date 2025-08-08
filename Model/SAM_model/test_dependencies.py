"""
Quick dependency test for Legal Query RAG system.
Tests that all critical dependencies can be imported and work correctly.
"""
import sys
import os

def test_sentence_transformers():
    """Test sentence-transformers and CrossEncoder import."""
    try:
        from sentence_transformers import CrossEncoder
        print("✅ sentence-transformers CrossEncoder imported successfully")
        
        # Try to create a model instance (this will download if not cached)
        print("🔄 Testing CrossEncoder model loading...")
        model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2')  # Smaller model for testing
        print("✅ CrossEncoder model loaded successfully")
        
        # Test prediction
        pairs = [['What is AI?', 'Artificial Intelligence is a branch of computer science.']]
        score = model.predict(pairs)
        print(f"✅ CrossEncoder prediction test passed: {score[0]:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Error with sentence-transformers: {e}")
        return False

def test_langchain_openai():
    """Test langchain-openai imports."""
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        print("✅ langchain-openai imported successfully")
        
        # Test if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("✅ OpenAI API key found")
        else:
            print("⚠️  OpenAI API key not set (set OPENAI_API_KEY environment variable)")
        
        return True
    except Exception as e:
        print(f"❌ Error with langchain-openai: {e}")
        return False

def test_faiss():
    """Test FAISS import and basic functionality."""
    try:
        import faiss
        import numpy as np
        
        print("✅ FAISS imported successfully")
        
        # Test basic functionality
        d = 64  # dimension
        nb = 100  # database size
        np.random.seed(1234)
        xb = np.random.random((nb, d)).astype('float32')
        
        # Build index
        index = faiss.IndexFlatL2(d)
        index.add(xb)
        
        print(f"✅ FAISS basic functionality test passed (indexed {index.ntotal} vectors)")
        return True
        
    except Exception as e:
        print(f"❌ Error with FAISS: {e}")
        return False

def test_core_modules():
    """Test our core modules can be imported."""
    try:
        from src.config import Config
        from src.legal_query_rag import LegalQueryRAG
        from Model.SAM_model.inference import LegalRAGInference
        print("✅ Core modules imported successfully")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded: {config.LLM_MODEL}")
        
        return True
    except Exception as e:
        print(f"❌ Error with core modules: {e}")
        return False

def main():
    """Run all dependency tests."""
    print("🧪 Legal Query RAG Dependency Test")
    print("=" * 50)
    
    tests = [
        ("Core Modules", test_core_modules),
        ("FAISS Vector Database", test_faiss),
        ("Sentence Transformers", test_sentence_transformers),
        ("LangChain OpenAI", test_langchain_openai),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All dependencies are working correctly!")
        print("\n✅ Your system is ready to run the Legal Query RAG system.")
        print("\nNext steps:")
        print("1. Set OpenAI API key: $env:OPENAI_API_KEY='your-key'")
        print("2. Run example: python example_usage.py")
    else:
        print("\n⚠️  Some dependencies have issues.")
        print("\nTroubleshooting:")
        if passed >= 2:  # Core and FAISS work
            print("✅ Core functionality should work")
            print("⚠️  Some advanced features may be limited")
        
        print("\nTo install missing dependencies:")
        print("pip install langchain langchain-openai sentence-transformers faiss-cpu")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
