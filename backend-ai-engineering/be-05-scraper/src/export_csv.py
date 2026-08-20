import csv
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

books = json.loads((OUTPUT_DIR / "books.json").read_text(encoding="utf-8"))
with open(OUTPUT_DIR / "books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["title", "product_url", "price_gbp", "availability_text", "rating_text"]
    )
    for b in books:
        writer.writerow(
            [b["title"], b["product_url"], b["price_gbp"], b["availability_text"], b["rating_text"]]
        )
print(f"exported {len(books)} rows to output/books.csv")