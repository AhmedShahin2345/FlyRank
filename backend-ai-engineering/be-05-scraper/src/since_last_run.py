import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
SNAPSHOT = OUTPUT_DIR / ".previous-books.json"


def load(path):
    if not path.exists():
        return {}
    return {b["product_url"]: b for b in json.loads(path.read_text(encoding="utf-8"))}


current = load(OUTPUT_DIR / "books.json")
previous = load(SNAPSHOT)

added = [url for url in current if url not in previous]
removed = [url for url in previous if url not in current]
changed = [
    url
    for url in current
    if url in previous and current[url]["price_gbp"] != previous[url]["price_gbp"]
]

print(f"books now: {len(current)}")
print(f"added since last run: {len(added)}")
print(f"removed since last run: {len(removed)}")
print(f"price changes: {len(changed)}")
for url in added[:5]:
    print("  +", url)
for url in removed[:5]:
    print("  -", url)