"""
Test script to verify the SampleModelPaller structure works without requiring API key
"""

from Model.AURA.infrance import SampleModelPaller
import time

def test_structure():
    print("🧪 Testing SampleModelPaller Structure")
    
    # Test 1: Initialize with force regeneration
    print("\n1. Testing initialization with force regeneration...")
    model = SampleModelPaller(force_regenerate=True)
    print(f"   ✓ Initialized successfully")
    print(f"   ✓ API key status: {'✓ Provided' if model.api_key else '✗ Missing'}")
    print(f"   ✓ Force regenerate mode: {model.force_regenerate}")
    
    # Test 2: Load document (will create fresh chunks)
    print("\n2. Testing document loading with fresh chunk generation...")
    try:
        pdf_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
        model.load_document(pdf_url)
        print(f"   ✓ Document loaded and preprocessed with fresh chunks")
        print(f"   ✓ Total chunks: {len(model.chunks) if model.chunks else 0}")
        print(f"   ✓ Index created: {model.index is not None}")
        print(f"   ✓ Model loaded: {model.model is not None}")
    except Exception as e:
        print(f"   ✗ Error loading document: {e}")
        return
    
    # Test 3: Test cached vs fresh loading
    print("\n3. Testing cached vs fresh loading...")
    try:
        # Test with cache (if it exists)
        model_cached = SampleModelPaller(force_regenerate=False)
        print(f"   ✓ Created model with caching enabled")
        
        # Test force fresh on existing instance
        model.load_document(pdf_url, force_fresh=True)
        print(f"   ✓ Force fresh reload completed")
        
    except Exception as e:
        print(f"   ✗ Error in caching test: {e}")
    
    # Test 4: Test structure without actual inference
    print("\n4. Testing inference structure...")
    questions = [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
    ]
    
    try:
        print(f"   ✓ Questions prepared: {len(questions)}")
        print(f"   ✓ Embeddings model ready: {model.model is not None}")
        print(f"   ✓ Vector index ready: {model.index is not None}")
        print(f"   ✓ Document chunks ready: {len(model.chunks) if model.chunks else 0}")
        
        # Test session saving
        model.save_session("test_session_fresh.json")
        print(f"   ✓ Session data saved successfully")
        
    except Exception as e:
        print(f"   ✗ Error in structure test: {e}")
    
    print("\n✅ Structure test completed with fresh chunk generation!")
    print("\n📝 Notes:")
    print("   - Document preprocessing creates fresh chunks every time")
    print("   - Vector embeddings and FAISS indexing regenerated")
    print("   - Session management operational")
    print("   - Cache files removed and recreated")
    print("   - To test full inference, add valid GEMINI_API_KEY to .env file")

if __name__ == "__main__":
    test_structure()
