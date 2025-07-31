import requests
import fitz  # PyMuPDF
import io

def fetch_pdf_text_from_url(url: str) -> str:
    """
    Streams a PDF from the given URL and extracts its text content using PyMuPDF (fitz).
    Returns the full text as a string.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    pdf_stream = io.BytesIO(response.content)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    # Example PDF URL (public domain sample)
    sample_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    pdf_text = fetch_pdf_text_from_url(sample_url)
    print(pdf_text[:1000]) 