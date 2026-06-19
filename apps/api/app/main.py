from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.schemas import DiagnoseRequest, DiagnoseResponse, HintRequest, HintResponse
from app.services.learning_loop import diagnose, get_constitution, get_dashboard_snapshot, hint

settings = get_settings()

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
    return get_dashboard_snapshot()


@app.post("/diagnose", response_model=DiagnoseResponse)
def diagnose_concept(request: DiagnoseRequest) -> DiagnoseResponse:
    return diagnose(request)


@app.post("/hints", response_model=HintResponse)
def request_hint(request: HintRequest) -> HintResponse:
    return hint(request)
