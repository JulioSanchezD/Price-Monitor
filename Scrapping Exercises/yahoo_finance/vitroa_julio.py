from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime as dt
import sqlite3 as db
import requests

def get_date_past_n_years(ref_date, years: int) -> dt.datetime:
    return ref_date - relativedelta(years=years)

def date_to_integer(date: dt.datetime) -> int:
    seconds: float = (date - dt.datetime(1970, 1, 1)).total_seconds()
    return round(seconds)

def get_data_json(r_json: dict) -> dict:
    data: dict = {
        "timestamp": r_json["chart"]["result"][0]["timestamp"],
        "open": r_json["chart"]["result"][0]["indicators"]["quote"][0]["open"],
        "high": r_json["chart"]["result"][0]["indicators"]["quote"][0]["high"],
        "low": r_json["chart"]["result"][0]["indicators"]["quote"][0]["low"],
        "close": r_json["chart"]["result"][0]["indicators"]["quote"][0]["close"],
        "adj_close": r_json["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"],
        "volume": r_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    }
    return data

if __name__ == "__main__":
    # Get periods dates
    today = dt.datetime.today()
    date_min = get_date_past_n_years(today, 8)

    # Request data
    url: str = "https://query1.finance.yahoo.com/v8/finance/chart/VITROA.MX"
    params: dict = {
        "period1": date_to_integer(date_min),
        "period2": date_to_integer(today),
        "interval": "1d",
        "events": "div%7Csplit"
    }
    r = requests.get(url=url, params=params)

    # Extract data from json
    data: dict = get_data_json(r.json())

    # Transform data to data frame
    df = pd.DataFrame(data=data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d")

    # Export DF to DB
    with db.connect("stock.db") as cnx:
        df.to_sql(name="vitroa", con=cnx)