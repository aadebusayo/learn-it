# Architecture

Learn It is a monorepo with a React/Next.js frontend, Python services, shared prompt rules, domain packages, and Docker-backed infrastructure.

## Runtime Components

- Web: Next.js App Router, TypeScript, Tailwind, graph-focused dashboard.
- API: FastAPI orchestration layer for ingestion, graph, learning paths, assessments, and retention.
- Worker: Python background worker for ingestion and scheduled review jobs.
- PostgreSQL: relational learner state, uploads, assessment attempts, scheduling state.
- Neo4j: concept graph, prerequisites, evidence, and dependency reasoning.
- Redis: queue broker, caching, short-lived orchestration state.
- Qdrant: vector retrieval over uploaded source chunks.

## Domain Boundaries

- Ingestion parses source material and emits structured artifacts.
- Knowledge Graph owns concept nodes, dependencies, evidence, and depth state.
- Assessment creates and grades active recall, teaching, implementation, and transfer tasks.
- Retention schedules reviews from retrieval performance and concept depth.
- Agents coordinate cognitive functions but do not own durable state.

## Data Flow

```text
Upload
  -> Parse
  -> Chunk
  -> Extract concepts
  -> Build graph
  -> Detect prerequisites
  -> Generate curriculum
  -> Create assessments
  -> Schedule retention
```

## Agent Set

- Curriculum Agent: dependency maps, learning sequences, milestones.
- Tutor Agent: multi-level explanations after diagnosis.
- Socratic Agent: challenge, counterexamples, edge cases.
- Assessment Agent: quizzes, exercises, transfer checks.
- Implementation Agent: projects and code practice.
- Reviewer Agent: evaluates explanations and code.
- Retention Agent: review intervals and weak-concept resurfacing.
- Research Agent: supporting resources and historical context.
