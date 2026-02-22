"""
OCR-based parser using Tesseract (STUB).

Handles scanned PDFs and images where text is embedded in pictures.
Use when text_extract_parser returns empty results.
"""

from app.core.interfaces.base_parser import BaseParser
from app.core.models import ParsedDocument


class OCRParser(BaseParser):
    """
    OCR-based parser using Tesseract.
    
    Handles scanned PDFs and images where text is embedded in pictures.
    Use when text_extract_parser returns empty results.
    
    Dependencies:
        - pytesseract: Python wrapper for Tesseract OCR
        - Pillow (PIL): Image processing library
        - tesseract-ocr: Tesseract OCR engine (system installation)
    
    Implementation notes:
        - Convert PDF pages to images using pdf2image
        - Run Tesseract OCR on each image
        - Combine results from all pages
        - Handle multiple languages if needed
    """
    
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse a document using OCR.
        
        Args:
            file_path: Path to the document file.
            
        Returns:
            ParsedDocument containing extracted text and metadata.
            
        Raises:
            NotImplementedError: This parser is not yet implemented.
        """
        raise NotImplementedError(
            "OCR parsing not yet implemented. Requires pytesseract and Pillow."
        )
