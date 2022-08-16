import yfinance as yf
import pandas as pd


class StockDataHandler:
    def __init__(self, stocks, start_date, end_date, open_or_close='Adj Close'):
        self._stocks = stocks
        self._start_date = start_date
        self._end_date = end_date
        self._open_or_close = open_or_close
        self._stock_data = pd.DataFrame()

    def initialize_data(self):
        self._download_data()

    def _download_data(self):
        stock_data = dict()
        for stock in self._stocks:
            ticker = yf.download(stock, self._start_date, self._end_date)
            stock_data[stock] = ticker[self._open_or_close]
        self._stock_data = pd.DataFrame(stock_data)

    @property
    def stock_data(self):
        return self._stock_data

    @property
    def stocks(self):
        return self._stocks

    def get_last_price_value(self):
        return self._stock_data.iloc[-1]
