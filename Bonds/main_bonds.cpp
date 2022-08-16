#include <iostream>
#include <cmath>
#include <string>

class Bond {
public:
	Bond(double principal, int maturity, double interest_rate, bool use_continuous_model) :
		principal(principal),
		maturity(maturity),
		interest_rate(interest_rate/100.0),
		use_continuous_model(use_continuous_model) {}

	virtual double calculate_price() = 0;

protected:
	double principal;
	int maturity;
	double interest_rate;
	bool use_continuous_model;

	double present_value(double amount, double period_year) {
		double value = amount / std::pow((1 + interest_rate), period_year);
		if (use_continuous_model) {
			value = amount * std::exp(-interest_rate*period_year);
		}
		return value;
	}
};

class ZeroCouponBond : public Bond {
public:
	ZeroCouponBond(double principal, int maturity, double interest_rate, bool use_continuous_model) :
		Bond(principal, maturity, interest_rate, use_continuous_model) {}

	double calculate_price() {
		return present_value(principal, maturity);
	}
};

class CouponBond : public Bond {
public:
	CouponBond(double principal, double rate, int maturity, double interest_rate, bool use_continuous_model) :
		Bond(principal, maturity, interest_rate, use_continuous_model),
		rate(rate/100.0) {}

	double calculate_price() {
		double price = 0;
		price = discount_coupon_payments(price);
		price = discount_principle_amount(price);
		return price;
	}

private:
	double rate;

	double discount_coupon_payments(double price) {
		for (int year = 1; year <= maturity; year++) {
			price += present_value(principal * rate, year);
		}
		return price;
	}

	double discount_principle_amount(double price) {
		return price + present_value(principal, maturity);
	}
};

int main() {
	ZeroCouponBond zero_coupon_bond(1000, 2, 4, true);
	double zc_price = zero_coupon_bond.calculate_price();

	std::cout << "Zero Coupon Bond price: " << zc_price << std::endl;

	CouponBond coupon_bond(1000, 10, 3, 4, true);
	double c_price = coupon_bond.calculate_price();

	std::cout << "Coupon Bond price: " << c_price << std::endl;
}