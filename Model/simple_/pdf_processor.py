"""
PDF Processing module using PyMuPDF
Handles PDF download and text extraction
"""
import os
import time
import requests
from typing import Optional, Tuple
import fitz  # PyMuPDF


class PDFProcessor:
    """Handles PDF download and text extraction using PyMuPDF"""
    
    def __init__(self, save_dir: str = "./documents"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def download_pdf(self, url: str, filename: Optional[str] = None) -> str:
        """Download PDF from URL (Azure blob or any URL)"""
        try:
            if not filename:
                filename = f"document_{int(time.time())}.pdf"
            
            filepath = os.path.join(self.save_dir, filename)
            
            print(f"Downloading PDF from: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"PDF downloaded successfully: {filepath}")
            return filepath
        except Exception as e:
            raise Exception(f"Failed to download PDF: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            print(f"Extracting text from PDF: {pdf_path}")
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num, page in enumerate(doc):
                text += page.get_text()
                if (page_num + 1) % 10 == 0:
                    print(f"Processed {page_num + 1} pages...")
            
            doc.close()
            print(f"Text extraction completed. Total characters: {len(text)}")
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def save_text_file(self, text: str, txt_filename: str) -> str:
        """Save extracted text as .txt file"""
        txt_path = os.path.join(self.save_dir, txt_filename)
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Text saved to: {txt_path}")
        return txt_path
    
    def process_pdf_from_url(self, url: str, doc_name: str = None) -> Tuple[str, str]:
        """Complete PDF processing pipeline"""
        try:
            # Download PDF
            pdf_filename = f"{doc_name or 'document'}.pdf"
            pdf_path = self.download_pdf(url, pdf_filename)
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Save as txt
            txt_filename = f"{doc_name or 'document'}.txt"
            txt_path = self.save_text_file(text, txt_filename)
            
            return text, txt_path
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")