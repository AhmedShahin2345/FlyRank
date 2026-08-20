import hashlib
import json
import os
from pathlib import Path

cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)

def get_cache_key(input_data, prompt_version):
    key_string = f"{json.dumps(input_data, sort_keys=True)}_{prompt_version}"
    return str(cache_dir / f"{hashlib.md5(key_string.encode()).hexdigest()}.json")

def load_cache(key):
    try:
        with open(key, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_cache(key, value):
    with open(key, 'w') as f:
        json.dump(value, f)
