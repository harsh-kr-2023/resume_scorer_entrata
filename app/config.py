"""
Configuration module for Resume Matcher.

Loads all settings from environment variables with sensible defaults.
Uses python-dotenv to load .env file at module level.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class that reads all settings from environment variables.
    
    All configuration values are loaded at class level to ensure consistency
    across the application. Values can be overridden via environment variables.
    """
    
    # LLM Configuration
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    # Retry Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "1.0"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # Database Configuration
    DB_PATH: str = os.getenv("DB_PATH", "results.db")
    
    # Strategy Defaults
    DEFAULT_PARSER: str = os.getenv("DEFAULT_PARSER", "text")
    DEFAULT_SCORER: str = os.getenv("DEFAULT_SCORER", "llm")
    DEFAULT_REPOSITORY: str = os.getenv("DEFAULT_REPOSITORY", "filesystem")
    
    # Directory Paths
    RULES_DIR: str = os.getenv("RULES_DIR", "app/rules")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "app/prompt_templates")
    RESULTS_DIR: str = os.getenv("RESULTS_DIR", "results")
    
    @classmethod
    def validate(cls) -> None:
        """
        Validate that required configuration values are present.
        
        Raises:
            ValueError: If LLM_API_KEY is not set.
        """
        if not cls.LLM_API_KEY:
            raise ValueError("LLM_API_KEY environment variable is required")
