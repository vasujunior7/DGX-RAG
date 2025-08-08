"""
Main Legal Query RAG System
Integrates all components for end-to-end legal document retrieval and generation.
"""
import asyncio
import time
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from .config import Config
from .data_ingestion import DocumentIngestion
from .embeddings import EmbeddingManager
from .vector_db import VectorDatabase
from .react_agent import ReActAgent
from .retrieval import HybridRetriever
from .reranking import DocumentReRanker
from .llm_generator import LLMGenerator
from .evaluation import ResponseEvaluator
from .fallback_llm import FallbackLLMGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalQueryRAG:
    """
    Complete Legal Query RAG system with parallel inference support for 15-20 queries.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.config.validate_config()
        
        # Initialize components
        self.document_ingestion = DocumentIngestion(self.config)
        self.embedding_manager = EmbeddingManager(self.config)
        self.vector_db = VectorDatabase(self.config)
        self.react_agent = ReActAgent(self.config)
        self.reranker = DocumentReRanker(self.config)
        self.llm_generator = LLMGenerator(self.config)
        self.evaluator = ResponseEvaluator(self.config)
        self.fallback_llm = FallbackLLMGenerator(self.config)  # Add fallback LLM
        
        self.retriever = None  # Initialized after vector DB is populated
        
        logger.info("Legal Query RAG system initialized")
    
    async def initialize_knowledge_base(self, document_paths: List[str]) -> None:
        """
        Initialize the knowledge base with legal documents.
        
        Args:
            document_paths: List of paths to legal documents
        """
        logger.info(f"Initializing knowledge base with {len(document_paths)} document paths")
        
        start_time = time.time()
        
        # Step 1: Ingest and preprocess documents
        logger.info("Step 1/3: Ingesting and preprocessing documents...")
        documents = await self.document_ingestion.process_documents(document_paths)
        
        if not documents:
            raise ValueError("No documents were successfully processed")
        
        # Step 2: Generate embeddings
        logger.info("Step 2/3: Generating embeddings...")
        embedded_docs = await self.embedding_manager.embed_documents(documents)
        
        # Step 3: Create vector database
        logger.info("Step 3/3: Creating vector database...")
        self.vector_db.create_index(embedded_docs)
        
        # Initialize hybrid retriever
        self.retriever = HybridRetriever(self.vector_db, self.embedding_manager, self.config)
        
        end_time = time.time()
        logger.info(f"Knowledge base initialized in {end_time - start_time:.2f} seconds")
        logger.info(f"Indexed {len(documents)} documents with {self.vector_db.index.ntotal if self.vector_db.index else 0} vectors")
    
    async def load_knowledge_base(self, index_path: str = None) -> bool:
        """
        Load pre-built knowledge base from disk.
        
        Args:
            index_path: Path to saved index files
            
        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.vector_db.load_index(index_path)
            if success:
                self.retriever = HybridRetriever(self.vector_db, self.embedding_manager, self.config)
                logger.info("Knowledge base loaded successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            return False
    
    def save_knowledge_base(self, index_path: str = None) -> None:
        """
        Save the current knowledge base to disk.
        
        Args:
            index_path: Path to save index files
        """
        try:
            self.vector_db.save_index(index_path)
            logger.info("Knowledge base saved successfully")
        except Exception as e:
            logger.error(f"Failed to save knowledge base: {e}")
    
    async def process_single_query(self, query: str, 
                                 use_react: bool = True,
                                 use_reranking: bool = True,
                                 use_evaluation: bool = True,
                                 max_iterations: int = 2) -> Dict[str, Any]:
        """
        Process a single legal query through the complete RAG pipeline.
        
        Args:
            query: User's legal query
            use_react: Whether to use ReAct agent for query processing
            use_reranking: Whether to use document re-ranking
            use_evaluation: Whether to evaluate the response
            max_iterations: Maximum iterations for improvement loop
            
        Returns:
            Complete response dictionary
        """
        if not self.retriever:
            raise ValueError("Knowledge base not initialized. Call initialize_knowledge_base() first.")
        
        start_time = time.time()
        iteration = 0
        current_query = query
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Processing query iteration {iteration}: {current_query[:100]}...")
            
            try:
                # Step 1: Query processing with ReAct agent (if enabled)
                if use_react:
                    react_result = await self.react_agent.process_query(current_query)
                    processed_query = react_result['processed_query']
                    logger.info(f"ReAct processed query: {processed_query[:100]}...")
                else:
                    processed_query = current_query
                    react_result = None
                
                # Step 2: Hybrid retrieval
                retrieved_docs = await self.retriever.hybrid_search(processed_query)
                logger.info(f"Retrieved {len(retrieved_docs)} documents")
                
                # Step 3: Document re-ranking (if enabled)
                if use_reranking and retrieved_docs:
                    reranked_docs = self.reranker.rerank_documents(processed_query, retrieved_docs)
                    logger.info(f"Re-ranked to {len(reranked_docs)} top documents")
                else:
                    reranked_docs = retrieved_docs
                
                # Step 4: Response generation
                response = await self.llm_generator.generate_response(
                    current_query, reranked_docs
                )
                
                # Step 5: Response evaluation (if enabled)
                if use_evaluation:
                    evaluation = await self.evaluator.evaluate_response(
                        current_query, response, reranked_docs
                    )
                    
                    # Check if regeneration is needed
                    if iteration < max_iterations and self.evaluator.should_regenerate(evaluation):
                        logger.info(f"Quality score {evaluation.get('overall_score', 0):.1f}/10 - Attempting improvement...")
                        
                        # Get improvement suggestions and refine query
                        suggestions = self.evaluator.generate_improvement_suggestions(evaluation)
                        current_query = await self.react_agent.refine_query_with_context(
                            current_query, reranked_docs
                        )
                        continue
                else:
                    evaluation = None
                
                # Success - prepare final response
                end_time = time.time()
                
                return {
                    'original_query': query,
                    'processed_query': processed_query,
                    'response': response,
                    'retrieved_documents': retrieved_docs,
                    'reranked_documents': reranked_docs,
                    'evaluation': evaluation,
                    'react_result': react_result,
                    'processing_time': end_time - start_time,
                    'iterations': iteration,
                    'status': 'success'
                }
                
            except Exception as e:
                logger.error(f"Error in iteration {iteration}: {e}")
                if iteration >= max_iterations:
                    return {
                        'original_query': query,
                        'processed_query': current_query,
                        'response': {'answer': f"Error processing query: {str(e)}"},
                        'retrieved_documents': [],
                        'reranked_documents': [],
                        'evaluation': None,
                        'react_result': None,
                        'processing_time': time.time() - start_time,
                        'iterations': iteration,
                        'status': 'error',
                        'error': str(e)
                    }
        
        # Max iterations reached
        return {
            'original_query': query,
            'processed_query': current_query,
            'response': {'answer': f"Could not generate satisfactory response after {max_iterations} iterations"},
            'retrieved_documents': retrieved_docs if 'retrieved_docs' in locals() else [],
            'reranked_documents': reranked_docs if 'reranked_docs' in locals() else [],
            'evaluation': evaluation if 'evaluation' in locals() else None,
            'react_result': react_result if 'react_result' in locals() else None,
            'processing_time': time.time() - start_time,
            'iterations': iteration,
            'status': 'max_iterations_reached'
        }
    
    async def process_batch_queries(self, queries: List[str],
                                  use_react: bool = True,
                                  use_reranking: bool = True,
                                  use_evaluation: bool = True) -> List[Dict[str, Any]]:
        """
        Process multiple queries in parallel (supports 15-20 queries efficiently).
        
        Args:
            queries: List of user queries
            use_react: Whether to use ReAct agent for query processing
            use_reranking: Whether to use document re-ranking
            use_evaluation: Whether to evaluate responses
            
        Returns:
            List of complete response dictionaries
        """
        if not self.retriever:
            raise ValueError("Knowledge base not initialized. Call initialize_knowledge_base() first.")
        
        if len(queries) > self.config.MAX_CONCURRENT_QUERIES:
            logger.warning(f"Batch size {len(queries)} exceeds maximum {self.config.MAX_CONCURRENT_QUERIES}")
        
        start_time = time.time()
        logger.info(f"Processing batch of {len(queries)} queries in parallel")
        
        try:
            # Step 1: Parallel query processing with ReAct agent
            if use_react:
                logger.info("Step 1/5: Processing queries with ReAct agent...")
                react_results = await self.react_agent.process_multiple_queries(queries)
                processed_queries = [result['processed_query'] for result in react_results]
            else:
                processed_queries = queries
                react_results = [None] * len(queries)
            
            # Step 2: Parallel hybrid retrieval
            logger.info("Step 2/5: Performing parallel hybrid retrieval...")
            batch_retrieved_docs = await self.retriever.batch_hybrid_search(processed_queries)
            
            # Step 3: Parallel document re-ranking
            if use_reranking:
                logger.info("Step 3/5: Re-ranking documents...")
                batch_reranked_docs = await self.reranker.batch_rerank(
                    processed_queries, batch_retrieved_docs
                )
            else:
                batch_reranked_docs = batch_retrieved_docs
            
            # Step 4: Parallel response generation
            logger.info("Step 4/5: Generating responses...")
            responses = await self.llm_generator.generate_batch_responses(
                queries, batch_reranked_docs
            )
            
            # Step 5: Parallel response evaluation
            if use_evaluation:
                logger.info("Step 5/5: Evaluating responses...")
                evaluations = await self.evaluator.batch_evaluate_responses(
                    queries, responses, batch_reranked_docs
                )
            else:
                evaluations = [None] * len(queries)
            
            # Step 6: Fallback processing for rejected responses
            logger.info("Step 6/6: Processing fallback responses for rejected answers...")
            
            # Identify queries that need fallback responses
            rejected_indices = []
            fallback_queries = []
            
            for i, evaluation in enumerate(evaluations):
                if evaluation and evaluation.get('recommendation') == 'REJECT':
                    rejected_indices.append(i)
                    fallback_queries.append(queries[i])
                    logger.info(f"Query {i+1} marked for fallback: {queries[i][:50]}...")
            
            # Generate fallback responses for rejected queries
            if fallback_queries:
                logger.info(f"Generating {len(fallback_queries)} fallback responses using general knowledge...")
                fallback_responses = await self.fallback_llm.generate_batch_fallback_responses(fallback_queries)
                
                # Replace rejected responses with fallback responses
                for idx, fallback_idx in enumerate(rejected_indices):
                    original_response = responses[fallback_idx]
                    fallback_response = fallback_responses[idx]
                    
                    # Update the response with fallback content but keep original metadata
                    responses[fallback_idx] = {
                        **original_response,  # Keep original structure
                        'answer': fallback_response.get('answer', original_response.get('answer', 'No answer available')),
                        'fallback_used': True,
                        'fallback_reason': 'RAG response was rejected by evaluation',
                        'original_rag_answer': original_response.get('answer', ''),
                        'source': fallback_response.get('source', 'fallback_llm'),
                        'type': fallback_response.get('type', 'general_legal_guidance'),
                        'disclaimer': fallback_response.get('disclaimer', ''),
                        'recommendation': fallback_response.get('recommendation', '')
                    }
                    
                    # Update evaluation to reflect fallback usage
                    if evaluations[fallback_idx]:
                        evaluations[fallback_idx]['fallback_used'] = True
                        evaluations[fallback_idx]['original_recommendation'] = 'REJECT'
                        evaluations[fallback_idx]['recommendation'] = 'FALLBACK'
                        evaluations[fallback_idx]['fallback_reason'] = 'RAG response rejected, fallback response provided'
                
                logger.info(f"Successfully generated {len(fallback_queries)} fallback responses")
            else:
                logger.info("No rejected responses found, no fallback processing needed")
            
            # Combine results
            final_results = []
            for i in range(len(queries)):
                result = {
                    'original_query': queries[i],
                    'processed_query': processed_queries[i] if i < len(processed_queries) else queries[i],
                    'response': responses[i] if i < len(responses) else {'answer': 'Error generating response'},
                    'retrieved_documents': batch_retrieved_docs[i] if i < len(batch_retrieved_docs) else [],
                    'reranked_documents': batch_reranked_docs[i] if i < len(batch_reranked_docs) else [],
                    'evaluation': evaluations[i] if i < len(evaluations) else None,
                    'react_result': react_results[i] if i < len(react_results) else None,
                    'processing_time': time.time() - start_time,
                    'batch_size': len(queries),
                    'status': 'success'
                }
                final_results.append(result)
            
            end_time = time.time()
            logger.info(f"Completed batch processing in {end_time - start_time:.2f} seconds")
            logger.info(f"Average time per query: {(end_time - start_time) / len(queries):.2f} seconds")
            
            return final_results
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            # Return error results for all queries
            error_results = []
            for query in queries:
                error_results.append({
                    'original_query': query,
                    'processed_query': query,
                    'response': {'answer': f"Batch processing error: {str(e)}"},
                    'retrieved_documents': [],
                    'reranked_documents': [],
                    'evaluation': None,
                    'react_result': None,
                    'processing_time': time.time() - start_time,
                    'batch_size': len(queries),
                    'status': 'error',
                    'error': str(e)
                })
            return error_results
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        embedding_model = self.config.ST_EMBEDDING_MODEL if self.config.EMBEDDING_PROVIDER == "sentence_transformers" else self.config.OPENAI_EMBEDDING_MODEL
        
        return {
            'config': {
                'embedding_model': embedding_model,
                'llm_model': self.config.LLM_MODEL,
                'max_concurrent_queries': self.config.MAX_CONCURRENT_QUERIES,
                'chunk_size': self.config.CHUNK_SIZE,
                'top_k_retrieval': self.config.TOP_K_RETRIEVAL
            },
            'knowledge_base': self.vector_db.get_index_stats(),
            'retrieval': self.retriever.get_retrieval_stats() if self.retriever else {'status': 'Not initialized'},
            'reranking': self.reranker.get_rerank_stats(),
            'generation': self.llm_generator.get_generation_stats(),
            'status': 'Ready' if self.retriever else 'Knowledge base not initialized'
        }
    
    async def add_documents(self, document_paths: List[str]) -> None:
        """
        Add new documents to existing knowledge base.
        
        Args:
            document_paths: List of new document paths to add
        """
        logger.info(f"Adding {len(document_paths)} new documents to knowledge base")
        
        # Process new documents
        new_documents = await self.document_ingestion.process_documents(document_paths)
        
        if not new_documents:
            logger.warning("No new documents were processed")
            return
        
        # Generate embeddings for new documents
        new_embedded_docs = await self.embedding_manager.embed_documents(new_documents)
        
        # Add to existing vector database
        existing_docs = list(zip(self.vector_db.documents, self.vector_db.embeddings))
        all_embedded_docs = existing_docs + new_embedded_docs
        
        # Recreate index with all documents
        self.vector_db.create_index(all_embedded_docs)
        
        # Update retriever
        self.retriever = HybridRetriever(self.vector_db, self.embedding_manager, self.config)
        
        logger.info(f"Added {len(new_documents)} documents. Total documents: {len(self.vector_db.documents)}")
