import time
import json
from typing import Optional
from .schema import EnrichInput, EnrichOutput
from .client import client, model_name
from .stub import stub_answer, fallback_answer
from .cache import get_cache_key, load_cache, save_cache

def run_enrich(input_data: EnrichInput, prompt_version: str = "enrich-v1.md") -> EnrichOutput:
    if os.getenv("LLM_STUB", "").lower() == "1":
        return stub_answer()
    
    if os.getenv("LLM_ENABLED", "true").lower() != "true":
        return fallback_answer()

    cache_key = get_cache_key(input_data.dict(), prompt_version)
    cached = load_cache(cache_key)
    if cached:
        return EnrichOutput(**cached)

    # Load prompt
    prompt_path = Path(f"prompts/{prompt_version}")
    with open(prompt_path, 'r') as f:
        system_prompt = f.read()

    user_message = json.dumps(input_data.dict())

    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2,
            timeout=30
        )
        raw_output = response.choices[0].message.content
    except Exception as e:
        # Retry logic for timeouts, 429s, and 5xx errors
        import random
        import time
        retries = 0
        max_retries = 3
        backoff_time = 1

        while retries < max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.2,
                    timeout=30
                )
                raw_output = response.choices[0].message.content
                break
            except Exception as retry_e:
                if retries >= max_retries:
                    raise retry_e
                # Only retry on timeouts, 429s, and 5xx errors
                if "timeout" in str(retry_e).lower() or \
                   (hasattr(retry_e, 'status_code') and 
                    (retry_e.status_code == 429 or retry_e.status_code >= 500)):
                    time.sleep(backoff_time + random.uniform(0, 1))
                    backoff_time *= 2
                    retries += 1
                else:
                    raise retry_e

    duration = time.time() - start_time

    # Parse and validate output
    try:
        parsed_output = parse_and_validate(raw_output)
        save_cache(cache_key, parsed_output.dict())
        log_cost(prompt_version, response.usage.prompt_tokens,
                 response.usage.completion_tokens, duration, 0)
        return parsed_output
    except Exception as e:
        # Repair attempt
        repair_prompt = f"{system_prompt}\n\n--- REPAIR REQUEST ---\n\nThe previous output was invalid due to: {str(e)}.\nPlease return ONLY the corrected JSON object."
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": repair_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                timeout=30
            )
            raw_output = response.choices[0].message.content
            parsed_output = parse_and_validate(raw_output)
            save_cache(cache_key, parsed_output.dict())
            log_cost(prompt_version, response.usage.prompt_tokens,
                     response.usage.completion_tokens, duration, 1)
            return parsed_output
        except Exception as repair_e:
            # Log to quarantine
            import logging
            from pathlib import Path
            quarantine_path = Path("logs/quarantine.jsonl")
            quarantine_path.parent.mkdir(exist_ok=True)
            with open(quarantine_path, 'a') as f:
                f.write(json.dumps({
                    "input": input_data.dict(),
                    "raw_output": raw_output,
                    "error": str(repair_e),
                    "prompt_version": prompt_version
                }) + "\n")
            raise ValueError(f"Failed to repair output after retry: {repair_e}")

def parse_and_validate(raw_output: str) -> EnrichOutput:
    # Strip code fences if present
    lines = raw_output.strip().split('\n')
    json_lines = []
    in_json_block = False
    for line in lines:
        if line.startswith("```json"):
            in_json_block = True
            continue
        elif line.startswith("```"):
            in_json_block = False
            continue
        elif in_json_block:
            json_lines.append(line)
        else:
            json_lines.append(line)

    json_str = '\n'.join(json_lines).strip()
    try:
        parsed = json.loads(json_str)
        return EnrichOutput(**parsed)
    except Exception as e:
        raise ValueError(f"Failed to parse or validate JSON: {e}")

def log_cost(prompt_version, prompt_tokens, completion_tokens, duration, repair_count):
    import logging
    from pathlib import Path
    log_path = Path("logs/cost.log")
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, 'a') as f:
        f.write(json.dumps({
            "prompt_version": prompt_version,
            "model": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "duration_ms": int(duration * 1000),
            "repair_count": repair_count
        }) + "\n")
