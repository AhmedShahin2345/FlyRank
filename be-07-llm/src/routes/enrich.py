import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from ..llm.client import call_model, load_prompt
from ..llm.schema import EnrichInput, EnrichOutput
from ..llm.stub import stub_answer

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

router = APIRouter(prefix="/enrich", tags=["enrich"])

PROMPT_VERSION = "v1"


@router.post("", response_model=EnrichOutput, status_code=200)
def enrich(item: EnrichInput):
    if os.environ.get("LLM_STUB") == "1":
        return stub_answer(item)
    prompt = load_prompt(PROMPT_VERSION)
    item_json = json.dumps(item.model_dump(), ensure_ascii=False)
    model = os.environ["LLM_MODEL"]
    raw = call_model(prompt, item_json, model)
    return json.loads(raw)