"""
Configuration class for RAG system
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

key = "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"

@dataclass
class RAGConfig:
    """Configuration class for RAG system"""
    openai_api_key: str = os.getenv("OPENAI_API_KEY", key)
    chunk_size: int = 1000
    chunk_overlap: int = 200
    batch_size: int = 8
    max_threads: int = 4
    similarity_threshold: float = 0.7
    max_chunks_retrieve: int = 5
    chunking_timeout: int = 7  # seconds
    save_dir: str = "./documents"