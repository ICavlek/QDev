from resources.StockMonteCarlo import StockMonteCarlo


def test_1():
    stock_monte_carlo = StockMonteCarlo(50, 0.0002, 0.01)
    stock_monte_carlo.simulate_random_walk()
    stock_monte_carlo.plot_all_values()
    #stock_monte_carlo.plot_mean_value()


if __name__ == '__main__':
    test_1()
