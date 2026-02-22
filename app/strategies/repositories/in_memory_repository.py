"""
In-memory repository (STUB).

Stores results in memory. Data is lost when the process stops.
Intended for testing and development only.
"""

from typing import Optional
from app.core.interfaces.base_repository import BaseRepository
from app.core.models import ScoreResult


class InMemoryRepository(BaseRepository):
    """
    Stores results in memory.
    
    Data is lost when the process stops. Intended for testing and development only.
    
    Implementation notes:
        - Use a list or dict to store results in memory
        - Add timestamps for each result
        - Implement filtering and sorting logic
        - Thread-safe if needed for concurrent requests
    
    Advantages:
        - Very fast
        - No file I/O
        - Good for testing
        - No cleanup needed
    
    Limitations:
        - Data lost on restart
        - Memory usage grows unbounded
        - Not suitable for production
    """
    
    def save(self, result: ScoreResult, role: str, resume_name: str) -> None:
        """
        Save a scoring result in memory.
        
        Args:
            result: The ScoreResult to save.
            role: The job role being evaluated for.
            resume_name: Name/identifier of the resume.
            
        Raises:
            NotImplementedError: This repository is not yet implemented.
        """
        raise NotImplementedError("In-memory persistence not yet implemented.")
    
    def get_rankings(self, role: Optional[str] = None) -> list[dict]:
        """
        Retrieve saved results from memory.
        
        Args:
            role: Optional role to filter by.
            
        Returns:
            List of result dictionaries sorted by score.
            
        Raises:
            NotImplementedError: This repository is not yet implemented.
        """
        raise NotImplementedError("In-memory persistence not yet implemented.")
