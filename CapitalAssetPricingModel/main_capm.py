import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class CAPM:
    RISK_FREE_RATE = 0.05
    MONTHS_IN_YEAR = 12

    def __init__(self, stocks, start_date, end_date):
        self._data = None
        self._stocks = stocks
        self._start_date = start_date
        self._end_date = end_date

    def download_data(self):
        data = {}

        for stock in self._stocks:
            ticker = yf.download(stock, self._start_date, self._end_date)
            data[stock] = ticker['Adj Close'] #includes dividends, stock splits -> more accurate then close

        return pd.DataFrame(data)

    def initialize(self):
        stock_data = self.download_data()
        #we use monthly returns instead of daily returns
        stock_data = stock_data.resample('M').last()
        #Name changes to stock_related_adjusted_closing_price = s_adjclose
        # and m_adjclose = market_adjusted_closing_price
        self._data = pd.DataFrame({
            's_adjclose':stock_data[self._stocks[0]], 'm_adjclose':stock_data[self._stocks[1]]
        })

        self._data[['s_returns', 'm_returns']] = np.log(
            self._data[['s_adjclose', 'm_adjclose']] / self._data[['s_adjclose', 'm_adjclose']].shift(1)
        )
        self._data = self._data[1:]
        print(self._data)

    def calculate_beta(self):
        covariance_matrix = np.cov(
            self._data['s_returns'], self._data['m_returns']
        )
        # beta = covariance_ibm_us500 / covariance_us500_us500 which is variance us500
        # beta = 1 stock moving exactly with the market
        # beta > 1 stock market risk is higher than that of an average stock
        # beta < 1 stock market risk is lower than that of an average stock
        # less risk -> less return
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print("Beta: ", beta)

    def regression(self):
        #E[r_a] - r_f = alpha + beta*(E[r_m]- r_f)
        # Linear regression
        # [stock_returns, market_returns] - slope is the beta
        # polyfit - order of the polynom
        beta, alpha = np.polyfit(
            self._data['m_returns'], self._data['s_returns'], deg=1
        )
        print("Beta: ", beta)
        #calculate the expected return according to the CAPM formula
        # we are after annual return (multiply by 12)
        expected_return = CAPM.RISK_FREE_RATE + \
                          beta * (
                                  self._data['m_returns'].mean()*CAPM.MONTHS_IN_YEAR - CAPM.RISK_FREE_RATE
                          )
        print("Expected return: ", expected_return)
        self.plot_regression(alpha, beta)

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(self._data['m_returns'], self._data['s_returns'], label="Data points")
        axis.plot(self._data['m_returns'], beta * self._data['m_returns'] + alpha, color='red', label='CAPM line')
        plt.title('CAPM, finding alpha and beta')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    stocks = ['IBM', '^GSPC'] #IBM and US500
    start_date = '2010-01-01'
    end_date = '2017-01-01'

    capm = CAPM(stocks, start_date, end_date)
    capm.initialize()
    capm.calculate_beta()
    capm.regression()


