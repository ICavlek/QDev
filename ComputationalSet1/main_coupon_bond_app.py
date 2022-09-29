from resources import fixedincome as fi
import matplotlib.pyplot as plt


class CouponBondAppBase:
    @classmethod
    def _print_header(cls):
        print("-----------------------------------------------------")

    @classmethod
    def _print_label(cls, label):
        print("**************   ", label, "   **************")

    @classmethod
    def _plot(cls, x_val, y_val, labels=None, xlabel=None, ylabel=None):
        fig, ax = plt.subplots()
        for i in range(0, len(x_val)):
            ax.plot(x_val[i], y_val[i], label=labels[i])
        ax.legend()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show(block=True)


class CouponBond(CouponBondAppBase):
    @classmethod
    def show_bond_payments(cls, bonds, labels, do_plot=True):
        cls._print_header()
        cls._print_bond_payments(bonds, labels)
        if do_plot:
            cls._plot_bond_payments(bonds)

    @classmethod
    def _print_bond_payments(cls, bonds, labels):
        for i in range(0, len(bonds)):
            cls._print_label(labels[i])
            print("Bond coupons:", bonds[i].get_coupons())

    @classmethod
    def _plot_bond_payments(cls, bonds):
        for bond in bonds:
            bond.plot_payments()


class CouponBondPriceCalculator(CouponBondAppBase):
    def __init__(self, yield_curves):
        self._yield_curves = yield_curves

    def create_yield_curves(self, tenors, rates):
        if len(tenors) != len(rates):
            raise Exception("Length of tenors and rates don't match")
        for i in range(0, len(tenors)):
            if len(tenors[i]) != len(rates[i]):
                raise Exception("Length of tenors and rates at index {index} don't match".format(index=i))
            self._yield_curves.append(fi.curve_factory(dates=tenors[i], rates=rates[i]))

    def show_bond_prices_based_on_yield_curves(self, bonds, labels, do_plot=True):
        self._print_header()
        bond_prices_all, rates_all = self._calculate_all_bond_prices_and_rates(bonds)
        self._print_bond_prices_based_on_yield_curves(bonds, bond_prices_all, labels)
        if do_plot:
            self._plot(rates_all, bond_prices_all, labels, xlabel="Rates/Yields", ylabel="Bond Prices")

    def _print_bond_prices_based_on_yield_curves(self, bonds, bond_prices_all, labels):
        for i in range(0, len(bonds)):
            self._print_label(labels[i])
            text = "Bond price for yield curve of rate {rate}%: {price}"
            for j in range(0, len(self._yield_curves)):
                yield_curve = self._yield_curves[j]
                rate_format = round(yield_curve.rates[0]*100, 1)
                if len(yield_curve.rates) > 1:
                    rate_format = "{index_0} - {index_len}".format(
                        index_0=round(yield_curve.rates[0]*100, 1),
                        index_len=round(yield_curve.rates[len(yield_curve.rates)-1]*100, 1)
                    )
                print(text.format(rate=rate_format, price=bond_prices_all[i][j]))

    def _calculate_all_bond_prices_and_rates(self, bonds):
        bond_prices_all = list()
        rates_all = list()
        for bond in bonds:
            bond_prices, rates = self._calculate_bond_prices_and_rates(bond)
            bond_prices_all.append(bond_prices)
            rates_all.append(rates)

        return bond_prices_all, rates_all

    def _calculate_bond_prices_and_rates(self, bond):
        bond_prices = list()
        rates = list()
        for yield_curve in self._yield_curves:
            bond_prices.append(bond.price(curve=yield_curve))
            rates.append(yield_curve.rates[0])

        return bond_prices, rates


class CouponBondYTMCalculator(CouponBondAppBase):
    def __init__(self, prices):
        self._prices = prices

    def add_prices(self, prices):
        for price in prices:
            self._prices.append(price)

    def show_yield_to_maturities_based_on_bond_prices(self, bonds, labels, do_plot=True):
        self._print_header()
        bond_prices_all, ytms_all = self._calculate_all_yield_to_maturities(bonds)
        self._print_yield_to_maturities_based_on_prices(bonds, ytms_all, labels)
        if do_plot:
            self._plot(bond_prices_all, ytms_all, labels, xlabel="Bond Prices", ylabel="Rates/Yields")

    def _print_yield_to_maturities_based_on_prices(self, bonds, ytms_all, labels):
        for i in range(0, len(bonds)):
            self._print_label(labels[i])
            text = "YTM based on price {price}:"
            for j in range(0, len(self._prices)):
                print(text.format(price=self._prices[j]), ytms_all[i][j])

    def _calculate_all_yield_to_maturities(self, bonds):
        bond_prices_all = list()
        ytms_all = list()
        for bond in bonds:
            bond_prices_all.append(self._prices)
            ytms = list()
            for price in self._prices:
                ytms.append(bond.YTM(price))
            ytms_all.append(ytms)
        return bond_prices_all, ytms_all


class CouponBondApp:
    def __init__(self, yield_curves=None, prices=None):
        if yield_curves is None:
            yield_curves = list()
        if prices is None:
            prices = list()
        self._coupon_bond_price_calculator = CouponBondPriceCalculator(yield_curves)
        self._coupon_bond_ytm_calculator = CouponBondYTMCalculator(prices)

    @classmethod
    def show_bond_payments(cls, bonds, labels):
        CouponBond.show_bond_payments(bonds, labels)

    @classmethod
    def create_coupon_bond(cls, years_to_maturity, face_value, coupon_rate_percent, annual_payment):
        return fi.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, annual_payment)

    def create_yield_curves(self, tenors, rates):
        self._coupon_bond_price_calculator.create_yield_curves(tenors, rates)

    def show_bond_prices_based_on_yield_curves(self, bonds, labels):
        self._coupon_bond_price_calculator.show_bond_prices_based_on_yield_curves(bonds, labels)

    def add_prices(self, prices):
        self._coupon_bond_ytm_calculator.add_prices(prices)

    def show_yield_to_maturities_based_on_bond_prices(self, bonds, labels):
        self._coupon_bond_ytm_calculator.show_yield_to_maturities_based_on_bond_prices(bonds, labels)


def example_calculate_zero_coupon_bond_price(coupon_bond_app):
    bonds = list()

    years_to_maturity = 5
    face_value = 10000
    coupon_rate_percent = 0
    no_annual_payment = 0
    bond = coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, no_annual_payment)
    bonds.append(bond)

    labels = ['Bond']
    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices(coupon_bond_app):
    bonds = list()

    years_to_maturity = 5
    face_value = 10000
    coupon_rate_percent = 6
    semiannual_payment = 2
    bond_1 = coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
    bonds.append(bond_1)

    years_to_maturity = 7
    face_value = 5000
    coupon_rate_percent = 4
    semiannual_payment = 2
    bond_2 = coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
    bonds.append(bond_2)

    labels = ['Bond1', 'Bond2']
    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app):
    bonds = list()

    years_to_maturities = [5, 6, 8, 10, 15, 20]
    face_value = 10000
    coupon_rate_percent = 6
    semiannual_payment = 2
    for years_to_maturity in years_to_maturities:
        bonds.append(
            coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
        )
    labels = ['5Y', '6Y', '8Y', '10Y', '15Y', '20Y']

    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app):
    bonds = list()

    years_to_maturity = 5
    face_value = 10000
    coupon_rates_percent = [6, 8, 10, 15, 20, 30]
    semiannual_payment = 2
    for coupon_rate_percent in coupon_rates_percent:
        bonds.append(
            coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
        )
    labels = ['6%', '8%', '10%', '15%', '20%', '30%']

    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_bond_yield_to_maturities_based_on_multiple_prices(coupon_bond_app):
    bonds = list()

    years_to_maturity = 5
    face_value = 10000
    coupon_rate_percent = 6
    semiannual_payment = 2
    bond = coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
    bonds.append(bond)

    labels = ["Bond"]
    coupon_bond_app.show_yield_to_maturities_based_on_bond_prices(bonds, labels)


def example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_maturities(coupon_bond_app):
    bonds = list()

    years_to_maturities = [5, 6, 8, 10, 15, 20]
    face_value = 10000
    coupon_rate_percent = 6
    semiannual_payment = 2
    for years_to_maturity in years_to_maturities:
        bonds.append(
            coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
        )
    labels = ['5Y', '6Y', '8Y', '10Y', '15Y', '20Y']

    coupon_bond_app.show_yield_to_maturities_based_on_bond_prices(bonds, labels)


def example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_rates(coupon_bond_app):
    bonds = list()

    years_to_maturity = 5
    face_value = 10000
    coupon_rates_percent = [6, 8, 10, 15, 20, 30]
    semiannual_payment = 2
    for coupon_rate_percent in coupon_rates_percent:
        bonds.append(
            coupon_bond_app.create_coupon_bond(years_to_maturity, face_value, coupon_rate_percent, semiannual_payment)
        )
    labels = ['6%', '8%', '10%', '15%', '20%', '30%']
    coupon_bond_app.show_yield_to_maturities_based_on_bond_prices(bonds, labels)


def example_coupon_bond_app_1():
    coupon_bond_app = CouponBondApp()
    example_calculate_zero_coupon_bond_price(coupon_bond_app)

    coupon_bond_app.create_yield_curves(
        tenors=[[30], [30], [30], [30], [30]],
        rates=[[5], [6], [7], [8], [9]]
    )
    example_calculate_multiple_bond_prices(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app)

    bond_prices = [8000, 9000, 10000, 11000, 12000]
    coupon_bond_app.add_prices(bond_prices)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices(coupon_bond_app)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_maturities(coupon_bond_app)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_rates(coupon_bond_app)


def example_coupon_bond_app_2():
    coupon_bond_app = CouponBondApp()
    example_calculate_zero_coupon_bond_price(coupon_bond_app)

    coupon_bond_app.create_yield_curves(
        tenors=[[1], [2, 3]],
        rates=[[5], [6, 7]]
    )
    example_calculate_multiple_bond_prices(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app)

    bond_prices = [8000, 9000, 10000, 11000, 12000]
    coupon_bond_app.add_prices(bond_prices)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices(coupon_bond_app)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_maturities(coupon_bond_app)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_rates(coupon_bond_app)


if __name__ == '__main__':
    example_coupon_bond_app_1()
    # example_coupon_bond_app_2()
