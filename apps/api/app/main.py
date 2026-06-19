from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.schemas import DiagnoseRequest, DiagnoseResponse, HintRequest, HintResponse, IngestionResponse, SourceDetail, SourceSummary
from app.services.ingestion_service import IngestionService
from app.services.learning_loop import diagnose, get_constitution, get_dashboard_snapshot, hint
from app.services.repository import LearningRepository

settings = get_settings()
repository = LearningRepository(settings.sqlite_path)
ingestion_service = IngestionService(repository)

app = FastAPI(
    title="Learn It API",
    version="0.1.0",
    description="Orchestration API for deliberate learning workflows.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/constitution")
def constitution() -> dict:
    return get_constitution().model_dump()


@app.get("/dashboard")
def dashboard() -> dict:
    return get_dashboard_snapshot(repository)


@app.get("/sources", response_model=list[SourceSummary])
def list_sources() -> list[dict]:
    return repository.list_sources()


@app.get("/sources/{source_id}", response_model=SourceDetail)
def get_source(source_id: str) -> dict:
    source = repository.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@app.post("/sources", response_model=IngestionResponse)
async def upload_source(file: UploadFile = File(...)) -> IngestionResponse:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded source is empty")

    result = ingestion_service.ingest(file.filename or "untitled.txt", file.content_type, data)
    saved = repository.get_source(result.source_id)
    if not saved:
        raise HTTPException(status_code=500, detail="Source ingestion did not persist")

    source = saved["source"]
    source["concept_count"] = len(saved["concepts"])
    source["chunk_count"] = len(saved["chunks"])
    return IngestionResponse(
        source=SourceSummary(**source),
        chunks_created=len(saved["chunks"]),
        concepts_created=len(saved["concepts"]),
        edges_created=len(saved["edges"]),
        path_steps_created=len(saved["path"]),
    )


@app.post("/diagnose", response_model=DiagnoseResponse)
def diagnose_concept(request: DiagnoseRequest) -> DiagnoseResponse:
    return diagnose(request)


@app.post("/hints", response_model=HintResponse)
def request_hint(request: HintRequest) -> HintResponse:
    return hint(request)
