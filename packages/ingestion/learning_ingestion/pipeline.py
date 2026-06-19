from uuid import uuid4

from pydantic import BaseModel

from .chunking import chunk_text
from .extraction import extract_concepts
from .models import ExtractedConcept, ExtractedEdge, LearningPathItem, SourceChunk
from .parsing import parse_document


class IngestionInput(BaseModel):
    filename: str
    content_type: str | None = None
    data: bytes


class IngestionResult(BaseModel):
    source_id: str
    title: str
    filename: str
    content_type: str
    summary: str
    chunks: list[SourceChunk]
    concepts: list[ExtractedConcept]
    edges: list[ExtractedEdge]
    path: list[LearningPathItem]


def ingest_source(request: IngestionInput) -> IngestionResult:
    source_id = f"src-{uuid4().hex[:12]}"
    parsed = parse_document(request.filename, request.content_type, request.data)
    chunks = chunk_text(source_id, parsed.text)
    concepts, edges, path = extract_concepts(source_id, chunks, parsed.title)

    return IngestionResult(
        source_id=source_id,
        title=parsed.title,
        filename=request.filename,
        content_type=parsed.content_type,
        summary=_summarize(parsed.text),
        chunks=chunks,
        concepts=concepts,
        edges=edges,
        path=path,
    )


def _summarize(text: str) -> str:
    first_sentence = text.replace("\n", " ").split(". ", 1)[0].strip()
    if not first_sentence:
        return "No extractable text was found."
    return first_sentence[:280]
