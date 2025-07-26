# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq

# class QASystem:
#     def __init__(self, retriever, model_name="llama3-8b-8192", temperature=0):
#         self.llm = ChatGroq(model_name=model_name, temperature=temperature)
#         self.qa = RetrievalQA.from_chain_type(
#             llm=self.llm,
#             retriever=retriever,
#             chain_type="stuff"
#         )
    
#     def ask_question(self, query: str) -> str:
#         answer = self.qa.run(query)
#         return answer

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import Dict, Any
from langchain.schema import BaseRetriever
from concurrent.futures import ThreadPoolExecutor
from typing import List

class QASystem:
    def __init__(self, retriever: BaseRetriever, model_name: str = "llama3-8b-8192", temperature: float = 0):
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model_name=model_name, 
            temperature=temperature,
            max_tokens=1000
        )
        
        # Create prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create RetrievalQA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def ask_question(self, query: str) -> Dict[str, Any]:
        try:
            result = self.qa({"query": query})
            return {
                "answer": result["result"],
                "sources": [doc.metadata.get("source", "Unknown") 
                          for doc in result.get("source_documents", [])]
            }
        except Exception as e:
            return {
                "error": f"Error processing question: {str(e)}",
                "answer": None,
                "sources": []
            }
    
    def batch_ask_questions(self, queries: List[str], max_workers: int = 3) -> List[Dict[str, Any]]:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.ask_question, queries))
        return results
