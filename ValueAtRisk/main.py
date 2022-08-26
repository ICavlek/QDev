import numpy as np
from scipy.stats import norm
import pandas as pd

from resources.StockDataHandler import StockDataHandler
from resources.MathHandler import MathHandler


class ValueAtRisk:
    def __init__(self, stocks, start_date, end_date):
        self._stock_data_handler = StockDataHandler(stocks, start_date, end_date)
        self._log_daily_return = None

    def initialize(self):
        self._stock_data_handler.initialize_data()
        self._log_daily_return = MathHandler.calculate_log_daily_return(self._stock_data_handler.stock_data)

    @property
    def log_daily_return(self):
        return self._log_daily_return

    @staticmethod
    def calculate_var(position, c, mu, sigma, n):
        # This is how we calculcate var tomorrow (n = 1)
        # VaR = DeltaS * (mu*delta*t - sigma*sqrt(delta*t)*alpha*(1-c)) -> multiple days
        # VaR = position * (mu - sigma*z) -> tomorrow
        # z = alpha
        var = position * (mu*n - sigma*np.sqrt(n)*norm.ppf(1 - c))
        return var


def test_1():
    stocks = ['C']
    start_date = '2014-01-01'
    end_date = '2018-01-01'
    value_at_risk = ValueAtRisk(stocks, start_date, end_date)
    value_at_risk.initialize()

    S = 1e6 # Investment, 1 million $
    c = 0.95 # confidence level 95 %
    # we assume that daily returns are normally distributed

    mu = np.mean(value_at_risk.log_daily_return)
    sigma = np.std(value_at_risk.log_daily_return)

    print("Value at risk is: $", value_at_risk.calculate_var(S, c, mu[0], sigma[0], 1))


if __name__ == '__main__':
    test_1()
