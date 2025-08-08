"""
Retrieval module for Legal Query RAG system.
Implements hybrid search combining semantic and keyword-based retrieval.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import logging
import re
from collections import defaultdict

import numpy as np

from .config import Config
from .vector_db import VectorDatabase
from .embeddings import EmbeddingManager

logger = logging.getLogger(__name__)

class HybridRetriever:
    """
    Hybrid retrieval system combining semantic search with keyword/BM25 search.
    """
    
    def __init__(self, vector_db: VectorDatabase, embedding_manager: EmbeddingManager, 
                 config: Config = None):
        self.vector_db = vector_db
        self.embedding_manager = embedding_manager
        self.config = config or Config()
        
        # Initialize BM25 parameters
        self.k1 = 1.5  # Term frequency saturation parameter
        self.b = 0.75  # Length normalization parameter
        
        # Build keyword index
        self.keyword_index = {}
        self.doc_lengths = {}
        self.avg_doc_length = 0
        self._build_keyword_index()
    
    def _build_keyword_index(self) -> None:
        """Build BM25 keyword index from documents."""
        if not self.vector_db.documents:
            return
        
        # Tokenize all documents
        doc_tokens = []
        total_tokens = 0
        
        for i, doc in enumerate(self.vector_db.documents):
            tokens = self._tokenize(doc.page_content)
            doc_tokens.append(tokens)
            self.doc_lengths[i] = len(tokens)
            total_tokens += len(tokens)
            
            # Build inverted index
            for token in set(tokens):
                if token not in self.keyword_index:
                    self.keyword_index[token] = []
                self.keyword_index[token].append(i)
        
        self.avg_doc_length = total_tokens / len(self.vector_db.documents) if self.vector_db.documents else 0
        self.doc_tokens = doc_tokens
        
        logger.info(f"Built keyword index with {len(self.keyword_index)} unique terms")
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25."""
        # Convert to lowercase and extract alphanumeric tokens
        tokens = re.findall(r'\b[a-z]+\b', text.lower())
        return tokens
    
    def _calculate_bm25_score(self, query_tokens: List[str], doc_id: int, 
                             total_docs: int) -> float:
        """Calculate BM25 score for a document given query tokens."""
        score = 0.0
        doc_length = self.doc_lengths.get(doc_id, 0)
        
        for term in query_tokens:
            if term not in self.keyword_index:
                continue
            
            # Term frequency in document
            doc_tokens = self.doc_tokens[doc_id]
            tf = doc_tokens.count(term)
            
            # Document frequency
            df = len(self.keyword_index[term])
            
            # IDF calculation
            idf = np.log((total_docs - df + 0.5) / (df + 0.5))
            
            # BM25 score calculation
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))
            
            score += idf * (numerator / denominator)
        
        return score
    
    def keyword_search(self, query: str, k: int = None) -> List[Tuple[int, float]]:
        """
        Perform BM25 keyword search.
        
        Args:
            query: Search query
            k: Number of top results to return
            
        Returns:
            List of (document_id, bm25_score) tuples
        """
        if k is None:
            k = self.config.TOP_K_RETRIEVAL
        
        if not self.vector_db.documents:
            return []
        
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        # Calculate BM25 scores for all documents
        scores = []
        total_docs = len(self.vector_db.documents)
        
        for doc_id in range(total_docs):
            score = self._calculate_bm25_score(query_tokens, doc_id, total_docs)
            if score > 0:
                scores.append((doc_id, score))
        
        # Sort by score and return top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
    
    async def semantic_search(self, query: str, k: int = None) -> List[Tuple[int, float]]:
        """
        Perform semantic search using embeddings.
        
        Args:
            query: Search query
            k: Number of top results to return
            
        Returns:
            List of (document_id, similarity_score) tuples
        """
        if k is None:
            k = self.config.TOP_K_RETRIEVAL
        
        # Get query embedding
        query_embedding = await self.embedding_manager.embed_single_query(query)
        
        if len(query_embedding) == 0:
            return []
        
        # Search vector database
        results = self.vector_db.search(query_embedding, k)
        
        # Convert to (doc_id, score) format
        doc_scores = []
        for doc, score in results:
            # Find document ID
            for i, vector_doc in enumerate(self.vector_db.documents):
                if vector_doc == doc:
                    doc_scores.append((i, score))
                    break
        
        return doc_scores
    
    async def hybrid_search(self, query: str, k: int = None, 
                          semantic_weight: float = 0.7, 
                          keyword_weight: float = 0.3) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query: Search query
            k: Number of top results to return
            semantic_weight: Weight for semantic search scores
            keyword_weight: Weight for keyword search scores
            
        Returns:
            List of document dictionaries with combined scores
        """
        if k is None:
            k = self.config.TOP_K_RETRIEVAL
        
        # Perform both searches
        semantic_results = await self.semantic_search(query, k * 2)  # Get more for fusion
        keyword_results = self.keyword_search(query, k * 2)
        
        # Normalize scores
        semantic_scores = self._normalize_scores([score for _, score in semantic_results])
        keyword_scores = self._normalize_scores([score for _, score in keyword_results])
        
        # Create score dictionaries
        semantic_dict = {doc_id: score for (doc_id, _), score in zip(semantic_results, semantic_scores)}
        keyword_dict = {doc_id: score for (doc_id, _), score in zip(keyword_results, keyword_scores)}
        
        # Combine scores
        combined_scores = defaultdict(float)
        all_doc_ids = set(semantic_dict.keys()) | set(keyword_dict.keys())
        
        for doc_id in all_doc_ids:
            semantic_score = semantic_dict.get(doc_id, 0.0)
            keyword_score = keyword_dict.get(doc_id, 0.0)
            
            combined_score = (semantic_weight * semantic_score + 
                            keyword_weight * keyword_score)
            combined_scores[doc_id] = combined_score
        
        # Sort by combined score
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Prepare final results
        final_results = []
        for doc_id, score in sorted_results[:k]:
            if doc_id < len(self.vector_db.documents):
                doc = self.vector_db.documents[doc_id]
                final_results.append({
                    'document': doc,
                    'combined_score': score,
                    'semantic_score': semantic_dict.get(doc_id, 0.0),
                    'keyword_score': keyword_dict.get(doc_id, 0.0),
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
        
        return final_results
    
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        """Normalize scores to [0, 1] range using min-max normalization."""
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [1.0] * len(scores)
        
        return [(score - min_score) / (max_score - min_score) for score in scores]
    
    async def batch_hybrid_search(self, queries: List[str], k: int = None) -> List[List[Dict[str, Any]]]:
        """
        Perform batch hybrid search for multiple queries.
        
        Args:
            queries: List of search queries
            k: Number of top results per query
            
        Returns:
            List of search results for each query
        """
        # Use semaphore to limit concurrent searches
        semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_QUERIES)
        
        async def search_single_query(query: str) -> List[Dict[str, Any]]:
            async with semaphore:
                return await self.hybrid_search(query, k)
        
        tasks = [search_single_query(query) for query in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error searching query {i}: {result}")
                final_results.append([])
            else:
                final_results.append(result)
        
        return final_results
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """Get retrieval system statistics."""
        return {
            'total_documents': len(self.vector_db.documents),
            'unique_terms': len(self.keyword_index),
            'average_doc_length': self.avg_doc_length,
            'vector_db_stats': self.vector_db.get_index_stats()
        }
