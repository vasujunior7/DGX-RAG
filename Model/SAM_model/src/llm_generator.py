"""
LLM Generation module for Legal Query RAG system.
Handles response generation using OpenAI models with parallel processing.
"""
import asyncio
import re
from typing import List, Dict, Any, Optional
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate

from .config import Config

logger = logging.getLogger(__name__)

class LLMGenerator:
    """
    Handles LLM-based response generation for legal queries.
    Supports parallel processing for multiple queries.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.LLM_MODEL,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS
        )
        
        self.system_prompt = """You are a legal research assistant specializing in analyzing legal documents and providing comprehensive answers to legal queries.

Guidelines for responses:
1. Provide accurate, well-structured answers based solely on the provided context
2. Cite specific sections, cases, or legal principles when available
3. If information is insufficient, clearly state limitations
4. Use legal terminology appropriately
5. Structure responses with clear headings and bullet points when helpful
6. Include relevant jurisdiction information when available
7. Distinguish between different types of legal sources (statutes, case law, regulations)

VERY IMPORTANT GUIDELINES:
- Always make sure to provide responses in maximum 5 sentences.

Format your response as:
## Answer
[Main response to the query]

## Supporting Evidence
[Specific citations and references from the provided documents]

## Limitations
[Any limitations or gaps in the available information]"""
    
    def create_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]], 
                     previous_context: Optional[str] = None) -> str:
        """
        Create a structured prompt for LLM generation.
        
        Args:
            query: User's legal query
            retrieved_docs: List of retrieved and re-ranked documents
            previous_context: Optional previous conversation context
            
        Returns:
            Formatted prompt string
        """
        # Prepare document context
        context_parts = []
        for i, doc in enumerate(retrieved_docs[:self.config.MAX_CHUNKS_PER_QUERY]):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            source = metadata.get('source', 'Unknown')
            
            context_parts.append(f"""
Document {i+1}:
Source: {source}
Content: {content[:800]}{"..." if len(content) > 800 else ""}
Relevance Score: {doc.get('rerank_score', doc.get('combined_score', 'N/A'))}
""")
        
        context_text = "\n".join(context_parts)
        
        # Build the full prompt
        prompt_parts = [
            f"Legal Query: {query}",
            f"\nRelevant Legal Documents:\n{context_text}"
        ]
        
        if previous_context:
            prompt_parts.append(f"\nPrevious Context: {previous_context}")
        
        prompt_parts.append("\nBased on the above legal documents, please provide a comprehensive answer to the query.")
        
        return "\n".join(prompt_parts)
    
    async def generate_response(self, query: str, retrieved_docs: List[Dict[str, Any]], 
                              previous_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response for a single query.
        
        Args:
            query: User's legal query
            retrieved_docs: List of retrieved and re-ranked documents
            previous_context: Optional previous conversation context
            
        Returns:
            Dictionary containing generated response and metadata
        """
        try:
            # Create prompt
            prompt = self.create_prompt(query, retrieved_docs, previous_context)
            
            # Prepare messages
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            # Generate response
            response = await self.llm.agenerate([messages])
            response_text = response.generations[0][0].text.strip()
            
            # Extract structured parts from response
            structured_response = self._parse_structured_response(response_text)
            
            return {
                'query': query,
                'answer': structured_response.get('answer', response_text),
                'supporting_evidence': structured_response.get('supporting_evidence', ''),
                'limitations': structured_response.get('limitations', ''),
                'full_response': response_text,
                'sources_used': len(retrieved_docs),
                'context_length': len(prompt),
                'model_used': self.config.LLM_MODEL
            }
            
        except Exception as e:
            logger.error(f"Error generating response for query '{query}': {e}")
            return {
                'query': query,
                'answer': f"I apologize, but I encountered an error while processing your query: {str(e)}",
                'supporting_evidence': '',
                'limitations': 'Error occurred during processing',
                'full_response': '',
                'sources_used': len(retrieved_docs),
                'error': str(e)
            }
    
    async def generate_batch_responses(self, queries: List[str], 
                                     batch_retrieved_docs: List[List[Dict[str, Any]]], 
                                     previous_contexts: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Generate responses for multiple queries in parallel.
        
        Args:
            queries: List of user queries
            batch_retrieved_docs: List of retrieved document lists for each query
            previous_contexts: Optional list of previous contexts for each query
            
        Returns:
            List of generated responses
        """
        # Use semaphore to limit concurrent LLM calls
        semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_QUERIES)
        
        async def generate_single_response(i: int) -> Dict[str, Any]:
            async with semaphore:
                query = queries[i]
                docs = batch_retrieved_docs[i]
                context = previous_contexts[i] if previous_contexts else None
                return await self.generate_response(query, docs, context)
        
        # Create tasks for all queries
        tasks = [generate_single_response(i) for i in range(len(queries))]
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error generating response for query {i}: {result}")
                final_results.append({
                    'query': queries[i],
                    'answer': f"Error occurred during response generation: {str(result)}",
                    'supporting_evidence': '',
                    'limitations': 'Processing error',
                    'full_response': '',
                    'sources_used': len(batch_retrieved_docs[i]) if i < len(batch_retrieved_docs) else 0,
                    'error': str(result)
                })
            else:
                final_results.append(result)
        
        return final_results
    
    def _parse_structured_response(self, response_text: str) -> Dict[str, str]:
        """Parse structured response into components."""
        import re
        
        structured = {}
        
        # Extract Answer section
        answer_match = re.search(r'## Answer\s*\n(.*?)(?=## |$)', response_text, re.DOTALL | re.IGNORECASE)
        if answer_match:
            structured['answer'] = answer_match.group(1).strip()
        
        # Extract Supporting Evidence section
        evidence_match = re.search(r'## Supporting Evidence\s*\n(.*?)(?=## |$)', response_text, re.DOTALL | re.IGNORECASE)
        if evidence_match:
            structured['supporting_evidence'] = evidence_match.group(1).strip()
        
        # Extract Limitations section
        limitations_match = re.search(r'## Limitations\s*\n(.*?)(?=## |$)', response_text, re.DOTALL | re.IGNORECASE)
        if limitations_match:
            structured['limitations'] = limitations_match.group(1).strip()
        
        return structured
    
    async def generate_follow_up_questions(self, query: str, response: str, 
                                         retrieved_docs: List[Dict[str, Any]]) -> List[str]:
        """
        Generate relevant follow-up questions based on the query and response.
        
        Args:
            query: Original query
            response: Generated response
            retrieved_docs: Documents used for generation
            
        Returns:
            List of follow-up questions
        """
        try:
            follow_up_prompt = f"""
Based on the legal query: "{query}"
And the provided response: "{response[:500]}..."

Generate 3-5 relevant follow-up questions that a legal researcher might want to ask to deepen their understanding of this topic. Focus on:
1. Related legal concepts or precedents
2. Jurisdictional variations
3. Practical applications
4. Recent developments or changes

Format as a numbered list."""

            messages = [HumanMessage(content=follow_up_prompt)]
            response = await self.llm.agenerate([messages])
            follow_up_text = response.generations[0][0].text.strip()
            
            # Extract questions from numbered list
            questions = []
            lines = follow_up_text.split('\n')
            for line in lines:
                line = line.strip()
                if re.match(r'^\d+\.\s+', line):
                    question = re.sub(r'^\d+\.\s+', '', line)
                    questions.append(question)
            
            return questions[:5]  # Limit to 5 questions
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return []
    
    def create_few_shot_examples(self) -> str:
        """Create few-shot examples for better legal reasoning."""
        return """
Example 1:
Query: "What are the requirements for establishing adverse possession in California?"
Answer: Based on California Civil Code Section 325, adverse possession requires: (1) actual occupation of the property, (2) open and notorious use, (3) exclusive possession, (4) continuous for 5+ years, and (5) payment of property taxes. The claimant must prove all elements by clear and convincing evidence.

Example 2:
Query: "Can a landlord terminate a lease for non-payment in New York?"
Answer: Under New York Real Property Law, landlords can terminate for non-payment after serving proper notice. For rent-stabilized units, this requires a 14-day demand notice. However, tenants have rights to cure the default and various defenses available under the Tenant Protection Act of 2019.
"""
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get LLM generation system statistics."""
        return {
            'model': self.config.LLM_MODEL,
            'max_tokens': self.config.MAX_TOKENS,
            'temperature': self.config.TEMPERATURE,
            'max_concurrent_queries': self.config.MAX_CONCURRENT_QUERIES,
            'status': 'Active'
        }
