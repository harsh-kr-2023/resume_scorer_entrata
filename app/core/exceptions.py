"""
Custom exception hierarchy for Resume Matcher.

Defines a base exception and specific subclasses for different failure modes
in the pipeline. This allows for precise error handling and meaningful
HTTP status code mapping.
"""


class MatcherError(Exception):
    """
    Base exception for all Resume Matcher errors.
    
    All custom exceptions in the application inherit from this base class,
    allowing for catch-all error handling when needed.
    
    Attributes:
        message: Human-readable error message.
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ParsingError(MatcherError):
    """
    Raised when document parsing fails.
    
    This exception is raised when:
    - The input file cannot be found
    - The file format is unsupported or corrupted
    - Text extraction produces no results
    - The parsing library encounters an error
    """
    pass


class RuleLoadingError(MatcherError):
    """
    Raised when rule JSON file is missing or malformed.
    
    This exception is raised when:
    - The rules file for the specified role does not exist
    - The JSON file is malformed and cannot be parsed
    - Required fields are missing from the rules structure
    """
    pass


class PromptBuildError(MatcherError):
    """
    Raised when prompt template is missing or substitution produces empty result.
    
    This exception is raised when:
    - The prompt template file cannot be found
    - Template substitution fails
    - The resulting prompt is empty after substitution
    """
    pass


class ScoringError(MatcherError):
    """
    Raised when LLM call fails or response cannot be parsed.
    
    This exception is raised when:
    - All retry attempts for the LLM call are exhausted
    - The LLM response is not valid JSON
    - The response is missing required fields
    - Response validation fails (e.g., score out of range)
    """
    pass


class PersistenceError(MatcherError):
    """
    Raised when database write or read fails.
    
    This exception is raised when:
    - File system write operations fail
    - Database connection or query fails
    - Directory creation fails
    - File permissions prevent read/write operations
    """
    pass
