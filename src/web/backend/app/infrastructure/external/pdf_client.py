"""PDF download and extraction client."""
import requests
from typing import Optional
import pdfplumber
import io


class PdfClient:
    """Client for downloading and extracting text from PDFs."""
    
    def download_pdf(self, pdf_url: str) -> bytes:
        """Download PDF from URL."""
        try:
            response = requests.get(pdf_url, timeout=60, stream=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"Failed to download PDF: {str(e)}")
    
    def extract_text(self, pdf_content: bytes) -> str:
        """Extract text from PDF content."""
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                return "\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def download_and_extract(self, pdf_url: str) -> str:
        """Download PDF and extract text in one operation."""
        pdf_content = self.download_pdf(pdf_url)
        return self.extract_text(pdf_content)

