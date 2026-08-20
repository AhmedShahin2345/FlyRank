import json
import os
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import openai
from pydantic import ValidationError

from .client import get_client, load_prompt
from .schema import EnrichInput, EnrichOutput

LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
BACKOFF_BASE = 1.0  # seconds


def extract_json(text: str) -> str:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    obj = re.search(r"\{.*\}", text, re.S)
    if obj:
        text = obj.group(0)
    # Small models sometimes emit raw control characters inside JSON strings
    # (a real newline instead of the \n escape). Convert them to \uXXXX escapes
    # so strict parsers accept the answer instead of quarantining it.
    text = re.sub(
        r"[\x00-\x1f\x7f]",
        lambda m: "\\u%04x" % ord(m.group()),
        text,
    )
    return text


def quarantine(input_item: dict, raw_output: str, error: str, prompt_version: str) -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input": input_item,
        "raw_output": raw_output,
        "error": error,
        "prompt_version": prompt_version,
    }
    with open(LOGS_DIR / "quarantine.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_call(prompt_version: str, model: str, duration_ms: int, repairs: int, usage=None) -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    usage = usage or {}
    with open(LOGS_DIR / "cost.log", "a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "prompt_version": prompt_version,
                    "model": model,
                    "input_tokens": usage.get("prompt_tokens", -1),
                    "output_tokens": usage.get("completion_tokens", -1),
                    "duration_ms": duration_ms,
                    "repairs": repairs,
                }
            )
            + "\n"
        )


def is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, openai.APITimeoutError):
        return True
    if isinstance(exc, openai.RateLimitError):
        return True
    if isinstance(exc, openai.InternalServerError):
        return True
    if isinstance(exc, openai.APIStatusError):
        return exc.status_code in RETRYABLE_STATUS
    return False


def complete(messages: list[dict], prompt_version: str, model: str) -> tuple[str, int, dict]:
    """Call the model once with timeout and bounded retries. Returns (text, retries, usage)."""
    client = get_client()
    retries = 0
    while True:
        try:
            res = client.chat.completions.create(
                model=model,
                temperature=0.2,
                messages=messages,
            )
            return (
                res.choices[0].message.content or "",
                retries,
                res.usage.model_dump() if res.usage else {},
            )
        except BaseException as exc:
            if not is_retryable(exc) or retries >= MAX_RETRIES:
                raise
            retries += 1
            sleep_s = BACKOFF_BASE * (2 ** (retries - 1)) + random.uniform(0, 0.5)
            time.sleep(sleep_s)


def run_pipeline(item: EnrichInput, prompt_version: str = "v1", model: str | None = None) -> EnrichOutput:
    import os

    from .cache import cache_key, get, put

    item_json = json.dumps(item.model_dump(), ensure_ascii=False)
    cache_enabled = os.environ.get("LLM_CACHE", "1") == "1"
    key = cache_key(item_json, prompt_version)
    if cache_enabled:
        cached = get(key)
        if cached is not None:
            return EnrichOutput.model_validate(cached)

    prompt = load_prompt(prompt_version)
    model = model or os.environ["LLM_MODEL"]

    start = time.perf_counter()
    first, retries, usage = complete(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": item_json},
        ],
        prompt_version,
        model,
    )
    repairs = 0
    try:
        parsed = extract_json(first)
        out = EnrichOutput.model_validate_json(parsed)
    except (json.JSONDecodeError, ValidationError) as first_err:
        repairs = 1
        repaired, _, usage = complete(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": item_json},
                {
                    "role": "user",
                    "content": (
                        "Your previous answer was rejected for this reason: "
                        f"{first_err}. Return only corrected JSON matching the schema. "
                        f"Here is what you returned: {first}"
                    ),
                },
            ],
            prompt_version,
            model,
        )
        try:
            parsed = extract_json(repaired)
            out = EnrichOutput.model_validate_json(parsed)
        except (json.JSONDecodeError, ValidationError) as second_err:
            quarantine(item.model_dump(), first, str(first_err), prompt_version)
            raise RuntimeError(f"model output rejected after repair: {second_err}")
    duration_ms = int((time.perf_counter() - start) * 1000)
    log_call(prompt_version, model, duration_ms, repairs, usage)
    if cache_enabled:
        put(key, out.model_dump())
    return out