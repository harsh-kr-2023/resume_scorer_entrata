"""
Core data models for Resume Matcher.

Defines the main data structures used throughout the pipeline:
- ParsedDocument: Result of document parsing
- ScoreResult: Result of scoring evaluation
- PipelineResult: Final result of the complete pipeline execution
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedDocument:
    """
    Represents a parsed document with extracted text and metadata.
    
    Attributes:
        text: The extracted text content from the document.
        metadata: Additional information about the document (e.g., page_count, file_type).
    """
    text: str
    metadata: dict


@dataclass
class ScoreResult:
    """
    Represents the scoring result for a resume evaluation.
    
    Attributes:
        score: Integer score from 0 to 100 indicating match quality.
        justification: 2-3 sentence summary explaining the score.
        gaps: List of identified gaps that would prevent success in the role.
        suggestions: List of actionable improvements for the candidate.
    """
    score: int
    justification: str
    gaps: list[str]
    suggestions: list[str]


@dataclass
class PipelineResult:
    """
    Represents the final result of a complete pipeline execution.
    
    Attributes:
        success: Whether the pipeline completed successfully.
        data: The ScoreResult if successful, None otherwise.
        error: Error message if pipeline failed, None otherwise.
        failed_step: Name of the step where failure occurred, None if successful.
    """
    success: bool
    data: Optional[ScoreResult]
    error: Optional[str]
    failed_step: Optional[str]
