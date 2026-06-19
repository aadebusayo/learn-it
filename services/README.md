# Services

These folders describe deployable Python service boundaries. The starter implementation keeps runnable code in `apps/api`, `apps/worker`, and domain packages while this directory documents the intended service split.

- `ingestion`: parse, chunk, extract concepts, and create source-grounded artifacts.
- `orchestration`: coordinate agents and learning-loop state transitions.
- `knowledge_graph`: own graph writes, dependency inference, and graph queries.
- `retrieval`: embed source chunks and retrieve evidence.
- `evaluation`: assess explanations, exercises, code, and transfer performance.
- `memory`: maintain learner state, concept depth, and misconception history.
- `scheduling`: compute retention intervals and review queues.
