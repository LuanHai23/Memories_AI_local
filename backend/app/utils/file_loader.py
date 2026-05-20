from pathlib import Path
from pypdf import PdfReader

def load_txt_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            return file.read()

def load_pdf_file(file_pathj: str) -> str:
    reader = PdfReader()

    pages_text = []

    for page_index, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages_text.append(
                f"\n\n[Page {page_index + 1}]\n{text}"
            )
    
    return "\n".join(pages_text)

# Hàm này dùng để đọc doc
def load_document_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return load_txt_file(file_path)
    
    if suffix == ".pdf":
        return load_txt_file(file_path)
    
    raise ValueError(
        f"Unsupported file type: {suffix}. Only .txt and .pdf are supported"
    )