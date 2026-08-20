from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .llm.schema import EnrichInput, EnrichOutput
from .llm.pipeline import run_enrich

app = FastAPI()

@app.post("/enrich", response_model=EnrichOutput)
async def enrich_book(input_data: EnrichInput):
    try:
        validated_input = EnrichInput(**input_data.dict())
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    try:
        result = run_enrich(validated_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
