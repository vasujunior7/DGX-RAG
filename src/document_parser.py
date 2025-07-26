from llama_parse import LlamaParse
from langchain.docstore.document import Document
from typing import List
import os

class DocumentParser:
    def __init__(self, api_key: str):
        self.parser = LlamaParse(
            api_key=api_key,
            result_type="text",
            max_timeout=1200
        )
    
    def parse_documents(self, file_paths: List[str]) -> List[Document]:
        print("🔄 Parsing documents...")
        parsed_docs = []
        for path in file_paths:
            doc = self.parser.load_data(path)
            parsed_docs.extend([
                Document(page_content=d.text, metadata={"source": str(path)})
                for d in doc
            ])
        return parsed_docs