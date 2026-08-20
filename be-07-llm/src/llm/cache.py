import hashlib
import json
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "cache"


def cache_key(item_json: str, prompt_version: str) -> str:
    digest = hashlib.sha256((item_json + "::" + prompt_version).encode("utf-8")).hexdigest()
    return f"{prompt_version}-{digest}"


def get(key: str):
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def put(key: str, output: dict) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    (CACHE_DIR / f"{key}.json").write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")