



"""
Legal Query RAG Inference System
Main interface for the Legal Query RAG system with parallel inference support.
"""
import asyncio
import os
import time
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from src.legal_query_rag import LegalQueryRAG
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LegalRAGInference:
    """
    Main inference class for Legal Query RAG system.
    Supports parallel processing of 15-20 queries with comprehensive legal document analysis.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Legal RAG system.
        
        Args:
            api_key: OpenAI API key (if not provided, will use environment variable)
        """
        # Set up configuration
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        self.config = Config()
        try:
            self.config.validate_config()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        
        # Initialize the RAG system
        self.rag_system = LegalQueryRAG(self.config)
        self.knowledge_base_initialized = False
        
        logger.info("Legal RAG Inference system initialized")
        embedding_model = self.config.ST_EMBEDDING_MODEL if self.config.EMBEDDING_PROVIDER == "sentence_transformers" else self.config.OPENAI_EMBEDDING_MODEL
        logger.info(f"Configuration: {self.config.LLM_MODEL} LLM, {embedding_model} embeddings via {self.config.EMBEDDING_PROVIDER}")
        logger.info(f"Max concurrent queries: {self.config.MAX_CONCURRENT_QUERIES}")
    
    async def load_documents(self, document_paths: List[str]) -> None:
        """
        Load and index legal documents for retrieval.
        
        Args:
            document_paths: List of paths to legal documents (PDFs, text files, etc.)
        """
        logger.info(f"Loading {len(document_paths)} documents...")
        
        try:
            await self.rag_system.initialize_knowledge_base(document_paths)
            self.knowledge_base_initialized = True
            logger.info("Knowledge base initialized successfully")
            
            # Print system statistics
            stats = self.rag_system.get_system_stats()
            logger.info(f"System stats: {stats}")
            
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            raise
    
    def load_document(self, file_path: str) -> None:
        """
        Load a single document (synchronous wrapper for compatibility).
        
        Args:
            file_path: Path to the document file
        """
        logger.info(f"Loading single document: {file_path}")
        
        # Run async method in event loop
        try:
            asyncio.run(self.load_documents([file_path]))
        except Exception as e:
            logger.error(f"Failed to load document {file_path}: {e}")
            raise
    
    async def async_inference(self, questions: List[str], 
                            use_react: bool = True,
                            use_reranking: bool = True,
                            use_evaluation: bool = True) -> List[Dict[str, Any]]:
        """
        Perform async inference on multiple legal queries with full RAG pipeline.
        
        Args:
            questions: List of legal queries
            use_react: Whether to use ReAct agent for query processing
            use_reranking: Whether to use document re-ranking
            use_evaluation: Whether to evaluate response quality
            
        Returns:
            List of comprehensive response dictionaries
        """
        if not self.knowledge_base_initialized:
            raise ValueError("Knowledge base not initialized. Call load_documents() first.")
        
        logger.info(f"Processing {len(questions)} legal queries in parallel...")
        
        try:
            # Process queries through the full RAG pipeline
            results = await self.rag_system.process_batch_queries(
                questions, 
                use_react=use_react,
                use_reranking=use_reranking,
                use_evaluation=use_evaluation
            )
            
            logger.info(f"Successfully processed {len(results)} queries")
            
            # Log evaluation summary if available
            evaluations = [r.get('evaluation') for r in results if r.get('evaluation')]
            if evaluations:
                eval_summary = self.rag_system.evaluator.get_evaluation_summary(evaluations)
                logger.info(f"Evaluation summary: {eval_summary}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise
    
    def inference(self, questions: List[str]) -> List[str]:
        """
        Synchronous inference method for compatibility.
        Returns simple string answers extracted from full responses.
        
        Args:
            questions: List of legal query strings
            
        Returns:
            List of answer strings
        """
        if not isinstance(questions, list):
            questions = [questions]
        
        logger.info(f"Running synchronous inference for {len(questions)} questions")
        
        try:
            # Run async inference
            results = asyncio.run(self.async_inference(questions))
            
            # Extract simple answers
            answers = []
            for result in results:
                response = result.get('response', {})
                answer = response.get('answer', response.get('full_response', 'No answer generated'))
                answers.append(answer)
            
            return answers
            
        except Exception as e:
            logger.error(f"Error in synchronous inference: {e}")
            return [f"Error processing query: {str(e)}"] * len(questions)
    
    async def single_query_inference(self, question: str,
                                   max_iterations: int = 2) -> Dict[str, Any]:
        """
        Process a single query with quality improvement iterations.
        
        Args:
            question: Legal query string
            max_iterations: Maximum improvement iterations
            
        Returns:
            Complete response dictionary with evaluation and sources
        """
        if not self.knowledge_base_initialized:
            raise ValueError("Knowledge base not initialized. Call load_documents() first.")
        
        logger.info(f"Processing single query with up to {max_iterations} iterations")
        
        try:
            result = await self.rag_system.process_single_query(
                question,
                max_iterations=max_iterations
            )
            
            logger.info(f"Query processed in {result.get('iterations', 0)} iterations")
            
            if result.get('evaluation'):
                eval_score = result['evaluation'].get('overall_score', 0)
                logger.info(f"Final quality score: {eval_score}/10")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in single query inference: {e}")
            raise
    
    def save_knowledge_base(self, path: str = None) -> None:
        """
        Save the current knowledge base to disk.
        
        Args:
            path: Optional path to save the index
        """
        if not self.knowledge_base_initialized:
            logger.warning("No knowledge base to save")
            return
        
        try:
            self.rag_system.save_knowledge_base(path)
            logger.info(f"Knowledge base saved to {path or 'default location'}")
        except Exception as e:
            logger.error(f"Failed to save knowledge base: {e}")
    
    def load_knowledge_base(self, path: str = None) -> bool:
        """
        Load a pre-built knowledge base from disk.
        
        Args:
            path: Path to the saved knowledge base
            
        Returns:
            True if successful, False otherwise
        """
        try:
            success = asyncio.run(self.rag_system.load_knowledge_base(path))
            if success:
                self.knowledge_base_initialized = True
                logger.info("Knowledge base loaded successfully")
            else:
                logger.warning("Failed to load knowledge base")
            return success
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information and statistics."""
        info = {
            'status': 'Ready' if self.knowledge_base_initialized else 'Not initialized',
            'knowledge_base_initialized': self.knowledge_base_initialized,
            'system_stats': self.rag_system.get_system_stats()
        }
        return info
    
    async def add_documents(self, document_paths: List[str]) -> None:
        """
        Add new documents to the existing knowledge base.
        
        Args:
            document_paths: List of paths to new documents
        """
        if not self.knowledge_base_initialized:
            logger.info("No existing knowledge base. Creating new one...")
            await self.load_documents(document_paths)
            return
        
        logger.info(f"Adding {len(document_paths)} new documents to existing knowledge base")
        
        try:
            await self.rag_system.add_documents(document_paths)
            logger.info("Documents added successfully")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

# Backward compatibility alias
class SampleModelPaller:
    """
    Backend-compatible wrapper class for Legal RAG system.
    Provides simplified interface with parallel threaded inference support.
    """
    
    def __init__(self):
        """Initialize the backend-compatible Legal RAG system."""
        # Initialize configuration and RAG system
        self.config = Config()
        self.rag_system = LegalQueryRAG(self.config)
        self.knowledge_base_initialized = False
        
        # Create directories for storing processed documents
        self.processed_docs_dir = Path("processed_documents")
        self.processed_docs_dir.mkdir(exist_ok=True)
        
        self.embeddings_cache_dir = Path("embeddings_cache")
        self.embeddings_cache_dir.mkdir(exist_ok=True)
        
        logger.info("SampleModelPaller (Backend-compatible) system initialized")
        logger.info(f"Processed documents will be saved to: {self.processed_docs_dir}")
    
    def load_document(self, file_path: str) -> None:
        """
        Load and process a PDF document from file path or URL.
        Performs document parsing, embedding generation, and vector DB indexing.
        Saves processed document data to local folder.
        
        Args:
            file_path: Path to PDF file (local path or URL)
        """
        import asyncio
        import urllib.request
        import ssl
        import shutil
        from pathlib import Path
        import hashlib
        
        print(f"Document loading started from: {file_path}")
        logger.info(f"Processing document: {file_path}")
        
        try:
            # Handle URL downloads
            if file_path.startswith(('http://', 'https://')):
                # Download file from URL
                url_hash = hashlib.md5(file_path.encode()).hexdigest()[:10]
                local_filename = self.processed_docs_dir / f"downloaded_{url_hash}.pdf"
                
                print(f"📥 Downloading file from URL...")
                print(f"🌐 URL: {file_path}")
                
                try:
                    # Create a custom opener to handle redirects and headers
                    import urllib.request
                    import ssl
                    
                    # Create SSL context that doesn't verify certificates (for some servers)
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    
                    # Create custom opener
                    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
                    
                    # Add headers to avoid blocking
                    request = urllib.request.Request(
                        file_path,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                    )
                    
                    # Download the file
                    with opener.open(request) as response:
                        with open(local_filename, 'wb') as f:
                            shutil.copyfileobj(response, f)
                    
                    document_path = str(local_filename)
                    print(f"✅ File downloaded successfully to: {local_filename}")
                    
                except Exception as download_error:
                    print(f"❌ Download failed: {download_error}")
                    logger.error(f"URL download failed: {download_error}")
                    raise Exception(f"Failed to download from URL: {download_error}")
                    
            else:
                document_path = file_path
            
            # Verify file exists
            if not Path(document_path).exists():
                raise FileNotFoundError(f"Document not found: {document_path}")
            
            # Copy document to processed folder for record keeping
            doc_name = Path(document_path).name
            processed_doc_path = self.processed_docs_dir / doc_name
            if not processed_doc_path.exists():
                shutil.copy2(document_path, processed_doc_path)
                print(f"Document copied to processed folder: {processed_doc_path}")
            
            # Load and process document using async method
            print("Starting document parsing and embedding generation...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                loop.run_until_complete(self.rag_system.initialize_knowledge_base([document_path]))
                self.knowledge_base_initialized = True
                
                # Save embeddings cache
                cache_file = self.embeddings_cache_dir / f"{doc_name}_embeddings.pkl"
                self.rag_system.save_knowledge_base(str(cache_file))
                
                print("✅ Document processing completed successfully!")
                print(f"📊 Vector database ready with embeddings")
                print(f"💾 Embeddings cached to: {cache_file}")
                
                # Print processing statistics
                stats = self.rag_system.get_system_stats()
                kb_stats = stats.get('knowledge_base', {})
                print(f"📈 Indexed {kb_stats.get('total_documents', 0)} document chunks")
                print(f"🔢 Vector dimensions: {kb_stats.get('dimension', 0)}")
                
                logger.info(f"Document loaded and indexed successfully: {document_path}")
                
            finally:
                loop.close()
                
        except Exception as e:
            error_msg = f"Failed to load document {file_path}: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(error_msg)
            raise
    
    def inference(self, questions: list[str]) -> list[str]:
        """
        Perform parallel threaded inference on a list of questions.
        Returns list of answers with faster response through parallel processing.
        
        Args:
            questions: List of question strings
            
        Returns:
            List of answer strings corresponding to each question
        """
        if not isinstance(questions, list):
            questions = [questions]
        
        if not self.knowledge_base_initialized:
            print("⚠️  Knowledge base not initialized. Please load a document first.")
            logger.warning("Attempted inference without initialized knowledge base")
            return ["Error: No document loaded. Please call load_document() first."] * len(questions)
        
        print(f"🚀 Starting batch inference for {len(questions)} questions...")
        logger.info(f"Processing {len(questions)} questions in batch")
        
        try:
            import asyncio
            
            # Use single event loop for batch processing instead of multiple threads
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Process all questions in a single batch - much more efficient!
                print("Processing all questions simultaneously...")
                start_time = time.time()
                
                # Run batch processing with the RAG system's built-in parallel processing
                results = loop.run_until_complete(
                    self.rag_system.process_batch_queries(
                        questions,
                        use_react=True,
                        use_reranking=True, 
                        use_evaluation=True  # Enable evaluation to detect rejections and trigger fallback
                    )
                )
                
                # Extract answers from results
                answers = []
                fallback_count = 0
                
                for i, result in enumerate(results):
                    if result and 'response' in result:
                        response = result['response']
                        answer = response.get('answer', response.get('full_response', 'No answer generated'))
                        answers.append(str(answer))
                        
                        # Check if fallback was used
                        if response.get('fallback_used', False):
                            fallback_count += 1
                            print(f"🔄 Q{i+1} used fallback (RAG rejected): {questions[i][:50]}...")
                        else:
                            print(f"✅ Q{i+1} completed: {questions[i][:50]}...")
                    else:
                        answers.append("No response generated")
                        print(f"❌ Q{i+1} failed: {questions[i][:50]}...")
                
                end_time = time.time()
                total_time = end_time - start_time
                
                print(f"🎉 Batch inference completed in {total_time:.2f} seconds!")
                print(f"⚡ Average time per question: {total_time/len(questions):.2f} seconds")
                logger.info(f"Successfully processed {len(answers)} questions in batch")
                
                # Print summary
                successful_answers = len([a for a in answers if not a.startswith('Error')])
                print(f"📊 Batch Processing Summary:")
                print(f"   - Total Questions: {len(questions)}")
                print(f"   - Successful Answers: {successful_answers}")
                print(f"   - Fallback Responses: {fallback_count}")
                print(f"   - RAG Responses: {successful_answers - fallback_count}")
                print(f"   - Total Time: {total_time:.2f} seconds")
                print(f"   - Speed: {len(questions)/total_time:.1f} questions/second")
                
                if fallback_count > 0:
                    print(f"ℹ️  {fallback_count} questions used fallback general knowledge responses due to RAG rejection")
                
                return answers
                
            finally:
                loop.close()
            
        except Exception as e:
            error_msg = f"Batch inference failed: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(error_msg)
            return [f"Error: {error_msg}"] * len(questions)
    
    def get_status(self) -> dict:
        """Get current system status and statistics."""
        status = {
            'knowledge_base_initialized': self.knowledge_base_initialized,
            'processed_docs_dir': str(self.processed_docs_dir),
            'embeddings_cache_dir': str(self.embeddings_cache_dir),
            'system_ready': self.knowledge_base_initialized
        }
        
        if self.knowledge_base_initialized:
            try:
                stats = self.rag_system.get_system_stats()
                status.update(stats)
            except Exception as e:
                status['error'] = str(e)
        
        return status