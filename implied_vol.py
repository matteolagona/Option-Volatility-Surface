import numpy as np
from scipy.optimize import brentq
from src.black_scholes import bs_price

def _check_inputs(price, S, K, T):
    if price <= 0:
        return False
    if S <= 0 or K <= 0:
        return False
    if T <= 0:
        return False
    return True

def _bs_price_diff(
    sigma,
    price,
    S,
    K,
    T,
    r,
    q,
    option_type
):
    model_price = bs_price(
        S=S,
        K=K,
        T=T,
        r=r,
        q=q,
        sigma=sigma,
        option_type=option_type
    )
    return model_price - price

def implied_volatility(
    price,
    S,
    K,
    T,
    r,
    option_type="call",
    q=0.0,
    initial_guess=0.2,
    sigma_min=1e-6,
    sigma_max=5.0
):
    if not _check_inputs(price, S, K, T):
        return np.nan

    try:
        iv = brentq(
            _bs_price_diff,
            a=sigma_min,
            b=sigma_max,
            args=(price, S, K, T, r, q, option_type),
            maxiter=500,
            xtol=1e-8
        )
        return iv

    except ValueError:
        return np.nan
