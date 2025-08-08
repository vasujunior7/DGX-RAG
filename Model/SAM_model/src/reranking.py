"""
Re-ranking module for Legal Query RAG system.
Implements cross-encoder re-ranking for improved retrieval relevance.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import logging

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None

from .config import Config

logger = logging.getLogger(__name__)

class DocumentReRanker:
    """
    Re-ranks retrieved documents using a cross-encoder model for better relevance.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the cross-encoder re-ranking model."""
        if CrossEncoder is None:
            logger.warning("sentence-transformers not installed. Re-ranking will be disabled.")
            return
        
        try:
            # Try loading the configured model first
            self.model = CrossEncoder(self.config.RERANK_MODEL)
            logger.info(f"Loaded re-ranking model: {self.config.RERANK_MODEL}")
        except Exception as e:
            logger.warning(f"Failed to load {self.config.RERANK_MODEL}: {e}")
            
            # Try a smaller, more reliable model as fallback
            try:
                fallback_model = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
                logger.info(f"Trying fallback model: {fallback_model}")
                self.model = CrossEncoder(fallback_model)
                logger.info(f"Loaded fallback re-ranking model: {fallback_model}")
            except Exception as e2:
                logger.error(f"Failed to load fallback re-ranking model: {e2}")
                logger.info("Re-ranking will be disabled - documents will use original retrieval scores")
                self.model = None
    
    def rerank_documents(self, query: str, 
                        retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Re-rank retrieved documents based on query-document relevance.
        
        Args:
            query: Original search query
            retrieved_docs: List of retrieved document dictionaries
            
        Returns:
            List of re-ranked documents with updated scores
        """
        if not retrieved_docs:
            return retrieved_docs
        
        if not self.model:
            logger.info("No re-ranking model available, using simple text similarity fallback")
            return self._fallback_rerank(query, retrieved_docs)
        
        try:
            # Prepare query-document pairs
            pairs = []
            for doc in retrieved_docs:
                content = doc.get('content', '')
                # Truncate content to avoid token limits
                truncated_content = content[:1000] if len(content) > 1000 else content
                pairs.append([query, truncated_content])
            
            # Get cross-encoder scores
            scores = self.model.predict(pairs)
            
            # Update documents with new scores
            reranked_docs = []
            for doc, score in zip(retrieved_docs, scores):
                doc_copy = doc.copy()
                doc_copy['rerank_score'] = float(score)
                doc_copy['original_score'] = doc_copy.get('combined_score', 0.0)
                reranked_docs.append(doc_copy)
            
            # Sort by re-ranking score
            reranked_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            # Return top-k re-ranked results
            top_k = min(self.config.RERANK_TOP_K, len(reranked_docs))
            return reranked_docs[:top_k]
            
        except Exception as e:
            logger.error(f"Error during re-ranking: {e}")
            logger.info("Falling back to simple text similarity")
            return self._fallback_rerank(query, retrieved_docs)
    
    def _fallback_rerank(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simple fallback re-ranking using text similarity when CrossEncoder is not available.
        """
        query_words = set(query.lower().split())
        
        reranked_docs = []
        for doc in retrieved_docs:
            content = doc.get('content', '').lower()
            content_words = set(content.split())
            
            # Simple Jaccard similarity
            if query_words and content_words:
                intersection = len(query_words.intersection(content_words))
                union = len(query_words.union(content_words))
                similarity = intersection / union if union > 0 else 0.0
            else:
                similarity = 0.0
            
            # Also consider original score
            original_score = doc.get('combined_score', 0.0)
            
            # Combine similarity with original score
            combined_score = 0.6 * similarity + 0.4 * original_score
            
            doc_copy = doc.copy()
            doc_copy['rerank_score'] = combined_score
            doc_copy['original_score'] = original_score
            doc_copy['text_similarity'] = similarity
            reranked_docs.append(doc_copy)
        
        # Sort by combined score
        reranked_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Return top-k results
        top_k = min(self.config.RERANK_TOP_K, len(reranked_docs))
        return reranked_docs[:top_k]
    
    async def batch_rerank(self, queries: List[str], 
                          batch_retrieved_docs: List[List[Dict[str, Any]]]) -> List[List[Dict[str, Any]]]:
        """
        Re-rank documents for multiple queries in parallel.
        
        Args:
            queries: List of search queries
            batch_retrieved_docs: List of retrieved document lists for each query
            
        Returns:
            List of re-ranked document lists
        """
        # Use semaphore to limit concurrent re-ranking operations
        semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_QUERIES)
        
        async def rerank_single_query(query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            async with semaphore:
                # Run re-ranking in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self.rerank_documents, query, docs)
        
        tasks = []
        for query, docs in zip(queries, batch_retrieved_docs):
            tasks.append(rerank_single_query(query, docs))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error re-ranking query {i}: {result}")
                final_results.append(batch_retrieved_docs[i])  # Return original results
            else:
                final_results.append(result)
        
        return final_results
    
    def calculate_relevance_score(self, query: str, document: str) -> float:
        """
        Calculate relevance score for a single query-document pair.
        
        Args:
            query: Search query
            document: Document content
            
        Returns:
            Relevance score (higher is better)
        """
        if not self.model:
            return 0.0
        
        try:
            score = self.model.predict([[query, document]])[0]
            return float(score)
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.0
    
    def filter_by_relevance_threshold(self, reranked_docs: List[Dict[str, Any]], 
                                    threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Filter documents by minimum relevance threshold.
        
        Args:
            reranked_docs: List of re-ranked documents
            threshold: Minimum relevance score threshold
            
        Returns:
            List of documents above the threshold
        """
        if not self.model:
            return reranked_docs
        
        filtered_docs = []
        for doc in reranked_docs:
            rerank_score = doc.get('rerank_score', 0.0)
            if rerank_score >= threshold:
                filtered_docs.append(doc)
        
        logger.info(f"Filtered {len(filtered_docs)} documents from {len(reranked_docs)} based on relevance threshold {threshold}")
        return filtered_docs
    
    def diversify_results(self, reranked_docs: List[Dict[str, Any]], 
                         diversity_lambda: float = 0.5) -> List[Dict[str, Any]]:
        """
        Apply diversity-aware re-ranking to avoid redundant results.
        
        Args:
            reranked_docs: List of re-ranked documents
            diversity_lambda: Balance between relevance (0.0) and diversity (1.0)
            
        Returns:
            List of diversified documents
        """
        if len(reranked_docs) <= 1:
            return reranked_docs
        
        # Simple diversity implementation based on content similarity
        selected_docs = [reranked_docs[0]]  # Always include top result
        
        for candidate in reranked_docs[1:]:
            # Calculate maximum similarity with already selected documents
            max_similarity = 0.0
            candidate_content = candidate.get('content', '').lower()
            
            for selected in selected_docs:
                selected_content = selected.get('content', '').lower()
                # Simple Jaccard similarity
                similarity = self._jaccard_similarity(candidate_content, selected_content)
                max_similarity = max(max_similarity, similarity)
            
            # Calculate diversity-aware score
            relevance_score = candidate.get('rerank_score', 0.0)
            diversity_score = 1.0 - max_similarity
            
            combined_score = (1 - diversity_lambda) * relevance_score + diversity_lambda * diversity_score
            candidate['diversity_score'] = combined_score
            
            # Add if diverse enough or if we haven't reached minimum count
            if diversity_score > 0.3 or len(selected_docs) < 3:
                selected_docs.append(candidate)
        
        # Sort by diversity-aware score if computed
        if len(selected_docs) > 1 and 'diversity_score' in selected_docs[0]:
            selected_docs.sort(key=lambda x: x.get('diversity_score', 0.0), reverse=True)
        
        return selected_docs
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based Jaccard similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_rerank_stats(self) -> Dict[str, Any]:
        """Get re-ranking system statistics."""
        return {
            'model_loaded': self.model is not None,
            'model_name': self.config.RERANK_MODEL,
            'rerank_top_k': self.config.RERANK_TOP_K,
            'status': 'Active' if self.model else 'Disabled'
        }
