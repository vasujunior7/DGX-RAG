"""
Vector database management for Legal Query RAG system.
"""
import os
import pickle
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import logging

try:
    import faiss
except ImportError:
    faiss = None

from langchain_core.documents import Document

from .config import Config
from .embeddings import EmbeddingManager

logger = logging.getLogger(__name__)

class VectorDatabase:
    """Manages vector storage and retrieval using FAISS."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.index = None
        self.documents = []
        self.embeddings = []
        self.index_path = self.config.INDEX_PATH
        
        if faiss is None:
            raise ImportError("FAISS is required for vector database. Install with: pip install faiss-cpu")
    
    def create_index(self, embedded_docs: List[Tuple[Document, np.ndarray]]) -> None:
        """
        Create and populate FAISS index with embedded documents.
        
        Args:
            embedded_docs: List of (document, embedding) tuples
        """
        if not embedded_docs:
            logger.warning("No embedded documents provided")
            return
        
        # Extract documents and embeddings
        self.documents = [doc for doc, _ in embedded_docs]
        embeddings_list = [emb for _, emb in embedded_docs]
        
        # Filter out empty embeddings
        valid_docs = []
        valid_embeddings = []
        
        for doc, emb in zip(self.documents, embeddings_list):
            if len(emb) > 0:
                valid_docs.append(doc)
                valid_embeddings.append(emb)
        
        if not valid_embeddings:
            logger.error("No valid embeddings found")
            return
        
        self.documents = valid_docs
        self.embeddings = np.array(valid_embeddings).astype('float32')
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        
        # Add embeddings to index
        self.index.add(self.embeddings)
        
        logger.info(f"Created FAISS index with {len(self.documents)} documents")
    
    def search(self, query_embedding: np.ndarray, k: int = None) -> List[Tuple[Document, float]]:
        """
        Search for similar documents using query embedding.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of top results to return
            
        Returns:
            List of (document, similarity_score) tuples
        """
        if k is None:
            k = self.config.TOP_K_RETRIEVAL
        
        if self.index is None:
            logger.error("Index not created. Call create_index first.")
            return []
        
        if len(query_embedding) == 0:
            logger.error("Empty query embedding")
            return []
        
        # Normalize query embedding
        query_emb = query_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_emb)
        
        # Search index
        scores, indices = self.index.search(query_emb, min(k, len(self.documents)))
        
        # Return results with similarity scores
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.documents):
                # Filter by similarity threshold
                if score >= self.config.SIMILARITY_THRESHOLD:
                    results.append((self.documents[idx], float(score)))
        
        return results
    
    def batch_search(self, query_embeddings: List[np.ndarray], 
                    k: int = None) -> List[List[Tuple[Document, float]]]:
        """
        Perform batch search for multiple queries.
        
        Args:
            query_embeddings: List of query embedding vectors
            k: Number of top results per query
            
        Returns:
            List of search results for each query
        """
        results = []
        for query_emb in query_embeddings:
            query_results = self.search(query_emb, k)
            results.append(query_results)
        
        return results
    
    def save_index(self, file_path: str = None) -> None:
        """Save FAISS index and metadata to disk."""
        if file_path is None:
            file_path = self.index_path
        
        if self.index is None:
            logger.error("No index to save")
            return
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, f"{file_path}.faiss")
            
            # Save documents and metadata
            metadata = {
                'documents': self.documents,
                'config': {
                    'embedding_dimension': self.config.EMBEDDING_DIMENSION,
                    'similarity_threshold': self.config.SIMILARITY_THRESHOLD
                }
            }
            
            with open(f"{file_path}.pkl", 'wb') as f:
                pickle.dump(metadata, f)
            
            logger.info(f"Saved index to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def load_index(self, file_path: str = None) -> bool:
        """
        Load FAISS index and metadata from disk.
        
        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = self.index_path
        
        try:
            # Load FAISS index
            if not os.path.exists(f"{file_path}.faiss"):
                logger.error(f"Index file {file_path}.faiss not found")
                return False
            
            self.index = faiss.read_index(f"{file_path}.faiss")
            
            # Load metadata
            if os.path.exists(f"{file_path}.pkl"):
                with open(f"{file_path}.pkl", 'rb') as f:
                    metadata = pickle.load(f)
                    self.documents = metadata['documents']
            
            logger.info(f"Loaded index from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index."""
        if self.index is None:
            return {'status': 'No index created'}
        
        return {
            'status': 'Active',
            'total_vectors': self.index.ntotal,
            'dimension': self.index.d,
            'total_documents': len(self.documents)
        }
