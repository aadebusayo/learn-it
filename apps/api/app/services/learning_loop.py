from learning_agents import LearningConstitution, route_agent
from learning_graph.models import sample_attention_graph, sample_learning_path

from app.schemas import DiagnoseRequest, DiagnoseResponse, HintRequest, HintResponse
from app.services.repository import LearningRepository


HINTS = {
    1: "Look for what changes and what stays invariant in the concept.",
    2: "Connect the operation to the learner action: predict, compare, or normalize before calculating.",
    3: "Write the first step explicitly, then stop and explain why it is allowed.",
    4: "Here is the full explanation path: define the problem, state the intuition, formalize it, implement it, and name a failure mode.",
}


def get_constitution() -> LearningConstitution:
    return LearningConstitution()


def get_dashboard_snapshot(repository: LearningRepository | None = None) -> dict:
    if repository:
        persisted_snapshot = repository.dashboard_snapshot()
        if persisted_snapshot:
            return persisted_snapshot

    graph = sample_attention_graph()
    return {
        "understanding_score": 67,
        "concepts_mastered_this_week": 4,
        "retention_rate": 82,
        "implementation_completion": 38,
        "concepts": [concept.model_dump(mode="json") for concept in graph.concepts],
        "edges": [edge.model_dump(mode="json") for edge in graph.edges],
        "path": [step.model_dump(mode="json") for step in sample_learning_path()],
    }


def diagnose(request: DiagnoseRequest) -> DiagnoseResponse:
    route = route_agent(request.learner_claim, has_attempted=request.attempted)
    return DiagnoseResponse(
        agent=route.agent.value,
        reason=route.reason,
        learner_action=route.learner_action,
        max_hint_level=int(route.max_hint_level),
        graph_updates=[
            {
                "type": "diagnostic_signal",
                "concept_id": request.concept_id,
                "status": "needs_attempt" if not request.attempted else "ready_for_feedback",
            }
        ],
        retention_updates=[
            {
                "concept_id": request.concept_id,
                "action": "schedule_review_after_attempt",
            }
        ],
    )


def hint(request: HintRequest) -> HintResponse:
    return HintResponse(
        concept_id=request.concept_id,
        hint_level=request.requested_level,
        hint=HINTS[request.requested_level],
        learner_action="Respond with your next attempted step before requesting a stronger hint.",
    )
