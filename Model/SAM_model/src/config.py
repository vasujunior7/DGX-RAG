"""
Configuration settings for the Legal Query RAG system.
"""
from json import load
import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
class Config:
    """Configuration class for the Legal Query RAG system."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Embedding Model Configuration
    EMBEDDING_PROVIDER: str = "sentence_transformers"  # "openai" or "sentence_transformers"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"  # OpenAI model
    ST_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Sentence Transformers model
    EMBEDDING_DIMENSION: int = 384  # for all-MiniLM-L6-v2 (768 for all-mpnet-base-v2)
    USE_GPU: bool = True  # Use GPU for embeddings if available
    
    # LLM Configuration
    LLM_MODEL: str = "gpt-4o"  # or "gpt-4o"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1
    
    # Document Processing
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_CHUNKS_PER_QUERY: int = 10
    
    # Parallel Processing
    MAX_CONCURRENT_QUERIES: int = 20
    BATCH_SIZE: int = 5
    
    # Vector Database
    VECTOR_DB_TYPE: str = "faiss"  # "faiss", "pinecone", "weaviate"
    INDEX_PATH: str = "vector_index"
    
    # Retrieval Configuration
    TOP_K_RETRIEVAL: int = 10
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Re-ranking
    RERANK_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    RERANK_TOP_K: int = 5
    
    # Evaluation
    EVALUATION_MODEL: str = "gpt-4o"
    MIN_ANSWER_QUALITY_SCORE: float = 0.7
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate the configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
