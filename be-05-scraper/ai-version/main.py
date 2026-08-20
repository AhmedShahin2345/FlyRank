import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"


def scrape():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    for book in soup.select("article.product_pod"):
        title = book.select_one("h3 a").get("title")
        price = book.select_one("p.price_color").get_text(strip=True)
        rating = book.select_one("p.star-rating").get("class")[1]
        print(title, price, rating)


if __name__ == "__main__":
    scrape()