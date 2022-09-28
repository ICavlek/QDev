from resources import fixedincome as fi


def example_yield_curve():
    tenors = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    spot_rates = [0.8, 0.95, 1.16, 1.4, 1.65, 2.1, 2.6, 3.0]
    yield_curve = fi.curve_factory(dates=tenors, rates=spot_rates)
    print("Spot Rate 5 year, compounded 2 per year:", yield_curve.spot_rate(5.0, 2))
    print("Simply compounded:", yield_curve.spot_rate(5.0, 0))
    print("Discount factor for 5 years:", yield_curve.discount_factor(5.0))

    maturity = 5  # 5 years
    face = 1000  # $1000 face value
    rate = 6  # 6% coupon rate
    frequency = 2  # semiannual payment
    bond = fi.create_coupon_bond(maturity, face, rate, frequency)
    price = bond.price(curve=yield_curve)
    yield_curve.plot_yields()
    yield_curve.plot_discount_factors()


def example_flat_yield_curve():
    yc = fi.curve_factory(dates=[10.0], rates=[5.0])
    print("Tenors: ", yc.get_tenors())
    print("Rates: ", yc.get_rates())
    print("Yield 1.0:", yc.get_yield(1.0))
    print("Yield 5:", yc.get_yield(5))
    print("Discount factor 1/12:", yc.discount_factor(1/12))
    print("Discount factor 7:", yc.discount_factor(7))
    #yc.plot_yields()
    #yc.plot_discount_factors()

    bond = fi.create_coupon_bond(maturity=5, face=10000, rate=5, frequency=2)
    print("Bond price with yield curve:", bond.price(yc))


if __name__ == '__main__':
    #example_yield_curve()
    example_flat_yield_curve()