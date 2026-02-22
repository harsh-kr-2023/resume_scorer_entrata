"""
Filesystem repository.

Persists scoring results as JSON files in a directory.
Simple and effective for small to medium datasets.
"""

import os
import json
import re
from datetime import datetime
from typing import Optional
from app.core.interfaces.base_repository import BaseRepository
from app.core.models import ScoreResult
from app.core.exceptions import PersistenceError


class FilesystemRepository(BaseRepository):
    """
    Persists scoring results as JSON files.
    
    Each result is saved as a separate JSON file in the output directory.
    Simple and effective for small to medium datasets.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize the filesystem repository.
        
        Args:
            output_dir: Directory path for storing result files.
        """
        self.output_dir = output_dir
        
        # Create directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            raise PersistenceError(f"Failed to create output directory: {str(e)}")
    
    def save(self, result: ScoreResult, role: str, resume_name: str) -> None:
        """
        Save a scoring result as a JSON file.
        
        Args:
            result: The ScoreResult to save.
            role: The job role being evaluated for.
            resume_name: Name/identifier of the resume.
            
        Raises:
            PersistenceError: If save operation fails.
        """
        try:
            # Create result dictionary
            timestamp = datetime.now().isoformat()
            result_dict = {
                "role": role,
                "resume_name": resume_name,
                "score": result.score,
                "justification": result.justification,
                "gaps": result.gaps,
                "suggestions": result.suggestions,
                "created_at": timestamp
            }
            
            # Generate safe filename
            safe_role = self._sanitize_filename(role)
            safe_resume = self._sanitize_filename(resume_name)
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_role}_{safe_resume}_{timestamp_str}.json"
            
            # Write to file
            file_path = os.path.join(self.output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise PersistenceError(f"Failed to save result: {str(e)}")
    
    def get_rankings(self, role: Optional[str] = None) -> list[dict]:
        """
        Retrieve saved results from filesystem.
        
        Args:
            role: Optional role to filter by.
            
        Returns:
            List of result dictionaries sorted by score (descending).
            
        Raises:
            PersistenceError: If retrieval operation fails.
        """
        try:
            results = []
            
            # Read all JSON files from output directory
            if not os.path.exists(self.output_dir):
                return results
            
            for filename in os.listdir(self.output_dir):
                if not filename.endswith('.json'):
                    continue
                
                file_path = os.path.join(self.output_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result_dict = json.load(f)
                    
                    # Filter by role if specified
                    if role is None or result_dict.get('role') == role:
                        results.append(result_dict)
                        
                except Exception as e:
                    # Log error but continue processing other files
                    print(f"Warning: Failed to read {filename}: {str(e)}")
                    continue
            
            # Sort by score descending
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            return results
            
        except Exception as e:
            raise PersistenceError(f"Failed to retrieve rankings: {str(e)}")
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """
        Sanitize a string to be safe for use in filenames.
        
        Args:
            name: Original string.
            
        Returns:
            Sanitized string safe for filenames.
        """
        # Remove or replace unsafe characters
        safe_name = re.sub(r'[^\w\s-]', '', name)
        safe_name = re.sub(r'[\s]+', '_', safe_name)
        return safe_name.strip('_')
