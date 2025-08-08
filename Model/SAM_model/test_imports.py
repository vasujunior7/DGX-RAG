"""Simple test to isolate import issues."""
try:
    print("Testing imports...")
    from langchain_openai import ChatOpenAI
    print("✅ langchain_openai import successful")
    
    from src.config import Config
    print("✅ Config import successful")
    
    from src.embeddings import EmbeddingManager
    print("✅ EmbeddingManager import successful")
    
    from src.legal_query_rag import LegalQueryRAG
    print("✅ LegalQueryRAG import successful")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
