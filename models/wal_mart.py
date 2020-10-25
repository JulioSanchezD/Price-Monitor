from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import tqdm
import datetime as dt
import os


def get_chrome_options(headless=False):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=800,800")
    chrome_options.add_argument("--disable-infobars")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable_gpu")
    return chrome_options


def get_firefox_options(headless=False):
    firefox_options = FirefoxOptions()
    firefox_options.headless = headless
    return firefox_options


class WalMart:
    scroll_pause_time = 1.5
    url = "https://super.walmart.com.mx"

    def __init__(self, browser="Firefox", executable_path=None, headless=False, zip_code="45643"):
        self.browser = browser
        self.executable_path = executable_path
        self.headless = headless
        self.zip_code = zip_code

    def __enter__(self):
        if self.browser == "Firefox":
            if not self.executable_path:
                self.driver = webdriver.Firefox(service_log_path=os.path.devnull, firefox_options=get_firefox_options(self.headless))
            else:
                self.driver = webdriver.Firefox(executable_path=self.executable_path, service_log_path=os.path.devnull, firefox_options=get_firefox_options(self.headless))
        elif self.browser == "Chrome":
            if not self.executable_path:
                self.driver = webdriver.Chrome(chrome_options=get_chrome_options(self.headless))
            else:
                self.driver = webdriver.Chrome(executable_path=self.executable_path, chrome_options=get_chrome_options(self.headless))
        else:
            raise Exception("Invalid Browser")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def enter_zipcode(self):
        # Wait until zipcode modal appears and enter zipcode
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "zipCode"))).send_keys(self.zip_code)
        self.driver.find_element_by_xpath('//button[@data-automation-id="arrow"]').click()
        sleep(WalMart.scroll_pause_time)
        # Close modal
        self.driver.find_element_by_xpath('//button[@data-automation-id="modalCloseButton"]').click()

    def scrap_by_category(self, category):
        self.driver.get(f"{WalMart.url}/productos?Ntt={category}")
        self.enter_zipcode()
        # Wait until prices appears
        sleep(WalMart.scroll_pause_time)

        # Get total products and scrollable table where the products are
        total_products = int(self.driver.find_element_by_xpath('//span[@data-automation-id="productTotal"]').text)
        scrollable_div = self.driver.find_element_by_xpath('//div[@id="scrollToTopComponent"]')
        i = 0
        p_bar = tqdm(total=total_products)

        # Initialize lists
        product_names = []
        product_prices = []
        scrap_date_times = []

        # Loop through products
        while i <= total_products:
            try:
                product = self.driver.find_element_by_xpath(f'//div[@data-automation-id="product-{i}"]')
            except NoSuchElementException:
                i += 1
                p_bar.update(1)
                # If product is not found, then scroll down until is loaded
                while len(self.driver.find_elements_by_xpath(f'//div[@data-automation-id="product-{i}"]')) == 0:
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                    sleep(WalMart.scroll_pause_time)
                # Wait until prices appears
                sleep(WalMart.scroll_pause_time)
            else:
                product_name = product.find_element_by_xpath('.//p[@data-testid="product-name"]').text
                product_price = product.find_element_by_xpath('.//p[@data-testid="price"]').text
                if category.lower() in product_name.lower():
                    product_names.append(product_name)
                    product_prices.append(product_price)
                    scrap_date_times.append(dt.datetime.now())
                i += 1
                p_bar.update(1)
        p_bar.close()

        # Return results as a tuple of lists
        return scrap_date_times, product_names, product_prices

