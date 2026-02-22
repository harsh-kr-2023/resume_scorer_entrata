"""
Regex-based scorer (STUB).

Uses keyword matching to produce a baseline score. No LLM required.
Useful as a fast fallback or for cost-sensitive environments.
"""

from app.core.interfaces.base_scorer import BaseScorer
from app.core.models import ScoreResult


class RegexScorer(BaseScorer):
    """
    Regex-based scorer that uses keyword matching.
    
    Uses keyword matching to produce a baseline score. No LLM required.
    Useful as a fast fallback or for cost-sensitive environments.
    
    Implementation notes:
        - Extract keywords from must_have and nice_to_have lists
        - Use regex to find matches in resume text
        - Calculate score based on match percentage
        - Generate simple gap analysis based on missing keywords
        - Provide generic suggestions for improvement
    
    Advantages:
        - No API costs
        - Very fast execution
        - Deterministic results
        - Works offline
    
    Limitations:
        - Cannot understand context or synonyms
        - No semantic understanding
        - Simple scoring logic
        - Generic feedback
    """
    
    def score(self, prompt: str) -> ScoreResult:
        """
        Score a resume using regex matching.
        
        Args:
            prompt: Complete evaluation prompt (parsed for keywords).
            
        Returns:
            ScoreResult containing score, justification, gaps, and suggestions.
            
        Raises:
            NotImplementedError: This scorer is not yet implemented.
        """
        raise NotImplementedError("Regex scoring not yet implemented.")
