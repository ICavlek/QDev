import numpy as np


class OptionPricing:
	def __init__(self, S0, E, T, rf, sigma, iterations):
		self._S0 = S0
		self._E = E
		self._T = T
		self._rf = rf
		self._sigma = sigma
		self._iterations = iterations
		self._stock_price = None

	def calculate_stock_prices_monte_carlo(self):
		# dimensions: 1 dimensional array with as many items as the itrations
		rand = np.random.normal(0, 1, [1, self._iterations])

		# equation for the S(t) stock price
		self._stock_price = self._S0 * np.exp(
			self._T * (self._rf - 0.5 * self._sigma ** 2) + self._sigma * np.sqrt(self._T) * rand
		)

	def calculate_option(self, option_type='call'):
		option_data = self._option_value(option_type)
		# average for the Monte-Carlo method
		# np.amax() returns the max(0,S-E) according to the formula
		average = np.sum(np.amax(option_data, axis=1)) / float(self._iterations)
		# have to use the exp(-rT) discount factor
		return np.exp(-1.0 * self._rf * self._T) * average

	def _option_value(self, option_type='call'):
		# we have 2 columns: first with 0s the second column will store the payoff
		# we need the first column of 0s: payoff function is max(0,S-E) for call option
		option_data = np.zeros([self._iterations, 2])

		#we need S-E because we have to calculate the max(S-E,0)
		option_data[:,1] = self._stock_price - self._E

		if option_type == 'put':
			# we need E-S because we have to calculate the max(E-S,0)
			option_data[:, 1] = self._E - self._stock_price

		return option_data


def test_1():
	S0 = 100  # underlying stock price at t=0
	E = 100  # strike price
	T = 1  # expiry
	rf = 0.05  # risk-free rate
	sigma = 0.2  # volatility of the underlying stock
	iterations = 1000000  # number of iterations in the Monte-Carlo simulation

	model = OptionPricing(S0, E, T, rf, sigma, iterations)
	model.calculate_stock_prices_monte_carlo()
	print("Call option price with Monte-Carlo approach: ", model.calculate_option('call'))
	print("Put option price with Monte-Carlo approach: ", model.calculate_option('put'))


if __name__ == "__main__":
	test_1()
