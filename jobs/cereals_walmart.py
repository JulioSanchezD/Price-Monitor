from models.wal_mart import WalMart
from utils import telegram_bot_sendtext
import os
import pandas as pd
import sqlite3

walmart = WalMart(browser='Chrome', zip_code="45643")
with walmart:
    try:
        scrap_result = walmart.scrap_by_category("cereal")
    except Exception as e:
        telegram_bot_sendtext(f"Cereal walmart robot crashed, error: {str(e)}")
    else:
        telegram_bot_sendtext(f"Finished walmart scrapping succesfully")

# Transform extracted data into DataFrame
df = pd.DataFrame({"scrap_date_time": scrap_result[0], "product_name": scrap_result[1], "product_prices": scrap_result[2]})
df["supermarket"] = "Wal-Mart"

# Save data into database
with sqlite3.connect(os.path.join(os.path.dirname(__file__), "prices.db")) as cnx:
    df.to_sql(name="cereals", con=cnx, if_exists='append', index=False)
