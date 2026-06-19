# Learn It

Learn It is a cognitive operating system for deliberate learning. It transforms dense material into prerequisite graphs, active recall, implementation practice, teaching sessions, and retention schedules.

The operating principle is simple:

> The system never removes productive struggle. It removes unnecessary friction.

## Monorepo Layout

```text
apps/
  web/      Next.js learning dashboard and concept graph UI
  api/      FastAPI orchestration API
  worker/   Background ingestion and scheduling worker
packages/
  shared/   TypeScript shared contracts for the web app
  prompts/  Agent constitution and prompt rules
  agents/   Python agent policy and routing primitives
  graph/    Python knowledge graph domain model
  ingestion/ assessment/ retrieval/ analytics/ docs stubs
services/
  ingestion/ orchestration/ knowledge_graph/ retrieval/ evaluation/ memory/ scheduling/
docs/
  Product, architecture, coding, and operating rules
```

## Quick Start

```bash
pnpm install
pnpm dev:web
```

In another terminal:

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e . -e ../../packages/agents -e ../../packages/graph
uvicorn app.main:app --reload --port 8000
```

Docker-based local infrastructure:

```bash
docker compose up --build
```

## Core Loop

Every concept moves through:

```text
Discover -> Diagnose -> Learn -> Apply -> Explain -> Challenge -> Retain
```

A concept is never treated as complete. It deepens across recognition, explanation, application, derivation, teaching, and innovation.
