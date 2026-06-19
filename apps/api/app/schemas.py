from pydantic import BaseModel, Field


class SourceSummary(BaseModel):
    id: str
    title: str
    filename: str
    content_type: str
    summary: str
    created_at: str | None = None
    concept_count: int = 0
    chunk_count: int = 0


class SourceDetail(BaseModel):
    source: dict
    chunks: list[dict]
    concepts: list[dict]
    edges: list[dict]
    path: list[dict]


class IngestionResponse(BaseModel):
    source: SourceSummary
    chunks_created: int
    concepts_created: int
    edges_created: int
    path_steps_created: int


class DiagnoseRequest(BaseModel):
    concept_id: str
    learner_claim: str = Field(min_length=1)
    attempted: bool = False


class DiagnoseResponse(BaseModel):
    agent: str
    reason: str
    learner_action: str
    max_hint_level: int
    graph_updates: list[dict[str, str]]
    retention_updates: list[dict[str, str]]


class HintRequest(BaseModel):
    concept_id: str
    attempt_summary: str = Field(min_length=1)
    requested_level: int = Field(ge=1, le=4)


class HintResponse(BaseModel):
    concept_id: str
    hint_level: int
    hint: str
    learner_action: str
