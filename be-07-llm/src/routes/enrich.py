import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from ..llm.schema import EnrichInput, EnrichOutput
from ..llm.stub import stub_answer

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

router = APIRouter(prefix="/enrich", tags=["enrich"])


@router.post("", response_model=EnrichOutput, status_code=200)
def enrich(item: EnrichInput):
    if os.environ.get("LLM_STUB") == "1":
        return stub_answer(item)
    raise HTTPException(status_code=501, detail="model call not wired yet — use LLM_STUB=1")