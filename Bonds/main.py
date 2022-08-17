from resources.Bonds import CouponBond, ZeroCouponBond


def test_1():
    discrete_zero_coupon_bond = ZeroCouponBond(1000, 2, 4)
    print("Discrete zero coupon bond price: %.2f" % discrete_zero_coupon_bond.calculate_price())

    continous_zero_coupon_bond = ZeroCouponBond(1000, 2, 4, True)
    print("Continuous zero coupon bond price: %.2f" % continous_zero_coupon_bond.calculate_price())

    discrete_coupon_bond = CouponBond(1000, 10, 3, 4)
    print("Discrete coupon bond price: %.2f" % discrete_coupon_bond.calculate_price())

    coupon_bond_continuous = CouponBond(1000, 10, 3, 4, True)
    print("Continous coupon bond price: %.2f" % coupon_bond_continuous.calculate_price())


if __name__ == '__main__':
    test_1()

