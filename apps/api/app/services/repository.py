import json
import sqlite3
from pathlib import Path
from typing import Any

from learning_ingestion import IngestionResult


class LearningRepository:
    def __init__(self, database_path: str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def save_ingestion(self, result: IngestionResult) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO sources (id, title, filename, content_type, summary)
                VALUES (?, ?, ?, ?, ?)
                """,
                (result.source_id, result.title, result.filename, result.content_type, result.summary),
            )
            connection.executemany(
                """
                INSERT INTO chunks (id, source_id, chunk_index, text, start_offset, end_offset)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (chunk.id, chunk.source_id, chunk.index, chunk.text, chunk.start_offset, chunk.end_offset)
                    for chunk in result.chunks
                ],
            )
            connection.executemany(
                """
                INSERT INTO concepts (id, source_id, label, depth, status, retrieval_health, next_review_at, evidence_chunk_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        concept.id,
                        concept.source_id,
                        concept.label,
                        concept.depth,
                        concept.status,
                        concept.retrieval_health,
                        concept.next_review_at,
                        concept.evidence_chunk_id,
                    )
                    for concept in result.concepts
                ],
            )
            connection.executemany(
                """
                INSERT INTO concept_edges (source, target, relation, confidence, source_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                [(edge.source, edge.target, edge.relation, edge.confidence, result.source_id) for edge in result.edges],
            )
            connection.executemany(
                """
                INSERT INTO learning_path (id, source_id, concept_id, stage, title, learner_action, estimated_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        item.id,
                        result.source_id,
                        item.concept_id,
                        item.stage,
                        item.title,
                        item.learner_action,
                        item.estimated_minutes,
                    )
                    for item in result.path
                ],
            )

    def list_sources(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT s.*, COUNT(DISTINCT c.id) AS concept_count, COUNT(DISTINCT ch.id) AS chunk_count
                FROM sources s
                LEFT JOIN concepts c ON c.source_id = s.id
                LEFT JOIN chunks ch ON ch.source_id = s.id
                GROUP BY s.id
                ORDER BY s.created_at DESC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            source = connection.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
            if not source:
                return None
            return {
                "source": dict(source),
                "chunks": [dict(row) for row in connection.execute("SELECT * FROM chunks WHERE source_id = ? ORDER BY chunk_index", (source_id,))],
                "concepts": [dict(row) for row in connection.execute("SELECT * FROM concepts WHERE source_id = ? ORDER BY rowid", (source_id,))],
                "edges": [dict(row) for row in connection.execute("SELECT source, target, relation, confidence FROM concept_edges WHERE source_id = ?", (source_id,))],
                "path": [dict(row) for row in connection.execute("SELECT * FROM learning_path WHERE source_id = ? ORDER BY rowid", (source_id,))],
            }

    def latest_source_id(self) -> str | None:
        with self._connect() as connection:
            row = connection.execute("SELECT id FROM sources ORDER BY created_at DESC LIMIT 1").fetchone()
            return str(row["id"]) if row else None

    def dashboard_snapshot(self) -> dict[str, Any] | None:
        latest_id = self.latest_source_id()
        if not latest_id:
            return None
        source_data = self.get_source(latest_id)
        if not source_data:
            return None

        concepts = source_data["concepts"]
        retention_values = [concept["retrieval_health"] for concept in concepts]
        retention_rate = round(sum(retention_values) / len(retention_values)) if retention_values else 0
        strong_count = sum(1 for concept in concepts if concept["status"] == "strong")

        return {
            "understanding_score": retention_rate,
            "concepts_mastered_this_week": strong_count,
            "retention_rate": retention_rate,
            "implementation_completion": 0,
            "active_source": source_data["source"],
            "concepts": [
                {
                    "id": concept["id"],
                    "label": concept["label"],
                    "depth": concept["depth"],
                    "status": concept["status"],
                    "retrieval_health": concept["retrieval_health"],
                    "next_review_at": concept["next_review_at"],
                }
                for concept in concepts
            ],
            "edges": source_data["edges"],
            "path": [
                {
                    "id": item["id"],
                    "concept_id": item["concept_id"],
                    "stage": item["stage"],
                    "title": item["title"],
                    "learner_action": item["learner_action"],
                    "estimated_minutes": item["estimated_minutes"],
                }
                for item in source_data["path"]
            ],
        }

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS sources (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    start_offset INTEGER NOT NULL,
                    end_offset INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS concepts (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
                    label TEXT NOT NULL,
                    depth INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    retrieval_health INTEGER NOT NULL,
                    next_review_at TEXT NOT NULL,
                    evidence_chunk_id TEXT REFERENCES chunks(id)
                );

                CREATE TABLE IF NOT EXISTS concept_edges (
                    source TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
                    target TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
                    relation TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS learning_path (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
                    concept_id TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
                    stage TEXT NOT NULL,
                    title TEXT NOT NULL,
                    learner_action TEXT NOT NULL,
                    estimated_minutes INTEGER NOT NULL
                );
                """
            )

    def export_json(self) -> str:
        return json.dumps({"sources": self.list_sources()}, indent=2)
