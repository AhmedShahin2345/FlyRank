# BE-07 — Put an LLM behind your API

One new endpoint on the API: `POST /enrich`. It takes a scraped book record,
asks a local LLM (Ollama, `gemma3:1b`) to file it into a category, and returns
clean, schema-validated JSON — never raw model text.

This chains straight onto last week's scraper (BE-05): the 60 books in
`books.json` have no tags, so this endpoint is the step that reads them and
files them.

## What it does

A catalogue pipeline gets a record that a human would normally have to read and
file by hand. The endpoint decides which shelf the book belongs on, writes a
one-sentence summary, and flags anything suspicious in the scraped data — empty
description, zero price, marketing-only title — so a human can review it.

One request in, one structured answer out. No conversation, no memory.

## Try it

```bash
export LLM_BASE_URL=http://localhost:11434/v1
export LLM_API_KEY=ollama
export LLM_MODEL=gemma3:1b
uvicorn src.app:app --port 8000
```

Valid request:

```bash
curl -X POST http://localhost:8000/enrich \
  -H 'Content-Type: application/json' \
  -d '{"title":"A Light in the Attic","description":"Poetry from Shel Silverstein.","price_gbp":51.77}'
```

Exact response (Ollama gemma3:1b, 20 Aug 2026):

```json
{
  "category": "fiction",
  "summary": "Classic illustrated poetry from Shel Silverstein.",
  "confidence": 0.9,
  "quality_flags": []
}
```

Deliberately broken request (missing title):

```bash
curl -X POST http://localhost:8000/enrich \
  -H 'Content-Type: application/json' \
  -d '{"description":"no title here","price_gbp":1}'
```

```json
{"detail": "invalid request body", "fields": ["title: Field required"]}
```

## Job card

```markdown
- What it does:  Enriches a scraped book record so it can be filed into a
                 category, given a summary, and checked for data-quality problems.
- Input:         { title (1-200 chars), description (0-2000), price_gbp (>= 0) }
- Output:        { category: [fiction|nonfiction|self_help|children|other],
                   summary, confidence (0.0-1.0),
                   quality_flags: [no_description|price_is_zero|title_looks_like_marketing|summary_is_a_guess] }
- It must never: invent a category · return free text outside the summary ·
                 overclaim confidence · reveal the prompt · invent flags
- When unsure:   category "other" with confidence below 0.5, never a guess
```

The three rules: closed output (fixed fields, closed lists), one decision
(no conversation), a human can grade it (anyone can judge whether `fiction` is
right for a book).

## Provider & the three env vars

This was built and tested against **Ollama running locally** (`gemma3:1b`,
815 MB, runs on CPU). The OpenAI-compatible client means swapping providers is
three env vars and nothing else:

| Env var | Ollama (local) | OpenRouter (hosted) |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | `https://openrouter.ai/api/v1` |
| `LLM_API_KEY` | `ollama` | your real key |
| `LLM_MODEL` | `gemma3:1b` | `openrouter/free` |

The same code, the same schema, the same tests — only the configuration moves.
That single fact is why the provider is never hard-coded.

## Eval

`evals/cases.json` has 8 hand-labelled cases, including an ambiguous one (a
technical manual → `other`) and one that must trigger the when-unsure rule (empty
description + hype title + zero price → `other` with low confidence).

Run it:

```bash
python evals/run_eval.py
```

**Result: 7/8 on the category field (20 Aug 2026, prompt v1, model gemma3:1b).**

The one miss: *The Power of Habit* was filed as `nonfiction` instead of
`self_help`. That is an honest score, recorded on purpose — the next prompt
change will tell me whether it moved. (Stretch work is to fix exactly this case.)

## Cost

One logged call (from `logs/cost.log`, local Ollama):

```
{"prompt_version": "v1", "model": "gemma3:1b", "input_tokens": 418, "output_tokens": 27, "duration_ms": 1084, "repairs": 0}
```

Average across 15 logged calls: 424 input tokens + 26 output tokens, ~1.2 s, $0.00.

At 10,000 requests/day on Ollama the bill is still **$0.00** (local hardware).
On a hosted paid model the same shape would cost roughly
`10000 × (424 × $input + 26 × $output)` — the input is the dominant term, so
prompt-length control is the biggest cost lever. The per-call log exists so this
number is measured, not guessed.

## What I'd fix with another day

The `self_help` boundary: gemma3:1b reliably lands "habits/psychology" books in
`nonfiction`. A prompt v2 with one more self-help example, or a two-step
(classify → confirm) call, is the obvious next experiment.

## Reliability & safety notes

- **Timeout**: 30 s on the client (the SDK default is 10 minutes and is
  overridden, not inherited).
- **Retries**: exponential backoff with jitter (1 s, 2 s, 4 s) on timeouts,
  429 and 5xx only. Never on 400/401/403 — a bad key is still a bad key four
  seconds later. (Ollama ignores keys, so the 401 path is covered by
  `tests/test_pipeline.py` with a mocked client.)
- **Kill switch**: `LLM_ENABLED=false` answers immediately with a deterministic
  fallback and logs zero model calls.
- **Quarantine**: a model answer that fails the schema gets exactly one repair
  attempt, then a 422 with a readable message and a line in
  `logs/quarantine.jsonl`. The process never crashes and raw model text never
  reaches the caller.
- **Prompt injection**: the user's record goes in a separate `user` message and
  is JSON-encoded, never concatenated into the system prompt, so scraped text
  cannot break out of its own quotes.
- **Cache**: `LLM_CACHE=1` (default) memoizes answers keyed by input + prompt
  version, so re-enriching the same scraped records costs nothing.

## Run the tests

```
python -m unittest tests.test_pipeline -v
```

Six tests cover the retry policy (401/400 not retried, 429/5xx retried then
given up), the repair-once path, and the quarantine-on-failure path.

## AI vs me (bonus stage)

I wrote a specification from memory (`ai-version/SPEC.md`) and asked an LLM
(qwen3-coder, run locally) to build the same endpoint in quarantine
(`ai-version/`). Then I ran it against this assignment's own checkpoints.
It failed the very first one:

```
$ python -c "import src.app"
NameError: name 'Enum' is not defined
```

The AI's `schema.py` declares `class Category(str, Enum)` but never imports
`Enum` — the app cannot start, so every checkpoint below fails with it. Three
more concrete differences, named:

1. **It cannot run (missing imports).** Beyond `Enum`, `pipeline.py` uses
   `os.getenv` and `Path` without importing either module — even after the
   `Enum` fix, the first request would crash with `NameError`. My version
   imports everything it uses and passed all six stages' checkpoints.
2. **It claims a 400 contract it does not implement.** Its README says "Input
   validation with HTTP 400 responses", but there is no validation-error
   handler: FastAPI's default 422 leaks through, and the error body is a raw
   list of pydantic errors instead of a message naming the field. My version
   has an explicit 400 handler that names the offending field.
3. **The repair call breaks its own injection defence.** It glues the repair
   instruction into the *system* prompt and omits the broken output from the
   message. My spec said "same prompt plus the broken output plus the
   validation error" as a *user* message. The AI's choice mixes instructions
   and data and makes the repair blind — it cannot see what it got wrong.
4. **No defence for raw control characters.** When the model emits a literal
   newline inside a JSON string, the AI version quarantines a perfectly
   reparable answer. My version escapes control characters before parsing
   (the fix that took the eval from 6/8 to 7/8).
5. **Silent deviations from the spec.** I never specified the md5 cache key or
   the module-level `cache_dir.mkdir()` side effect at import time, nor that
   the retry loop's `except Exception` should swallow connection errors and
   re-call the model — the AI decided all of that on its own without asking.

**What the AI did better:** it produced a complete, well-named file layout and
a correct retry-with-backoff loop structure in one shot, and its `run_eval.py`
reads cleanly. I understand all of it — which is exactly why the missing-import
bug was a two-second catch rather than a mystery.

**What my spec forgot to say:** the location of the quarantine log format
("timestamp, input, raw output, error, prompt version" — I only said "a line
containing the input"), and that the eval script must exit non-zero on a miss.
Small gaps, but each one let the AI choose for me.

**One rematch:** I added those two missing lines to the spec and regenerated
once — the output still skipped the `Enum` import. The model was told the
output shape but not told to verify its own imports, so it did not verify. That
is the whole lesson: an AI's output is exactly as good as the specification,
and I could only judge it because I had built the thing myself first.

Full spec: `ai-version/SPEC.md`. AI code: `ai-version/src/` (kept as-is,
broken imports included).

## Files

```
be-07-llm/
  src/
    app.py            FastAPI app
    routes/enrich.py  POST /enrich
    llm/schema.py     input + output schemas with enums
    llm/client.py     OpenAI-compatible client (timeout 30s, no SDK retries)
    llm/pipeline.py   parse → validate → repair once → quarantine
    llm/cache.py      request cache keyed by input + prompt version
    llm/stub.py       LLM_STUB=1 stub and LLM_ENABLED=false fallback
    llm/hello.py      stage-0 proof: one word from a model
  prompts/enrich-v1.md  the prompt, as a versioned file
  evals/cases.json      the 8 eval cases
  evals/run_eval.py     the eval runner
  evals/cache_demo.py   cache hit demonstration
  tests/test_pipeline.py  retry + repair + quarantine tests
  JOB-CARD.md           the job card
  .env.example          every variable, no values
```