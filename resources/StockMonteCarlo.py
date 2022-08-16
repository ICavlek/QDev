import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class StockMonteCarlo:
    def __init__(self, S0, mu, sigma, N=252, NUM_OF_SIMULATIONS=1000):
        self._S0 = S0
        self._mu = mu
        self._sigma = sigma
        self._N = N
        self._NUM_OF_SIMULATIONS = NUM_OF_SIMULATIONS
        self._simulation_data= pd.DataFrame()

    def simulate_random_walk(self):
        result = list()
        # number of simulations - possible S(t) realizations of the process
        for i in range(self._NUM_OF_SIMULATIONS):
            prices = [self._S0]
            for j in range(self._N):
                # we simulate the change day by day (t=1)
                stock_price = \
                    prices[-1] * np.exp(
                        (self._mu - 0.5 * self._sigma ** 2) + self._sigma * np.random.normal()
                    )
                prices.append(stock_price)
            result.append(prices)
        self._simulation_data = pd.DataFrame(result)
        self._simulation_data = self._simulation_data.T

    def plot_all_values(self):
        plt.plot(self._simulation_data)
        plt.show()

    def plot_mean_value(self):
        plt.plot(self._simulation_data.mean(axis=1))
        plt.show()