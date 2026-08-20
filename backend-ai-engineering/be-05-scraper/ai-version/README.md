# AI version of the scraper — kept for comparison

This file is what a fresh AI prompt produced when asked to "write a Python
scraper for books.toscrape.com". It was generated first, then deliberately
quarantined here so it can be compared against the real implementation in
`src/`.

## Why it is wrong

Run it and compare:

| Behaviour | AI version (`ai-version/main.py`) | Working version (`src/main.py`) |
|---|---|---|
| Books scraped | 20 (page 1 only) | 60 (all pages) |
| Pagination | hardcoded single URL | follows the `next` link |
| Price format | `Â£51.77` (mojibake) | `£51.77` |
| Encoding | trusts the wrong header charset | detects and corrects it |
| Politeness | no `User-Agent`, no timeout, no delay | UA, 10s timeout, 500ms delay |
| Caching | none | full disk cache, cache hits on re-run |
| Output | printed to stdout, then lost | validated `books.json` on disk |
| Failure handling | crashes on any missing element | schema validation + failure report |
| Re-runnable | no | idempotent, diffable with `since_last_run.py` |

The point of keeping it is to make the difference visible: a scraper that only
works on one specific page on a good day is not a scraper, it is a screenshot.