from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routes.enrich import router as enrich_router

app = FastAPI(title="Book Enrichment API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    fields = [f"{e.get('loc', ['?'])[-1]}: {e.get('msg', 'invalid')}" for e in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"detail": "invalid request body", "fields": fields},
    )


app.include_router(enrich_router)


@app.get("/health")
def health():
    return {"status": "ok"}