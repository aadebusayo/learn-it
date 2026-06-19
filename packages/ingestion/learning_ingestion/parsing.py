from io import BytesIO

from pypdf import PdfReader

from .models import ParsedDocument


TEXT_CONTENT_TYPES = {
    "text/plain",
    "text/markdown",
    "application/octet-stream",
}


def parse_document(filename: str, content_type: str | None, data: bytes) -> ParsedDocument:
    normalized_type = content_type or "application/octet-stream"
    title = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").strip() or "Untitled source"

    if filename.lower().endswith(".pdf") or normalized_type == "application/pdf":
        reader = PdfReader(BytesIO(data))
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        return ParsedDocument(title=title, text=_clean_text(text), content_type="application/pdf")

    if normalized_type in TEXT_CONTENT_TYPES or filename.lower().endswith((".md", ".markdown", ".txt")):
        text = data.decode("utf-8", errors="replace")
        return ParsedDocument(title=title, text=_clean_text(text), content_type=normalized_type)

    text = data.decode("utf-8", errors="replace")
    return ParsedDocument(title=title, text=_clean_text(text), content_type=normalized_type)


def _clean_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    compacted: list[str] = []
    blank_seen = False
    for line in lines:
        if not line.strip():
            if not blank_seen:
                compacted.append("")
            blank_seen = True
            continue
        compacted.append(line)
        blank_seen = False
    return "\n".join(compacted).strip()
