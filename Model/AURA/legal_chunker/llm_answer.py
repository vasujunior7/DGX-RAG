from typing import List
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_answer(context_chunks: List[str], question: str, anthropic_api_key: str = None) -> str:
    """
    Sends a custom prompt to Anthropic Claude using langchain-anthropic.
    Returns the LLM's answer.
    """
    if anthropic_api_key is None:
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable.")

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
    llm = ChatAnthropic(
        anthropic_api_key=anthropic_api_key,
        model="claude-3-5-sonnet-20241022",
        temperature=0.1
    )
    response = llm.invoke(prompt)
    return response.content.strip() if hasattr(response, 'content') else str(response) 