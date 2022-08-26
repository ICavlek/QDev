import numpy as np
import scipy.optimize as optimization

from resources.MathHandler import MathHandler
from resources.DataPlotter import DataPlotter


class SharpeRatioOptimizer:
    def __init__(self, log_daily_returns, stocks, num_of_generated_portfolios=10000):
        self._log_daily_returns = log_daily_returns
        self._stocks = stocks
        self._num_of_stocks = len(stocks)
        self._num_of_generated_portfolios = num_of_generated_portfolios
        self._portfolio_weights = list()
        self._portfolio_means = list()
        self._portfolio_risks = list()
        self._optimum = None

    def calculate_optimal_portfolio(self):
        self._generate_portfolios()
        self._optimum = SharpeRatioOptimizer.optimize_portfolio(
            self._portfolio_weights, self._log_daily_returns, self._num_of_stocks
        )

    def show_portfolios_with_sharpe_ratio(self):
        val1 = SharpeRatioOptimizer.statistics(self._optimum['x'], self._log_daily_returns)[1]
        val2 = SharpeRatioOptimizer.statistics(self._optimum['x'], self._log_daily_returns)[0]
        DataPlotter.show_portfolios_scatter_with_sharpe_ratio(
            self._optimum, self._log_daily_returns, self._portfolio_means, self._portfolio_risks, val1, val2
        )

    def print_kpis(self):
        print("Stocks: ", self._stocks)
        print("Optimal porfolio: ", self._optimum['x'].round(3))
        print(
            "Expected return, risk and Sharpe ratio: ",
            SharpeRatioOptimizer.statistics(
                self._optimum['x'].round(3), self._log_daily_returns
            )
        )

    def _generate_portfolios(self):
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

    def _transform_to_np_arrrays(self):
        self._portfolio_weights = np.array(self._portfolio_weights)
        self._portfolio_risks = np.array(self._portfolio_risks)
        self._portfolio_means = np.array(self._portfolio_means)

    @staticmethod
    def statistics(weights, returns):
        portfolio_return = MathHandler.portfolio_return(returns, weights)
        portfolio_volatility = MathHandler.portfolio_risks(returns, weights)
        return np.array([
            portfolio_return, portfolio_volatility, portfolio_return / portfolio_volatility
        ])

    @staticmethod
    def min_function_sharpe(weights, returns):
        return -SharpeRatioOptimizer.statistics(weights, returns)[2]

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
            fun=SharpeRatioOptimizer.min_function_sharpe, x0=weights[0], args=returns,
            method='SLSQP', bounds=bounds, constraints=constraints
        )