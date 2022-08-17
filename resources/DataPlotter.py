import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class DataPlotter:

    @staticmethod
    def show_data(data, xlabel=10, ylabel=5):
        data.plot(figsize=(xlabel, ylabel))
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

    @staticmethod
    def plot_capm_regression(m_returns, s_returns, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(m_returns, s_returns, label="Data points")
        axis.plot(m_returns, beta * m_returns + alpha, color='red', label='CAPM line')
        plt.title('CAPM, finding alpha and beta')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_stock_return_compared_to_normal_distribution(stock_data, stock_mean, stock_sigma):
        plt.hist(stock_data, bins=700)
        x = np.linspace(stock_mean - 3 * stock_sigma, stock_mean + 3 * stock_sigma, 100)
        plt.plot(x, norm.pdf(x, stock_mean, stock_sigma))
        plt.show()
