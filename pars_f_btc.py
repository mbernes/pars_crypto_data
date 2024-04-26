from binance import Client



API_KEY = ''
API_SECRET = ''

client = Client(api_key=API_KEY, api_secret=API_SECRET)

futures_tickers = client.futures_ticker()
print(futures_tickers)

for ticker in futures_tickers:
    print(ticker['symbol'])
     