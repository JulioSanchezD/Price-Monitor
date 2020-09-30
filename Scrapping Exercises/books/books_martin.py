# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

# %%
url = 'http://books.toscrape.com/catalogue/page-{0}.html'

# %%
titles = []
prices = []

for page in range(1, 51):
    r = requests.get(url.format(page))
    if not r.status_code == 200:
        continue

    soup = BeautifulSoup(r.text, 'html.parser')

    articles = soup.find_all('article', {'class': 'product_pod'})
    for article in articles:
        if article.find('p', {'class': 'star-rating Two'}):
            title = article.select_one('h3 > a').get('title')
            titles.append(title)

            price = article.find('p', {'class': 'price_color'}).text
            prices.append(price[2:])

# %%
df = pd.DataFrame({'title': titles, 'price': prices})

# %%
df.to_excel('books_martin.xlsx', index=False)
