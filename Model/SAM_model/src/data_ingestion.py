"""
Data ingestion and preprocessing module for Legal Query RAG system.
"""
import os
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    DirectoryLoader,
    UnstructuredFileLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from .config import Config

logger = logging.getLogger(__name__)

class DocumentIngestion:
    """Handles document ingestion and preprocessing for the RAG system."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""]
        )
        
    async def load_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Load documents from multiple file paths asynchronously.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            List of loaded documents
        """
        tasks = []
        for file_path in file_paths:
            tasks.append(self._load_single_document(file_path))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        documents = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to load {file_paths[i]}: {result}")
            else:
                documents.extend(result)
        
        return documents
    
    async def _load_single_document(self, file_path: str) -> List[Document]:
        """Load a single document based on file extension."""
        path = Path(file_path)
        
        try:
            if path.suffix.lower() == '.pdf':
                loader = PyPDFLoader(file_path)
            elif path.suffix.lower() in ['.txt', '.md']:
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                loader = UnstructuredFileLoader(file_path)
            
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata.update({
                    'source': file_path,
                    'filename': path.name,
                    'file_type': path.suffix
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []
    
    def load_directory(self, directory_path: str, file_types: List[str] = None) -> List[Document]:
        """
        Load all documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            file_types: List of file extensions to include (e.g., ['.pdf', '.txt'])
            
        Returns:
            List of loaded documents
        """
        if file_types is None:
            file_types = ['.pdf', '.txt', '.md', '.docx']
        
        loader = DirectoryLoader(
            directory_path,
            glob=f"**/*{{{','.join(file_types)}}}",
            loader_cls=UnstructuredFileLoader,
            use_multithreading=True
        )
        
        documents = loader.load()
        return documents
    
    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """
        Preprocess and clean document text.
        
        Args:
            documents: List of documents to preprocess
            
        Returns:
            List of preprocessed documents
        """
        preprocessed_docs = []
        
        for doc in documents:
            # Clean text
            cleaned_text = self._clean_text(doc.page_content)
            
            # Skip empty documents
            if not cleaned_text.strip():
                continue
            
            # Update document content
            doc.page_content = cleaned_text
            preprocessed_docs.append(doc)
        
        return preprocessed_docs
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\.,!?;:()\[\]{}"\'-]', ' ', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of document chunks
        """
        chunks = []
        
        for doc in documents:
            doc_chunks = self.text_splitter.split_documents([doc])
            
            # Add chunk metadata
            for i, chunk in enumerate(doc_chunks):
                chunk.metadata.update({
                    'chunk_id': i,
                    'total_chunks': len(doc_chunks),
                    'chunk_size': len(chunk.page_content)
                })
            
            chunks.extend(doc_chunks)
        
        logger.info(f"Created {len(chunks)} document chunks")
        return chunks
    
    async def process_documents(self, file_paths: List[str]) -> List[Document]:
        """
        Complete document processing pipeline.
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            List of processed document chunks
        """
        # Load documents
        documents = await self.load_documents(file_paths)
        
        if not documents:
            logger.warning("No documents loaded")
            return []
        
        # Preprocess
        documents = self.preprocess_documents(documents)
        
        # Chunk documents
        chunks = self.chunk_documents(documents)
        
        logger.info(f"Processed {len(documents)} documents into {len(chunks)} chunks")
        return chunks
