import matplotlib.pyplot as plt
import numpy as np


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
    def show_portfolios_scatter_with_sharpe_ratio(opt, rets, portfolio_rets, portfolio_vols, val1, val2):
        plt.figure(figsize=(10, 6))
        plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.plot(
            val1,
            val2,
            'g*',
            markersize=20
        )
        plt.show()