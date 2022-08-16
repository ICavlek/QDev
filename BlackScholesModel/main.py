from resources.BlackScholesModels import BlackScholesAnalytical, BlackScholesMonteCarlo
from resources.PortfolioHandler import PortfolioHandler


def test_1():
	S0 = 100  # underlying stock price at t=0
	E = 100  # strike price
	T = 1  # expiry
	rf = 0.05  # risk-free rate
	sigma = 0.2  # volatility of the underlying stock
	iterations = 1000000  # number of iterations in the Monte-Carlo simulation

	model = BlackScholesAnalytical(S0, E, T, rf, sigma)
	model.calculate_d1_d2()
	model.print_option_price_values()

	model = BlackScholesMonteCarlo(S0, E, T, rf, sigma, iterations)
	model.calculate_stock_prices_monte_carlo()
	model.print_option_price_values()


def test_2():
	stocks = ['AAPL']
	start_date = '2017-01-01'
	end_date = '2022-01-01'
	weights = [1]

	portfolio_handler = PortfolioHandler(stocks, start_date, end_date, weights)
	portfolio_handler.initialize_portfolio()

	S0 = portfolio_handler.current_portfolio_price[0]
	E = S0
	T = 20/252 # 1 month
	rf = 0.05
	sigma = portfolio_handler.sigma
	iterations = 1000000

	model = BlackScholesAnalytical(S0, E, T, rf, sigma)
	model.calculate_d1_d2()
	model.print_option_price_values()

	model = BlackScholesMonteCarlo(S0, E, T, rf, sigma, iterations)
	model.calculate_stock_prices_monte_carlo()
	model.print_option_price_values()


if __name__ == "__main__":
	#test_1()
	test_2()
