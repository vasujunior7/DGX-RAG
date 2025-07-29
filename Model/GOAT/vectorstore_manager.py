# # vectorstore_manager.py

# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings

# def create_vectorstore(documents, collection_name="rag-chroma"):
#     embedding = OpenAIEmbeddings()
#     vectorstore = Chroma.from_documents(
#         documents=documents,
#         embedding=embedding,
#         collection_name=collection_name
#     )
#     return vectorstore

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vectorstore(documents, collection_name="rag-chroma"):
    # Use Hugging Face sentence-transformers embeddings (open-source)
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        collection_name=collection_name
    )
    return vectorstore
