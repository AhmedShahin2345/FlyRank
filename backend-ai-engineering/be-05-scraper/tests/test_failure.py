import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import main


def run_with_extra_urls(extra_urls):
    import json
    import time

    start = time.time()
    main.CACHE_DIR.mkdir(exist_ok=True)
    main.OUTPUT_DIR.mkdir(exist_ok=True)
    pages = main.fetch_catalogue_pages()
    book_urls = main.discover_book_urls(pages) + extra_urls
    valid, invalid, failed, cache_hits = [], [], [], 0
    for url in book_urls:
        try:
            raw, source = main.extract_raw_record(url, source_page=url)
        except RuntimeError:
            failed.append(url)
            continue
        if source == "cache":
            cache_hits += 1
        else:
            time.sleep(main.REQUEST_DELAY)
        try:
            valid.append(main.normalize(raw))
        except Exception as exc:
            invalid.append({"url": url, "reason": str(exc)})
    unique = {b.product_url for b in valid}
    (main.OUTPUT_DIR / "books.json").write_text(
        json.dumps([b.model_dump() for b in valid], indent=2), encoding="utf-8"
    )
    report = {
        "duration_seconds": round(time.time() - start, 2),
        "pages_fetched": len(pages),
        "cache_hits": cache_hits,
        "valid_records": len(valid),
        "invalid_records": len(invalid),
        "failed_pages": len(failed),
        "unique_urls": len(unique),
    }
    (main.OUTPUT_DIR / "run-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    fake_url = "https://books.toscrape.com/catalogue/this-book-does-not-exist/index.html"
    report = run_with_extra_urls([fake_url])
    assert report["valid_records"] == 60, "the 60 good records must survive"
    assert report["failed_pages"] == 1, "the fake URL must be logged and skipped"
    books = __import__("json").load(open(main.OUTPUT_DIR / "books.json"))
    assert len(books) == 60, "books.json must still hold exactly 60 records"
    print("FAILURE TEST PASSED: run finished, 60 good records survived, 1 failure reported")