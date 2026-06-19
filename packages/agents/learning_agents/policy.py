from enum import IntEnum, StrEnum
from pydantic import BaseModel


class AgentRole(StrEnum):
    curriculum = "curriculum"
    tutor = "tutor"
    socratic = "socratic"
    assessment = "assessment"
    implementation = "implementation"
    reviewer = "reviewer"
    retention = "retention"
    research = "research"


class HintLevel(IntEnum):
    direction = 1
    conceptual_guidance = 2
    partial_solution = 3
    full_explanation = 4


class LearningConstitution(BaseModel):
    prime_directive: str = "Never remove productive struggle; remove unnecessary friction."
    optimization_targets: tuple[str, ...] = (
        "Understanding over completion",
        "Retrieval over recognition",
        "Application over memorization",
        "Productive struggle over convenience",
        "Long-term retention over short-term satisfaction",
    )
    required_topic_facets: tuple[str, ...] = (
        "problem",
        "intuition",
        "mathematics",
        "implementation",
        "limitations",
        "historical_context",
    )


class AgentRoute(BaseModel):
    agent: AgentRole
    reason: str
    learner_action: str
    max_hint_level: HintLevel


def route_agent(intent: str, has_attempted: bool) -> AgentRoute:
    normalized = intent.lower()

    if "review" in normalized or "grade" in normalized:
        return AgentRoute(
            agent=AgentRole.reviewer,
            reason="The learner is asking for evaluation of an attempt.",
            learner_action="Submit the explanation, derivation, or code artifact for critique.",
            max_hint_level=HintLevel.full_explanation,
        )

    if "build" in normalized or "implement" in normalized or "project" in normalized:
        return AgentRoute(
            agent=AgentRole.implementation,
            reason="The next durable signal is implementation capability.",
            learner_action="Describe the smallest working artifact you can attempt first.",
            max_hint_level=HintLevel.partial_solution if has_attempted else HintLevel.conceptual_guidance,
        )

    if "quiz" in normalized or "test" in normalized or "assess" in normalized:
        return AgentRoute(
            agent=AgentRole.assessment,
            reason="The learner needs retrieval and transfer checks.",
            learner_action="Answer before receiving feedback or examples.",
            max_hint_level=HintLevel.direction,
        )

    if "why" in normalized or "challenge" in normalized or "edge" in normalized:
        return AgentRoute(
            agent=AgentRole.socratic,
            reason="The learner is ready for assumptions, edge cases, or counterexamples.",
            learner_action="Commit to a prediction before seeing the resolution.",
            max_hint_level=HintLevel.conceptual_guidance,
        )

    return AgentRoute(
        agent=AgentRole.tutor,
        reason="The learner needs guided explanation after diagnosis.",
        learner_action="State what you already know and where the confusion begins.",
        max_hint_level=HintLevel.conceptual_guidance if not has_attempted else HintLevel.partial_solution,
    )
