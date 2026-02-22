"""
Multimodal LLM parser (STUB).

Sends the document directly to a vision-capable LLM for text extraction.
Best for complex layouts, tables, and mixed-format documents.
"""

from app.core.interfaces.base_parser import BaseParser
from app.core.models import ParsedDocument


class LLMParser(BaseParser):
    """
    Multimodal LLM parser.
    
    Sends the document directly to a vision-capable LLM for text extraction.
    Best for complex layouts, tables, and mixed-format documents.
    
    Dependencies:
        - Vision-capable LLM (e.g., GPT-4 Vision, Claude 3)
        - PDF to image conversion library
    
    Implementation notes:
        - Convert PDF pages to images
        - Send images to vision-capable LLM
        - Request structured text extraction
        - Handle tables and complex layouts
        - Preserve document structure in output
    
    Advantages:
        - Handles complex layouts better than OCR
        - Can understand context and structure
        - Works with tables, charts, and mixed content
        - No need for separate OCR engine
    """
    
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse a document using multimodal LLM.
        
        Args:
            file_path: Path to the document file.
            
        Returns:
            ParsedDocument containing extracted text and metadata.
            
        Raises:
            NotImplementedError: This parser is not yet implemented.
        """
        raise NotImplementedError(
            "LLM parsing not yet implemented. Requires multimodal model support."
        )
