"""
Evaluation module for Legal Query RAG system.
Evaluates response quality and provides feedback loops.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import logging
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .config import Config

logger = logging.getLogger(__name__)

class ResponseEvaluator:
    """
    Evaluates generated responses and provides quality scores and feedback.
    """
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.evaluator_llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.EVALUATION_MODEL,
            temperature=0.0,  # Use deterministic evaluation
            max_tokens=500
        )
        
        self.evaluation_prompt = """You are an expert legal research evaluator. Your task is to evaluate the quality of legal query responses.

Evaluate the response based on these criteria:
1. ACCURACY: Is the legal information correct and current?
2. COMPLETENESS: Does it adequately address all aspects of the query?
3. RELEVANCE: Is the response directly relevant to the question asked?
4. CLARITY: Is the response clear and well-structured?
5. CITATIONS: Are legal sources properly referenced?

Score each criterion from 1-10 and provide an overall score.

Format your evaluation as:
ACCURACY: X/10 - [Brief explanation]
COMPLETENESS: X/10 - [Brief explanation]
RELEVANCE: X/10 - [Brief explanation]
CLARITY: X/10 - [Brief explanation]
CITATIONS: X/10 - [Brief explanation]
OVERALL: X/10
RECOMMENDATION: [APPROVE/IMPROVE/REJECT]
FEEDBACK: [Specific suggestions for improvement if needed]"""
    
    async def evaluate_response(self, query: str, response: Dict[str, Any], 
                              retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate a single response for quality and accuracy.
        
        Args:
            query: Original user query
            response: Generated response dictionary
            retrieved_docs: Documents used for generation
            
        Returns:
            Evaluation results dictionary
        """
        try:
            # Prepare evaluation context
            response_text = response.get('full_response', response.get('answer', ''))
            sources_info = f"Used {len(retrieved_docs)} sources" if retrieved_docs else "No sources used"
            
            evaluation_input = f"""
Query: {query}
Response: {response_text}
Sources: {sources_info}
Context Quality: {self._assess_context_quality(retrieved_docs)}

Please evaluate this legal response:"""
            
            messages = [
                SystemMessage(content=self.evaluation_prompt),
                HumanMessage(content=evaluation_input)
            ]
            
            # Get evaluation
            eval_response = await self.evaluator_llm.agenerate([messages])
            eval_text = eval_response.generations[0][0].text.strip()
            
            # Parse evaluation
            parsed_eval = self._parse_evaluation(eval_text)
            
            # Add metadata
            parsed_eval.update({
                'query': query,
                'response_id': response.get('query', ''),
                'sources_count': len(retrieved_docs),
                'raw_evaluation': eval_text
            })
            
            return parsed_eval
            
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {
                'query': query,
                'overall_score': 0.0,
                'recommendation': 'ERROR',
                'feedback': f"Evaluation failed: {str(e)}",
                'error': str(e)
            }
    
    async def batch_evaluate_responses(self, queries: List[str], 
                                     responses: List[Dict[str, Any]], 
                                     batch_retrieved_docs: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Evaluate multiple responses in parallel.
        
        Args:
            queries: List of original queries
            responses: List of generated responses
            batch_retrieved_docs: List of retrieved document lists for each query
            
        Returns:
            List of evaluation results
        """
        # Use semaphore to limit concurrent evaluations
        semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_QUERIES)
        
        async def evaluate_single_response(i: int) -> Dict[str, Any]:
            async with semaphore:
                query = queries[i] if i < len(queries) else ""
                response = responses[i] if i < len(responses) else {}
                docs = batch_retrieved_docs[i] if i < len(batch_retrieved_docs) else []
                return await self.evaluate_response(query, response, docs)
        
        # Create tasks
        tasks = [evaluate_single_response(i) for i in range(len(responses))]
        
        # Execute evaluations in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error evaluating response {i}: {result}")
                final_results.append({
                    'query': queries[i] if i < len(queries) else "",
                    'overall_score': 0.0,
                    'recommendation': 'ERROR',
                    'feedback': f"Evaluation failed: {str(result)}",
                    'error': str(result)
                })
            else:
                final_results.append(result)
        
        return final_results
    
    def _parse_evaluation(self, eval_text: str) -> Dict[str, Any]:
        """Parse evaluation text into structured format."""
        evaluation = {}
        
        # Extract individual scores
        criteria = ['ACCURACY', 'COMPLETENESS', 'RELEVANCE', 'CLARITY', 'CITATIONS']
        scores = []
        
        for criterion in criteria:
            pattern = rf'{criterion}:\s*(\d+)/10'
            match = re.search(pattern, eval_text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                evaluation[f'{criterion.lower()}_score'] = score
                scores.append(score)
            else:
                evaluation[f'{criterion.lower()}_score'] = 0
                scores.append(0)
        
        # Extract overall score
        overall_match = re.search(r'OVERALL:\s*(\d+)/10', eval_text, re.IGNORECASE)
        if overall_match:
            evaluation['overall_score'] = int(overall_match.group(1))
        else:
            # Calculate as average if not provided
            evaluation['overall_score'] = sum(scores) / len(scores) if scores else 0
        
        # Extract recommendation
        recommendation_match = re.search(r'RECOMMENDATION:\s*(APPROVE|IMPROVE|REJECT)', eval_text, re.IGNORECASE)
        if recommendation_match:
            evaluation['recommendation'] = recommendation_match.group(1).upper()
        else:
            # Determine based on overall score
            score = evaluation['overall_score']
            if score >= 8:
                evaluation['recommendation'] = 'APPROVE'
            elif score >= 6:
                evaluation['recommendation'] = 'IMPROVE'
            else:
                evaluation['recommendation'] = 'REJECT'
        
        # Extract feedback
        feedback_match = re.search(r'FEEDBACK:\s*(.*?)$', eval_text, re.DOTALL | re.IGNORECASE)
        if feedback_match:
            evaluation['feedback'] = feedback_match.group(1).strip()
        else:
            evaluation['feedback'] = 'No specific feedback provided'
        
        return evaluation
    
    def _assess_context_quality(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Assess the quality of retrieved context documents."""
        if not retrieved_docs:
            return "No context provided"
        
        # Calculate average relevance score
        scores = []
        for doc in retrieved_docs:
            score = doc.get('rerank_score', doc.get('combined_score', 0))
            if isinstance(score, (int, float)):
                scores.append(score)
        
        if not scores:
            return f"{len(retrieved_docs)} documents, unknown quality"
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 0.8:
            quality = "High"
        elif avg_score >= 0.6:
            quality = "Medium"
        else:
            quality = "Low"
        
        return f"{len(retrieved_docs)} documents, {quality} quality (avg score: {avg_score:.2f})"
    
    def should_regenerate(self, evaluation: Dict[str, Any]) -> bool:
        """
        Determine if response should be regenerated based on evaluation.
        
        Args:
            evaluation: Evaluation results dictionary
            
        Returns:
            True if response should be regenerated
        """
        recommendation = evaluation.get('recommendation', 'REJECT')
        overall_score = evaluation.get('overall_score', 0)
        
        # Regenerate if recommendation is REJECT or IMPROVE with low score
        return (recommendation == 'REJECT' or 
                (recommendation == 'IMPROVE' and overall_score < self.config.MIN_ANSWER_QUALITY_SCORE * 10))
    
    def generate_improvement_suggestions(self, evaluation: Dict[str, Any]) -> List[str]:
        """
        Generate specific improvement suggestions based on evaluation.
        
        Args:
            evaluation: Evaluation results dictionary
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check individual scores for specific improvements
        if evaluation.get('accuracy_score', 0) < 7:
            suggestions.append("Improve legal accuracy by citing more authoritative sources")
        
        if evaluation.get('completeness_score', 0) < 7:
            suggestions.append("Provide more comprehensive coverage of all query aspects")
        
        if evaluation.get('relevance_score', 0) < 7:
            suggestions.append("Focus more directly on the specific question asked")
        
        if evaluation.get('clarity_score', 0) < 7:
            suggestions.append("Improve response structure and clarity")
        
        if evaluation.get('citations_score', 0) < 7:
            suggestions.append("Add more specific legal citations and references")
        
        # Add general suggestions based on overall score
        overall_score = evaluation.get('overall_score', 0)
        if overall_score < 5:
            suggestions.append("Consider retrieving different or additional source documents")
            suggestions.append("Refine the query processing and understanding")
        
        return suggestions
    
    def get_evaluation_summary(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for a batch of evaluations.
        
        Args:
            evaluations: List of evaluation results
            
        Returns:
            Summary statistics dictionary
        """
        if not evaluations:
            return {'status': 'No evaluations provided'}
        
        # Calculate averages
        criteria_scores = {}
        criteria = ['accuracy', 'completeness', 'relevance', 'clarity', 'citations', 'overall']
        
        for criterion in criteria:
            scores = [eval_dict.get(f'{criterion}_score', 0) for eval_dict in evaluations]
            criteria_scores[f'avg_{criterion}_score'] = sum(scores) / len(scores) if scores else 0
        
        # Count recommendations
        recommendations = [eval_dict.get('recommendation', 'UNKNOWN') for eval_dict in evaluations]
        recommendation_counts = {}
        for rec in ['APPROVE', 'IMPROVE', 'REJECT']:
            recommendation_counts[rec.lower() + '_count'] = recommendations.count(rec)
        
        # Calculate pass rate
        approved = recommendation_counts.get('approve_count', 0)
        pass_rate = (approved / len(evaluations)) * 100 if evaluations else 0
        
        return {
            'total_evaluations': len(evaluations),
            'pass_rate': pass_rate,
            **criteria_scores,
            **recommendation_counts,
            'needs_improvement': recommendation_counts.get('improve_count', 0) + recommendation_counts.get('reject_count', 0)
        }
