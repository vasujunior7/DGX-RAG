from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def embed_and_index(chunks: List[str], batch_size: int = 64, device: str = None) -> Tuple[faiss.IndexFlatL2, np.ndarray]:
    """
    Embeds the list of text chunks using 'all-MiniLM-L6-v2' and builds a FAISS index.
    Returns the FAISS index and the embeddings array.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device) if device else SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True, batch_size=batch_size)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings 