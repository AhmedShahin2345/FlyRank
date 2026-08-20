import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from ..llm.pipeline import run_pipeline
from ..llm.schema import EnrichInput, EnrichOutput
from ..llm.stub import fallback_answer, stub_answer

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

router = APIRouter(prefix="/enrich", tags=["enrich"])

PROMPT_VERSION = "v1"


@router.post("", response_model=EnrichOutput, status_code=200)
def enrich(item: EnrichInput):
    if os.environ.get("LLM_STUB") == "1":
        return stub_answer(item)
    if os.environ.get("LLM_ENABLED", "true").lower() in ("false", "0", "no"):
        return fallback_answer()
    try:
        return run_pipeline(item, PROMPT_VERSION)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc))