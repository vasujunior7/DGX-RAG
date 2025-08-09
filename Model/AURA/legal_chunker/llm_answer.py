from typing import List
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env from current directory or parent directories    

def get_llm_answer(context_chunks: List[str], question: str, openai_api_key: str = None) -> str:
    """
    Sends a custom prompt to OpenAI GPT using langchain-openai.
    Returns the LLM's answer.
    """
    if openai_api_key is None:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY environment variable.")

    context = "\n\n".join(context_chunks)
    prompt = f"""
Context:
{context}

Question: {question}
You are a legal expert. answer in a way that is easy to understand and in a way that is not too technical.
Instructions:
- Answer only from the context above.
- If the answer is not found, then give answer from your knowledge.
- Answer in max 1 - 2 lines.
- Keep the answer short and legally accurate.
"""
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model="gpt-3.5-turbo",
        temperature=0.1
    )
    response = llm.invoke(prompt)
    return response.content.strip() if hasattr(response, 'content') else str(response) 