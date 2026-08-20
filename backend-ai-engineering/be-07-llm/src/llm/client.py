import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


def load_prompt(version: str = "v1") -> str:
    return (PROMPTS_DIR / f"enrich-{version}.md").read_text(encoding="utf-8")


def get_client() -> OpenAI:
    return OpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        timeout=30.0,
        max_retries=0,
    )


def call_model(prompt: str, item_json: str, model: str) -> str:
    client = get_client()
    res = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": item_json},
        ],
    )
    return res.choices[0].message.content or ""