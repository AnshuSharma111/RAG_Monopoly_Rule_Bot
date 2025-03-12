from langchain_text_splitters import RecursiveCharacterTextSplitter
import fitz
import re
import hashlib

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    raw_text = "\n".join([page.get_text("text") for page in doc])

    # Normalize spaces & remove broken hyphenation
    clean_text = raw_text.replace(" -\n", "").replace("\n", " ")
    return " ".join(clean_text.split())  # Remove extra spaces

def get_pdf_metadata (path):
    doc = fitz.open(path)
    metadata = doc.metadata
    return metadata

def generate_id (text, index):
    hash_value = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"chunk_{index}_{hash_value}"

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

chunks = generate_chunks("monopoly.pdf")
print(chunks)