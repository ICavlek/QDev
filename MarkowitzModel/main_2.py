from resources.PortfolioHandler import PortfolioHandler
from resources.SharpeRatioOptimizer import SharpeRatioOptimizer


def portfolio_example():
    stocks = ['AAPL', 'NFLX', 'TSLA', 'AMZN', 'GOOG', 'WMT']
    weights = [0.15, 0.2, 0.15, 0.2, 0.15, 0.15]
    start_date = '2013-01-01'
    end_date = '2022-01-01'

    portfolio_handler = PortfolioHandler(
        stocks, start_date, end_date, weights
    )
    portfolio_handler.initialize_portfolio()
    portfolio_handler.print_kpis()
    portfolio_handler.show_stocks()

    sharpe_ratio_optimizer = SharpeRatioOptimizer(
        portfolio_handler.daily_returns, stocks, 10000
    )
    sharpe_ratio_optimizer.calculate_optimal_portfolio()
    sharpe_ratio_optimizer.print_kpis()
    sharpe_ratio_optimizer.show_portfolios_with_sharpe_ratio()


if __name__ == '__main__':
    portfolio_example()