import numpy as np
from scipy import stats

class BlackScholesBase:
	def __init__(self, S0, E, T, rf, sigma):
		self._S0 = S0
		self._E = E
		self._T = T
		self._rf = rf
		self._sigma = sigma


class BlackScholesAnalytical(BlackScholesBase):
	def __init__(self, S0, E, T, rf, sigma):
		super().__init__(S0, E, T, rf, sigma)
		self._d1 = None
		self._d2 = None

	def calculate_d1_d2(self):
		# calculate d1 and d2 parameters
		self._d1 = \
			(np.log(self._S0 / self._E) +
			 (self._rf + self._sigma * self._sigma / 2.0) * self._T) / (self._sigma * np.sqrt(self._T))
		self._d2 = self._d1 - self._sigma * np.sqrt(self._T)

	def print_option_price_values(self):
		print("Call option price with analytical approach: ", self.call_option_price())
		print("Put option price with analytical approach: ", self.put_option_price())

	def call_option_price(self):
		# use the N(x) to calculate the price of the option
		return self._S0 * stats.norm.cdf(self._d1) - self._E * np.exp(-self._rf * self._T) * stats.norm.cdf(self._d2)

	def put_option_price(self):
		# use the N(x) to calculate the price of the option
		return -self._S0 * stats.norm.cdf(-self._d1) + self._E * np.exp(-self._rf * self._T) * stats.norm.cdf(-self._d2)


class BlackScholesMonteCarlo(BlackScholesBase):
	def __init__(self, S0, E, T, rf, sigma, iterations):
		super().__init__(S0, E, T, rf, sigma)
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

	def print_option_price_values(self):
		print("Call option price with Monte-Carlo approach: ", self.calculate_option('call'))
		print("Put option price with Monte-Carlo approach: ", self.calculate_option('put'))

	def _option_value(self, option_type='call'):
		# we have 2 columns: first with 0s the second column will store the payoff
		# we need the first column of 0s: payoff function is max(0,S-E) for call option
		option_data = np.zeros([self._iterations, 2])

		# we need S-E because we have to calculate the max(S-E,0)
		option_data[:,1] = self._stock_price - self._E

		if option_type == 'put':
			# we need E-S because we have to calculate the max(E-S,0)
			option_data[:, 1] = self._E - self._stock_price

		return option_data
