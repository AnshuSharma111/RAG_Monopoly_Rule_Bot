from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
import pytesseract
import re

def extract_text_from_pdf (pdf_path):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Extract text using Tesseract OCR
    ocr_text = "\n".join(pytesseract.image_to_string(img) for img in images)
    return ocr_text

def generate_chunks (path):
    # Extract text from PDF
    text = extract_text_from_pdf(path)

    # First, split document by headings which are in all caps and followedand preceded by a newline character
    regex = r"\n[A-Z ]+\n"
    sections = re.split(regex, text)

    # Now, apply recursive character splitting to each chunk
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 750,
        chunk_overlap = 200
    )

    # Chunking
    chunks = []

    for section in sections:
        chunks.extend(recursive_splitter.split_text(section))

    return chunks