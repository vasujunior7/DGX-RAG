from pdf_stream_reader import fetch_pdf_text_from_url
from legal_chunker.chunker import smart_legal_chunk, parallel_smart_legal_chunk
import time

if __name__ == "__main__":
    # Use the same sample PDF URL as before
    sample_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    pdf_text = fetch_pdf_text_from_url(sample_url)
    print("Testing smart_legal_chunk...")
    start = time.time()
    chunks = smart_legal_chunk(pdf_text)
    elapsed = time.time() - start
    print(f"Total chunks: {len(chunks)} (smart_legal_chunk) in {elapsed:.2f}s")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i+1} ---\n{chunk[:500]}\n...")
    print("\nTesting parallel_smart_legal_chunk...")
    start = time.time()
    p_chunks = parallel_smart_legal_chunk(pdf_text)
    elapsed = time.time() - start
    print(f"Total chunks: {len(p_chunks)} (parallel_smart_legal_chunk) in {elapsed:.2f}s")
    for i, chunk in enumerate(p_chunks[:3]):
        print(f"\n--- Parallel Chunk {i+1} ---\n{chunk[:500]}\n...") 