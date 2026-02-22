"""
Text extraction parser using pdfplumber.

Extracts text directly from PDF files using pdfplumber library.
Best for PDFs with embedded text (not scanned images).
"""

import os
import pdfplumber
from app.core.interfaces.base_parser import BaseParser
from app.core.models import ParsedDocument
from app.core.exceptions import ParsingError


class TextExtractParser(BaseParser):
    """
    Parser that extracts text directly from PDF files.
    
    Uses pdfplumber to extract embedded text from PDF documents.
    Works best with PDFs that contain actual text layers (not scanned images).
    """
    
    def parse(self, file_path: str) -> ParsedDocument:
        """
        Parse a PDF file and extract text content.
        
        Args:
            file_path: Path to the PDF file.
            
        Returns:
            ParsedDocument containing extracted text and metadata.
            
        Raises:
            ParsingError: If file not found, parsing fails, or no text extracted.
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise ParsingError(f"File not found: {file_path}")
        
        try:
            # Open PDF and extract text
            with pdfplumber.open(file_path) as pdf:
                pages = pdf.pages
                page_count = len(pages)
                
                # Extract text from all pages
                text_parts = []
                for page in pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                # Join all pages with newlines
                extracted_text = "\n".join(text_parts)
                
                # Validate that we got some text
                if not extracted_text.strip():
                    raise ParsingError("PDF produced no extractable text")
                
                # Build metadata
                metadata = {
                    "page_count": page_count,
                    "file_type": "pdf"
                }
                
                return ParsedDocument(text=extracted_text, metadata=metadata)
                
        except ParsingError:
            # Re-raise our own exceptions
            raise
        except Exception as e:
            raise ParsingError(f"Failed to parse PDF: {str(e)}")
