import numpy as np
import pandas as pd

from resources.StockDataHandler import StockDataHandler
from resources.DataPlotter import DataPlotter
from resources.MathHandler import MathHandler


class CAPM:
    def __init__(self, stocks, start_date, end_date, risk_free_rate=0.05):
        self._stock_data_handler = StockDataHandler(stocks, start_date, end_date)
        self._remodified_data = None
        self._risk_free_rate = risk_free_rate
        self._months_in_year = 12

    def initialize(self):
        self._stock_data_handler.initialize_data()
        self._reshape_data()

    def calculate_beta_analyticaly(self):
        # beta = systematic (market) risk, it can only be calculated, not removed
        # unsystematic risk is removed by diverzifying portfolio
        # beta = covariance_ibm_us500 / covariance_us500_us500 which is variance us500
        # beta = 1 stock moving exactly with the market
        # beta > 1 stock market risk is higher than that of an average stock
        # beta < 1 stock market risk is lower than that of an average stock
        # less risk -> less return
        covariance_matrix = np.cov(
            self._remodified_data['s_returns'], self._remodified_data['m_returns']
        )
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        return beta

    def caculate_alpha_beta_polyfit(self):
        # E[r_a] - r_f = alpha + beta*(E[r_m]- r_f)
        # Linear regression
        # [stock_returns, market_returns] - slope is the beta
        # polyfit - order of the polynom
        beta, alpha = np.polyfit(
            self._remodified_data['m_returns'], self._remodified_data['s_returns'], deg=1
        )
        return alpha, beta

    def calculate_expected_return(self, beta):
        expected_return = self._risk_free_rate + \
            beta * (self._remodified_data['m_returns'].mean() * self._months_in_year - self._risk_free_rate)
        return expected_return

    def plot_capm_regression(self, alpha, beta):
        DataPlotter.plot_capm_regression(
            self._remodified_data['m_returns'], self._remodified_data['s_returns'], alpha, beta
        )

    def compare_stock_return_to_normal_distribution(self):
        stock_data = self._stock_data_handler.stock_data
        # Assumption stock_data is in combo [stock, US500]
        log_daily_returns = MathHandler.calculate_log_daily_return(stock_data.iloc[:,0])
        stock_variance = log_daily_returns.var()
        stock_mean = log_daily_returns.mean()
        stock_sigma = np.sqrt(stock_variance)
        DataPlotter.plot_stock_return_compared_to_normal_distribution(log_daily_returns, stock_mean, stock_sigma)

    def _reshape_data(self):
        stock_data = self._stock_data_handler.stock_data
        stocks = self._stock_data_handler.stocks
        stock_data = stock_data.resample('M').last()
        # Name changes to stock_related_adjusted_closing_price = s_adjclose
        # and m_adjclose = market_adjusted_closing_price
        self._remodified_data = pd.DataFrame({
            's_adjclose': stock_data[stocks[0]], 'm_adjclose': stock_data[stocks[1]]
        })
        self._remodified_data[['s_returns', 'm_returns']] = np.log(
            self._remodified_data[['s_adjclose', 'm_adjclose']] / self._remodified_data[['s_adjclose', 'm_adjclose']].shift(1)
        )
        self._remodified_data = self._remodified_data[1:]