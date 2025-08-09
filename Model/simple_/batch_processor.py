"""
Asynchronous batch processing module
Handles concurrent question processing with threading
"""
import asyncio
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from simple_.config import RAGConfig
from simple_.vector_manager import VectorManager


class BatchProcessor:
    """Handles asynchronous batch processing of questions"""
    
    def __init__(self, config: RAGConfig, vector_manager: VectorManager):
        self.config = config
        self.vector_manager = vector_manager
        self.executor = ThreadPoolExecutor(max_workers=config.max_threads)
        print(f"BatchProcessor initialized - Batch size: {config.batch_size}, Max threads: {config.max_threads}")
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Process a single question"""
        try:
            print(f"Processing question: {question[:50]}...")
            
            # Retrieve relevant context
            relevant_chunks, scores = self.vector_manager.retrieve_relevant_chunks(question)
            
            result = {
                'question': question,
                'context': relevant_chunks,
                'scores': scores,
                'has_context': len(relevant_chunks) > 0
            }
            
            print(f"Question processed - Context found: {result['has_context']}")
            return result
            
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            return {
                'question': question,
                'context': [],
                'scores': [],
                'has_context': False,
                'error': str(e)
            }
    
    async def process_batch_async(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Process a batch of questions asynchronously"""
        print(f"Processing batch of {len(questions)} questions...")
        loop = asyncio.get_event_loop()
        
        # Submit all questions to thread pool
        futures = [
            loop.run_in_executor(self.executor, self.process_question, question)
            for question in questions
        ]
        
        # Wait for all to complete
        results = await asyncio.gather(*futures)
        print(f"Batch processing completed")
        return results
    
    def create_batches(self, questions: List[str]) -> List[List[str]]:
        """Split questions into batches of configured size"""
        batches = []
        for i in range(0, len(questions), self.config.batch_size):
            batch = questions[i:i + self.config.batch_size]
            batches.append(batch)
        
        print(f"Created {len(batches)} batches from {len(questions)} questions")
        return batches
    
    async def process_all_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Process all questions in batches"""
        print(f"Starting batch processing for {len(questions)} questions...")
        batches = self.create_batches(questions)
        all_results = []
        
        # Process batches concurrently
        batch_tasks = [
            self.process_batch_async(batch) 
            for batch in batches
        ]
        
        print(f"Processing {len(batch_tasks)} batches concurrently...")
        batch_results = await asyncio.gather(*batch_tasks)
        
        # Flatten results
        for batch_result in batch_results:
            all_results.extend(batch_result)
        
        print(f"All questions processed. Total results: {len(all_results)}")
        return all_results
    
    def shutdown(self):
        """Shutdown the thread pool executor"""
        self.executor.shutdown(wait=True)
        print("BatchProcessor shutdown completed")