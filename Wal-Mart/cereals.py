from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime as dt
import pandas as pd
import sqlite3
import os

SCROLL_PAUSE_TIME: float = 1.5
product_names: list = []
product_prices: list = []
scrap_date_times: list = []

with webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver.exe', service_log_path=os.path.devnull) as driver:
    # Search by category
    driver.get("https://super.walmart.com.mx/productos?Ntt=cereal")
    # Wait until modal appears
    sleep(0.5)
    driver.find_element_by_xpath('//button[@data-automation-id="modalCloseButton"]').click()
    # Wait until prices appears
    sleep(SCROLL_PAUSE_TIME)

    # Loop through products
    total_products: int = int(driver.find_element_by_xpath('//span[@data-automation-id="productTotal"]').text)
    scrollable_div = driver.find_element_by_xpath('//div[@id="scrollToTopComponent"]')
    i: int = 0
    while i <= total_products:
        try:
            product = driver.find_element_by_xpath(f'//div[@data-automation-id="product-{i}"]')
        except NoSuchElementException:
            i += 1
            # If product is not found, then scroll down until is loaded
            while len(driver.find_elements_by_xpath(f'//div[@data-automation-id="product-{i}"]')) == 0:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                sleep(SCROLL_PAUSE_TIME)
            # Wait until prices appears
            sleep(SCROLL_PAUSE_TIME)
        else:
            product_name: str = product.find_element_by_xpath('.//p[@data-testid="product-name"]').text
            product_price: str = product.find_element_by_xpath('.//p[@data-testid="price"]').text
            if "cereal" in product_name.lower():
                product_names.append(product_name)
                product_prices.append(product_price)
                scrap_date_times.append(dt.datetime.now())
            i += 1

# Transform extracted data into DataFrame
df = pd.DataFrame({"scrap_date_time": scrap_date_times, "product_name": product_names, "product_prices": product_prices})
df["supermarket"] = "Wal-Mart"

# Save data into database
with sqlite3.connect("prices.db") as cnx:
    df.to_sql(name="cereals", con=cnx, if_exists='append')



