import os
from dotenv import load_dotenv
from src.document_parser import DocumentParser
from src.document_splitter import DocumentSplitter
from src.vectorstore_manager import VectorStoreManager
from src.qa_system import QASystem
import datetime
def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    parser = DocumentParser(api_key=os.environ["LLAMA_PARSE_API_KEY"])
    splitter = DocumentSplitter()
    vector_manager = VectorStoreManager()
    
    # Document paths
    document_paths = ["CHOTGDP23004V012223.pdf"]
    
    # Process documents 
    docs = parser.parse_documents(document_paths)
    split_docs = splitter.process_documents(docs)
    
    # Create and save vector store with cache
    vector_manager.create_vectorstore(split_docs)
    vector_manager.save_state("vector_store_index")
    
    # Initialize QA system
    retriever = vector_manager.get_retriever()
    qa_system = QASystem(retriever)
    
    # Batch process questions
    questions = [
        "What if my bags disappear while traveling — will the company help?",
        "If I lose my luggage during a trip, can I get assistance?",
        "Am I covered if my belongings are lost on a trip?"
    ]
    
    print("🚀 Processing batch questions...")
    results = qa_system.batch_ask_questions(questions)
    
    for query, result in zip(questions, results):
        print(f"\n🤔 Question: {query}")
        if "error" in result:
            print("❌ Error:", result["error"])
        else:
            print("🧠 Answer:", result["answer"])
            print("📚 Sources:", ", ".join(result["sources"]))
            print("-" * 80)

if __name__ == "__main__":
    start = datetime.datetime.now()
    print(f"🔄 Starting HackRX Model 1 at {start.strftime('%Y-%m-%d %H:%M:%S')}")
    main()

    end = datetime.datetime.now()
    print(f"🔄 Finished HackRX Model 1 at {end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏳ Total time taken: {end - start}")