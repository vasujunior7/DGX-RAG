from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List

class DocumentSplitter:
    @staticmethod
    def smart_split(doc: Document) -> List[Document]:
        length = len(doc.page_content)
        
        # Optimize chunk sizes
        if length < 1500:
            chunk_size, overlap = 500, 50
        elif length < 5000:
            chunk_size, overlap = 1000, 100
        else:
            chunk_size, overlap = 1500, 150
            
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return splitter.split_documents([doc])
    
    def process_documents(self, docs: List[Document]) -> List[Document]:
        print("🔀 Splitting documents smartly...")
        split_docs = []
        for doc in docs:
            split_docs.extend(self.smart_split(doc))
        print(f"✅ Total chunks created: {len(split_docs)}")
        return split_docs