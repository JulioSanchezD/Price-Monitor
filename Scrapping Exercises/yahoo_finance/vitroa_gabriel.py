import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# Se inicializa el lector yahoo finanzas
vitroa = yf.Ticker("VITROA.MX")
# Se extraen los datos de ocho años a la fecha
dfVitroa = (pd.DataFrame(vitroa.history(start=(date.today()-timedelta(days=365*8)).strftime("%Y-%m-%d"), end=date.today().strftime("%Y-%m-%d")))).reset_index()
# Se cambia el formato de la columna date
dfVitroa.loc[:,'Date'] = dfVitroa.Date.apply(lambda x: x.strftime("%Y-%m-%d"))
