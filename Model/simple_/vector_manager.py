# # """
# # Vector embedding and retrieval management using FAISS
# # Handles OpenAI embeddings and similarity search
# # """
# # from typing import List, Tuple
# # from langchain.embeddings import OpenAIEmbeddings
# # from langchain.schema import Document
# # from langchain.vectorstores import FAISS
# # from config import RAGConfig


# # class VectorManager:
# #     """Manages vector embeddings and retrieval using FAISS"""
    
# #     def __init__(self, config: RAGConfig):
# #         self.config = config
# #         print("Initializing OpenAI embeddings...")
# #         self.embeddings = OpenAIEmbeddings(
# #             openai_api_key=config.openai_api_key,
# #             chunk_size=1000  # Batch size for embedding
# #         )
# #         self.vector_store = None
# #         self.chunks = []
# #         print("VectorManager initialized")
    
# #     def create_embeddings(self, chunks: List[str]) -> None:
# #         """Create embeddings for chunks and build FAISS index"""
# #         try:
# #             print(f"Creating embeddings for {len(chunks)} chunks...")
# #             self.chunks = chunks
            
# #             # Create documents
# #             documents = [Document(page_content=chunk) for chunk in chunks]
            
# #             # Create FAISS vector store with batch embedding
# #             print("Building FAISS index...")
# #             self.vector_store = FAISS.from_documents(
# #                 documents, 
# #                 self.embeddings
# #             )
            
# #             print(f"Vector store created successfully with {len(chunks)} chunks")
            
# #         except Exception as e:
# #             raise Exception(f"Failed to create embeddings: {str(e)}")
    
# #     def retrieve_relevant_chunks(self, query: str) -> Tuple[List[str], List[float]]:
# #         """Retrieve relevant chunks with similarity scores"""
# #         if not self.vector_store:
# #             print("No vector store available")
# #             return [], []
        
# #         try:
# #             # Perform similarity search with scores
# #             results = self.vector_store.similarity_search_with_score(
# #                 query, 
# #                 k=self.config.max_chunks_retrieve
# #             )
            
# #             chunks = []
# #             scores = []
            
# #             for doc, score in results:
# #                 # Convert distance to similarity (FAISS returns distance)
# #                 similarity = 1 / (1 + score)
                
# #                 if similarity >= self.config.similarity_threshold:
# #                     chunks.append(doc.page_content)
# #                     scores.append(similarity)
            
# #             print(f"Retrieved {len(chunks)} relevant chunks for query")
# #             return chunks, scores
            
# #         except Exception as e:
# #             print(f"Retrieval error: {str(e)}")
# #             return [], []
    
# #     def get_vector_store_info(self) -> dict:
# #         """Get information about the current vector store"""
# #         if not self.vector_store:
# #             return {"status": "No vector store loaded"}
        
# #         return {
# #             "status": "Vector store loaded",
# #             "total_chunks": len(self.chunks),
# #             "similarity_threshold": self.config.similarity_threshold,
# #             "max_retrieve": self.config.max_chunks_retrieve
# #         }

# """
# Vector embedding and retrieval management using FAISS
# Handles OpenAI embeddings and similarity search
# """
# from typing import List, Tuple
# from langchain_openai import OpenAIEmbeddings
# from langchain.schema import Document
# from langchain.vectorstores import FAISS
# from config import RAGConfig


# class VectorManager:
#     """Manages vector embeddings and retrieval using FAISS"""
    
#     def __init__(self, config: RAGConfig):
#         self.config = config
#         print("Initializing OpenAI embeddings...")
#         self.embeddings = OpenAIEmbeddings(
#             openai_api_key=config.openai_api_key
#         )
#         self.vector_store = None
#         self.chunks = []
#         print("VectorManager initialized")
    
#     def create_embeddings(self, chunks: List[str]) -> None:
#         """Create embeddings for chunks and build FAISS index"""
#         try:
#             print(f"Creating embeddings for {len(chunks)} chunks...")
#             self.chunks = chunks
            
#             # Create documents
#             documents = [Document(page_content=chunk) for chunk in chunks]
            
#             # Create FAISS vector store with batch embedding
#             print("Building FAISS index...")
#             self.vector_store = FAISS.from_documents(
#                 documents, 
#                 self.embeddings
#             )
            
#             print(f"Vector store created successfully with {len(chunks)} chunks")
            
#         except Exception as e:
#             raise Exception(f"Failed to create embeddings: {str(e)}")
    
#     def retrieve_relevant_chunks(self, query: str) -> Tuple[List[str], List[float]]:
#         """Retrieve relevant chunks with similarity scores"""
#         if not self.vector_store:
#             print("No vector store available")
#             return [], []
        
#         try:
#             # Perform similarity search with scores
#             results = self.vector_store.similarity_search_with_score(
#                 query, 
#                 k=self.config.max_chunks_retrieve
#             )
            
#             chunks = []
#             scores = []
            
#             for doc, score in results:
#                 # Convert distance to similarity (FAISS returns distance)
#                 similarity = 1 / (1 + score)
                
#                 if similarity >= self.config.similarity_threshold:
#                     chunks.append(doc.page_content)
#                     scores.append(similarity)
            
#             print(f"Retrieved {len(chunks)} relevant chunks for query")
#             return chunks, scores
            
#         except Exception as e:
#             print(f"Retrieval error: {str(e)}")
#             return [], []
    
#     def get_vector_store_info(self) -> dict:
#         """Get information about the current vector store"""
#         if not self.vector_store:
#             return {"status": "No vector store loaded"}
        
#         return {
#             "status": "Vector store loaded",
#             "total_chunks": len(self.chunks),
#             "similarity_threshold": self.config.similarity_threshold,
#             "max_retrieve": self.config.max_chunks_retrieve
#         }

"""
Vector embedding and retrieval management using FAISS
Handles OpenAI embeddings and similarity search
"""
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from simple_.config import RAGConfig


class VectorManager:
    """Manages vector embeddings and retrieval using FAISS"""
    
    def __init__(self, config: RAGConfig):
        self.config = config
        print("Initializing OpenAI embeddings...")
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=config.openai_api_key
        )
        self.vector_store = None
        self.chunks = []
        print("VectorManager initialized")
    
    def create_embeddings(self, chunks: List[str]) -> None:
        """Create embeddings for chunks and build FAISS index"""
        try:
            print(f"Creating embeddings for {len(chunks)} chunks...")
            self.chunks = chunks
            
            # Create documents
            documents = [Document(page_content=chunk) for chunk in chunks]
            
            # Create FAISS vector store with batch embedding
            print("Building FAISS index...")
            self.vector_store = FAISS.from_documents(
                documents, 
                self.embeddings
            )
            
            print(f"Vector store created successfully with {len(chunks)} chunks")
            
        except Exception as e:
            raise Exception(f"Failed to create embeddings: {str(e)}")
    
    def retrieve_relevant_chunks(self, query: str) -> Tuple[List[str], List[float]]:
        """Retrieve relevant chunks with similarity scores"""
        if not self.vector_store:
            print("No vector store available")
            return [], []
        
        try:
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(
                query, 
                k=self.config.max_chunks_retrieve
            )
            
            chunks = []
            scores = []
            
            for doc, score in results:
                # Convert distance to similarity (FAISS returns distance)
                similarity = 1 / (1 + score)
                
                if similarity >= self.config.similarity_threshold:
                    chunks.append(doc.page_content)
                    scores.append(similarity)
            
            print(f"Retrieved {len(chunks)} relevant chunks for query")
            return chunks, scores
            
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return [], []
    
    def get_vector_store_info(self) -> dict:
        """Get information about the current vector store"""
        if not self.vector_store:
            return {"status": "No vector store loaded"}
        
        return {
            "status": "Vector store loaded",
            "total_chunks": len(self.chunks),
            "similarity_threshold": self.config.similarity_threshold,
            "max_retrieve": self.config.max_chunks_retrieve
        }