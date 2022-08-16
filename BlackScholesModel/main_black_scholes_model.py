from scipy import stats
from numpy import log, exp, sqrt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def call_option_price(S, E, T, rf, sigma):
    #calculate d1 and d2 parameters
    d1 = (log(S/E) + (rf + sigma*sigma/2.0)*T) / (sigma * sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    print(d1)
    print(d2)
    #use the N(x) to calculate the price of the option
    return S*stats.norm.cdf(d1) - E*exp(-rf*T)*stats.norm.cdf(d2)


def put_option_price(S, E, T, rf, sigma):
    #calculate d1 and d2 parameters
    d1 = (log(S/E) + (rf + sigma*sigma/2.0)*T) / (sigma * sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    print(d1)
    print(d2)
    #use the N(x) to calculate the price of the option
    return -S*stats.norm.cdf(-d1) + E*exp(-rf*T)*stats.norm.cdf(-d2)

def test_1():
    # underlying stock price at t=0
    S0 = 100
    # strike price
    E = 100
    # expiry 1 year = 365 days
    T = 1
    # risk free rate
    rf = 0.05
    # volatility of the underlying stock
    sigma = 0.2
    print(
        "Call option price according to Black-Scholes model: ",
        call_option_price(S0, E, T, rf, sigma)
    )

    print(
        "Put option price according to Black-Scholes model: ",
        put_option_price(S0, E, T, rf, sigma)
    )

NUM_OF_SIMULATIONS = 1000
def stock_monte_carlo(S0, mu, sigma, N=252): #252 average trading days
    result = []

    #number of simulations - possible S(t) realizations of the process

    for i in range(NUM_OF_SIMULATIONS):
        prices = [S0]
        for j in range(N):
            # we simulate the change day by day (t=1)
            stock_price = \
                prices[-1] * np.exp(
                    (mu - 0.5*sigma**2) + sigma*np.random.normal()
                )
            prices.append(stock_price)
        result.append(prices)

    simulation_data = pd.DataFrame(result)
    simulation_data = simulation_data.T
    #plt.plot(simulation_data)
    #plt.show()
    simulation_data['mean'] = simulation_data.mean(axis=1)
    print(simulation_data)
    plt.plot(simulation_data['mean'])
    plt.show()

def test_2():
    stock_monte_carlo(50, 0.0002, 0.01)

if __name__ == '__main__':
    #test_1()
    test_2()
