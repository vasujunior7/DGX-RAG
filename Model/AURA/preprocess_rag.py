# import concurrent.futures
# from pdf_stream_reader import fetch_pdf_text_from_url
# from legal_chunker.chunker import smart_legal_chunk, parallel_smart_legal_chunk
# from legal_chunker.embed_and_index import embed_and_index
# import pickle
# import faiss
# import json
# from concurrent.futures import ThreadPoolExecutor, as_completed

# PDF_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

# def fast_rag_pipeline(question, k=5):
#     print("Fetching and chunking PDF...")
#     pdf_text = fetch_pdf_text_from_url(PDF_URL)
#     # Use parallel chunking for speed
#     chunks = parallel_smart_legal_chunk(pdf_text)
#     print(f"Total chunks: {len(chunks)}. Embedding and indexing...")
#     index, _ = embed_and_index(chunks)
#     print("Saving chunks and index...")
#     with open("chunks.pkl", "wb") as f:
#         pickle.dump(chunks, f)
#     faiss.write_index(index, "faiss.index")
#     print("Preprocessing complete.")
#     return "Answer to your question" # Placeholder for actual RAG logic

# def batch_rag_pipeline(questions, k=5, max_workers=5):
#     results = {}
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         future_to_question = {executor.submit(fast_rag_pipeline, q, k): q for q in questions}
#         for future in as_completed(future_to_question):
#             q = future_to_question[future]
#             try:
#                 results[q] = future.result()
#             except Exception as e:
#                 results[q] = f"Error: {e}"
#     return results

# if __name__ == "__main__":
#     import time
#     # QUESTIONS = ["What is the policy?", "What are the terms?", "What is the contact information?"]
#     print("Batch processing questions in parallel...")
#     start = time.time()
#     # answers = batch_rag_pipeline(QUESTIONS, max_workers=5)
#     elapsed = time.time() - start
#     # print(json.dumps(answers, indent=2, ensure_ascii=False))
#     print(f"Total time for batch: {elapsed:.2f} seconds") 
import pickle
import faiss
from pdf_stream_reader import fetch_pdf_text_from_url
from legal_chunker.chunker import parallel_smart_legal_chunk
from legal_chunker.embed_and_index import embed_and_index

PDF_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

def preprocess_document(pdf_url: str, index_path="faiss.index", chunks_path="chunks.pkl"):
    print("🔄 Fetching PDF from URL...")
    pdf_text = fetch_pdf_text_from_url(pdf_url)

    print("✂️ Chunking document (parallel, clause-aware)...")
    chunks = parallel_smart_legal_chunk(pdf_text)
    print(f"✅ Total chunks created: {len(chunks)}")

    print("🧠 Embedding and indexing chunks...")
    index, _ = embed_and_index(chunks)

    print(f"💾 Saving FAISS index to: {index_path}")
    faiss.write_index(index, index_path)

    print(f"💾 Saving chunks to: {chunks_path}")
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Preprocessing complete.")

if __name__ == "__main__":
    import time
    start = time.time()
    preprocess_document(PDF_URL)
    print(f"⏱️ Total preprocessing time: {time.time() - start:.2f} seconds")
