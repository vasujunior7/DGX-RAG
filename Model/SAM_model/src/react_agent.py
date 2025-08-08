"""
ReAct Agent for query processing and reasoning in Legal Query RAG system.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import logging
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .config import Config

logger = logging.getLogger(__name__)

class ReActAgent:
    """
    ReAct (Reasoning + Acting) agent for query processing and refinement.
    Implements reasoning, action, and observation loops for better query handling.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.LLM_MODEL,
            temperature=0.1,
            max_tokens=500
        )
        
        self.system_prompt = """You are a legal query processing agent. Your task is to:
1. REASON about the user's legal query to understand their intent
2. ACT by refining, expanding, or restructuring the query for better retrieval
3. OBSERVE the results and suggest improvements

For legal queries, consider:
- Legal terminology and concepts
- Jurisdiction relevance
- Case law vs statute vs regulation distinctions
- Temporal aspects (recent vs historical law)

Format your response as:
REASONING: [Your analysis of the query]
ACTION: [Refined/expanded query]
CONFIDENCE: [0.0-1.0 confidence score]"""
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a single query using ReAct methodology.
        
        Args:
            query: Original user query
            context: Additional context for query processing
            
        Returns:
            Dictionary containing processed query and metadata
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Process this legal query: {query}")
            ]
            
            if context:
                context_str = f"Additional context: {context}"
                messages.append(HumanMessage(content=context_str))
            
            response = await self.llm.agenerate([messages])
            response_text = response.generations[0][0].text.strip()
            
            # Parse response
            parsed_response = self._parse_react_response(response_text)
            
            return {
                'original_query': query,
                'processed_query': parsed_response.get('action', query),
                'reasoning': parsed_response.get('reasoning', ''),
                'confidence': parsed_response.get('confidence', 0.5),
                'raw_response': response_text
            }
            
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            return {
                'original_query': query,
                'processed_query': query,
                'reasoning': '',
                'confidence': 0.0,
                'error': str(e)
            }
    
    async def process_multiple_queries(self, queries: List[str], 
                                     context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Process multiple queries in parallel using ReAct methodology.
        
        Args:
            queries: List of user queries
            context: Additional context for query processing
            
        Returns:
            List of processed query dictionaries
        """
        # Process queries in parallel with concurrency limit
        semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_QUERIES)
        
        async def process_single_query(query: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.process_query(query, context)
        
        tasks = [process_single_query(query) for query in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing query {i}: {result}")
                processed_results.append({
                    'original_query': queries[i],
                    'processed_query': queries[i],
                    'reasoning': '',
                    'confidence': 0.0,
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def _parse_react_response(self, response: str) -> Dict[str, Any]:
        """Parse ReAct agent response into structured format."""
        parsed = {}
        
        # Extract reasoning
        reasoning_match = re.search(r'REASONING:\s*(.+?)(?=ACTION:|CONFIDENCE:|$)', 
                                  response, re.DOTALL | re.IGNORECASE)
        if reasoning_match:
            parsed['reasoning'] = reasoning_match.group(1).strip()
        
        # Extract action (processed query)
        action_match = re.search(r'ACTION:\s*(.+?)(?=CONFIDENCE:|$)', 
                               response, re.DOTALL | re.IGNORECASE)
        if action_match:
            parsed['action'] = action_match.group(1).strip()
        
        # Extract confidence
        confidence_match = re.search(r'CONFIDENCE:\s*([0-9]*\.?[0-9]+)', 
                                   response, re.IGNORECASE)
        if confidence_match:
            try:
                parsed['confidence'] = float(confidence_match.group(1))
            except ValueError:
                parsed['confidence'] = 0.5
        
        return parsed
    
    async def refine_query_with_context(self, query: str, 
                                      retrieved_docs: List[Dict[str, Any]], 
                                      previous_results: List[str] = None) -> str:
        """
        Refine query based on retrieved documents and previous results.
        
        Args:
            query: Original query
            retrieved_docs: List of retrieved document metadata
            previous_results: Previous search results for comparison
            
        Returns:
            Refined query string
        """
        doc_summaries = []
        for doc in retrieved_docs[:3]:  # Use top 3 docs for context
            summary = doc.get('content', '')[:200] + "..."
            doc_summaries.append(summary)
        
        context_prompt = f"""
Based on the initial query: "{query}"
Retrieved documents contain: {'; '.join(doc_summaries)}

The retrieved documents seem {'relevant' if retrieved_docs else 'insufficient'}.
Please refine the query to get better legal document matches.
Focus on legal terminology, jurisdiction, and specific legal concepts.

Refined query:"""
        
        try:
            messages = [HumanMessage(content=context_prompt)]
            response = await self.llm.agenerate([messages])
            refined_query = response.generations[0][0].text.strip()
            
            return refined_query if refined_query else query
            
        except Exception as e:
            logger.error(f"Error refining query: {e}")
            return query
    
    def extract_legal_entities(self, query: str) -> Dict[str, List[str]]:
        """
        Extract legal entities and concepts from query.
        
        Args:
            query: Input query string
            
        Returns:
            Dictionary of extracted entities by type
        """
        entities = {
            'statutes': [],
            'cases': [],
            'jurisdictions': [],
            'legal_concepts': [],
            'dates': []
        }
        
        # Simple regex-based entity extraction
        # In production, use spaCy or other NER libraries
        
        # Extract potential case citations (e.g., "v.", "Smith v. Jones")
        case_pattern = r'\b\w+\s+v\.?\s+\w+\b'
        entities['cases'] = re.findall(case_pattern, query, re.IGNORECASE)
        
        # Extract years/dates
        date_pattern = r'\b(19|20)\d{2}\b'
        entities['dates'] = re.findall(date_pattern, query)
        
        # Extract legal concepts (simple keyword matching)
        legal_keywords = [
            'contract', 'tort', 'criminal', 'constitutional', 'property',
            'evidence', 'procedure', 'appeal', 'motion', 'judgment',
            'liability', 'damages', 'injunction', 'statute', 'regulation'
        ]
        
        for keyword in legal_keywords:
            if keyword in query.lower():
                entities['legal_concepts'].append(keyword)
        
        return entities
