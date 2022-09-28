from resources import fixedincome as fi


def example_bonds():
    dates = [0.5, 1.0, 1.5] # 6 months, 1 year, 1.5 year
    rates = [5, 5, 105] # $5, $5, $105
    bonds = fi.bond_factory(dates=dates, rates=rates)


def example_coupon_bond():
    maturity = 5 # 5 years
    face = 1000 # $1000 face value
    rate = 6 # 6% coupon rate
    frequency = 2 # semiannual payment
    bond = fi.create_coupon_bond(maturity, face, rate, frequency)
    print("Payment dates: ", bond.get_dates())
    print("Number of payments: ", len(bond))
    print("Coupons: ", bond.get_coupons())
    print("Maturity: ", bond.get_maturity())

    print("Bond price before setting: ", bond.get_price())
    bond.set_price(100)
    print("Bond price after setting: ", bond.get_price())
    print("Yield to maturity: ", bond.YTM())


def example_zero_coupon_bond():
    maturity = 10 # 10 years
    face = 1000 # 1000$ face value
    rate = 0 # 0% coupon rate
    frequency = 0 # Zero coupon bond
    zero_coupon_bond = fi.create_coupon_bond(maturity, face, rate, frequency)
    print("Payments: ", zero_coupon_bond.get_coupons())
    print("Yield to Maturity: ", zero_coupon_bond.YTM(price=100)) # Zero coupon bond return continuous YTM e^(-rt)


def example_plotting():
    bond = fi.create_coupon_bond(maturity=3.0, face=10000, rate=8, frequency=2)
    print("Payments: ", bond.get_coupons())
    bond.plot_payments()
    # Small bug, figure doesn't hold, closes after program ends


def example_multiple_ytm():
    bond = fi.create_coupon_bond(maturity=10, face=10000, rate=9, frequency=2)
    print("Payment dates: ", bond.get_dates())
    print("Payments: ", bond.get_coupons())
    print("YTM for price $9000:", bond.YTM(9000))
    print("YTM for price $9500:", bond.YTM(9500))
    print("YTM for price $10000:", bond.YTM(10000))
    print("YTM for price $10500:", bond.YTM(10500))
    print("YTM for price $11000:", bond.YTM(11000))


if __name__ == '__main__':
    #example_bonds()
    #example_coupon_bond()
    example_zero_coupon_bond()
    #example_plotting()
    #example_multiple_ytm()

