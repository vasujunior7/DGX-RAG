"""
Fallback LLM module for Legal Query RAG system.
Provides general knowledge responses when RAG answers are rejected.
"""
import asyncio
from typing import List, Dict, Any, Optional
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .config import Config

logger = logging.getLogger(__name__)

class FallbackLLMGenerator:
    """
    Fallback LLM that uses general knowledge when RAG system fails or is rejected.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        
        # Use a different model for fallback (or same model but with different prompts)
        self.fallback_llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.LLM_MODEL,  # Could use a different model like "gpt-4" for better general knowledge
            temperature=0.3,  # Slightly more creative for general knowledge
            max_tokens=1000
        )
        
        logger.info(f"Fallback LLM initialized with model: {self.config.LLM_MODEL}")
    
    async def generate_fallback_response(self, query: str) -> Dict[str, Any]:
        """
        Generate a fallback response using the LLM's general knowledge.
        
        Args:
            query: The original user query
            
        Returns:
            Dictionary containing the fallback response
        """
        logger.info(f"Generating fallback response for query: {query[:100]}...")
        
        try:
            # Create a specialized prompt for general legal knowledge
            system_prompt = """You are a knowledgeable legal assistant. The user has asked a legal question, but the specialized document search could not provide a satisfactory answer from the available legal documents.

Please provide a helpful response based on your general legal knowledge. Follow these guidelines:

make sure to: give answer in maximum 5 sentences

Be helpful but cautious, and always emphasize the importance of proper legal counsel."""

            human_prompt = f"""Legal Query: {query}

Please provide a helpful general response based on legal principles and common practices. Remember to include appropriate disclaimers about seeking professional legal advice."""

            # Generate response
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.fallback_llm.ainvoke(messages)
            
            fallback_response = {
                'answer': response.content,
                'source': 'fallback_llm_general_knowledge',
                'type': 'general_legal_guidance',
                'disclaimer': 'This response is based on general legal principles and is not specific legal advice.',
                'recommendation': 'Consult with a qualified attorney for advice specific to your situation.',
                'generated_by': 'fallback_llm'
            }
            
            logger.info("Fallback response generated successfully")
            return fallback_response
            
        except Exception as e:
            logger.error(f"Error generating fallback response: {e}")
            
            # Return a basic error response
            return {
                'answer': "I apologize, but I'm unable to provide a comprehensive answer to your legal question at this time. Legal matters can be complex and fact-specific. I strongly recommend consulting with a qualified attorney who can provide advice tailored to your specific situation and jurisdiction.",
                'source': 'fallback_error',
                'type': 'error_response',
                'disclaimer': 'This is a fallback response due to system limitations.',
                'recommendation': 'Please consult with a qualified attorney for legal advice.',
                'generated_by': 'fallback_error',
                'error': str(e)
            }
    
    async def generate_batch_fallback_responses(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Generate fallback responses for multiple queries in parallel.
        
        Args:
            queries: List of query strings
            
        Returns:
            List of fallback response dictionaries
        """
        logger.info(f"Generating fallback responses for {len(queries)} queries")
        
        # Process queries in parallel
        tasks = [self.generate_fallback_response(query) for query in queries]
        
        try:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle any exceptions
            fallback_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    logger.error(f"Error in fallback response {i}: {response}")
                    fallback_responses.append({
                        'answer': f"I apologize, but I encountered an error while processing your legal question. Please consult with a qualified attorney for assistance.",
                        'source': 'fallback_error',
                        'type': 'error_response',
                        'error': str(response)
                    })
                else:
                    fallback_responses.append(response)
            
            return fallback_responses
            
        except Exception as e:
            logger.error(f"Error in batch fallback generation: {e}")
            return [{
                'answer': f"I apologize, but I encountered an error while processing your legal question. Please consult with a qualified attorney for assistance.",
                'source': 'fallback_error',
                'type': 'error_response',
                'error': str(e)
            }] * len(queries)
    
    def format_fallback_response(self, query: str, fallback_response: Dict[str, Any]) -> str:
        """
        Format the fallback response for display.
        
        Args:
            query: Original query
            fallback_response: Fallback response dictionary
            
        Returns:
            Formatted response string
        """
        answer = fallback_response.get('answer', 'No response available')
        disclaimer = fallback_response.get('disclaimer', '')
        recommendation = fallback_response.get('recommendation', '')
        
        formatted_response = f"{answer}\n\n"
        
        if disclaimer:
            formatted_response += f"⚠️  **Disclaimer:** {disclaimer}\n\n"
        
        if recommendation:
            formatted_response += f"💡 **Recommendation:** {recommendation}"
        
        return formatted_response.strip()
