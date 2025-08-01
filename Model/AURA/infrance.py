import os
import time
import pickle
import json
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from dotenv import load_dotenv

from pdf_stream_reader import fetch_pdf_text_from_url
from legal_chunker.chunker import parallel_smart_legal_chunk
from legal_chunker.embed_and_index import embed_and_index
from legal_chunker.llm_answer import get_llm_answer

load_dotenv()


class SampleModelPaller:
    def __init__(self, api_key: str = None, force_regenerate: bool = True):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.force_regenerate = force_regenerate
        self.model = None
        self.index = None
        self.chunks = None
        self.documents = []  # Store documents sent to model
        print("SampleModel initialized with API key:", "✓ Provided" if self.api_key else "✗ Missing")
        if force_regenerate:
            print("🔄 Force regenerate mode: Will create fresh chunks and index")

    def load_document(self, file_path: str, force_fresh: bool = None) -> None:
        """Load and preprocess document for RAG pipeline"""
        print("Document loaded from:", file_path)
        
        # Determine if we should force regeneration
        should_regenerate = force_fresh if force_fresh is not None else self.force_regenerate
        
        # Load or preprocess chunks and index
        chunks_path = "chunks.pkl"
        index_path = "faiss.index"
        
        # Remove existing files if force regeneration is requested
        if should_regenerate:
            if Path(chunks_path).exists():
                os.remove(chunks_path)
                print("🗑️ Removed existing chunks file")
            if Path(index_path).exists():
                os.remove(index_path)
                print("🗑️ Removed existing index file")
        
        if Path(chunks_path).exists() and Path(index_path).exists() and not should_regenerate:
            print("✅ Preprocessed files found. Loading existing data.")
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)
            self.index = faiss.read_index(index_path)
        else:
            print("🔄 Preprocessing document (creating fresh chunks and index)...")
            pdf_text = fetch_pdf_text_from_url(file_path)
            self.chunks = parallel_smart_legal_chunk(pdf_text)
            print(f"✂️ Total chunks created: {len(self.chunks)}")
            self.index, _ = embed_and_index(self.chunks)
            
            # Save preprocessed data
            with open(chunks_path, "wb") as f:
                pickle.dump(self.chunks, f)
            faiss.write_index(self.index, index_path)
            print("✅ Preprocessing complete (fresh files saved).")
        
        # Load embedding model
        if self.model is None:
            print("🧠 Loading embedding model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Store document info
        self.documents.append({
            "file_path": file_path,
            "chunk_count": len(self.chunks),
            "loaded_at": time.time()
        })
        
        return None
    
    def inference(self, questions: List[str]) -> List[str]:
        """Make inference on multiple questions using RAG pipeline"""
        print("Inference made with questions:", len(questions))
        
        if not self.chunks or not self.index or not self.model:
            raise ValueError("Document must be loaded before inference")
        
        # Store questions sent to model
        for question in questions:
            self.documents.append({
                "type": "question",
                "content": question,
                "timestamp": time.time()
            })
        
        # Run batch RAG pipeline
        results = self._batch_rag_pipeline(questions, k=5, max_workers=5)
        
        # Store results
        for i, result in enumerate(results):
            self.documents.append({
                "type": "answer", 
                "question": questions[i],
                "content": result,
                "timestamp": time.time()
            })
        
        return results
    
    def _fast_rag_pipeline(self, question: str, k: int = 5) -> str:
        """Single question RAG pipeline"""
        query_emb = self.model.encode([question], convert_to_numpy=True)
        D, I = self.index.search(query_emb, k)
        top_chunks = [self.chunks[i] for i in I[0] if i >= 0]
        answer = get_llm_answer(top_chunks, question, self.api_key)
        return answer
    
    def _batch_rag_pipeline(self, questions: List[str], k: int = 5, max_workers: int = 5) -> List[str]:
        """Batch processing of questions using ThreadPoolExecutor"""
        results = [None] * len(questions)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {
                executor.submit(self._fast_rag_pipeline, q, k): i
                for i, q in enumerate(questions)
            }
            for future in as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    results[i] = future.result()
                except Exception as e:
                    results[i] = f"Error: {e}"
        return results
    
    def save_session(self, filepath: str = "session_data.json") -> None:
        """Save all documents and interactions to file"""
        session_data = {
            "documents": self.documents,
            "session_info": {
                "total_chunks": len(self.chunks) if self.chunks else 0,
                "model_loaded": self.model is not None,
                "api_key_provided": self.api_key is not None
            }
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        print(f"Session data saved to {filepath}")


# Legacy constants and functions for backward compatibility
PDF_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

QUESTIONS = [
    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
    "What is the waiting period for pre-existing diseases (PED) to be covered?",
    "Does this policy cover maternity expenses, and what are the conditions?",
    "What is the waiting period for cataract surgery?",
    "Are the medical expenses for an organ donor covered under this policy?",
    "What is the No Claim Discount (NCD) offered in this policy?",
    "Is there a benefit for preventive health check-ups?",
    "How does the policy define a 'Hospital'?",
    "What is the extent of coverage for AYUSH treatments?",
    "Are there any sub-limits on room rent and ICU charges for Plan A?",
]

PDF_URL = "https://hackrx.blob.core.windows.net/assets/hackrx_6/policies/EDLHLGA23009V012223.pdf?sv=2023-01-03&st=2025-07-30T06%3A46%3A49Z&se=2025-09-01T06%3A46%3A00Z&sr=c&sp=rl&sig=9szykRKdGYj0BVm1skP%2BX8N9%2FRENEn2k7MQPUp33jyQ%3D"


QUESTIONS = [
    "What is the maximum distance covered under the Air Ambulance benefit, and how is reimbursement calculated if the distance exceeds this limit?",
    "Under what conditions will Air Ambulance expenses be reimbursed under this policy?",
    "What are the exclusions listed for Air Ambulance coverage in this add-on?",
    "Does the policy cover routine medical care for expectant mothers, and what does it include?",
    "What options does the insured have for the duration of Well Mother cover during pregnancy?",
    "Are infertility treatments covered under the Well Mother or Well Baby add-ons?",
    "What is included under Healthy Baby Expenses or Well Baby Care after birth?",
    "Does the policy cover preventive care services and immunizations for a newborn, and for how long?",
    "Are air ambulance expenses payable through cashless claims or reimbursement only?",
    "Can the insured claim transportation costs if the destination hospital has similar capabilities as the origin hospital?",
]




if __name__ == "__main__":
    print("🚀 Starting SampleModelPaller pipeline...")
    start = time.time()

    # Initialize the model with force regeneration enabled
    model_paller = SampleModelPaller(force_regenerate=True)
    
    # Load document (will create fresh chunks)
    model_paller.load_document(PDF_URL)
    
    # Run inference
    print("❓ Answering questions...")
    answers = model_paller.inference(QUESTIONS)

    print(answers)
    # Output
    with open("answers.json", "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)

    # Save session data
    model_paller.save_session("session_data.json")

    print("✅ Answers saved to answers.json")
    print("✅ Session data saved to session_data.json")
    print(f"⏱️ Total time: {time.time() - start:.2f} seconds")


# Legacy functions for backward compatibility
def preprocess_if_needed(force_regenerate: bool = False):
    chunks_path = "chunks.pkl"
    index_path = "faiss.index"
    
    # Remove existing files if force regeneration is requested
    if force_regenerate:
        if Path(chunks_path).exists():
            os.remove(chunks_path)
            print("🗑️ Removed existing chunks file")
        if Path(index_path).exists():
            os.remove(index_path)
            print("🗑️ Removed existing index file")
    
    if Path(chunks_path).exists() and Path(index_path).exists() and not force_regenerate:
        print("✅ Preprocessed files found. Skipping preprocessing.")
        with open(chunks_path, "rb") as f:
            chunks = pickle.load(f)
        index = faiss.read_index(index_path)
    else:
        print("🔄 Preprocessing starting (creating fresh chunks and index)...")
        pdf_text = fetch_pdf_text_from_url(PDF_URL)
        chunks = parallel_smart_legal_chunk(pdf_text)
        print(f"✂️ Total chunks created: {len(chunks)}")
        index, _ = embed_and_index(chunks)
        with open(chunks_path, "wb") as f:
            pickle.dump(chunks, f)
        faiss.write_index(index, index_path)
        print("✅ Preprocessing complete (fresh files saved).")
    return chunks, index

def fast_rag_pipeline(question, model, index, chunks, k=5):
    query_emb = model.encode([question], convert_to_numpy=True)
    D, I = index.search(query_emb, k)
    top_chunks = [chunks[i] for i in I[0] if i >= 0]
    answer = get_llm_answer(top_chunks, question)
    return answer

def batch_rag_pipeline(questions, model, index, chunks, k=5, max_workers=5):
    results = [None] * len(questions)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(fast_rag_pipeline, q, model, index, chunks, k): i
            for i, q in enumerate(questions)
        }
        for future in as_completed(future_to_index):
            i = future_to_index[future]
            try:
                results[i] = future.result()
            except Exception as e:
                results[i] = f"Error: {e}"
    return results
