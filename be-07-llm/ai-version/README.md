This is a FastAPI backend for book enrichment. It provides an endpoint `/enrich` that takes a scraped book record and returns a clean, validated JSON classification.

Features:
- Input validation with HTTP 400 responses for invalid fields
- OpenAI-compatible LLM integration with retry logic
- Caching based on input hash + prompt version
- Stub mode for testing (`LLM_STUB=1`)
- Fallback mode when LLM is disabled (`LLM_ENABLED=false`)
- Cost logging to `logs/cost.log`
- Quarantine logging for failed outputs to `logs/quarantine.jsonl`

Usage:
```bash
uvicorn src.app:app --reload
```

Endpoint:
POST /enrich

Input schema:
- title (string, 1-200 chars)
- description (string, max 2000 chars)
- price_gbp (float >= 0)

Output schema:
- category (one of fiction, nonfiction, self_help, children, other)
- summary (string, 1-200 chars)
- confidence (float 0.0-1.0)
- quality_flags (array of strings from [no_description, price_is_zero, title_looks_like_marketing, summary_is_a_guess])

Environment variables:
- LLM_BASE_URL
- LLM_API_KEY
- LLM_MODEL
- LLM_STUB=1 (to enable stub mode)
- LLM_ENABLED=false (to disable model calls)

Evaluation:
Run `python run_eval.py` to test with 8 hand-labelled cases.
---
