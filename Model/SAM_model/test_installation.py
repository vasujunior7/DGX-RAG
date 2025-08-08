"""
Test script for Legal Query RAG system installation and basic functionality.
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test core imports
        from src.config import Config
        from src.legal_query_rag import LegalQueryRAG
        from Model.SAM_model.inference import LegalRAGInference
        print("✅ Core modules imported successfully")
        
        # Test LangChain imports (may fail if not installed)
        try:
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            print("✅ LangChain OpenAI modules available")
        except ImportError as e:
            print(f"⚠️  LangChain modules not available: {e}")
            print("   Install with: pip install langchain langchain-openai")
        
        # Test FAISS import
        try:
            import faiss
            print("✅ FAISS available")
        except ImportError:
            print("⚠️  FAISS not available")
            print("   Install with: pip install faiss-cpu")
        
        # Test sentence transformers
        try:
            from sentence_transformers import CrossEncoder
            print("✅ Sentence Transformers available")
        except ImportError:
            print("⚠️  Sentence Transformers not available")
            print("   Install with: pip install sentence-transformers")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration setup."""
    print("\nTesting configuration...")
    
    try:
        from src.config import Config
        
        config = Config()
        
        # Check if API key is set
        if config.OPENAI_API_KEY:
            print("✅ OpenAI API key is configured")
        else:
            print("⚠️  OpenAI API key not set")
            print("   Set environment variable: OPENAI_API_KEY")
        
        # Check other configuration values
        print(f"✅ LLM Model: {config.LLM_MODEL}")
        print(f"✅ Embedding Model: {config.EMBEDDING_MODEL}")
        print(f"✅ Max Concurrent Queries: {config.MAX_CONCURRENT_QUERIES}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_basic_initialization():
    """Test basic system initialization."""
    print("\nTesting basic initialization...")
    
    try:
        from Model.SAM_model.inference import LegalRAGInference
        
        # Test initialization without API key (should not fail)
        legal_rag = LegalRAGInference()
        print("✅ LegalRAGInference initialized")
        
        # Test system info
        info = legal_rag.get_system_info()
        print(f"✅ System status: {info.get('status', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_file_structure():
    """Test that all required files are present."""
    print("\nTesting file structure...")
    
    required_files = [
        "src/__init__.py",
        "src/config.py",
        "src/data_ingestion.py",
        "src/embeddings.py",
        "src/vector_db.py",
        "src/react_agent.py",
        "src/retrieval.py",
        "src/reranking.py",
        "src/llm_generator.py",
        "src/evaluation.py",
        "src/legal_query_rag.py",
        "infrance.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests."""
    print("🧪 Legal Query RAG System Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Basic Initialization", test_basic_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
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
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("2. Install missing dependencies: pip install -r requirements.txt")
        print("3. Run example: python example_usage.py")
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("3. Check file permissions and paths")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
