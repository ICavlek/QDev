from resources.StockDataHandler import StockDataHandler
from resources.MathHandler import MathHandler
from resources.DataPlotter import DataPlotter


class PortfolioHandler:
    def __init__(self, stocks, start_date, end_date, portfolio_weights):
        self._stock_data_handler = StockDataHandler(stocks, start_date, end_date)
        self._log_daily_returns = None
        self._portfolio_weights = portfolio_weights
        self._portfolio_means = list()
        self._portfolio_risks = list()

    @property
    def log_daily_returns(self):
        return self._log_daily_returns

    @property
    def mu(self):
        return MathHandler.portfolio_return(
            self._log_daily_returns, self._portfolio_weights
        )

    @property
    def sigma(self):
        return MathHandler.portfolio_risks(
            self._log_daily_returns, self._portfolio_weights
        )

    @property
    def current_portfolio_price(self):
        return self._stock_data_handler.get_last_price_value()

    def initialize_portfolio(self):
        self._stock_data_handler.initialize_data()
        self._log_daily_returns = MathHandler.calculate_log_daily_return(self._stock_data_handler.stock_data)
        self._portfolio_means.append(
            MathHandler.portfolio_return(
                self._log_daily_returns, self._portfolio_weights
            )
        )
        self._portfolio_risks.append(
            MathHandler.portfolio_risks(
                self._log_daily_returns, self._portfolio_weights
            )
        )

    def print_kpis(self):
        #print(self._log_daily_returns)
        #print(MathHandler.annual_expected_return(self._log_daily_returns))
        #print(MathHandler.annual_covariance(self._log_daily_returns))
        print("Average portfolio return: ", self.mu)
        print("Average portfolio risk: ", self.sigma)

    def show_stocks(self):
        DataPlotter.show_data(self._stock_data_handler.stock_data)