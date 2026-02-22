"""
LLM-based scorer using LangChain.

Uses LangChain to call LLM APIs (Anthropic or OpenAI) for resume scoring.
Implements retry logic and response validation.
"""

import json
import logging
from typing import Any
from app.core.interfaces.base_scorer import BaseScorer
from app.core.models import ScoreResult
from app.core.exceptions import ScoringError
from app.config import Config

logger = logging.getLogger(__name__)


class LLMScorer(BaseScorer):
    """
    LLM-based scorer using LangChain.
    
    Uses LangChain to abstract LLM API calls. Supports both Anthropic and OpenAI.
    Implements retry logic for reliability and validates LLM responses.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the LLM scorer.
        
        Args:
            config: Configuration object containing LLM settings.
        """
        self.config = config
        self.max_retries = config.MAX_RETRIES
        self.retry_delay = config.RETRY_DELAY
        
        # Initialize the appropriate LLM based on provider
        if config.LLM_PROVIDER.lower() == "anthropic":
            from langchain_anthropic import ChatAnthropic
            self.llm = ChatAnthropic(
                model=config.LLM_MODEL,
                api_key=config.LLM_API_KEY,
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS
            )
        elif config.LLM_PROVIDER.lower() == "openai":
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=config.LLM_MODEL,
                api_key=config.LLM_API_KEY,
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")
    
    def score(self, prompt: str) -> ScoreResult:
        """
        Score a resume using the LLM.
        
        Args:
            prompt: Complete evaluation prompt.
            
        Returns:
            ScoreResult containing score, justification, gaps, and suggestions.
            
        Raises:
            ScoringError: If LLM call fails or response is invalid.
        """
        last_error = None
        
        # Retry loop
        for attempt in range(self.max_retries):
            try:
                logger.info(f"LLM scoring attempt {attempt + 1}/{self.max_retries}")
                
                # Call the LLM
                response = self.llm.invoke(prompt)
                
                # Extract content from response
                if hasattr(response, 'content'):
                    content = response.content
                else:
                    content = str(response)
                
                # Parse JSON response
                try:
                    result_dict = json.loads(content)
                except json.JSONDecodeError as e:
                    # Try to extract JSON from markdown code blocks
                    if "```json" in content:
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        content = content[json_start:json_end].strip()
                        result_dict = json.loads(content)
                    elif "```" in content:
                        json_start = content.find("```") + 3
                        json_end = content.find("```", json_start)
                        content = content[json_start:json_end].strip()
                        result_dict = json.loads(content)
                    else:
                        raise ScoringError(f"Failed to parse LLM response as JSON: {str(e)}")
                
                # Validate response structure
                self._validate_response(result_dict)
                
                # Build and return ScoreResult
                return ScoreResult(
                    score=int(result_dict['score']),
                    justification=result_dict['justification'],
                    gaps=result_dict['gaps'],
                    suggestions=result_dict['suggestions']
                )
                
            except ScoringError:
                # Re-raise our own exceptions
                raise
            except Exception as e:
                last_error = e
                logger.warning(f"LLM call attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay)
        
        # All retries exhausted
        raise ScoringError(
            f"LLM call failed after {self.max_retries} retries. Last error: {str(last_error)}"
        )
    
    def _validate_response(self, result_dict: dict) -> None:
        """
        Validate that the LLM response has all required fields.
        
        Args:
            result_dict: Parsed JSON response from LLM.
            
        Raises:
            ScoringError: If validation fails.
        """
        required_fields = ['score', 'justification', 'gaps', 'suggestions']
        
        for field in required_fields:
            if field not in result_dict:
                raise ScoringError(f"LLM response missing required field: {field}")
        
        # Validate score is an integer between 0 and 100
        try:
            score = int(result_dict['score'])
            if not 0 <= score <= 100:
                raise ScoringError(f"Score must be between 0 and 100, got: {score}")
        except (ValueError, TypeError):
            raise ScoringError(f"Score must be an integer, got: {result_dict['score']}")
        
        # Validate justification is non-empty string
        if not isinstance(result_dict['justification'], str) or not result_dict['justification'].strip():
            raise ScoringError("Justification must be a non-empty string")
        
        # Validate gaps and suggestions are lists
        if not isinstance(result_dict['gaps'], list):
            raise ScoringError("Gaps must be a list")
        if not isinstance(result_dict['suggestions'], list):
            raise ScoringError("Suggestions must be a list")
