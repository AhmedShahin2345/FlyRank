You are building a FastAPI backend endpoint for a book-enrichment feature.
The working reference implementation lives in ../src/ and its README is at
../README.md. Reproduce the same feature from this spec. Write your whole
implementation under ai-version/src/. Do not copy the reference files.

SPEC

Job: an endpoint POST /enrich that takes a scraped book record and returns a
clean, validated JSON classification. One request in, one structured answer out.

Input schema (validate BEFORE any model call; invalid input must return HTTP 400
naming the offending field):
  title: string, min 1 max 200 chars, required
  description: string, max 2000 chars, optional (default "")
  price_gbp: float, >= 0, required

Output schema (the contract, defined in code, with enums for every category-like
field):
  category: one of [fiction, nonfiction, self_help, children, other]
  summary: string, min 1 max 200 chars
  confidence: float, 0.0 to 1.0
  quality_flags: array of strings, each from
    [no_description, price_is_zero, title_looks_like_marketing, summary_is_a_guess]

Prompt: lives in a versioned file prompts/enrich-v1.md, never as a string inside
a route handler. It must contain: a one-sentence role, the exact output shape
with the closed lists, the rules (never invent a category, never add fields,
never return anything but the JSON object), a when-unsure instruction (use
"other" with confidence below 0.5 rather than guessing), and at least two
examples. User content is sent as a separate user message, JSON-encoded, never
concatenated into the system prompt.

Call the model with the openai Python package pointed at an OpenAI-compatible
base URL from env vars. Set temperature low (0.2). Set an explicit timeout of 30
seconds (do not leave the SDK default). Disable the SDK's own retries and
implement your own retry loop instead: retry only on timeouts, 429, and 5xx,
with exponential backoff plus jitter (1s, 2s, 4s). Never retry 400, 401, or 403.

Model output handling: strip code fences / preamble if present, find the JSON
object, parse it, then validate against the schema. If parse or validation
fails, make exactly ONE repair call: same prompt plus the broken output plus the
validation error, asking for corrected JSON only. If the repair also fails,
return HTTP 422 with a readable message and append a line to logs/quarantine.jsonl
containing the input, the raw model output, the error, and the prompt version.
Never crash. Never return raw model text to the caller.

Operational: if env var LLM_STUB=1, skip the model entirely and return a
hard-coded schema-valid answer. If env var LLM_ENABLED=false, skip the model and
return a deterministic fallback (category "other", confidence 0.1, flag
summary_is_a_guess). Log one structured line per model call to logs/cost.log with
prompt version, model, input/output token counts, duration in ms, and repair
count. Env vars: LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, loaded from .env.

Also create: evals/cases.json with 8 hand-labelled cases (including one ambiguous
case that must fall back to "other" and one that must trigger the when-unsure
rule) and a run_eval.py that runs them through the endpoint and prints a score.
Write a short ai-version/README.md describing what you built.

Rules: write clean, well-structured, readable Python. Include minimal comments.
Make the endpoint runnable with uvicorn src.app:app. Put the route in a router
module, the client + schema + pipeline in an llm/ package, exactly like the
structure described. Do not add features that were not specified.