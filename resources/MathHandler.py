import numpy as np


class MathHandler:
    NUM_TRADING_DAYS = 252

    @staticmethod
    def calculate_log_daily_return(data):
        # Log used because of normalization to measure all variables in comparable metric
        # [1:] exclude Nan
        return np.log(data/data.shift(1))[1:]

    @staticmethod
    def get_random_weight(length):
        w = np.random.random(length)
        w /= np.sum(w)
        return w

    @staticmethod
    def annual_expected_return(log_daily_return):
        return log_daily_return * MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def annual_covariance(log_daily_return):
        # if covariance(i,j) > 0 asset returns move together
        # if covariance(i,j) < 0 asset returns move inversely
        # covariance(i,i) = variance(i)
        # high positive covariance does not provide much diversification
        return log_daily_return.cov() * MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def portfolio_return(log_daily_return, weights):
        return np.sum(log_daily_return.mean()*weights)*MathHandler.NUM_TRADING_DAYS

    @staticmethod
    def portfolio_risks(log_daily_return, weights):
        # expected portfolio variance
        # portfolio volatility
        #sigma = sqrt(w^T*sigma_covariance_matrix*w)
        return np.sqrt(
            np.dot(
                np.transpose(
                    weights
                ),
                np.dot(
                    log_daily_return.cov()*MathHandler.NUM_TRADING_DAYS, weights
                )
            )
        )