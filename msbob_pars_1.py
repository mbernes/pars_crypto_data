import pandas as pd
import numpy as np
import backtesting
import requests
from binance import Client
from datetime import date, timedelta


day_back = 8           # Кількість днів від поточної дати до початку тестування 23.05.2023 (01.01.2023)

# tickers = ['ETHUSDT', 'BTCUSDT', 'ADAUSDT', 'XRPUSDT']   # Список інструментів
tickers = ['BTCUSDT']   # Список інструментів

# tickers = []
#
# with open('ticker_list.txt', 'r') as file:
#     for line in file:
#         ticker = line.strip()
#         tickers.append(ticker)

print(tickers)


# Таймфрейми
timeframes = [
    Client.KLINE_INTERVAL_1MINUTE
    # Client.KLINE_INTERVAL_3MINUTE,
    # Client.KLINE_INTERVAL_5MINUTE,
    # Client.KLINE_INTERVAL_15MINUTE,
    # Client.KLINE_INTERVAL_30MINUTE,
    # Client.KLINE_INTERVAL_1HOUR,
    # Client.KLINE_INTERVAL_4HOUR,
    # Client.KLINE_INTERVAL_1DAY
]


class ExchangeData:
    def __init__(self, api_key, api_secret, symbol, interval, start_date, end_date):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.df = self._get_historical_klines()

    def _get_historical_klines(self):
        klines = self.client.get_historical_klines(self.symbol, self.interval,
                                                   self.start_date.strftime("%d %b %Y %H:%M:%S"),
                                                   self.end_date.strftime("%d %b %Y %H:%M:%S"))

        df = pd.DataFrame(klines, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                           'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                           'Taker buy quote asset volume', 'Ignore'])

        # df.drop(
        #     columns=['Volume', 'Close time', 'Quote asset volume', 'Number of trades',
        #              'Taker buy base asset volume',
        #              'Taker buy quote asset volume', 'Ignore'], inplace=True
        # )
        df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
        # df = df.set_index('timestamp')
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Close'] = pd.to_numeric(df['Close'])
        # df.set_index(pd.to_datetime(df.index, unit='ms'), inplace=True)
        print(self.start_date)
        return df



name_file_csv = 'RESULT.csv'



def read_data_csv(file_name = 'AAPL_200D.csv' ):
    data = pd.read_csv(file_name)
    df_csv = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close'])

    return df_csv

def import_binance(symbol = 'BTCUSDT', interval = '1d', limit = 500 ):
    global name_file_csv
    name_file_csv = f'RESULT_{symbol}_{interval}_{limit}.csv'
    response = requests.get(f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}')
    data = response.json()
    df_binance = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'])
    df_binance.drop(
        columns=['volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'], inplace=True
    )
    df_binance['Datetime'] = pd.to_datetime(df_binance['Datetime'], unit='ms')
    df_binance['Open'] = pd.to_numeric(df_binance['Open'])
    df_binance['High'] = pd.to_numeric(df_binance['High'])
    df_binance['Low'] = pd.to_numeric(df_binance['Low'])
    df_binance['Close'] = pd.to_numeric(df_binance['Close'])

    return df_binance



def save_data_csv(df, file_name='RESULT_MSBOB.csv'):
    df.to_csv(file_name, index=False)



# df = read_data_csv('BTCUSDT.csv')             # Завантаження даних з локального файлу.

# df = import_binance('BTCUSDT', '1h', 1000)      # Тікер, ТФ, кількість барів
# df_deal = create_df_deal()                      # Створення датафрейму угод
# run_strategy()                                  # Виконання стратегії
# print(df_deal)                                  # Друк угод в консоль (можна вимкнути)
# save_data_csv(df_deal, name_file_csv)           # Збереження угод в файл .csv (RESULT_BTCUSDT_1h_1000.csv)


def get_data_one_ticker(ticker, tf, day_back):

    exchange_df = ExchangeData(
        api_key='binance_api',
        api_secret='binance_api',
        symbol=ticker,
        interval=tf,
        start_date=date.today() - timedelta(days=day_back),
        end_date=date.today()
    )

    df_get = exchange_df.df

    return df_get


for ticker in tickers:
    for tf in timeframes:
        df = get_data_one_ticker(ticker=ticker, tf=tf, day_back=day_back )
        filename = f'data_1/{ticker}_data_{tf}.csv'

        save_data_csv(df, filename)  # Збереження даних в файл .csv (BTCUSDT_1h.csv)

        df = df.drop(df.index)
        df = df.drop(df.columns, axis=1)


# df = read_data_csv('data\BTCUSDT_data_4h.csv')
# print(df)



