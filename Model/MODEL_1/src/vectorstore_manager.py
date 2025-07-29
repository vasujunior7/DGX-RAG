from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from typing import List, Optional
import torch
import os
from .cache_manager import SemanticCache

class VectorStoreManager:
    def __init__(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        device = 'cpu'
        print(f"Using device: {device}")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': device}
        )
        self.vectorstore = None
        self.cache = SemanticCache()

    def create_vectorstore(self, documents: List[Document]) -> None:
        print("📦 Creating FAISS index...")
        self.vectorstore = FAISS.from_documents(documents, self.embedding_model)
        
    def save_vectorstore(self, path: str) -> None:
        if self.vectorstore is None:
            raise ValueError("No vectorstore to save. Create one first using create_vectorstore()")
        self.vectorstore.save_local(path)
        print(f"✅ Vector index saved as '{path}'")
    
    def load_vectorstore(self, path: str) -> None:
        print("📂 Loading vector store...")
        self.vectorstore = FAISS.load_local(
            folder_path=path,
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True
        )
        print("✅ Vector store loaded successfully")

    def save_state(self, path: str) -> None:
        """Save both vectorstore and cache state"""
        os.makedirs(path, exist_ok=True)
        self.save_vectorstore(path)
        self.cache.save(path)
        print("✅ Saved complete state to", path)
    
    def load_state(self, path: str) -> None:
        """Load both vectorstore and cache state"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")
        self.load_vectorstore(path)
        self.cache.load(path)
        print("✅ Loaded complete state from", path)

    def get_retriever(self, k: int = 4):
        if self.vectorstore is None:
            raise ValueError("No vectorstore available. Create or load one first.")
        return self.vectorstore.as_retriever(
            search_kwargs={"k": k},
            search_type="similarity"
        )