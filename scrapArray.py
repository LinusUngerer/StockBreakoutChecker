import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url)[0]
sp500_tickers = table['Symbol'].tolist()

print(sp500_tickers)
