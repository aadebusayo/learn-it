from pydantic import BaseModel, Field


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
