from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    title: str
    text: str
    content_type: str


class SourceChunk(BaseModel):
    id: str
    source_id: str
    index: int
    text: str
    start_offset: int
    end_offset: int


class ExtractedConcept(BaseModel):
    id: str
    source_id: str
    label: str
    depth: int = Field(ge=0, le=5)
    status: str
    retrieval_health: int = Field(ge=0, le=100)
    next_review_at: str
    evidence_chunk_id: str | None = None


class ExtractedEdge(BaseModel):
    source: str
    target: str
    relation: str
    confidence: float = Field(ge=0, le=1)


class LearningPathItem(BaseModel):
    id: str
    concept_id: str
    stage: str
    title: str
    learner_action: str
    estimated_minutes: int = Field(gt=0)
