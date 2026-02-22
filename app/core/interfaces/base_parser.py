"""
Abstract base class for document parsing strategies.

All parsers must convert a file into a ParsedDocument.
"""

from abc import ABC, abstractmethod
from app.core.models import ParsedDocument


class BaseParser(ABC):
    """
    Abstract base class for document parsing strategies.
    
    All parsers must convert a file into a ParsedDocument. Different parsing
    strategies can be implemented for different file types or extraction methods
    (e.g., text extraction, OCR, multimodal LLM).
    """
    
    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse a document file and extract text content.
        
        Args:
            file_path: Absolute or relative path to the document file.
            
        Returns:
            ParsedDocument containing extracted text and metadata.
            
        Raises:
            ParsingError: If parsing fails for any reason.
        """
        pass
