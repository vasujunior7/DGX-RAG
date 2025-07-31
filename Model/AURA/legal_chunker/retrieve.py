from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


def retrieve_top_k(query: str, index: faiss.IndexFlatL2, chunks: List[str], k: int = 5) -> List[str]:
    """
    Embeds the user query and retrieves the top-k most similar chunks from the FAISS index.
    Returns the top-k text chunks.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, k)
    return [chunks[i] for i in I[0] if i >= 0] 