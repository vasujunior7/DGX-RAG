"""
Example usage script for Legal Query RAG system.
Demonstrates parallel processing of 15-20 legal queries.
"""
import asyncio
import os
import time
from pathlib import Path

from Model.SAM_model.inference import LegalRAGInference

async def main():
    """Main example function demonstrating the Legal Query RAG system."""
    
    # Initialize the system
    print("🏛️  Initializing Legal Query RAG system...")
    
    # You need to set your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Please set OPENAI_API_KEY environment variable")
        return
    
    # Initialize the inference system
    legal_rag = LegalRAGInference(api_key=api_key)
    
    # Example legal documents (replace with your actual document paths)
    document_paths = [
        # Add paths to your legal documents here
        # "path/to/constitution.pdf",
        # "path/to/case_law.pdf", 
        # "path/to/statutes.txt",
        # "C:\\Users\\saumi\\Desktop\\CODES\\HackRX\\cached_pdfs\\6635d94cf9023c83521982b3043ec70c.pdf"
        "C:\\Users\\saumi\\Desktop\\CODES\\HackRX\\cached_pdfs\\f15345ba5ce7155ebb1fc8f231da2654.pdf"
    ]
    
    # For demo purposes, we'll create some sample content
    print("📄 Loading legal documents...")
    
    if document_paths:
        # Load actual documents
        await legal_rag.load_documents(document_paths)
    else:
        print("⚠️  No document paths provided. Using demo mode.")
        print("   Add your legal document paths to the document_paths list above.")
        return
    
    # Example legal queries (15-20 queries for parallel processing demo)
    legal_queries = [
        # "If my car is stolen, what case will it be in law?",
        # "If I am arrested without a warrant, is that legal?",
        # "If someone denies me a job because of my caste, is that allowed?",
        # "If the government takes my land for a project, can I stop it?",
        # "If my child is forced to work in a factory, is that legal?",
        # "If I am stopped from speaking at a protest, is that against my rights?",
        # "If a religious place stops me from entering because I'm a woman, is that constitutional?",
        # "If I change my religion, can the government stop me?",
        # "If the police torture someone in custody, what right is being violated?",
        # "If I'm denied admission to a public university because I'm from a backward community, can I do something?",
        "NAME OF President of INDIA"           
    ]
    
    print(f"\n🔍 Processing {len(legal_queries)} legal queries in parallel...")
    start_time = time.time()
    
    try:
        # Process all queries in parallel
        results = await legal_rag.async_inference(
            legal_queries,
            use_react=True,      # Use ReAct agent for query processing
            use_reranking=True,  # Use document re-ranking
            use_evaluation=True  # Use response evaluation
        )
        
        end_time = time.time()
        
        print(f"\n✅ Completed processing in {end_time - start_time:.2f} seconds")
        print(f"📊 Average time per query: {(end_time - start_time) / len(legal_queries):.2f} seconds")
        
        # Display results summary
        print("\n" + "="*80)
        print("📋 RESULTS SUMMARY")
        print("="*80)
        
        approved_count = 0
        total_score = 0
        
        for i, result in enumerate(results, 1):
            query = result['original_query'] + "..." if len(result['original_query']) > 60 else result['original_query']
            
            response = result.get('response', {})
            answer = response.get('answer', 'No answer generated')
            answer_preview = answer + "..." if len(answer) > 100 else answer
            
            # Check if fallback was used
            fallback_indicator = " 🔄 FALLBACK" if response.get('fallback_used', False) else ""
            
            evaluation = result.get('evaluation', {})
            if evaluation:
                score = evaluation.get('overall_score', 0)
                recommendation = evaluation.get('recommendation', 'N/A')
                # Show original recommendation if fallback was used
                if evaluation.get('fallback_used', False):
                    original_rec = evaluation.get('original_recommendation', 'REJECT')
                    recommendation = f"{original_rec}→FALLBACK"
                
                total_score += score
                if recommendation == 'APPROVE':
                    approved_count += 1
                
                print(f"\n{i:2d}. Query: {query}{fallback_indicator}")
                print(f"    Answer: {answer_preview}")
                print(f"    Score: {score}/10 | Status: {recommendation}")
                print(f"    Sources: {len(result.get('retrieved_documents', []))}")
            else:
                print(f"\n{i:2d}. Query: {query}{fallback_indicator}")
                print(f"    Answer: {answer_preview}")
                print(f"    Score: N/A | Status: N/A")
        
        # Overall statistics
        if results and any(r.get('evaluation') for r in results):
            avg_score = total_score / len([r for r in results if r.get('evaluation')])
            approval_rate = (approved_count / len(results)) * 100
            
            # Count fallback responses
            fallback_count = len([r for r in results if r.get('response', {}).get('fallback_used', False)])
            rag_count = len(results) - fallback_count
            
            print("\n" + "="*80)
            print("📊 OVERALL STATISTICS")
            print("="*80)
            print(f"Total queries processed: {len(results)}")
            print(f"RAG responses: {rag_count}")
            print(f"Fallback responses: {fallback_count}")
            print(f"Average quality score: {avg_score:.1f}/10")
            print(f"Approval rate: {approval_rate:.1f}%")
            print(f"Total processing time: {end_time - start_time:.2f} seconds")
            
            if fallback_count > 0:
                fallback_rate = (fallback_count / len(results)) * 100
                print(f"Fallback rate: {fallback_rate:.1f}% (RAG responses rejected and replaced with general knowledge)")
        
        # Show detailed result for first query
        if results:
            print("\n" + "="*80)
            print("🔍 DETAILED EXAMPLE (First Query)")
            print("="*80)
            
            first_result = results[0]
            print(f"Original Query: {first_result['original_query']}")
            if first_result.get('processed_query') != first_result['original_query']:
                print(f"Processed Query: {first_result['processed_query']}")
            
            response = first_result.get('response', {})
            print(f"\nFull Answer:")
            print(response.get('answer', 'No answer generated'))
            
            if response.get('supporting_evidence'):
                print(f"\nSupporting Evidence:")
                print(response['supporting_evidence'])
            
            evaluation = first_result.get('evaluation', {})
            if evaluation:
                print(f"\nEvaluation Details:")
                print(f"- Accuracy: {evaluation.get('accuracy_score', 0)}/10")
                print(f"- Completeness: {evaluation.get('completeness_score', 0)}/10")
                print(f"- Relevance: {evaluation.get('relevance_score', 0)}/10")
                print(f"- Clarity: {evaluation.get('clarity_score', 0)}/10")
                print(f"- Citations: {evaluation.get('citations_score', 0)}/10")
                print(f"- Overall: {evaluation.get('overall_score', 0)}/10")
                print(f"- Recommendation: {evaluation.get('recommendation', 'N/A')}")
                
                if evaluation.get('feedback'):
                    print(f"- Feedback: {evaluation['feedback']}")
        
        # System information
        print("\n" + "="*80)
        print("⚙️  SYSTEM INFORMATION")
        print("="*80)
        
        sys_info = legal_rag.get_system_info()
        stats = sys_info.get('system_stats', {})
        config = stats.get('config', {})
        
        print(f"Status: {sys_info.get('status', 'Unknown')}")
        print(f"LLM Model: {config.get('llm_model', 'Unknown')}")
        print(f"Embedding Model: {config.get('embedding_model', 'Unknown')}")
        print(f"Max Concurrent Queries: {config.get('max_concurrent_queries', 'Unknown')}")
        
        kb_stats = stats.get('knowledge_base', {})
        print(f"Documents Indexed: {kb_stats.get('total_documents', 'Unknown')}")
        print(f"Vector Index Size: {kb_stats.get('total_vectors', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()

def demo_single_query():
    """Demonstrate single query processing with quality improvement."""
    
    async def single_query_demo():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Please set OPENAI_API_KEY environment variable")
            return
        
        legal_rag = LegalRAGInference(api_key=api_key)
        
        # This would need actual documents
        print("📄 Note: This demo requires actual legal documents to be loaded.")
        print("   Please add document paths to the example above.")
        
        # Example single query with quality improvement
        query = "What are the key elements required to establish a valid contract under common law?"
        
        try:
            result = await legal_rag.single_query_inference(query, max_iterations=2)
            
            print(f"Query: {query}")
            print(f"Final Answer: {result['response']['answer']}")
            print(f"Quality Score: {result['evaluation']['overall_score']}/10")
            print(f"Iterations: {result['iterations']}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    asyncio.run(single_query_demo())

if __name__ == "__main__":
    # Run the main parallel processing demo
    from datetime import datetime
    print(f"Starting Legal Query RAG demo at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    asyncio.run(main())

    print("Legal Query RAG demo completed.")
    print(f"Time taken: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Uncomment to run single query demo instead
    # demo_single_query()
