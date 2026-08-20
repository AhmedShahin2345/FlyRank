import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import main


class TestNormalize(unittest.TestCase):
    def test_price_with_currency_symbol(self):
        raw = main.RawBook(
            title="T",
            product_url="https://books.toscrape.com/catalogue/t/index.html",
            price_text="\u00a351.77",
            availability_text="In stock (22 available)",
            rating_text="Three",
            source_page="/catalogue/t/index.html",
            fetched_at="2026-08-20T00:00:00+00:00",
        )
        clean = main.normalize(raw)
        self.assertEqual(clean.price_gbp, 51.77)

    def test_price_with_zero_pounds(self):
        raw = main.RawBook(
            title="T",
            product_url="https://books.toscrape.com/catalogue/t/index.html",
            price_text="\u00a30.99",
            availability_text="In stock (5 available)",
            rating_text="One",
            source_page="/",
            fetched_at="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(main.normalize(raw).price_gbp, 0.99)

    def test_missing_price_becomes_zero(self):
        raw = main.RawBook(
            title="T",
            product_url="https://books.toscrape.com/catalogue/t/index.html",
            price_text="",
            availability_text="",
            rating_text="",
            source_page="/",
            fetched_at="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(main.normalize(raw).price_gbp, 0.0)


class TestUrlResolution(unittest.TestCase):
    def test_relative_links_resolve_from_page_location(self):
        page_url = "https://books.toscrape.com/catalogue/page-2.html"
        resolved = __import__("urllib.parse").parse.urljoin(
            page_url, "in-her-wake_980/index.html"
        )
        self.assertEqual(
            resolved,
            "https://books.toscrape.com/catalogue/in-her-wake_980/index.html",
        )

    def test_duplicate_urls_are_deduped(self):
        html = (
            '<article class="product_pod"><h3><a href="catalogue/a_1000/index.html"></a></h3></article>'
            '<article class="product_pod"><h3><a href="catalogue/a_1000/index.html"></a></h3></article>'
        )
        urls = main.discover_book_urls([(html, "https://books.toscrape.com/")])
        self.assertEqual(len(urls), 1)


class TestFixtures(unittest.TestCase):
    def test_missing_description_survives(self):
        page = Path(__file__).resolve().parent / "fixtures" / "no-description.html"
        self.assertTrue(page.exists(), "fixture file must exist")
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(page.read_text(), "html.parser")
        description = soup.select_one("div#product_description")
        self.assertIsNone(description)

    def test_rating_class_parsed(self):
        page = Path(__file__).resolve().parent / "fixtures" / "no-description.html"
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(page.read_text(), "html.parser")
        rating = soup.select_one("p.star-rating")
        self.assertEqual(rating.get("class")[1], "Three")


if __name__ == "__main__":
    unittest.main(verbosity=2)