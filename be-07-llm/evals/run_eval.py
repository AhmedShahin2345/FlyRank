import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from llm.pipeline import run_pipeline
from llm.schema import EnrichInput

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

cases = json.loads(
    (Path(__file__).resolve().parent / "cases.json").read_text(encoding="utf-8")
)

passed = 0
failures = []
for i, case in enumerate(cases, 1):
    try:
        out = run_pipeline(EnrichInput(**case["input"]))
        ok = out.category.value == case["expected"]["category"]
        if ok:
            passed += 1
        else:
            failures.append((i, case["note"], case["expected"]["category"], out.category.value))
    except Exception as exc:
        failures.append((i, case["note"], case["expected"]["category"], f"ERROR: {exc}"))

total = len(cases)
print(f"EVAL SCORE: {passed}/{total} on category (date={__import__('datetime').datetime.now().date()}, prompt=v1, model={os.environ.get('LLM_MODEL')})")
for n, note, want, got in failures:
    print(f"  FAIL case {n} ({note}): expected {want}, got {got}")
sys.exit(0 if passed == total else 1)