import os
import uuid
from pypdf import PdfReader
from docx import Document as DocxDocument
from fastapi import UploadFile

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> tuple[str, str, int]:
    ext = file.filename.split(".")[-1].lower()
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return unique_name, file_path, len(content)

def extract_text(file_path: str, file_type: str) -> str:
    try:
        if file_type == "pdf":
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif file_type in ["docx", "doc"]:
            doc = DocxDocument(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        elif file_type == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    except Exception as e:
        return f"Error extracting text: {str(e)}"