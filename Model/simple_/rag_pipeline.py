# """
# Main RAG pipeline with fallback mechanism
# Orchestrates all components and handles responses
# """
# from typing import List, Dict, Any
# from langchain.chat_models import ChatOpenAI
# from config import RAGConfig
# from pdf_processor import PDFProcessor
# from fast_chunker import FastChunker
# from vector_manager import VectorManager
# from batch_processor import BatchProcessor


# class RAGPipeline:
#     """Main RAG pipeline with fallback mechanism"""
    
#     def __init__(self, config: RAGConfig):
#         self.config = config
#         print("Initializing RAG Pipeline...")
        
#         # Initialize components
#         self.pdf_processor = PDFProcessor(config.save_dir)
#         self.chunker = FastChunker(config.chunk_size, config.chunk_overlap)
#         self.vector_manager = VectorManager(config)
#         self.batch_processor = None
        
#         # Initialize LLMs
#         print("Initializing LLM models...")
#         self.chat_llm = ChatOpenAI(
#             openai_api_key=config.openai_api_key,
#             model="gpt-3.5-turbo",
#             temperature=0.7
#         )
        
#         self.fallback_llm = ChatOpenAI(
#             openai_api_key=config.openai_api_key,
#             model="gpt-3.5-turbo",
#             temperature=0.7
#         )
        
#         print("RAG Pipeline initialized successfully")
    
#     def load_document(self, pdf_url: str, doc_name: str = None) -> str:
#         """Load and process document from PDF URL"""
#         try:
#             print(f"Loading document from URL: {pdf_url}")
            
#             # Process PDF
#             text, txt_path = self.pdf_processor.process_pdf_from_url(pdf_url, doc_name)
            
#             # Fast chunking
#             chunks = self.chunker.chunk_text_fast(text)
            
#             # Create embeddings
#             self.vector_manager.create_embeddings(chunks)
            
#             # Initialize batch processor
#             self.batch_processor = BatchProcessor(self.config, self.vector_manager)
            
#             result_message = f"Document processed successfully. {len(chunks)} chunks created."
#             print(result_message)
#             return result_message
            
#         except Exception as e:
#             error_message = f"Document loading failed: {str(e)}"
#             print(error_message)
#             raise Exception(error_message)
    
#     def generate_response(self, question: str, context: List[str], has_context: bool) -> str:
#         """Generate response with or without context"""
#         try:
#             if has_context and context:
#                 # Use context-aware response
#                 context_text = "\n\n".join(context)
#                 prompt = f"""Based on the following context, please answer the question. If the context doesn't contain enough information to answer the question completely, say so and provide what information you can.

# Context:
# {context_text}

# Question: {question}

# Answer:"""
                
#                 print("Generating context-aware response...")
#                 response = self.chat_llm.predict(prompt)
#                 return response
#             else:
#                 # Fallback to normal ChatGPT response
#                 prompt = f"""Please answer the following question using your general knowledge:

# Question: {question}

# Answer:"""
                
#                 print("Generating fallback response (no context)...")
#                 response = self.fallback_llm.predict(prompt)
#                 return f"[No relevant context found - General AI response]: {response}"
                
#         except Exception as e:
#             error_message = f"Error generating response: {str(e)}"
#             print(error_message)
#             return error_message
    
#     async def ask_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
#         """Process multiple questions with batch processing"""
#         if not self.batch_processor:
#             raise Exception("No document loaded. Please load a document first.")
        
#         try:
#             print(f"Processing {len(questions)} questions...")
            
#             # Process questions in batches
#             processed_questions = await self.batch_processor.process_all_questions(questions)
            
#             results = []
#             for i, pq in enumerate(processed_questions):
#                 print(f"Generating response for question {i+1}/{len(processed_questions)}")
                
#                 # Generate response
#                 response = self.generate_response(
#                     pq['question'], 
#                     pq['context'], 
#                     pq['has_context']
#                 )
                
#                 results.append({
#                     'question': pq['question'],
#                     'answer': response,
#                     'has_context': pq['has_context'],
#                     'context_chunks': len(pq['context']),
#                     'similarity_scores': pq['scores']
#                 })
            
#             print(f"All {len(results)} questions processed successfully")
#             return results
            
#         except Exception as e:
#             error_message = f"Question processing failed: {str(e)}"
#             print(error_message)
#             raise Exception(error_message)
    
#     def ask_single_question(self, question: str) -> Dict[str, Any]:
#         """Ask a single question (synchronous)"""
#         if not self.batch_processor:
#             raise Exception("No document loaded. Please load a document first.")
        
#         print(f"Processing single question: {question}")
        
#         # Process single question
#         result = self.batch_processor.process_question(question)
        
#         # Generate response
#         response = self.generate_response(
#             result['question'], 
#             result['context'], 
#             result['has_context']
#         )
        
#         final_result = {
#             'question': result['question'],
#             'answer': response,
#             'has_context': result['has_context'],
#             'context_chunks': len(result['context']),
#             'similarity_scores': result['scores']
#         }
        
#         print("Single question processed successfully")
#         return final_result
    
#     def get_system_status(self) -> Dict[str, Any]:
#         """Get current system status"""
#         return {
#             'document_loaded': self.batch_processor is not None,
#             'vector_store_info': self.vector_manager.get_vector_store_info(),
#             'config': {
#                 'chunk_size': self.config.chunk_size,
#                 'batch_size': self.config.batch_size,
#                 'max_threads': self.config.max_threads,
#                 'similarity_threshold': self.config.similarity_threshold
#             }
#         }
    
#     def shutdown(self):
#         """Shutdown the pipeline and cleanup resources"""
#         if self.batch_processor:
#             self.batch_processor.shutdown()
#         print("RAG Pipeline shutdown completed")


"""
Main RAG pipeline with fallback mechanism
Orchestrates all components and handles responses
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from simple_.config import RAGConfig
from simple_.pdf_processor import PDFProcessor
from simple_.fast_chunker import FastChunker
from simple_.vector_manager import VectorManager
from simple_.batch_processor import BatchProcessor


class RAGPipeline:
    """Main RAG pipeline with fallback mechanism"""
    
    def __init__(self, config: RAGConfig):
        self.config = config
        print("Initializing RAG Pipeline...")
        
        # Initialize components
        self.pdf_processor = PDFProcessor(config.save_dir)
        self.chunker = FastChunker(config.chunk_size, config.chunk_overlap)
        self.vector_manager = VectorManager(config)
        self.batch_processor = None
        
        # Initialize LLMs
        print("Initializing LLM models...")
        self.chat_llm = ChatOpenAI(
            openai_api_key=config.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        self.fallback_llm = ChatOpenAI(
            openai_api_key=config.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        print("RAG Pipeline initialized successfully")
    
    def load_document(self, pdf_url: str, doc_name: str = None) -> str:
        """Load and process document from PDF URL"""
        try:
            print(f"Loading document from URL: {pdf_url}")
            
            # Process PDF
            text, txt_path = self.pdf_processor.process_pdf_from_url(pdf_url, doc_name)
            
            # Fast chunking
            chunks = self.chunker.chunk_text_fast(text)
            
            # Create embeddings
            self.vector_manager.create_embeddings(chunks)
            
            # Initialize batch processor
            self.batch_processor = BatchProcessor(self.config, self.vector_manager)
            
            result_message = f"Document processed successfully. {len(chunks)} chunks created."
            print(result_message)
            return result_message
            
        except Exception as e:
            error_message = f"Document loading failed: {str(e)}"
            print(error_message)
            raise Exception(error_message)
    
    def generate_response(self, question: str, context: List[str], has_context: bool) -> str:
        """Generate response with or without context"""
        try:
            if has_context and context:
                # Use context-aware response
                context_text = "\n\n".join(context)
                prompt = f"""Based on the following context, please answer the question. If the context doesn't contain enough information to answer the question completely, say so and provide what information you can.

Context:
{context_text}

Question: {question}

Answer:"""
                
                print("Generating context-aware response...")
                response = self.chat_llm.predict(prompt)
                return response
            else:
                # Fallback to normal ChatGPT response
                prompt = f"""Please answer the following question using your general knowledge:

Question: {question}

Answer:"""
                
                print("Generating fallback response (no context)...")
                response = self.fallback_llm.predict(prompt)
                return f"[No relevant context found - General AI response]: {response}"
                
        except Exception as e:
            error_message = f"Error generating response: {str(e)}"
            print(error_message)
            return error_message
    
    async def ask_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Process multiple questions with batch processing"""
        if not self.batch_processor:
            raise Exception("No document loaded. Please load a document first.")
        
        try:
            print(f"Processing {len(questions)} questions...")
            
            # Process questions in batches
            processed_questions = await self.batch_processor.process_all_questions(questions)
            
            results = []
            for i, pq in enumerate(processed_questions):
                print(f"Generating response for question {i+1}/{len(processed_questions)}")
                
                # Generate response
                response = self.generate_response(
                    pq['question'], 
                    pq['context'], 
                    pq['has_context']
                )
                
                results.append({
                    'question': pq['question'],
                    'answer': response,
                    'has_context': pq['has_context'],
                    'context_chunks': len(pq['context']),
                    'similarity_scores': pq['scores']
                })
            
            print(f"All {len(results)} questions processed successfully")
            return results
            
        except Exception as e:
            error_message = f"Question processing failed: {str(e)}"
            print(error_message)
            raise Exception(error_message)
    
    def ask_single_question(self, question: str) -> Dict[str, Any]:
        """Ask a single question (synchronous)"""
        if not self.batch_processor:
            raise Exception("No document loaded. Please load a document first.")
        
        print(f"Processing single question: {question}")
        
        # Process single question
        result = self.batch_processor.process_question(question)
        
        # Generate response
        response = self.generate_response(
            result['question'], 
            result['context'], 
            result['has_context']
        )
        
        final_result = {
            'question': result['question'],
            'answer': response,
            'has_context': result['has_context'],
            'context_chunks': len(result['context']),
            'similarity_scores': result['scores']
        }
        
        print("Single question processed successfully")
        return final_result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'document_loaded': self.batch_processor is not None,
            'vector_store_info': self.vector_manager.get_vector_store_info(),
            'config': {
                'chunk_size': self.config.chunk_size,
                'batch_size': self.config.batch_size,
                'max_threads': self.config.max_threads,
                'similarity_threshold': self.config.similarity_threshold
            }
        }
    
    def shutdown(self):
        """Shutdown the pipeline and cleanup resources"""
        if self.batch_processor:
            self.batch_processor.shutdown()
        print("RAG Pipeline shutdown completed")