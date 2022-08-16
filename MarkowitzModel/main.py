import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization


class StockDataHandler:
    def __init__(self, stocks, start_date, end_date, open_or_close='Adj Close'):
        self._stocks = stocks
        self._start_date = start_date
        self._end_date = end_date
        self._open_or_close = open_or_close
        self._stock_data = dict()

    def initialize_data(self):
        self._download_data()

    def _download_data(self):
        for stock in self._stocks:
            ticker = yf.download(stock, self._start_date, self._end_date)
            self._stock_data[stock] = ticker[self._open_or_close]
        self._stock_data = pd.DataFrame(self._stock_data)

    @property
    def stock_data(self):
        return self._stock_data

    @property
    def stocks(self):
        return self._stocks


class MathHandler:
    NUM_TRADING_DAYS = 252

    @staticmethod
    def calculate_log_daily_return(data):
        # Log used because of normalization to measure all variables in comparable metric
        # [1:] exclude Nan
        return np.log(data/data.shift(1))[1:]

    @staticmethod
    def get_random_weight(length):
        w = np.random.random(length)
        w /= np.sum(w)
        return w

    @staticmethod
    def annual_expected_return(log_daily_return):
        return log_daily_return * MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def annual_covariance(log_daily_return):
        # if covariance(i,j) > 0 asset returns move together
        # if covariance(i,j) < 0 asset returns move inversely
        # covariance(i,i) = variance(i)
        # high positive covariance does not provide much diversification
        return log_daily_return.cov() * MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def portfolio_return(log_daily_return, weights):
        return np.sum(log_daily_return.mean()*weights)*MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def portfolio_risks(log_daily_return, weights):
        # expected portfolio variance
        # portfolio volatility
        #sigma = sqrt(w^T*sigma_covariance_matrix*w)
        return np.sqrt(
            np.dot(
                np.transpose(
                    weights
                ),
                np.dot(
                    log_daily_return.cov()*MathHandler.NUM_TRADING_DAYS, weights
                )
            )
        )


class DataPlotter:

    @staticmethod
    def show_data(data, xlabel=10, ylabel=5):
        data.plot(figsize=(xlabel, ylabel))
        plt.show()

    @staticmethod
    def show_portfolios_scatter(returns, volatilities, xlabel=10, ylabel=6):
        returns = np.array(returns)
        volatilities = np.array(volatilities)
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilities, returns, c=returns/volatilities, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.show()

    @staticmethod
    def show_portfolios_scatter_with_sharpe_ratio(opt, rets, portfolio_rets, portfolio_vols):
        plt.figure(figsize=(10, 6))
        plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.plot(
            SharpeRatioOptimizator.statistics(opt['x'], rets)[1],
            SharpeRatioOptimizator.statistics(opt['x'], rets)[0],
            'g*',
            markersize=20
        )
        plt.show()


class SharpeRatioOptimizator:

    def __init__(self, log_daily_returns, stocks, num_of_generated_portfolios=10000):
        self._log_daily_returns = log_daily_returns
        self._stocks = stocks
        self._num_of_stocks = len(stocks)
        self._num_of_generated_portfolios = num_of_generated_portfolios
        self._portfolio_weights = list()
        self._portfolio_means = list()
        self._portfolio_risks = list()

    def generate_portfolios(self):
        for i in range(self._num_of_generated_portfolios):
            weight = MathHandler.get_random_weight(self._num_of_stocks)
            self._portfolio_weights.append(weight)
            self._portfolio_means.append(
                MathHandler.portfolio_return(
                    self._log_daily_returns, weight
                )
            )
            self._portfolio_risks.append(
                MathHandler.portfolio_risks(
                    self._log_daily_returns, weight
                )
            )
        self._transform_to_np_arrrays()

    def show_portfolios(self):
        DataPlotter.show_portfolios_scatter(self._portfolio_means, self._portfolio_risks)

    def show_portfolios_with_sharpe_ratio(self):
        optimum = SharpeRatioOptimizator.optimize_portfolio(
            self._portfolio_weights, self._log_daily_returns, self._num_of_stocks
        )
        self._print_optimum_portfolio(optimum)
        DataPlotter.show_portfolios_scatter_with_sharpe_ratio(
            optimum, self._log_daily_returns, self._portfolio_means, self._portfolio_risks
        )

    def _transform_to_np_arrrays(self):
        self._portfolio_weights = np.array(self._portfolio_weights)
        self._portfolio_risks = np.array(self._portfolio_risks)
        self._portfolio_means = np.array(self._portfolio_means)

    def _print_optimum_portfolio(self, optimum):
        print("Stocks: ", self._stocks)
        print("Optimal porfolio: ", optimum['x'].round(3))
        print(
            "Expected return, volatility and Sharpe ratio: ",
            SharpeRatioOptimizator.statistics(optimum['x'].round(3), self._log_daily_returns)
        )

    @staticmethod
    def statistics(weights, returns):
        portfolio_return = MathHandler.portfolio_return(returns, weights)
        portfolio_volatility = MathHandler.portfolio_risks(returns, weights)
        return np.array([
            portfolio_return, portfolio_volatility, portfolio_return / portfolio_volatility
        ])

    @staticmethod
    def min_function_sharpe(weights, returns):
        return -SharpeRatioOptimizator.statistics(weights, returns)[2]

    @staticmethod
    def optimize_portfolio(weights, returns, num_of_stocks):
        # constraint of lambda is that the sum of weights - 1 = 0
        constraints = {
            'type': 'eq', 'fun': lambda x: np.sum(x) - 1
        }
        bounds = tuple(
            (0, 1) for i in range(num_of_stocks)
        )
        return optimization.minimize(
            fun=SharpeRatioOptimizator.min_function_sharpe, x0=weights[0], args=returns,
            method='SLSQP', bounds=bounds, constraints=constraints
        )


class PortfolioHandler:
    def __init__(self, stocks, start_date, end_date, portfolio_weights):
        self._stock_data_handler = StockDataHandler(stocks, start_date, end_date)
        self._log_daily_returns = None
        self._portfolio_weights = portfolio_weights
        self._portfolio_means = list()
        self._portfolio_risks = list()

    @property
    def log_daily_returns(self):
        return self._log_daily_returns

    def initialize_portfolio(self):
        self._stock_data_handler.initialize_data()
        self._log_daily_returns = MathHandler.calculate_log_daily_return(self._stock_data_handler.stock_data)
        self._portfolio_means.append(
            MathHandler.portfolio_return(
                self._log_daily_returns, self._portfolio_weights
            )
        )
        self._portfolio_risks.append(
            MathHandler.portfolio_risks(
                self._log_daily_returns, self._portfolio_weights
            )
        )

    def print_kpis(self):
        #print(self._log_daily_returns)
        #print(MathHandler.annual_expected_return(self._log_daily_returns))
        #print(MathHandler.annual_covariance(self._log_daily_returns))
        print("Average portfolio return: ", MathHandler.portfolio_return(self._log_daily_returns, weights))
        print("Average portfolio risk: ", MathHandler.portfolio_risks(self._log_daily_returns, weights))

    def show_stocks(self):
        DataPlotter.show_data(self._stock_data_handler.stock_data)


def test_1(stocks, start_date, end_date, weights):
    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()
    portfolio_handler.print_kpis()
    portfolio_handler.show_stocks()


def test_2(stocks, start_date, end_date, weights):
    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()

    sharpe_ratio_optimizator = SharpeRatioOptimizator(portfolio_handler.log_daily_returns, stocks)
    sharpe_ratio_optimizator.generate_portfolios()
    sharpe_ratio_optimizator.show_portfolios_with_sharpe_ratio()

if __name__ == '__main__':
    stocks = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
    start_date = '2012-01-01'
    end_date = '2017-01-01'
    weights = [0.2, 0.05, 0.25, 0.15, 0.3, 0.05]
    #test_1(stocks, start_date, end_date, weights)
    test_2(stocks, start_date, end_date, weights)
