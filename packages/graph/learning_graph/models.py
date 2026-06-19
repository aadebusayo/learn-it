from enum import IntEnum, StrEnum
from pydantic import BaseModel, Field


class KnowledgeDepth(IntEnum):
    recognition = 0
    explanation = 1
    application = 2
    derivation = 3
    teaching = 4
    innovation = 5


class ConceptStatus(StrEnum):
    strong = "strong"
    developing = "developing"
    weak = "weak"
    missing = "missing"


class EdgeRelation(StrEnum):
    prerequisite = "prerequisite"
    supports = "supports"
    contrasts = "contrasts"
    implements = "implements"


class LearningStage(StrEnum):
    discover = "discover"
    diagnose = "diagnose"
    learn = "learn"
    apply = "apply"
    explain = "explain"
    challenge = "challenge"
    retain = "retain"


class EvidenceSpan(BaseModel):
    source_id: str
    label: str
    start_offset: int | None = None
    end_offset: int | None = None


class ConceptNode(BaseModel):
    id: str
    label: str
    depth: KnowledgeDepth = KnowledgeDepth.recognition
    status: ConceptStatus = ConceptStatus.missing
    retrieval_health: int = Field(ge=0, le=100)
    next_review_at: str
    evidence: list[EvidenceSpan] = Field(default_factory=list)


class ConceptEdge(BaseModel):
    source: str
    target: str
    relation: EdgeRelation
    confidence: float = Field(ge=0, le=1)
    evidence: list[EvidenceSpan] = Field(default_factory=list)


class LearningPathStep(BaseModel):
    id: str
    concept_id: str
    stage: LearningStage
    title: str
    learner_action: str
    estimated_minutes: int = Field(gt=0)


class KnowledgeGraphSnapshot(BaseModel):
    concepts: list[ConceptNode]
    edges: list[ConceptEdge]


def sample_attention_graph() -> KnowledgeGraphSnapshot:
    concepts = [
        ConceptNode(
            id="paper",
            label="Attention Is All You Need",
            depth=KnowledgeDepth.application,
            status=ConceptStatus.developing,
            retrieval_health=74,
            next_review_at="Today",
        ),
        ConceptNode(
            id="matmul",
            label="Matrix multiplication",
            depth=KnowledgeDepth.derivation,
            status=ConceptStatus.strong,
            retrieval_health=88,
            next_review_at="Jun 21",
        ),
        ConceptNode(
            id="dot",
            label="Dot products",
            depth=KnowledgeDepth.application,
            status=ConceptStatus.developing,
            retrieval_health=71,
            next_review_at="Tomorrow",
        ),
        ConceptNode(
            id="softmax",
            label="Softmax",
            depth=KnowledgeDepth.explanation,
            status=ConceptStatus.weak,
            retrieval_health=46,
            next_review_at="Today",
        ),
        ConceptNode(
            id="embeddings",
            label="Embeddings",
            depth=KnowledgeDepth.application,
            status=ConceptStatus.developing,
            retrieval_health=69,
            next_review_at="Jun 22",
        ),
        ConceptNode(
            id="info",
            label="Information theory",
            depth=KnowledgeDepth.recognition,
            status=ConceptStatus.missing,
            retrieval_health=18,
            next_review_at="Today",
        ),
    ]
    edges = [
        ConceptEdge(source="matmul", target="paper", relation=EdgeRelation.prerequisite, confidence=0.94),
        ConceptEdge(source="dot", target="paper", relation=EdgeRelation.prerequisite, confidence=0.91),
        ConceptEdge(source="softmax", target="paper", relation=EdgeRelation.prerequisite, confidence=0.89),
        ConceptEdge(source="embeddings", target="paper", relation=EdgeRelation.supports, confidence=0.82),
        ConceptEdge(source="info", target="paper", relation=EdgeRelation.supports, confidence=0.67),
    ]
    return KnowledgeGraphSnapshot(concepts=concepts, edges=edges)


def sample_learning_path() -> list[LearningPathStep]:
    return [
        LearningPathStep(
            id="diagnose-softmax",
            concept_id="softmax",
            stage=LearningStage.diagnose,
            title="Diagnose softmax intuition",
            learner_action="Predict how logits change probabilities before seeing the formula.",
            estimated_minutes=8,
        ),
        LearningPathStep(
            id="apply-dot-products",
            concept_id="dot",
            stage=LearningStage.apply,
            title="Apply dot products to attention scores",
            learner_action="Compute three token-to-token scores by hand.",
            estimated_minutes=15,
        ),
        LearningPathStep(
            id="explain-attention",
            concept_id="paper",
            stage=LearningStage.explain,
            title="Teach back scaled dot-product attention",
            learner_action="Explain the operation without relying on a memorized phrase.",
            estimated_minutes=12,
        ),
    ]
