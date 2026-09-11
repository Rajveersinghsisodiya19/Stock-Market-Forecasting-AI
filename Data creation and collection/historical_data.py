from twelvedata import TDClient
import pandas as pd
import numpy as np

td = TDClient(apikey="TWELVE_DATA_API_KEY")

# 🇮🇳 Indian company

d1 = td.time_series(
    symbol="INFY",
    interval="1day",
    outputsize=5000
).as_pandas()
d1["company"] = "INFY"


# 🇺🇸 US companies

d2 = td.time_series(
    symbol="AAPL",
    interval="1day",
    outputsize=5000
).as_pandas()
d2["company"] = "AAPL"


d3 = td.time_series(
    symbol="MSFT",
    interval="1day",
    outputsize=5000
).as_pandas()
d3["company"] = "MSFT"


d4 = td.time_series(
    symbol="GOOGL",
    interval="1day",
    outputsize=5000
).as_pandas()
d4["company"] = "GOOGL"


d5 = td.time_series(
    symbol="AMZN",
    interval="1day",
    outputsize=5000
).as_pandas()
d5["company"] = "AMZN"


d6 = td.time_series(
    symbol="NVDA",
    interval="1day",
    outputsize=5000
).as_pandas()
d6["company"] = "NVDA"


d7 = td.time_series(
    symbol="TSLA",
    interval="1day",
    outputsize=5000
).as_pandas()
d7["company"] = "TSLA"


d8 = td.time_series(
    symbol="META",
    interval="1day",
    outputsize=5000
).as_pandas()
d8["company"] = "META"


df = pd.concat(
    [d1, d2, d3, d4, d5, d6, d7, d8],
    ignore_index=True
)

df.to_csv("historical_data.csv", index=False)

print("csv file created!!")


