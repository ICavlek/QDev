from MarkowitzModel.src.PortfolioHandler import PortfolioHandler
from MarkowitzModel.src.SharpeRatioOptimizator import SharpeRatioOptimizator


def test_1(stocks, start_date, end_date, weights):
    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()
    portfolio_handler.print_kpis()
    portfolio_handler.show_stocks()


def test_2(stocks, start_date, end_date, weights):
    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()

    sharpe_ratio_optimizator = SharpeRatioOptimizator(portfolio_handler.log_daily_returns, stocks)
    sharpe_ratio_optimizator.calculate_optimal_portfolio()
    sharpe_ratio_optimizator.print_kpis()
    sharpe_ratio_optimizator.show_portfolios_with_sharpe_ratio()


if __name__ == '__main__':
    stocks = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
    start_date = '2017-01-01'
    end_date = '2021-01-01'
    weights = [0.2, 0.05, 0.25, 0.15, 0.3, 0.05]
    #test_1(stocks, start_date, end_date, weights)
    test_2(stocks, start_date, end_date, weights)
