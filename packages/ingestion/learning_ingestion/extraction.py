import re
from collections import Counter

from .models import ExtractedConcept, ExtractedEdge, LearningPathItem, SourceChunk

STOPWORDS = {
    "about",
    "after",
    "also",
    "because",
    "before",
    "between",
    "could",
    "every",
    "first",
    "from",
    "have",
    "into",
    "more",
    "other",
    "should",
    "system",
    "their",
    "there",
    "these",
    "thing",
    "this",
    "through",
    "using",
    "where",
    "which",
    "while",
    "with",
    "would",
}

HEADING_PATTERN = re.compile(r"^(?:#{1,4}\s+|\d+\.\s+)?([A-Z][A-Za-z0-9 /:()\-]{3,80})$", re.MULTILINE)
TERM_PATTERN = re.compile(r"\b([A-Z][a-z]+(?:\s+(?:[A-Z][a-z]+|[a-z]{3,})){0,4})\b")


def extract_concepts(source_id: str, chunks: list[SourceChunk], title: str) -> tuple[list[ExtractedConcept], list[ExtractedEdge], list[LearningPathItem]]:
    labels = _rank_candidate_labels(chunks, title)
    concepts: list[ExtractedConcept] = []

    for index, label in enumerate(labels[:12]):
        evidence_chunk = _find_evidence_chunk(label, chunks)
        status = "weak" if index < 3 else "missing" if index > 7 else "developing"
        health = max(18, 72 - index * 5)
        concepts.append(
            ExtractedConcept(
                id=_concept_id(source_id, label),
                source_id=source_id,
                label=label,
                depth=0 if status == "missing" else 1,
                status=status,
                retrieval_health=health,
                next_review_at="Today" if index < 4 else "Tomorrow",
                evidence_chunk_id=evidence_chunk.id if evidence_chunk else None,
            )
        )

    edges = _build_edges(concepts)
    path = _build_learning_path(concepts)
    return concepts, edges, path


def _rank_candidate_labels(chunks: list[SourceChunk], title: str) -> list[str]:
    text = "\n".join(chunk.text for chunk in chunks)
    candidates: list[str] = [title]
    candidates.extend(match.group(1).strip(" :-") for match in HEADING_PATTERN.finditer(text))
    candidates.extend(match.group(1).strip() for match in TERM_PATTERN.finditer(text))

    counter: Counter[str] = Counter()
    for candidate in candidates:
        normalized = _normalize_label(candidate)
        if not normalized:
            continue
        counter[normalized] += 3 if candidate == title else 1

    return [label for label, _ in counter.most_common()]


def _normalize_label(label: str) -> str | None:
    cleaned = re.sub(r"\s+", " ", label).strip(" .:-")
    if len(cleaned) < 4 or len(cleaned) > 72:
        return None
    words = cleaned.split()
    if words[0].lower() in STOPWORDS:
        return None
    if all(word.lower() in STOPWORDS for word in words):
        return None
    return cleaned


def _find_evidence_chunk(label: str, chunks: list[SourceChunk]) -> SourceChunk | None:
    lowered = label.lower()
    return next((chunk for chunk in chunks if lowered in chunk.text.lower()), chunks[0] if chunks else None)


def _concept_id(source_id: str, label: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:48]
    return f"{source_id}-{slug or 'concept'}"


def _build_edges(concepts: list[ExtractedConcept]) -> list[ExtractedEdge]:
    if len(concepts) < 2:
        return []

    anchor = concepts[0]
    edges: list[ExtractedEdge] = []
    for concept in concepts[1:]:
        relation = "prerequisite" if concept.status in {"weak", "developing"} else "supports"
        edges.append(ExtractedEdge(source=concept.id, target=anchor.id, relation=relation, confidence=0.62))
    return edges


def _build_learning_path(concepts: list[ExtractedConcept]) -> list[LearningPathItem]:
    stages = ["diagnose", "learn", "apply", "explain", "challenge", "retain"]
    path: list[LearningPathItem] = []
    for index, concept in enumerate(concepts[:6]):
        stage = stages[index % len(stages)]
        path.append(
            LearningPathItem(
                id=f"{concept.id}-{stage}",
                concept_id=concept.id,
                stage=stage,
                title=f"{stage.title()} {concept.label}",
                learner_action=_learner_action(stage, concept.label),
                estimated_minutes=8 + index * 3,
            )
        )
    return path


def _learner_action(stage: str, label: str) -> str:
    actions = {
        "diagnose": f"Write what you already know about {label} and one point of confusion.",
        "learn": f"Explain the intuition for {label} before reading the formal version.",
        "apply": f"Use {label} in a small worked example or implementation sketch.",
        "explain": f"Teach {label} back in your own words without looking at the source.",
        "challenge": f"Name an edge case or limitation for {label}.",
        "retain": f"Schedule a retrieval review for {label} and answer from memory.",
    }
    return actions[stage]
