# # # # document_loader.py

# # # from langchain.text_splitter import RecursiveCharacterTextSplitter
# # # from langchain_community.document_loaders import WebBaseLoader

# # # def load_and_split_documents(urls, chunk_size=250, chunk_overlap=0):
# # #     docs = [WebBaseLoader(url).load() for url in urls]
# # #     docs_flat = [item for sublist in docs for item in sublist]

# # #     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
# # #         chunk_size=chunk_size,
# # #         chunk_overlap=chunk_overlap
# # #     )
# # #     return text_splitter.split_documents(docs_flat)


# # # document_loader.py

# # import requests
# # import os
# # from typing import List
# # from langchain.text_splitter import RecursiveCharacterTextSplitter
# # from langchain_community.document_loaders import PyMuPDFLoader

# # def download_pdf(url: str, save_path: str = "temp_policy.pdf") -> str:
# #     """Downloads the PDF from the given URL and saves it locally."""
# #     response = requests.get(url)
# #     with open(save_path, "wb") as f:
# #         f.write(response.content)
# #     return save_path

# # def load_and_split_documents(urls: List[str], chunk_size=250, chunk_overlap=0):
# #     docs_flat = []

# #     for url in urls:
# #         if url.lower().endswith(".pdf"):
# #             pdf_path = download_pdf(url)
# #             loader = PyMuPDFLoader(pdf_path)
# #             documents = loader.load()
# #             docs_flat.extend(documents)
# #             os.remove(pdf_path)  # clean up
# #         else:
# #             raise ValueError("Only PDF URLs are currently supported in this loader.")

# #     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
# #         chunk_size=chunk_size,
# #         chunk_overlap=chunk_overlap
# #     )

# #     return text_splitter.split_documents(docs_flat)


# import requests
# import os
# from typing import List
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyMuPDFLoader

# def download_pdf(url: str, save_path: str = "temp_policy.pdf") -> str:
#     """Downloads the PDF from the given URL and saves it locally."""
#     response = requests.get(url)
#     with open(save_path, "wb") as f:
#         f.write(response.content)
#     return save_path

# def load_and_split_documents(urls: List[str], chunk_size=250, chunk_overlap=0):
#     docs_flat = []

#     for url in urls:
#         if ".pdf" in url.lower():  # FIXED LINE
#             pdf_path = download_pdf(url)
#             loader = PyMuPDFLoader(pdf_path)
#             documents = loader.load()
#             docs_flat.extend(documents)
#             os.remove(pdf_path)  # clean up
#         else:
#             raise ValueError("Only PDF URLs are currently supported in this loader.")

#     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )

#     return text_splitter.split_documents(docs_flat)

import requests
import os
import hashlib
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader

PDF_CACHE_DIR = "cached_pdfs"

# Ensure cache directory exists
os.makedirs(PDF_CACHE_DIR, exist_ok=True)

def get_pdf_filename_from_url(url: str) -> str:
    """Create a consistent filename from the URL using a hash."""
    hashed_name = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(PDF_CACHE_DIR, f"{hashed_name}.pdf")

def download_pdf_if_not_exists(url: str) -> str:
    """Download PDF if not already cached."""
    local_path = get_pdf_filename_from_url(url)
    if not os.path.exists(local_path):
        print(f"Downloading PDF from: {url}")
        response = requests.get(url)
        with open(local_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Using cached PDF: {local_path}")
    return local_path

def load_and_split_documents(urls: List[str], chunk_size=250, chunk_overlap=0):
    docs_flat = []

    for url in urls:
        if ".pdf" in url.lower():
            pdf_path = download_pdf_if_not_exists(url)
            loader = PyMuPDFLoader(pdf_path)
            documents = loader.load()
            docs_flat.extend(documents)
        else:
            raise ValueError("Only PDF URLs are currently supported in this loader.")

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return text_splitter.split_documents(docs_flat)
