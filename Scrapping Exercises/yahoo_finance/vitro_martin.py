# %%
import datetime
import io
import time

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

# %%
date_max = datetime.date.today()
date_min = date_max - relativedelta(years=3)

tstamp_max = time.mktime(date_max.timetuple())
tstamp_min = time.mktime(date_min.timetuple())

# %%
period1 = str(tstamp_min).split('.')[0]
period2 = str(tstamp_max).split('.')[0]

# %%
url = 'https://query1.finance.yahoo.com/v7/finance/download/VITROA.MX'

params = {
    'period1': period1,
    'period2': period2,
    'interval': '1d',
    'events': 'history'
}

r = requests.get(url, params=params)

# %%
df = pd.read_csv(io.StringIO(r.text))
df.to_csv('vitro.csv', index=False)
