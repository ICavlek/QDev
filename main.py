from resources.PortfolioHandler import PortfolioHandler
from resources.SharpeRatioOptimizer import SharpeRatioOptimizer
from resources.BlackScholesModels import BlackScholesAnalytical, BlackScholesMonteCarlo


def example_portfolio():
    stocks = ['AAPL', 'NFLX', 'TSLA', 'AMZN', 'GOOG', 'WMT']
    weights = [0.15, 0.2, 0.15, 0.2, 0.15, 0.15]
    start_date = '2013-01-01'
    end_date = '2022-01-01'

    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()
    portfolio_handler.print_kpis()
    #portfolio_handler.show_stocks()

    sharpe_ratio_optimizer = SharpeRatioOptimizer(
        portfolio_handler.daily_returns, stocks, num_of_generated_portfolios=10000
    )
    sharpe_ratio_optimizer.calculate_optimal_portfolio()
    sharpe_ratio_optimizer.print_kpis()
    sharpe_ratio_optimizer.show_portfolios_with_sharpe_ratio()


def example_black_scholes():
    stocks = ['AAPL']
    start_date = '2017-01-01'
    end_date = '2022-01-01'
    weights = [1]

    portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
    portfolio_handler.initialize_portfolio()

    S0 = portfolio_handler.current_portfolio_price
    E = S0
    T = 20/252 # 1 month
    rf = 0.05
    sigma = portfolio_handler.sigma
    iterations = 1000000

    model_analytical = BlackScholesAnalytical(S0, E, T, rf, sigma)
    model_analytical.calculate_d1_d2()
    model_analytical.print_option_price_values()

    model_monte_carlo = BlackScholesMonteCarlo(S0, E, T, rf, sigma, iterations)
    model_monte_carlo.calculate_stock_prices()
    model_monte_carlo.print_option_price_values()


if __name__ == '__main__':
    #example_portfolio()
    example_black_scholes()
