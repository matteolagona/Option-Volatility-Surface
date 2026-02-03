import numpy as np
from typing import Union


ArrayLike = Union[float, np.ndarray]


def discount_factor(
    rate: ArrayLike,
    maturity: ArrayLike,
    compounding: str = "continuous"
) -> ArrayLike:
    rate = np.asarray(rate)
    maturity = np.asarray(maturity)

    if compounding == "continuous":
        return np.exp(-rate * maturity)

    elif compounding == "simple":
        return 1.0 / (1.0 + rate * maturity)

    elif compounding == "annual":
        return 1.0 / np.power(1.0 + rate, maturity)

    else:
        raise ValueError(
            "Unsupported compounding type. "
            "Choose from ['continuous', 'simple', 'annual']."
        )


def zero_coupon_price(
    rate: ArrayLike,
    maturity: ArrayLike,
    compounding: str = "continuous"
) -> ArrayLike:
    return discount_factor(rate, maturity, compounding)


class FlatYieldCurve:
    def __init__(self, rate: float, compounding: str = "continuous"):
        self.rate = rate
        self.compounding = compounding

    def discount(self, maturity: ArrayLike) -> ArrayLike:
        return discount_factor(
            self.rate,
            maturity,
            compounding=self.compounding
        )
