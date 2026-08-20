# BE-05 — The Polite Scraper

A small, polite web scraper for the public sandbox site
[books.toscrape.com](https://books.toscrape.com/). It walks all three catalogue
pages, extracts every book, normalises the data, validates it, and writes clean
JSON to disk. This is Stage 5 of the FlyRank "Connecting your CRUD to the
database" track.

## What it does

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

On the first run you see `FETCH` next to each page and each book as it is
downloaded. Every HTML response is written into `cache/`. Run it a second time
and every line says `CACHE HIT` — no bytes hit the network.

The result lands in three files under `output/`:

- `books.json` — 60 validated records (one per book on the site)
- `errors.json` — anything that failed validation (empty on a healthy run)
- `run-report.json` — page count, records, cache hits, failures, runtime

## The checkpoints

1. **Fetch + cache.** Every request carries a `User-Agent` identifying the
   project, a 10s timeout, and a 500ms pause between real downloads. Responses
   are cached to `cache/` and reused on later runs. (The site has no
   `robots.txt` — it returns 404 — so there is nothing to honour beyond being
   light on the server. "No robots file" is a missing file, not a licence.)
2. **Discover the catalogue.** The script follows the `next` pagination link
   until all three pages are gathered, then collects the 60 unique book URLs.
3. **Extract raw records.** Eight fields per book: title, product URL, price
   text, availability, star rating, description, source page, fetch timestamp.
4. **Normalise + validate.** Prices become numbers (`£51.77` → `51.77`) and
   every record must match the `CleanBook` schema. Output is idempotent: run it
   ten times and `books.json` is byte-for-byte the same.
5. **Survive failures.** `tests/test_failure.py` injects a made-up URL and
   proves the run finishes, the 60 good records survive, and the bad one is
   counted and reported instead of crashing the job.

## Tests

```
python -m unittest discover -s tests -p "test_*.py" -v
```

Seven tests cover price parsing, relative URL resolution, URL de-duplication,
missing descriptions, and rating parsing, plus the end-to-end failure run.

## Extras

- `src/export_csv.py` — turn `books.json` into `books.csv` for spreadsheets.
- `src/since_last_run.py` — diff the current run against the previous one and
  report books added / removed / price-changed.
- `output/books.csv` — the 60 books as a CSV, committed so the data is visible
  without re-running.

## Honest notes

- The site declares `ISO-8859-1` but actually serves UTF-8, which mangles the
  pound sign (`Â£`) if you trust the header. The scraper checks the declared
  charset against the apparent encoding and corrects it, so prices come out as
  clean `£`.
- Book URLs on pages 2 and 3 are relative to `catalogue/`, not the site root.
  Links are resolved against the page they were found on, which is why the
  discovery step finds the same 60 books on every run.

## AI vs me

`ai-version/main.py` is the scraper an LLM writes when you just ask for "a
scraper for books.toscrape.com". Run it and it prints 20 lines — the whole
first page — and stops:

- It hardcodes one page, so it silently misses 40 of the 60 books.
- It trusts the header charset and prints `Â£51.77` instead of `£51.77`.
- No `User-Agent`, no timeout, no delay between requests, no caching — it
  hammers the server on every run and leaves no trace of what it fetched.
- It prints to stdout and throws everything away; there is nothing to read back,
  diff, or re-run against.

Everything it does wrong is exactly what the checkpoints above fix, which is
why the "AI version" and the "working version" are two different files and the
working one is the one in `src/`.

## Deliverable

- Repo: https://github.com/AhmedShahin2345/FlyRank/tree/main/be-05-scraper
- Data: https://github.com/AhmedShahin2345/FlyRank/blob/main/be-05-scraper/output/books.json
- Run report: https://github.com/AhmedShahin2345/FlyRank/blob/main/be-05-scraper/output/run-report.json