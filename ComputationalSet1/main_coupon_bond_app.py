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


class CouponBondApp(CouponBondAppBase):
    def __init__(self):
        self._yield_curves = list()

    def create_yield_curves(self, tenors, rates):
        if len(tenors) != len(rates):
            raise Exception("Length of tenors and rates don't match")
        for i in range(0, len(tenors)):
            if len(tenors[i]) != len(rates[i]):
                raise Exception("Length of tenors and rates at index {index} don't match".format(index=i))
            self._yield_curves.append(fi.curve_factory(dates=tenors[i], rates=rates[i]))

    @classmethod
    def show_bond_payments(cls, bonds, labels, do_plot=True):
        cls._print_header()
        cls._print_bond_payments(bonds, labels)
        if do_plot:
            cls._plot_bond_payments(bonds)

    def show_bond_prices_based_on_yield_curves(self, bonds, labels, do_plot=True):
        self._print_header()
        self._print_bond_prices_based_on_yield_curves(bonds, labels)
        if do_plot:
            bond_prices_all, rates_all = self._calculate_all_bond_prices_and_rates(bonds)
            self._plot(rates_all, bond_prices_all, labels, xlabel="Rates/Yields", ylabel="Bond Prices")

    def show_yield_to_maturities_based_on_bond_prices(self, bonds, prices, labels, do_plot=True):
        self._print_header()
        if do_plot:
            bond_prices_all, ytms_all = self._calculate_all_yield_to_maturities(bonds, prices)
            self._plot(bond_prices_all, ytms_all, labels, xlabel="Bond Prices", ylabel="Rates/Yields")

    @classmethod
    def _print_bond_payments(cls, bonds, labels):
        for i in range(0, len(bonds)):
            cls._print_label(labels[i])
            print("Bond coupons:", bonds[i].get_coupons())

    @classmethod
    def _plot_bond_payments(cls, bonds):
        for bond in bonds:
            bond.plot_payments()

    def _print_bond_prices_based_on_yield_curves(self, bonds, labels):
        for i in range(0, len(bonds)):
            self._print_label(labels[i])
            text = "Bond price for yield curve of rate {rate}%: {price}"
            for yield_curve in self._yield_curves:
                rate_format = round(yield_curve.rates[0]*100,1)
                if len(yield_curve.rates) > 1:
                    rate_format = "{index_0} - {index_len}".format(
                        index_0=round(yield_curve.rates[0]*100,1),
                        index_len=round(yield_curve.rates[len(yield_curve.rates)-1]*100,1)
                    )
                print(text.format(rate=rate_format, price=bonds[i].price(curve=yield_curve)))

    def _calculate_all_bond_prices_and_rates(self, bonds):
        bond_prices_all = list()
        rates_all = list()
        for bond in bonds:
            bond_prices, rates = self._calculate_bond_prices_and_rates(bond)
            bond_prices_all.append(bond_prices)
            rates_all.append(rates)

        return bond_prices_all, rates_all

    def _calculate_all_yield_to_maturities(self, bonds, prices):
        bond_prices_all = list()
        ytms_all = list()
        for bond in bonds:
            bond_prices_all.append(prices)
            ytms = list()
            for price in prices:
                ytms.append(bond.YTM(price))
            ytms_all.append(ytms)
        return bond_prices_all, ytms_all

    def _calculate_bond_prices_and_rates(self, bond):
        bond_prices = list()
        rates = list()
        for yield_curve in self._yield_curves:
            bond_prices.append(bond.price(curve=yield_curve))
            rates.append(yield_curve.rates[0])

        return bond_prices, rates


def example_calculate_zero_coupon_bond_price(coupon_bond_app):
    bonds = list()
    maturity = 5  # 5 years
    face_value = 10000  # $10000 face value
    rate = 0  # 6% coupon rate
    frequency = 0  # semiannual payment, if 0 -> zero coupon bond
    bond = fi.create_coupon_bond(maturity, face_value, rate, frequency)
    bonds.append(bond)

    labels = ['Bond']
    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices(coupon_bond_app):
    bonds = list()

    maturity = 5  # 5 years
    face_value = 10000  # $10000 face value
    rate = 6  # 6% coupon rate
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    bond_1 = fi.create_coupon_bond(maturity, face_value, rate, frequency)
    bonds.append(bond_1)

    maturity = 7  # 5 years
    face_value = 5000  # $10000 face value
    rate = 4  # 6% coupon rate
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    bond_2 = fi.create_coupon_bond(maturity, face_value, rate, frequency)
    bonds.append(bond_2)

    labels = ['Bond1', 'Bond2']
    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app):
    bonds = list()

    maturities = [5, 6, 8, 10, 15, 20]  # multiple years
    face_value = 10000  # $10000 face value
    rate = 6  # 6% coupon rate
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    for maturity in maturities:
        bonds.append(fi.create_coupon_bond(maturity, face_value, rate, frequency))
    labels = ['5Y', '6Y', '8Y', '10Y', '15Y', '20Y']

    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app):
    bonds = list()

    maturity = 5  # 5 years
    face_value = 10000  # $10000 face value
    rates = [6, 8, 10, 15, 20, 30]  # multiple rates
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    for rate in rates:
        bonds.append(fi.create_coupon_bond(maturity, face_value, rate, frequency))
    labels = ['6%', '8%', '10%', '15%', '20%', '30%']

    coupon_bond_app.show_bond_payments(bonds, labels)
    coupon_bond_app.show_bond_prices_based_on_yield_curves(bonds, labels)


def example_calculate_bond_yield_to_maturities_based_on_multiple_prices(coupon_bond_app):
    bonds = list()

    maturity = 5  # 5 years
    face_value = 10000  # $10000 face value
    rate = 6  # 6% coupon rate
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    bond = fi.create_coupon_bond(maturity, face_value, rate, frequency)
    bonds.append(bond)

    bond_prices = [8000, 9000, 10000, 11000, 12000]
    labels = ["Bond"]
    coupon_bond_app.show_yield_to_maturities_based_on_bond_prices(bonds, bond_prices, labels)


def example_calculate_bond_yield_to_maturities_based_on_multiple_prices_and_multiple_maturities(coupon_bond_app):
    bonds = list()

    maturities = [5, 6, 8, 10, 15, 20]  # multiple years
    face_value = 10000  # $10000 face value
    rate = 6  # 6% coupon rate
    frequency = 2  # semiannual payment, if 0 -> zero coupon bond
    for maturity in maturities:
        bonds.append(fi.create_coupon_bond(maturity, face_value, rate, frequency))
    labels = ['5Y', '6Y', '8Y', '10Y', '15Y', '20Y']


def example_coupon_bond_app_1():
    coupon_bond_app = CouponBondApp()
    coupon_bond_app.create_yield_curves(
        tenors=[[30], [30], [30], [30], [30]],
        rates=[[5], [6], [7], [8], [9]]
    )

    example_calculate_zero_coupon_bond_price(coupon_bond_app)
    example_calculate_multiple_bond_prices(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app)
    example_calculate_bond_yield_to_maturities_based_on_multiple_prices(coupon_bond_app)


def example_coupon_bond_app_2():
    coupon_bond_app = CouponBondApp()
    coupon_bond_app.create_yield_curves(
        tenors=[[1], [2, 3]],
        rates=[[5], [6, 7]]
    )

    example_calculate_zero_coupon_bond_price(coupon_bond_app)
    example_calculate_multiple_bond_prices(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_maturities(coupon_bond_app)
    example_calculate_multiple_bond_prices_with_different_rates(coupon_bond_app)


if __name__ == '__main__':
    example_coupon_bond_app_1()
    #example_coupon_bond_app_2()
