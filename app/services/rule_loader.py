"""
Service for loading role-specific evaluation rules from JSON files.

Handles reading and parsing rule files that define must-have skills,
nice-to-have skills, weights, and evaluation context for different roles.
"""

import json
import os
from app.core.exceptions import RuleLoadingError


class RuleLoader:
    """
    Loads role-specific evaluation rules from JSON files.
    
    Rules define the criteria for evaluating candidates for different roles,
    including required skills, preferred skills, scoring weights, and context.
    """
    
    def __init__(self, rules_dir: str):
        """
        Initialize the rule loader.
        
        Args:
            rules_dir: Directory path containing rule JSON files.
        """
        self.rules_dir = rules_dir
    
    def load(self, role: str) -> dict:
        """
        Load rules for a specific role.
        
        Args:
            role: The role identifier (e.g., 'backend_engineer').
            
        Returns:
            Dictionary containing must_have, nice_to_have, weights, and context.
            
        Raises:
            RuleLoadingError: If file not found or JSON is malformed.
        """
        file_path = os.path.join(self.rules_dir, f"{role}.json")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise RuleLoadingError(f"No rules found for role: {role}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            
            # Validate required fields
            required_fields = ['must_have', 'nice_to_have', 'weights', 'context']
            for field in required_fields:
                if field not in rules:
                    raise RuleLoadingError(
                        f"Malformed rules file for role: {role} - missing field: {field}"
                    )
            
            return rules
            
        except json.JSONDecodeError as e:
            raise RuleLoadingError(f"Malformed rules file for role: {role} - {str(e)}")
        except Exception as e:
            raise RuleLoadingError(f"Error loading rules for role: {role} - {str(e)}")
