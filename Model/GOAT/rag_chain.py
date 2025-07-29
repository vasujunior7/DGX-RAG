# rag_chain.py

from langchain import hub
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain():
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatGroq(model="llama3-8b-8192", temperature=0)
    return prompt | llm | StrOutputParser()

def generate_answer(rag_chain, docs, question):
    return rag_chain.invoke({"context": docs, "question": question})
