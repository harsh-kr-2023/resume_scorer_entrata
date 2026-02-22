"""
Service for building evaluation prompts from templates.

Handles loading prompt templates and substituting placeholders with
resume text, job description, and evaluation rules.
"""

import os
from app.core.exceptions import PromptBuildError


class PromptBuilder:
    """
    Builds evaluation prompts from templates with variable substitution.
    
    Takes a base template and substitutes placeholders with actual values
    from the resume, job description, and evaluation rules.
    """
    
    def __init__(self, templates_dir: str):
        """
        Initialize the prompt builder.
        
        Args:
            templates_dir: Directory path containing prompt template files.
        """
        self.templates_dir = templates_dir
    
    def build(self, resume_text: str, jd_text: str, rules: dict) -> str:
        """
        Build a complete evaluation prompt.
        
        Args:
            resume_text: The candidate's resume text.
            jd_text: The job description text.
            rules: Dictionary containing evaluation rules (must_have, nice_to_have, weights, context).
            
        Returns:
            Complete prompt string ready for LLM evaluation.
            
        Raises:
            PromptBuildError: If template not found or result is empty.
        """
        template_path = os.path.join(self.templates_dir, "base_scoring.txt")
        
        # Check if template exists
        if not os.path.exists(template_path):
            raise PromptBuildError("Prompt template not found")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        except Exception as e:
            raise PromptBuildError(f"Failed to read prompt template: {str(e)}")
        
        # Format list fields as bullet points
        must_have_formatted = "\n".join(f"- {item}" for item in rules['must_have'])
        nice_to_have_formatted = "\n".join(f"- {item}" for item in rules['nice_to_have'])
        
        # Extract weights
        weights = rules['weights']
        must_have_weight = weights.get('must_have_match', 60)
        nice_to_have_weight = weights.get('nice_to_have_match', 25)
        experience_weight = weights.get('experience_relevance', 15)
        
        # Substitute placeholders
        try:
            prompt = template.format(
                resume=resume_text,
                jd=jd_text,
                must_have=must_have_formatted,
                nice_to_have=nice_to_have_formatted,
                must_have_weight=must_have_weight,
                nice_to_have_weight=nice_to_have_weight,
                experience_weight=experience_weight,
                context=rules['context']
            )
        except KeyError as e:
            raise PromptBuildError(f"Missing placeholder in template: {str(e)}")
        
        # Validate result
        if not prompt.strip():
            raise PromptBuildError("Prompt assembly produced empty result")
        
        return prompt
