"""
Abstract base class for scoring strategies.

All scorers must take a prompt string and return a ScoreResult.
"""

from abc import ABC, abstractmethod
from app.core.models import ScoreResult


class BaseScorer(ABC):
    """
    Abstract base class for scoring strategies.
    
    All scorers must take a prompt string and return a ScoreResult. Different
    scoring strategies can be implemented using different methods (e.g., LLM-based,
    regex-based, ML model-based).
    """
    
    @abstractmethod
    def score(self, prompt: str) -> ScoreResult:
        """
        Score a resume against a job description using the provided prompt.
        
        Args:
            prompt: Formatted prompt containing resume, JD, and evaluation criteria.
            
        Returns:
            ScoreResult containing score, justification, gaps, and suggestions.
            
        Raises:
            ScoringError: If scoring fails for any reason.
        """
        pass
