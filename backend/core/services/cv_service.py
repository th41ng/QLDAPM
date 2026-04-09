import json
import mimetypes
import os
from pathlib import Path

from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from werkzeug.datastructures import FileStorage

from ..security import slugify

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_resume_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_dir(base_dir: str) -> Path:
    path = Path(base_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_uploaded_file(file_storage: FileStorage, base_dir: str, prefix: str) -> tuple[str, str, str]:
    safe_name = slugify(Path(file_storage.filename).stem)
    ext = Path(file_storage.filename).suffix.lower()
    file_name = f"{prefix}-{safe_name}{ext}"
    upload_dir = ensure_upload_dir(base_dir)
    destination = upload_dir / file_name
    file_storage.save(destination)
    mime_type = mimetypes.guess_type(str(destination))[0] or "application/octet-stream"
    return file_name, str(destination), mime_type


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()


def extract_text_from_doc(path: str) -> str:
    # Best-effort support for .doc uploads.
    try:
        import subprocess

        output_dir = Path(path).parent
        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "docx",
                "--outdir",
                str(output_dir),
                path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        converted = Path(path).with_suffix(".docx")
        if converted.exists():
            return extract_text_from_docx(str(converted))
    except Exception:
        pass
    return ""


def extract_text_from_upload(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    if ext == ".docx":
        return extract_text_from_docx(path)
    if ext == ".doc":
        return extract_text_from_doc(path)
    return ""


def generate_pdf_from_resume(data: dict, output_path: str) -> str:
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50
    lines = [
        data.get("full_name", ""),
        data.get("headline", ""),
        "",
        "Summary:",
        data.get("summary", ""),
        "",
        "Skills:",
        data.get("skills", ""),
        "",
        "Experience:",
        data.get("experience", ""),
        "",
        "Education:",
        data.get("education", ""),
    ]
    for line in lines:
        if y < 60:
            c.showPage()
            y = height - 50
        c.drawString(50, y, line[:120])
        y -= 18
    c.save()
    return output_path


def generate_docx_from_resume(data: dict, output_path: str) -> str:
    doc = Document()
    doc.add_heading(data.get("full_name", "Resume"), level=1)
    if data.get("headline"):
        doc.add_paragraph(data["headline"])
    for label, key in [
        ("Summary", "summary"),
        ("Skills", "skills"),
        ("Experience", "experience"),
        ("Education", "education"),
    ]:
        doc.add_heading(label, level=2)
        doc.add_paragraph(data.get(key, ""))
    doc.save(output_path)
    return output_path

