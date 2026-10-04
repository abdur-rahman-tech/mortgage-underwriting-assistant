
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


def parse_pdf(data: bytes, filename: str) -> str:
    reader = PdfReader(BytesIO(data))
    pages = []

    for number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = f"[Could not extract page {number}: {exc}]"

        pages.append(
            f"\n--- {filename} | Page {number} ---\n{text.strip()}"
        )

    return "\n".join(pages)


def parse_docx(data: bytes, filename: str) -> str:
    from docx import Document

    document = Document(BytesIO(data))
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return f"\n--- {filename} ---\n" + "\n".join(paragraphs)


def parse_text(data: bytes, filename: str) -> str:
    text = data.decode("utf-8", errors="replace")
    return f"\n--- {filename} ---\n{text}"


def parse_uploaded_documents(uploaded_files) -> str:
    if not uploaded_files:
        return ""

    chunks = []

    for uploaded in uploaded_files:
        filename = uploaded.name
        suffix = Path(filename).suffix.lower()
        data = uploaded.getvalue()

        if suffix == ".pdf":
            chunks.append(parse_pdf(data, filename))
        elif suffix == ".docx":
            chunks.append(parse_docx(data, filename))
        elif suffix == ".txt":
            chunks.append(parse_text(data, filename))
        else:
            chunks.append(
                f"\n--- {filename} ---\nUnsupported file type."
            )

    return "\n".join(chunks).strip()
