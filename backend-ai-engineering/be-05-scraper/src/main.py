import json
import re
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, ValidationError

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "output"

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/AhmedShahin2345/FlyRank)"
TIMEOUT = 10
REQUEST_DELAY = 0.5

BASE_URL = "https://books.toscrape.com"
FIRST_PAGE = "https://books.toscrape.com/"
CACHE_PAGES = 3


class RawBook(BaseModel):
    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str
    fetched_at: str


class CleanBook(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float = Field(ge=0)
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str
    fetched_at: str


def get(url: str, use_cache: bool = True) -> tuple[str | None, str, int]:
    cache_path = CACHE_DIR / (re.sub(r"[^a-zA-Z0-9_-]", "_", url) + ".html")
    if use_cache and cache_path.exists():
        return cache_path.read_text(encoding="utf-8", errors="replace"), "cache", 200
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
    except requests.RequestException:
        return None, "error", 0
    if resp.status_code != 200:
        return None, "failed", resp.status_code
    if resp.encoding and resp.encoding.lower() == "iso-8859-1" and resp.apparent_encoding:
        resp.encoding = resp.apparent_encoding
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(resp.text, encoding="utf-8")
    return resp.text, "fetch", resp.status_code


def fetch_catalogue_pages() -> list[tuple[str, str]]:
    pages = []
    url = FIRST_PAGE
    for _ in range(CACHE_PAGES):
        html, source, _ = get(url)
        if html is None:
            break
        pages.append((html, url))
        size = len(html.encode("utf-8"))
        print(f"{'CACHE HIT' if source == 'cache' else 'FETCH'} {url} ({size} bytes)")
        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one("li.next a")
        if next_link is None:
            break
        url = urllib.parse.urljoin(url, next_link["href"])
        if source == "fetch":
            time.sleep(REQUEST_DELAY)
    return pages


def discover_book_urls(pages: list[tuple[str, str]]) -> list[str]:
    urls = []
    for html, page_url in pages:
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.select("article.product_pod h3 a"):
            urls.append(urllib.parse.urljoin(page_url, link["href"]))
    seen = set()
    unique = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def extract_raw_record(url: str, source_page: str) -> tuple[RawBook, str]:
    html, source, _ = get(url)
    if html is None:
        raise RuntimeError(f"failed to fetch {url}")
    soup = BeautifulSoup(html, "html.parser")
    price_text = soup.select_one("p.price_color")
    availability = soup.select_one("p.instock.availability")
    rating = soup.select_one("p.star-rating")
    description = soup.select_one("div#product_description")
    desc_p = description.find_next("p") if description else None
    return (
        RawBook(
            title=soup.select_one("h1").get_text(strip=True),
            product_url=url,
            price_text=price_text.get_text(strip=True) if price_text else "",
            availability_text=availability.get_text(" ", strip=True) if availability else "",
            rating_text=rating.get("class")[1] if rating and len(rating.get("class", [])) > 1 else "",
            description=desc_p.get_text(strip=True) if desc_p else None,
            source_page=source_page,
            fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ),
        source,
    )


def normalize(raw: RawBook) -> CleanBook:
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", raw.price_text)
    price_gbp = float(match.group(1)) if match else 0.0
    return CleanBook(
        title=raw.title,
        product_url=raw.product_url,
        price_text=raw.price_text,
        price_gbp=price_gbp,
        availability_text=raw.availability_text,
        rating_text=raw.rating_text,
        description=raw.description,
        source_page=raw.source_page,
        fetched_at=raw.fetched_at,
    )


def run() -> None:
    start = time.time()
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    pages = fetch_catalogue_pages()
    book_urls = discover_book_urls(pages)

    valid = []
    invalid = []
    failed = []
    cache_hits = 0
    for url in book_urls:
        try:
            raw, source = extract_raw_record(url, source_page=url.replace(BASE_URL, ""))
        except RuntimeError:
            failed.append(url)
            continue
        if source == "cache":
            cache_hits += 1
        else:
            time.sleep(REQUEST_DELAY)
        try:
            clean = normalize(raw)
            valid.append(clean)
        except ValidationError as exc:
            invalid.append({"url": url, "reason": str(exc)})

    unique_urls = {b.product_url for b in valid}
    books_path = OUTPUT_DIR / "books.json"
    books_path.write_text(
        json.dumps([b.model_dump() for b in valid], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    errors_path = OUTPUT_DIR / "errors.json"
    errors_path.write_text(json.dumps(invalid, indent=2), encoding="utf-8")

    duration = round(time.time() - start, 2)
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duration_seconds": duration,
        "pages_fetched": len(pages),
        "cache_hits": cache_hits,
        "valid_records": len(valid),
        "invalid_records": len(invalid),
        "failed_pages": len(failed),
        "unique_urls": len(unique_urls),
    }
    (OUTPUT_DIR / "run-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (OUTPUT_DIR / ".previous-books.json").write_text(
        json.dumps([b.model_dump() for b in valid], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()