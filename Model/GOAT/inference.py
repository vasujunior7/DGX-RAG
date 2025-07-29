# main.py

from config import *
from document_loader import load_and_split_documents
from vectorstore_manager import create_vectorstore
from retriever import get_retriever
from rag_chain import build_rag_chain, generate_answer
from graders.retrieval_grader import grade_retrieval
from graders.hallucination_grader import grade_hallucination
from graders.answer_grader import grade_answer


# class SampleModel:
#     def __init__(self, api_key: str = None):
#         self.api_key = api_key
#         print("SampleModel initialized with API key:")


#     def load_document(self, file_path: str) -> None:
#         print("Document loaded from:", file_path)
#         return None
    
#     def inference(self, question: str) -> str:
#         print("Inference made with question:", question)
#         return "Sample response to the question."



class GOATModel:
    def __init__(self):
        self.documents = []
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None

    def load_document(self, urls):
        urls = [urls]
        self.documents = load_and_split_documents(urls)
        self.vectorstore = create_vectorstore(self.documents)
        self.retriever = get_retriever(self.vectorstore)
        self.rag_chain = build_rag_chain()
        
    def inference(self, question: str):
        generation = generate_answer(self.rag_chain, self.retriever.invoke(question), question)
        return generation



if __name__ == "__main__":
    # Step 1: Load and split documents
    urls = [
        "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    ]
    documents = load_and_split_documents(urls)

    # Step 2: Vectorstore and Retriever
    vectorstore = create_vectorstore(documents)
    retriever = get_retriever(vectorstore)

    # Step 3: RAG chain and questions
    questions = [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]

    rag_chain = build_rag_chain()

    for q in questions:
        docs = retriever.invoke(q)  # preferred in latest langchain-core
        generation = generate_answer(rag_chain, docs, q)

        # print(f"\n📄 Question: {q}\n")
        # print("📄 Retrieved Document Grade:")
        # print(grade_retrieval(docs[0].page_content, q))

        # print("\n🧠 Hallucination Grade:")
        # print(grade_hallucination(docs, generation))

        # print("\n✅ Answer Grade:")
        # print(grade_answer(q, generation))

        print("\n📝 Final Generated Answer:")
        print(generation)
        print("=" * 80)



