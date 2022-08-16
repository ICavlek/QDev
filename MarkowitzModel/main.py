import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization


class StockDataHandler:
    def __init__(self, stocks, start_date, end_date, open_or_close='Close'):
        self._stocks = stocks
        self._start_date = start_date
        self._end_date = end_date
        self._open_or_close = open_or_close
        self._stock_data = dict()

    def download_data(self):
        for stock in self._stocks:
            ticker = yf.Ticker(stock)
            self._stock_data[stock] = \
                ticker.history(start=start_date, end=end_date)[self._open_or_close]
        self._stock_data = pd.DataFrame(self._stock_data)

    @property
    def stock_data(self):
        return self._stock_data

    @property
    def stocks(self):
        return self._stocks


class MathHandler:
    NUM_TRADING_DAYS = 252

    def __init__(self, data):
        self._log_daily_return = MathHandler.calculate_return(data)

    @staticmethod
    def calculate_return(data):
        # Log used because of normalization to measure all variables in comparable metric
        # [1:] exclude Nan
        return np.log(data/data.shift(1))[1:]

    @staticmethod
    def get_random_weight(length):
        w = np.random.random(length)
        w /= np.sum(w)
        return w

    @property
    def log_daily_return(self):
        return self._log_daily_return

    def annual_expected_return(self):
        return self._log_daily_return.mean() * MathHandler.NUM_TRADING_DAYS

    def annual_covariance(self):
        # if covariance(i,j) > 0 asset returns move together
        # if covariance(i,j) < 0 asset returns move inversely
        # covariance(i,i) = variance(i)
        # high positive covariance does not provide much diversification
        return self._log_daily_return.cov() * MathHandler.NUM_TRADING_DAYS

    def portfolio_return(self, weights):
        return np.sum(self._log_daily_return.mean()*weights)*MathHandler.NUM_TRADING_DAYS

    def portfolio_risks(self, weights):
        # expected portfolio variance
        # portfolio volatility
        #sigma = sqrt(w^T*sigma_covariance_matrix*w)
        return np.sqrt(
            np.dot(
                np.transpose(
                    weights
                ),
                np.dot(
                    self._log_daily_return.cov()*MathHandler.NUM_TRADING_DAYS, weights
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

    @staticmethod
    # C/P From Math Handler because optimization procedure is being done here
    # Needs refactoring
    def statistics(weights, returns):
        portfolio_return = np.sum(returns.mean() * weights) * MathHandler.NUM_TRADING_DAYS
        portfolio_volatility = np.sqrt(
            np.dot(
                np.transpose(
                    weights
                ),
                np.dot(
                    returns.cov() * MathHandler.NUM_TRADING_DAYS, weights
                )
            )
        )
        return np.array([
            portfolio_return, portfolio_volatility, portfolio_return / portfolio_volatility
        ])

    # scipy optimize module can find the minimum of a given function
    # therefore, we are returning minimum of -f(x) because it is the same as max of f(x)
    @staticmethod
    def min_function_sharpe(weights, returns):
        return -SharpeRatioOptimizator.statistics(weights, returns)[2]

    # constraint of lambda is that the sum of weights - 1 = 0
    @staticmethod
    def optimize_portfolio(weights, returns, num_of_stocks):
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
    def __init__(self, stocks, start_date, end_date, num_of_portfolios):
        self._stock_data_handler = StockDataHandler(stocks, start_date, end_date)
        self._stock_data_handler.download_data()
        self._math_handler = MathHandler(self._stock_data_handler.stock_data)
        self._num_of_stocks = len(stocks)
        self._num_of_portfolios = num_of_portfolios
        self._portfolio_means = list()
        self._portfolio_risks = list()
        self._portfolio_weights = list()

    def generate_portfolios(self):
        for i in range(self._num_of_portfolios):
            weight = self._math_handler.get_random_weight(self._num_of_stocks)
            self._portfolio_weights.append(weight)
            self._portfolio_means.append(self._math_handler.portfolio_return(weight))
            self._portfolio_risks.append(self._math_handler.portfolio_risks(weight))
        self._transform_to_np_arrrays()

    def show_portfolios(self):
        DataPlotter.show_portfolios_scatter(self._portfolio_means, self._portfolio_risks)

    def show_portfolios_with_sharpe_ratio(self):
        optimum = SharpeRatioOptimizator.optimize_portfolio(
            self._portfolio_weights, self._math_handler.log_daily_return, self._num_of_stocks
        )
        self._print_optimum_portfolio(optimum)
        DataPlotter.show_portfolios_scatter_with_sharpe_ratio(
            optimum, self._math_handler.log_daily_return, self._portfolio_means, self._portfolio_risks
        )

    def _transform_to_np_arrrays(self):
        self._portfolio_means = np.array(self._portfolio_means)
        self._portfolio_risks = np.array(self._portfolio_risks)
        self._portfolio_weights = np.array(self._portfolio_weights)

    def _print_optimum_portfolio(self, optimum):
        print("Stocks: ", self._stock_data_handler.stocks)
        print("Optimal porfolio: ", optimum['x'].round(3))
        print(
            "Expected return, volatility and Sharpe ratio: ",
            SharpeRatioOptimizator.statistics(optimum['x'].round(3), self._math_handler.log_daily_return)
        )


def test_1(stocks, start_date, end_date):
    weights = [0.2, 0.05, 0.25, 0.15, 0.3, 0.05]

    stock_data_handler = StockDataHandler(stocks, start_date, end_date)
    stock_data_handler.download_data()

    math_handler = MathHandler(stock_data_handler.stock_data)
    print(math_handler.log_daily_return)
    print(math_handler.annual_expected_return())
    print(math_handler.annual_covariance())
    print(math_handler.portfolio_return(weights))
    print(math_handler.portfolio_risks(weights))

    #DataPlotter.show_data(stock_data_handler.stock_data)

def test_2(stocks, start_date, end_date):
    NUM_OF_PORTFOLIOS = 10000
    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, NUM_OF_PORTFOLIOS)
    portfolio_handler.generate_portfolios()
    portfolio_handler.show_portfolios()
    portfolio_handler.show_portfolios_with_sharpe_ratio()

if __name__ == '__main__':
    stocks = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
    start_date = '2012-01-01'
    end_date = '2017-01-01'
    test_1(stocks, start_date, end_date)
    #test_2(stocks, start_date, end_date)
