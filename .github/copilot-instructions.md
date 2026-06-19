# Learn It Engineering Instructions

This repository builds a deliberate-learning system, not a generic PDF chatbot. Every feature should preserve productive struggle while removing unnecessary friction.

## Product Rules

- Optimize for durable understanding, retrieval, transfer, implementation, and long-term retention.
- Treat the knowledge graph as the product. LLMs are interfaces to graph-backed learner state.
- Prefer active learner participation over passive explanation.
- Use escalating hints before full answers: direction, conceptual guidance, partial solution, full explanation.
- Never mark a concept as done. Track depth and retention state.

## Coding Rules

- Keep domain logic in packages or service modules, not directly in route handlers or React pages.
- Model concepts, dependencies, assessments, learning states, and agent policies explicitly.
- Make APIs deterministic where possible; put stochastic LLM behavior behind typed interfaces.
- Use structured data over prompt-string parsing for graph updates and assessments.
- Keep defaults local-development friendly, but do not hide production concerns behind toy abstractions.
- Prefer small, typed modules with plain names over clever framework magic.

## UI Rules

- Build the real learning workspace as the first screen, not a marketing landing page.
- Show meaningful progress: depth, retrieval health, implementation status, graph expansion, and review due dates.
- Avoid superficial gamification such as coins, arbitrary badges, or inflated XP.
- Keep dashboard surfaces dense, calm, and scannable.

## Backend Rules

- FastAPI routes should call application services.
- Background work belongs in the worker or service modules.
- Graph operations should preserve evidence, dependency type, confidence, and source spans.
- Retention scheduling must be driven by retrieval performance, not activity streaks.
