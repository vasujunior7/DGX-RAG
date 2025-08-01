from typing import List, Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_enhanced_llm_answer(context_chunks: List[str], question: str, 
                          explanation_data: Optional[Dict] = None, 
                          anthropic_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Enhanced LLM answer with explainability and structured JSON response
    Optimized for HackRX evaluation criteria: Accuracy, Token Efficiency, Explainability
    """
    if anthropic_api_key is None:
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable.")

    # Prepare context with chunk identifiers for traceability
    numbered_context = []
    for i, chunk in enumerate(context_chunks):
        numbered_context.append(f"[CLAUSE_{i+1}]\n{chunk}")
    
    context = "\n\n".join(numbered_context)
    
    # Enhanced prompt for legal domain with explainability
    prompt = f"""
Context (Legal Document Clauses):
{context}

Question: {question}

Instructions:
You are a legal expert analyzing insurance/policy documents. Provide a comprehensive answer with the following requirements:

1. ACCURACY: Answer precisely based only on the provided clauses
2. EXPLAINABILITY: Reference specific clause numbers [CLAUSE_X] that support your answer
3. STRUCTURED RESPONSE: Provide clear, organized information

Response Format:
- Main Answer: Direct answer to the question (1-2 sentences)
- Supporting Clauses: List the specific clause numbers used
- Conditions/Limitations: Any relevant conditions or limitations mentioned
- Confidence Level: High/Medium/Low based on clause clarity

If information is not found in the provided clauses, clearly state this and explain what information would be needed.

Answer:"""

    llm = ChatAnthropic(
        anthropic_api_key=anthropic_api_key,
        model="claude-3-5-sonnet-20241022",
        temperature=0.1  # Low temperature for consistency in legal analysis
    )
    
    response = llm.invoke(prompt)
    answer_text = response.content.strip() if hasattr(response, 'content') else str(response)
    
    # Extract clause references for traceability
    clause_references = []
    import re
    clause_matches = re.findall(r'\[CLAUSE_(\d+)\]', answer_text)
    for match in clause_matches:
        clause_num = int(match) - 1  # Convert to 0-based index
        if clause_num < len(context_chunks):
            clause_references.append({
                'clause_number': int(match),
                'clause_preview': context_chunks[clause_num][:150] + '...',
                'relevance': 'high'  # Could be enhanced with scoring
            })
    
    # Structure the response for HackRX evaluation
    structured_response = {
        'answer': answer_text,
        'metadata': {
            'question_complexity': explanation_data.get('question_complexity', 'unknown') if explanation_data else 'unknown',
            'chunks_used': len(context_chunks),
            'total_chunks_available': explanation_data.get('total_candidates', 0) if explanation_data else 0,
            'token_efficiency': f"Used {len(context_chunks)} chunks instead of {explanation_data.get('total_candidates', 5)} candidates" if explanation_data else "Standard processing",
            'processing_strategy': 'smart_retrieval' if explanation_data else 'standard'
        },
        'explainability': {
            'supporting_clauses': clause_references,
            'decision_rationale': f"Selected chunks based on semantic similarity and legal keyword matching for question type: {explanation_data.get('question_complexity', 'standard')}" if explanation_data else "Standard clause matching",
            'confidence_indicators': {
                'clause_match_quality': 'high' if clause_references else 'medium',
                'context_completeness': 'high' if len(context_chunks) >= 2 else 'medium'
            }
        },
        'sources': [f"Clause {ref['clause_number']}" for ref in clause_references] or ['Document clauses'],
        'performance_metrics': {
            'retrieval_precision': len(clause_references) / len(context_chunks) if context_chunks else 0,
            'context_efficiency': len(context_chunks) / max(explanation_data.get('total_candidates', 5), 1) if explanation_data else 1.0
        }
    }
    
    return structured_response

def get_llm_answer_compatible(context_chunks: List[str], question: str, anthropic_api_key: Optional[str] = None) -> str:
    """
    Backward compatible version that returns just the answer string
    For use with existing code that expects string response
    """
    enhanced_response = get_enhanced_llm_answer(context_chunks, question, None, anthropic_api_key)
    return enhanced_response['answer']

# Export both functions
__all__ = ['get_enhanced_llm_answer', 'get_llm_answer_compatible'] 