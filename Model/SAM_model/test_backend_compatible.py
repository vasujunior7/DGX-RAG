"""
Test script for backend-compatible SampleModelPaller class.
Demonstrates the simplified interface with parallel threaded inference.
"""
import os
from Model.SAM_model.inference import SampleModelPaller
import time

def test_sample_model_paller():
    """Test the SampleModelPaller backend-compatible interface."""
    
    print("🔧 Testing SampleModelPaller Backend-Compatible Interface")
    print("=" * 60)
    
    # Initialize the system
    print("1️⃣  Initializing SampleModelPaller...")
    model = SampleModelPaller()
    
    # Check initial status
    print("\n2️⃣  Checking initial status...")
    status = model.get_status()
    print(f"System ready: {status['system_ready']}")
    print(f"Processed docs directory: {status['processed_docs_dir']}")
    print(f"Embeddings cache directory: {status['embeddings_cache_dir']}")
    
    # Load a document
    print("\n3️⃣  Loading legal document...")
    # document_path = "C:\\Users\\saumi\\Desktop\\CODES\\HackRX\\cached_pdfs\\f15345ba5ce7155ebb1fc8f231da2654.pdf"
    document_path = "https://hackrx.blob.core.windows.net/assets/hackrx_6/policies/HDFHLIP23024V072223.pdf?sv=2023-01-03&st=2025-07-30T06%3A46%3A49Z&se=2025-09-01T06%3A46%3A00Z&sr=c&sp=rl&sig=9szykRKdGYj0BVm1skP%2BX8N9%2FRENEn2k7MQPUp33jyQ%3D"
    
    # Check if it's a URL or local file
    is_url = document_path.startswith(('http://', 'https://'))
    file_exists = not is_url and os.path.exists(document_path)
    
    if is_url or file_exists:
        print(f"Loading document: {document_path}")
        try:
            model.load_document(document_path)
        except Exception as e:
            print(f"❌ Error loading document: {e}")
            print("\n5️⃣  Testing inference without document (error handling)...")
            test_questions = ["What are fundamental rights?"]
            answers = model.inference(test_questions)
            print(f"Response: {answers[0]}")
            return
        print(f"Loading document: {document_path}")
        model.load_document(document_path)
        
        # Check status after loading
        print("\n4️⃣  Status after document loading...")
        status = model.get_status()
        print(f"System ready: {status['system_ready']}")
        if 'knowledge_base' in status:
            kb_stats = status['knowledge_base']
            print(f"Total documents: {kb_stats.get('total_documents', 0)}")
            print(f"Vector count: {kb_stats.get('total_vectors', 0)}")
        
        # Test parallel inference
        print("\n5️⃣  Testing parallel inference...")
        test_questions = [
            "What are fundamental rights in Indian Constitution?",
            "How does the legal system handle theft cases?",
            "What are the procedures for filing a civil case?",
            "Can government take private property for public use?",
            "What rights do citizens have during police arrest?",
            "What are fundamental rights in Indian Constitution?",
            "How does the legal system handle theft cases?",
            "What are the procedures for filing a civil case?",
            "Can government take private property for public use?",
            "What rights do citizens have during police arrest?"
        ]
        
        print(f"Processing {len(test_questions)} questions in parallel...")
        answers = model.inference(test_questions)
        
        print(f"\n📋 Results:")
        print("-" * 50)
        for i, (question, answer) in enumerate(zip(test_questions, answers), 1):
            print(f"\nQ{i}: {question}")
            print(f"A{i}: {answer}")
            print("-" * 50)
        
        print(f"\n✅ Backend-compatible interface test completed successfully!")
        print(f"📊 Processed {len(answers)} questions with parallel threading")
        
    else:
        print(f"⚠️  Document not found: {document_path}")
        print("Please update the document_path variable with a valid PDF file path.")
        
        # Test with sample questions anyway (will show error handling)
        print("\n5️⃣  Testing inference without document (error handling)...")
        test_questions = ["What are fundamental rights?"]
        answers = model.inference(test_questions)
        print(f"Response: {answers[0]}")

if __name__ == "__main__":
    # Set OpenAI API key if available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in environment variables")
        print("Please set it for full functionality testing")
        
    start_time = time.time()
    test_sample_model_paller()
    end_time = time.time()
    
    print(f"\n⏱️ Total execution time: {end_time - start_time:.2f} seconds")
