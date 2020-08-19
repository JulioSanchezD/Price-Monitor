from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


n_book, n_page = 0, 1
url: str = "http://books.toscrape.com/catalogue/page-{}.html"
df = pd.DataFrame(columns=["Title", "Price", "Instock Availability"])

print("Searching books...")
while (r := requests.get(url=url.format(n_page))).status_code == 200:
    print(f"Searching page {n_page}")
    n_page += 1
    soup = BeautifulSoup(r.text, "html.parser")
    books: list = soup.find_all("article", {"class": "product_pod"})
    for book in books:
        if book.find("p", {"class": "star-rating Two"}):
            df.loc[n_book, "Title"] = book.h3.a["title"]
            df.loc[n_book, "Price"] = book.find("p", {"class": "price_color"}).text[2:]
            df.loc[n_book, "Instock Availability"] = book.find("p", {"class": "instock availability"}).text.strip()
            n_book += 1

df.to_csv("Scrapping Exercises/books/books_julio.csv", index=False)
