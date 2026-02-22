"""
Abstract base class for persistence strategies.

All repositories must support saving results and retrieving rankings.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.core.models import ScoreResult


class BaseRepository(ABC):
    """
    Abstract base class for persistence strategies.
    
    All repositories must support saving results and retrieving rankings.
    Different persistence strategies can be implemented (e.g., filesystem,
    SQLite, in-memory, cloud storage).
    """
    
    @abstractmethod
    def save(self, result: ScoreResult, role: str, resume_name: str) -> None:
        """
        Persist a scoring result.
        
        Args:
            result: The ScoreResult to save.
            role: The job role being evaluated for.
            resume_name: Name/identifier of the resume.
            
        Raises:
            PersistenceError: If save operation fails.
        """
        pass
    
    @abstractmethod
    def get_rankings(self, role: Optional[str] = None) -> list[dict]:
        """
        Retrieve saved results, optionally filtered by role.
        
        Args:
            role: Optional role to filter by. If None, returns all results.
            
        Returns:
            List of result dictionaries sorted by score (descending).
            
        Raises:
            PersistenceError: If retrieval operation fails.
        """
        pass
