from bs4 import BeautifulSoup
from word2number import w2n
import requests
import pandas as pd

# Se crea el dataframe para almacenar los datos
book_info = pd.DataFrame(columns = ['Book', 'Price', 'Rating', 'Availability'])
# Url a scrapear
url = "http://books.toscrape.com/catalogue/page-{}.html"
# Contador de paginas
num_page = 1
# Se hace el request con el url
book_page = requests.get(url.format(num_page))
# Mientras la conexión sea exitosa
while book_page.status_code == 200:
    # Se imprime el número de pagina que se está leyendo
    print("Estoy leyendo la página {}".format(num_page))
    # Se crea un objeto Soup
    book_page_soup = BeautifulSoup(book_page.content, 'html.parser')
    # Se crea una lista con todos los objetos de tipo article con el atributo product_pod
    books_soup = book_page_soup.find_all('article',{"class":"product_pod"})
    # Se recorre la lista de objetos (libros)
    for book_soup in books_soup:
        # Título del libro
        book = book_soup.h3.get_text()
        # Precio del libro
        price = pd.to_numeric(book_soup.find("p", {"class": "price_color"}).get_text()[1:])
        # Rating
        rating = w2n.word_to_num(list(book_soup.find('p').attrs.values())[0][1])
        # Disponibilidad
        availability = True if 'In stock' in book_soup.find("p", {"class": "instock availability"}).get_text() else False
        # Se agrega la información del libro
        book_info = book_info.append({'Book': book, 'Price': price, 'Rating': rating, 'Availability': availability}, ignore_index=True)
        # Se imprime el título del libro que se agregó
        print("Agregue la información del libro: {}".format(book))
    # Se incrementa el contador de pagina
    num_page += 1
    # Se lee la siguiente pagina
    book_page = requests.get(url.format(num_page))

# Se crea un writer de excel con pandas.
writer = pd.ExcelWriter('books_gabo.xlsx', engine='xlsxwriter')
# Se divide la información de los libros por rating y se agrega una hoja por calificación
for rating in sorted(book_info.Rating.unique().tolist()):
    # Se filtran los libros con el rating correspondiente
    aux = book_info[book_info.Rating == rating]
    # Se agrega la pestaña de excel
    aux.to_excel(writer, sheet_name='Rating_{}'.format(rating), index=False)
# Se cierra el archivo y se escribe.
writer.save()
