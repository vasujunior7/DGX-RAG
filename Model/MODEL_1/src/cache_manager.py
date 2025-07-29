from typing import List, Dict, Tuple, Optional
import numpy as np
from datetime import datetime, timedelta
import faiss
import pickle
import os
from functools import lru_cache
import hashlib

class SemanticCache:
    def __init__(self, cache_size: int = 1000, similarity_threshold: float = 0.8, ttl_hours: int = 24):
        self.cache_size = cache_size
        self.similarity_threshold = similarity_threshold
        self.ttl_hours = ttl_hours
        self.cache: Dict[str, Tuple[np.ndarray, List[str], datetime]] = {}
        self.index = faiss.IndexFlatL2(768)  # dimension for all-MiniLM-L6-v2
    
    def _compute_cache_key(self, query_embedding: np.ndarray) -> str:
        return str(hash(query_embedding.tobytes()))
    
    def get(self, query_embedding: np.ndarray) -> Optional[List[str]]:
        """Try to find similar cached results"""
        if len(self.cache) == 0:
            return None
            
        # Search for similar queries
        D, I = self.index.search(query_embedding.reshape(1, -1), 1)
        
        if D[0][0] < self.similarity_threshold:
            cache_key = list(self.cache.keys())[I[0][0]]
            cached_embedding, results, timestamp = self.cache[cache_key]
            
            # Check if cache entry has expired
            if datetime.now() - timestamp > timedelta(hours=self.ttl_hours):
                self._remove_cache_entry(cache_key)
                return None
                
            return results
        return None
    
    def add(self, query_embedding: np.ndarray, results: List[str]):
        """Add results to cache"""
        cache_key = self._compute_cache_key(query_embedding)
        
        # If cache is full, remove oldest entry
        if len(self.cache) >= self.cache_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][2])
            self._remove_cache_entry(oldest_key)
        
        self.cache[cache_key] = (query_embedding, results, datetime.now())
        self.index.add(query_embedding.reshape(1, -1))
    
    def _remove_cache_entry(self, cache_key: str):
        """Remove entry from cache and update FAISS index"""
        if cache_key in self.cache:
            del self.cache[cache_key]
            # Rebuild FAISS index
            self.index = faiss.IndexFlatL2(768)
            for key, (embedding, _, _) in self.cache.items():
                self.index.add(embedding.reshape(1, -1))
    
    def save(self, path: str):
        """Save cache to disk"""
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'semantic_cache.pkl'), 'wb') as f:
            pickle.dump(self.cache, f)
    
    def load(self, path: str):
        """Load cache from disk"""
        cache_file = os.path.join(path, 'semantic_cache.pkl')
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                self.cache = pickle.load(f)
            # Rebuild FAISS index
            self.index = faiss.IndexFlatL2(768)
            for key, (embedding, _, _) in self.cache.items():
                self.index.add(embedding.reshape(1, -1))

class ResponseCache:
    def __init__(self, maxsize=1000):
        self.cache = lru_cache(maxsize=maxsize)(self._get_cached_response)
        
    def _get_cache_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str):
        return None  # Implement storage logic
    
    def get(self, query: str):
        cache_key = self._get_cache_key(query)
        return self.cache(cache_key)
    
    def set(self, query: str, response: dict):
        cache_key = self._get_cache_key(query)
        # Implement storage logic