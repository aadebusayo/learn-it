# Coding Rules

## General

- Keep domain behavior explicit and typed.
- Avoid framework-specific logic in domain packages.
- Prefer small services that return structured objects.
- Use direct names from the learning domain: concept, prerequisite, retrieval, teaching, depth, retention.
- Add abstractions only when they clarify the learning model or remove real duplication.

## TypeScript

- Use strict TypeScript.
- Shared UI contracts belong in `packages/shared`.
- React components should receive typed data and avoid embedding backend assumptions.
- Pages should compose components and call thin API clients.

## Python

- FastAPI route handlers should call application services.
- Pydantic models define public API shapes.
- Domain dataclasses or Pydantic models define internal learning entities.
- Keep LLM calls behind interfaces so prompts, tools, and model providers are replaceable.
- Use structured graph operations instead of free-form text mutations.

## Data

- Store source evidence with graph mutations.
- Track confidence for extracted concepts and prerequisite edges.
- Preserve learner attempts; do not overwrite diagnostic history.
- Retention schedules must derive from performance signals.

## Testing Direction

- Start with domain-service tests for graph planning, hint escalation, and retention scheduling.
- Add API contract tests when routes stabilize.
- Add end-to-end tests only around critical learning workflows.
