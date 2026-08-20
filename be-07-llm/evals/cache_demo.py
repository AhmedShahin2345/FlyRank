import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dotenv import load_dotenv
from llm.pipeline import run_pipeline
from llm.schema import EnrichInput

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

item = EnrichInput(
    title="A Light in the Attic",
    description="Poetry from Shel Silverstein.",
    price_gbp=51.77,
)

start = time.perf_counter()
first = run_pipeline(item)
t1 = time.perf_counter() - start

start = time.perf_counter()
second = run_pipeline(item)
t2 = time.perf_counter() - start

print(f"first call:  {t1*1000:.0f} ms -> {first.model_dump()}")
print(f"second call: {t2*1000:.0f} ms -> {second.model_dump()}")
print(f"cache hit:   {t2 < t1 / 2} (second was {'fast, from cache' if t2 < t1 / 2 else 'slow — cache miss'})")