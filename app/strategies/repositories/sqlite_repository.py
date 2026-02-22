"""
SQLite repository (STUB).

Persists scoring results in a SQLite database.
Useful for production environments needing queryable storage with SQL support.
"""

from typing import Optional
from app.core.interfaces.base_repository import BaseRepository
from app.core.models import ScoreResult


class SQLiteRepository(BaseRepository):
    """
    Persists scoring results in a SQLite database.
    
    Useful for production environments needing queryable storage with SQL support.
    
    Implementation notes:
        - Create table with columns: id, role, resume_name, score, justification, 
          gaps (JSON), suggestions (JSON), created_at
        - Use sqlite3 module for database operations
        - Implement connection pooling for concurrent requests
        - Add indexes on role and score columns for fast queries
        - Support transactions for data integrity
    
    Advantages:
        - SQL query capabilities
        - Better for large datasets
        - Supports complex filtering and aggregation
        - ACID compliance
        - No external database server needed
    """
    
    def save(self, result: ScoreResult, role: str, resume_name: str) -> None:
        """
        Save a scoring result to SQLite database.
        
        Args:
            result: The ScoreResult to save.
            role: The job role being evaluated for.
            resume_name: Name/identifier of the resume.
            
        Raises:
            NotImplementedError: This repository is not yet implemented.
        """
        raise NotImplementedError(
            "SQLite persistence not yet implemented. Requires sqlite3."
        )
    
    def get_rankings(self, role: Optional[str] = None) -> list[dict]:
        """
        Retrieve saved results from SQLite database.
        
        Args:
            role: Optional role to filter by.
            
        Returns:
            List of result dictionaries sorted by score.
            
        Raises:
            NotImplementedError: This repository is not yet implemented.
        """
        raise NotImplementedError(
            "SQLite persistence not yet implemented. Requires sqlite3."
        )
