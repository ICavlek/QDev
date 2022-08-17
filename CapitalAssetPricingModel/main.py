from resources.CAPM import CAPM


def test_1(stock, start_date, end_date):
    stocks = [stock, '^GSPC']  # IBM and US500
    start_date = '2010-01-01'
    end_date = '2020-01-01'

    capm = CAPM(stocks, start_date, end_date)
    capm.initialize()
    beta_analytical = capm.calculate_beta_analyticaly()
    print("Beta analyticaly: ", beta_analytical)
    alpha_polyfit, beta_polyfit = capm.caculate_alpha_beta_polyfit()
    print("Beta polyfit: ", beta_polyfit)
    print("Expected return: ", capm.calculate_expected_return(beta_polyfit))
    capm.plot_capm_regression(alpha_polyfit, beta_polyfit)
    capm.compare_stock_return_to_normal_distribution()


if __name__ == '__main__':
    #test_1('IBM', '2010-01-01', '2020-01-01')
    test_1('AAPL', '2010-01-01', '2022-01-01')
