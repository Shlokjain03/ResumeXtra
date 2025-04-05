import fitz  # PyMuPDF

def extract_text(filepath):
    text = ""
    if filepath.endswith(".pdf"):
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
    else:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    return text