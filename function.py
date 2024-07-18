import PyPDF2
import fitz
"""
def text_extractor_for_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    first_page = reader.pages[0]
    return first_page.extract_text()
"""
def text_extractor_for_pdf(pdf_bytes):
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text("text") # Extract text from each page
        return text