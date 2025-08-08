
"""
Embedding generation module for Legal Query RAG system.
Supports both OpenAI and Sentence Transformers embeddings with GPU acceleration.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import logging
import torch

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    OpenAIEmbeddings = None

from langchain_core.documents import Document

from .config import Config

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """Manages document and query embeddings using Sentence Transformers or OpenAI API."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.model = None
        self.device = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the embedding model based on configuration."""
        if self.config.EMBEDDING_PROVIDER == "sentence_transformers":
            self._initialize_sentence_transformers()
        elif self.config.EMBEDDING_PROVIDER == "openai":
            self._initialize_openai_embeddings()
        else:
            logger.error(f"Unknown embedding provider: {self.config.EMBEDDING_PROVIDER}")
            raise ValueError(f"Unsupported embedding provider: {self.config.EMBEDDING_PROVIDER}")
    
    def _initialize_sentence_transformers(self):
        """Initialize Sentence Transformers model with GPU support."""
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
        
        # Determine device
        if self.config.USE_GPU and torch.cuda.is_available():
            self.device = 'cuda'
            logger.info("Using GPU for embeddings")
        else:
            self.device = 'cpu'
            logger.info("Using CPU for embeddings")
        
        try:
            # Load the model
            self.model = SentenceTransformer(self.config.ST_EMBEDDING_MODEL, device=self.device)
            logger.info(f"Loaded Sentence Transformer model: {self.config.ST_EMBEDDING_MODEL} on {self.device}")
            
            # Update embedding dimension based on actual model
            test_embedding = self.model.encode(["test"])
            actual_dim = len(test_embedding[0])
            if actual_dim != self.config.EMBEDDING_DIMENSION:
                logger.info(f"Updating embedding dimension from {self.config.EMBEDDING_DIMENSION} to {actual_dim}")
                self.config.EMBEDDING_DIMENSION = actual_dim
                
        except Exception as e:
            logger.error(f"Failed to load Sentence Transformer model: {e}")
            # Fallback to a smaller, more reliable model
            try:
                fallback_model = "all-MiniLM-L6-v2"
                logger.info(f"Trying fallback model: {fallback_model}")
                self.model = SentenceTransformer(fallback_model, device=self.device)
                logger.info(f"Loaded fallback model: {fallback_model}")
            except Exception as e2:
                logger.error(f"Failed to load fallback model: {e2}")
                raise
    
    def _initialize_openai_embeddings(self):
        """Initialize OpenAI embeddings."""
        if OpenAIEmbeddings is None:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        
        if not self.config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key required for OpenAI embeddings")
        
        self.model = OpenAIEmbeddings(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.OPENAI_EMBEDDING_MODEL
        )
        logger.info(f"Initialized OpenAI embeddings: {self.config.OPENAI_EMBEDDING_MODEL}")
    
    async def embed_documents(self, documents: List[Document]) -> List[Tuple[Document, np.ndarray]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            documents: List of documents to embed
            
        Returns:
            List of tuples containing (document, embedding)
        """
        logger.info(f"Generating embeddings for {len(documents)} documents")
        
        if self.config.EMBEDDING_PROVIDER == "sentence_transformers":
            return await self._embed_documents_st(documents)
        else:
            return await self._embed_documents_openai(documents)
    
    async def _embed_documents_st(self, documents: List[Document]) -> List[Tuple[Document, np.ndarray]]:
        """Generate embeddings using Sentence Transformers."""
        texts = [doc.page_content for doc in documents]
        
        try:
            # Run embedding in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, 
                lambda: self.model.encode(
                    texts, 
                    batch_size=self.config.BATCH_SIZE,
                    show_progress_bar=True,
                    convert_to_numpy=True
                )
            )
            
            embedded_docs = []
            for doc, embedding in zip(documents, embeddings):
                embedded_docs.append((doc, embedding))
            
            logger.info(f"Generated embeddings for {len(embedded_docs)} documents using Sentence Transformers")
            return embedded_docs
            
        except Exception as e:
            logger.error(f"Error generating document embeddings: {e}")
            # Return empty embeddings for failed documents
            return [(doc, np.array([])) for doc in documents]
    
    async def _embed_documents_openai(self, documents: List[Document]) -> List[Tuple[Document, np.ndarray]]:
        """Generate embeddings using OpenAI API."""
        # Process in batches to avoid API rate limits
        batch_size = self.config.BATCH_SIZE
        embedded_docs = []
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            batch_texts = [doc.page_content for doc in batch]
            
            try:
                # Generate embeddings for batch
                batch_embeddings = await self.model.aembed_documents(batch_texts)
                
                # Pair documents with embeddings
                for doc, embedding in zip(batch, batch_embeddings):
                    embedded_docs.append((doc, np.array(embedding)))
                
                logger.info(f"Processed batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
                
                # Small delay to respect rate limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error embedding batch {i//batch_size + 1}: {e}")
                # Add empty embeddings for failed batch
                for doc in batch:
                    embedded_docs.append((doc, np.array([])))
        
        logger.info(f"Generated embeddings for {len(embedded_docs)} documents using OpenAI")
        return embedded_docs
    
    async def embed_queries(self, queries: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple queries.
        
        Args:
            queries: List of query strings
            
        Returns:
            List of query embeddings
        """
        logger.info(f"Generating embeddings for {len(queries)} queries")
        
        if self.config.EMBEDDING_PROVIDER == "sentence_transformers":
            return await self._embed_queries_st(queries)
        else:
            return await self._embed_queries_openai(queries)
    
    async def _embed_queries_st(self, queries: List[str]) -> List[np.ndarray]:
        """Generate query embeddings using Sentence Transformers."""
        try:
            # Run embedding in thread pool
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                lambda: self.model.encode(
                    queries,
                    batch_size=len(queries),  # Process all queries at once
                    show_progress_bar=False,
                    convert_to_numpy=True
                )
            )
            
            logger.info(f"Generated embeddings for {len(embeddings)} queries using Sentence Transformers")
            return [np.array(emb) for emb in embeddings]
            
        except Exception as e:
            logger.error(f"Error embedding queries: {e}")
            return [np.array([]) for _ in queries]
    
    async def _embed_queries_openai(self, queries: List[str]) -> List[np.ndarray]:
        """Generate query embeddings using OpenAI API."""
        try:
            query_embeddings = await self.model.aembed_documents(queries)
            embeddings = [np.array(emb) for emb in query_embeddings]
            
            logger.info(f"Generated embeddings for {len(embeddings)} queries using OpenAI")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error embedding queries: {e}")
            return [np.array([]) for _ in queries]
    
    async def embed_single_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query string
            
        Returns:
            Query embedding
        """
        embeddings = await self.embed_queries([query])
        return embeddings[0] if embeddings else np.array([])
    
    def calculate_similarity(self, query_embedding: np.ndarray, 
                           doc_embeddings: List[np.ndarray]) -> List[float]:
        """
        Calculate cosine similarity between query and document embeddings.
        
        Args:
            query_embedding: Query embedding vector
            doc_embeddings: List of document embedding vectors
            
        Returns:
            List of similarity scores
        """
        if len(query_embedding) == 0:
            return [0.0] * len(doc_embeddings)
        
        similarities = []
        
        for doc_emb in doc_embeddings:
            if len(doc_emb) == 0:
                similarities.append(0.0)
                continue
            
            # Cosine similarity
            dot_product = np.dot(query_embedding, doc_emb)
            norm_query = np.linalg.norm(query_embedding)
            norm_doc = np.linalg.norm(doc_emb)
            
            if norm_query == 0 or norm_doc == 0:
                similarity = 0.0
            else:
                similarity = dot_product / (norm_query * norm_doc)
            
            similarities.append(float(similarity))
        
        return similarities
    
    def get_top_k_similar(self, query_embedding: np.ndarray, 
                         embedded_docs: List[Tuple[Document, np.ndarray]], 
                         k: int = None) -> List[Tuple[Document, float]]:
        """
        Get top-k most similar documents for a query.
        
        Args:
            query_embedding: Query embedding vector
            embedded_docs: List of (document, embedding) tuples
            k: Number of top results to return
            
        Returns:
            List of (document, similarity_score) tuples, sorted by similarity
        """
        if k is None:
            k = self.config.TOP_K_RETRIEVAL
        
        # Extract embeddings
        doc_embeddings = [emb for _, emb in embedded_docs]
        
        # Calculate similarities
        similarities = self.calculate_similarity(query_embedding, doc_embeddings)
        
        # Create (document, similarity) pairs and sort by similarity
        doc_sim_pairs = [(doc, sim) for (doc, _), sim in zip(embedded_docs, similarities)]
        doc_sim_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and return top-k
        filtered_pairs = [
            (doc, sim) for doc, sim in doc_sim_pairs 
            if sim >= self.config.SIMILARITY_THRESHOLD
        ]
        
        return filtered_pairs[:k]
    
    def get_embedding_info(self) -> Dict[str, Any]:
        """Get information about the embedding system."""
        info = {
            'provider': self.config.EMBEDDING_PROVIDER,
            'dimension': self.config.EMBEDDING_DIMENSION,
        }
        
        if self.config.EMBEDDING_PROVIDER == "sentence_transformers":
            info.update({
                'model': self.config.ST_EMBEDDING_MODEL,
                'device': self.device,
                'gpu_available': torch.cuda.is_available(),
                'gpu_enabled': self.config.USE_GPU
            })
        else:
            info.update({
                'model': self.config.OPENAI_EMBEDDING_MODEL,
                'api_key_set': bool(self.config.OPENAI_API_KEY)
            })
        
        return info
