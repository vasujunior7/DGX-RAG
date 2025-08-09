"""
Main execution file for RAG system
Example usage and testing of all components
"""
import asyncio
import json
from config import RAGConfig
from rag_pipeline import RAGPipeline


def print_result(result: dict, question_num: int = None):
    """Pretty print a single result"""
    prefix = f"Q{question_num}: " if question_num else "Q: "
    print(f"\n{'='*60}")
    print(f"{prefix}{result['question']}")
    print(f"{'='*60}")
    print(f"Answer: {result['answer']}")
    print(f"\nContext Available: {result['has_context']}")
    print(f"Context Chunks Used: {result['context_chunks']}")
    if result['similarity_scores']:
        print(f"Similarity Scores: {[f'{score:.3f}' for score in result['similarity_scores']]}")


def print_system_status(status: dict):
    """Pretty print system status"""
    print(f"\n{'='*40} SYSTEM STATUS {'='*40}")
    print(f"Document Loaded: {status['document_loaded']}")
    print(f"Vector Store: {status['vector_store_info']['status']}")
    if 'total_chunks' in status['vector_store_info']:
        print(f"Total Chunks: {status['vector_store_info']['total_chunks']}")
    print(f"Configuration:")
    for key, value in status['config'].items():
        print(f"  {key}: {value}")
    print(f"{'='*92}")


async def main():
    """Main execution function"""
    print("🚀 Starting RAG System Demo")
    print("="*50)
    
    # Configuration - REPLACE WITH YOUR OPENAI API KEY
    config = RAGConfig(
        openai_api_key="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",  # ⚠️ REPLACE THIS
        chunk_size=1000,
        chunk_overlap=200,
        batch_size=8,
        max_threads=4,
        similarity_threshold=0.7,
        save_dir="./documents"
    )
    
    # Initialize RAG pipeline
    rag = RAGPipeline(config)
    
    try:
        # Example 1: Load document from PDF URL
        print("\n📄 Loading document...")
        # REPLACE WITH YOUR ACTUAL PDF URL (Azure blob, Google Drive, etc.)
        pdf_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
        
        # For testing, you can use a sample PDF URL like:
        # pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        
        try:
            result = rag.load_document(pdf_url, "sample_document")
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ Document loading failed: {str(e)}")
            print("Please check your PDF URL and try again.")
            return
        
        # Check system status
        status = rag.get_system_status()
        print_system_status(status)
        
        # Example 2: Ask a single question
        print("\n🤔 Testing single question...")
        try:
            single_result = rag.ask_single_question("What is the main topic of this document?")
            print_result(single_result)
        except Exception as e:
            print(f"❌ Single question failed: {str(e)}")
        
        # Example 3: Ask multiple questions in batches
        print(f"\n🔄 Testing batch processing (batch size: {config.batch_size})...")
        
        # Sample questions - modify based on your document
        questions = [
             "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
        
        try:
            print(f"Processing {len(questions)} questions in batches...")
            results = await rag.ask_questions(questions)
            
            print(f"\n📊 BATCH PROCESSING RESULTS")
            print(f"Total Questions: {len(results)}")
            
            # Display results
            for i, result in enumerate(results, 1):
                print_result(result, i)
            
            # Summary statistics
            context_found = sum(1 for r in results if r['has_context'])
            print(f"\n📈 SUMMARY STATISTICS")
            print(f"Questions with Context: {context_found}/{len(results)}")
            print(f"Fallback Responses: {len(results) - context_found}/{len(results)}")
            
        except Exception as e:
            print(f"❌ Batch processing failed: {str(e)}")
        
        # Example 4: Test fallback mechanism
        print(f"\n🔄 Testing fallback mechanism...")
        try:
            fallback_question = "What is the capital of France?"  # Should trigger fallback
            fallback_result = rag.ask_single_question(fallback_question)
            print_result(fallback_result)
        except Exception as e:
            print(f"❌ Fallback test failed: {str(e)}")
    
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
    
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up...")
        rag.shutdown()
        print("✅ RAG System Demo completed!")


def interactive_mode():
    """Interactive mode for testing"""
    print("🔄 Starting Interactive Mode")
    print("Type 'quit' to exit, 'status' for system info")
    
    config = RAGConfig(
        openai_api_key=input("Enter your OpenAI API key: ").strip(),
        chunk_size=1000,
        chunk_overlap=200,
        batch_size=8
    )
    
    rag = RAGPipeline(config)
    
    # Load document
    pdf_url = input("Enter PDF URL: ").strip()
    doc_name = input("Enter document name (optional): ").strip() or None
    
    try:
        result = rag.load_document(pdf_url, doc_name)
        print(f"✅ {result}")
        
        while True:
            question = input("\n🤔 Ask a question: ").strip()
            
            if question.lower() == 'quit':
                break
            elif question.lower() == 'status':
                status = rag.get_system_status()
                print_system_status(status)
                continue
            elif not question:
                continue
            
            try:
                result = rag.ask_single_question(question)
                print_result(result)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
    
    finally:
        rag.shutdown()


def test_mode():
    """Test mode with sample data"""
    print("🧪 Starting Test Mode")
    print("This mode uses a sample PDF for testing purposes")
    
    config = RAGConfig(
        openai_api_key=input("Enter your OpenAI API key: ").strip(),
        chunk_size=500,  # Smaller chunks for testing
        chunk_overlap=100,
        batch_size=4,    # Smaller batches for testing
        similarity_threshold=0.6  # Lower threshold for testing
    )
    
    rag = RAGPipeline(config)
    
    # Use a sample PDF URL for testing
    test_pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    try:
        print(f"Loading test document from: {test_pdf_url}")
        result = rag.load_document(test_pdf_url, "test_document")
        print(f"✅ {result}")
        
        # Test questions for the sample document
        test_questions = [
            "What is this document about?",
            "What type of document is this?",
            "Is there any specific content mentioned?",
            "What is the purpose of this file?"
        ]
        
        print(f"\n🧪 Testing with {len(test_questions)} questions...")
        
        # Test single question
        print("\n--- Single Question Test ---")
        single_result = rag.ask_single_question(test_questions[0])
        print_result(single_result)
        
        # Test batch processing
        print("\n--- Batch Processing Test ---")
        async def run_batch_test():
            results = await rag.ask_questions(test_questions)
            for i, result in enumerate(results, 1):
                print_result(result, i)
        
        asyncio.run(run_batch_test())
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    
    finally:
        rag.shutdown()


def benchmark_mode():
    """Benchmark mode to test performance"""
    print("📊 Starting Benchmark Mode")
    
    config = RAGConfig(
        openai_api_key=input("Enter your OpenAI API key: ").strip(),
        chunk_size=1000,
        chunk_overlap=200,
        batch_size=8,
        max_threads=4
    )
    
    rag = RAGPipeline(config)
    
    pdf_url = input("Enter PDF URL for benchmarking: ").strip()
    
    import time
    
    try:
        # Benchmark document loading
        print("\n⏱️ Benchmarking document loading...")
        start_time = time.time()
        result = rag.load_document(pdf_url, "benchmark_doc")
        load_time = time.time() - start_time
        print(f"✅ Document loaded in {load_time:.2f} seconds")
        print(f"Result: {result}")
        
        # Benchmark single question
        print("\n⏱️ Benchmarking single question...")
        test_question = "What is the main topic of this document?"
        start_time = time.time()
        result = rag.ask_single_question(test_question)
        single_time = time.time() - start_time
        print(f"✅ Single question processed in {single_time:.2f} seconds")
        
        # Benchmark batch processing
        print("\n⏱️ Benchmarking batch processing...")
        questions = [f"Question {i}: What is mentioned about topic {i}?" for i in range(1, 17)]  # 16 questions
        
        start_time = time.time()
        
        async def run_benchmark():
            return await rag.ask_questions(questions)
        
        results = asyncio.run(run_benchmark())
        batch_time = time.time() - start_time
        
        print(f"✅ Batch processing completed in {batch_time:.2f} seconds")
        print(f"📊 Performance Summary:")
        print(f"  - Document Loading: {load_time:.2f}s")
        print(f"  - Single Question: {single_time:.2f}s")
        print(f"  - Batch Processing ({len(questions)} questions): {batch_time:.2f}s")
        print(f"  - Average per question in batch: {batch_time/len(questions):.2f}s")
        
        context_found = sum(1 for r in results if r['has_context'])
        print(f"  - Questions with context: {context_found}/{len(results)}")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {str(e)}")
    
    finally:
        rag.shutdown()


if __name__ == "__main__":
    print("🤖 RAG System - Choose mode:")
    print("1. Demo mode (automated testing)")
    print("2. Interactive mode (manual Q&A)")
    print("3. Test mode (sample PDF)")
    print("4. Benchmark mode (performance testing)")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            asyncio.run(main())
            break
        elif choice == "2":
            print("\n" + "="*50)
            interactive_mode()
            break
        elif choice == "3":
            print("\n" + "="*50)
            test_mode()
            break
        elif choice == "4":
            print("\n" + "="*50)
            benchmark_mode()
            break
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")
            continue