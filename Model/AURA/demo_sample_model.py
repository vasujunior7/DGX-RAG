"""
Example usage of the SampleModelPaller class for RAG pipeline
"""

from Model.AURA.infrance import SampleModelPaller

def main():
    print("🚀 SampleModelPaller Demo")
    
    # Option 1: Initialize with force regeneration (creates fresh chunks)
    print("\n📌 Option 1: Creating fresh chunks and index...")
    model = SampleModelPaller(force_regenerate=True)
    
    # Load a document (will create fresh chunks)
    pdf_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    model.load_document(pdf_url)
    
    # Ask some questions
    questions = [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
        "Does this policy cover maternity expenses?"
    ]
    
    # Get answers
    answers = model.inference(questions)
    
    # Display results
    print("\n📋 Q&A Results:")
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        print(f"\nQ{i}: {q}")
        print(f"A{i}: {a}")
    
    # Save session data
    model.save_session("demo_session_fresh.json")
    print("\n✅ Demo completed with fresh chunks. Session saved to demo_session_fresh.json")
    
    # Option 2: Show how to use cached data (if available)
    print("\n" + "="*60)
    print("📌 Option 2: Using cached data (if available)...")
    model_cached = SampleModelPaller(force_regenerate=False)
    model_cached.load_document(pdf_url)  # Will use cache if available
    
    print("✅ Demo with caching option ready")

if __name__ == "__main__":
    main()
