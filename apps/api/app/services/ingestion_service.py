from learning_ingestion import IngestionInput, IngestionResult, ingest_source

from app.services.repository import LearningRepository


class IngestionService:
    def __init__(self, repository: LearningRepository) -> None:
        self.repository = repository

    def ingest(self, filename: str, content_type: str | None, data: bytes) -> IngestionResult:
        result = ingest_source(IngestionInput(filename=filename, content_type=content_type, data=data))
        self.repository.save_ingestion(result)
        return result
