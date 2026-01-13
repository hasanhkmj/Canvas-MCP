import io
from pypdf import PdfReader

def extract_pdf_text(buffer: bytes, max_chars: int = 0) -> str:
    """
    Extract text from a PDF buffer.
    
    Args:
        buffer: The PDF file content as bytes.
        max_chars: Maximum characters to return (0 for no limit).
        
    Returns:
        The extracted text.
    """
    try:
        reader = PdfReader(io.BytesIO(buffer))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        text = text.strip()
        
        if max_chars > 0 and len(text) > max_chars:
            text = text[:max_chars]
            
        return text
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")
