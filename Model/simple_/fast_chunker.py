"""
Ultra-fast text chunking module
Optimized for speed with character-based splitting
"""
import re
import time
from typing import List


class FastChunker:
    """Ultra-fast text chunking optimized for speed"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        # Pre-compile regex patterns for performance
        self.sentence_pattern = re.compile(r'[.!?]+\s+')
        self.whitespace_pattern = re.compile(r'\s+')
        print(f"FastChunker initialized - Chunk size: {chunk_size}, Overlap: {overlap}")
    
    def clean_text(self, text: str) -> str:
        """Fast text cleaning"""
        # Remove extra whitespace
        text = self.whitespace_pattern.sub(' ', text)
        return text.strip()
    
    def chunk_text_fast(self, text: str) -> List[str]:
        """Ultra-fast chunking using character-based splitting"""
        start_time = time.time()
        print(f"Starting fast chunking for text of length: {len(text)}")
        
        # Clean text quickly
        text = self.clean_text(text)
        text_length = len(text)
        
        if text_length <= self.chunk_size:
            print("Text is smaller than chunk size, returning single chunk")
            return [text]
        
        chunks = []
        start = 0
        
        while start < text_length:
            end = start + self.chunk_size
            
            # If this is the last chunk, take everything remaining
            if end >= text_length:
                chunks.append(text[start:])
                break
            
            # Try to find a good breaking point (sentence end)
            chunk_text = text[start:end]
            
            # Look for sentence boundaries in the last 100 characters
            search_start = max(0, len(chunk_text) - 100)
            sentence_match = None
            
            for match in self.sentence_pattern.finditer(chunk_text[search_start:]):
                sentence_match = match
            
            if sentence_match:
                # Break at sentence boundary
                actual_end = start + search_start + sentence_match.end()
                chunks.append(text[start:actual_end])
                start = actual_end - self.overlap
            else:
                # No sentence boundary found, break at word
                chunk_text = text[start:end]
                last_space = chunk_text.rfind(' ')
                if last_space > self.chunk_size * 0.8:  # At least 80% of chunk size
                    actual_end = start + last_space
                    chunks.append(text[start:actual_end])
                    start = actual_end - self.overlap
                else:
                    # Just break at character limit
                    chunks.append(chunk_text)
                    start = end - self.overlap
            
            # Ensure we don't go backwards
            if start < 0:
                start = 0
        
        # Performance check
        elapsed = time.time() - start_time
        chunks_clean = [chunk.strip() for chunk in chunks if chunk.strip()]
        
        print(f"Chunking completed in {elapsed:.2f} seconds")
        print(f"Created {len(chunks_clean)} chunks")
        
        if elapsed > 7:
            print(f"WARNING: Chunking took {elapsed:.2f} seconds (exceeds 7s limit)")
        
        return chunks_clean