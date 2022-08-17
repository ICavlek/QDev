import numpy as np


class BondBase:
    def __init__(self, principal, maturity, interest_rate, use_continuous_model):
        self._principal = principal
        self._maturity = maturity
        self._interest_rate = interest_rate / 100
        self._use_continuous_model = use_continuous_model

    def _present_value(self, amount, period_year):
        value = amount / (1 + self._interest_rate) ** period_year
        if self._use_continuous_model:
            value = amount * np.exp(-self._interest_rate*period_year)
        return value


class ZeroCouponBond(BondBase):
    def __init__(self, principal, maturity, interest_rate, use_continous_model=False):
        super().__init__(principal, maturity, interest_rate, use_continous_model)

    def calculate_price(self):
        return self._present_value(self._principal, self._maturity)


class CouponBond(BondBase):
    def __init__(self, principal, rate, maturity, interest_rate, use_continous_model=False):
        super().__init__(principal, maturity, interest_rate, use_continous_model)
        self._rate = rate / 100

    def calculate_price(self):
        price = self._discount_coupon_payment()
        price = self._discount_principle_amount(price)
        return price

    def _discount_coupon_payment(self, price=0):
        for t in range(1, self._maturity + 1):
            price = price + self._present_value(self._principal * self._rate, t)
        return price

    def _discount_principle_amount(self, price):
        price = price + self._present_value(self._principal, self._maturity)
        return price