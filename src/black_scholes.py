import numpy as np
from scipy.stats import norm


def d1_d2(S, K, T, r, q, sigma):
    if T <= 0 or sigma <= 0:
        return np.nan, np.nan

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_price(S, K, T, r, sigma, option_type="call", q=0.0):
    if T <= 0:
        if option_type == "call":
            return max(S - K, 0.0)
        elif option_type == "put":
            return max(K - S, 0.0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    d1, d2 = d1_d2(S, K, T, r, q, sigma)

    if option_type == "call":
        price = (
            S * np.exp(-q * T) * norm.cdf(d1)
            - K * np.exp(-r * T) * norm.cdf(d2)
        )
    elif option_type == "put":
        price = (
            K * np.exp(-r * T) * norm.cdf(-d2)
            - S * np.exp(-q * T) * norm.cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


def bs_delta(S, K, T, r, sigma, option_type="call", q=0.0):
    d1, _ = d1_d2(S, K, T, r, q, sigma)

    if option_type == "call":
        return np.exp(-q * T) * norm.cdf(d1)
    elif option_type == "put":
        return np.exp(-q * T) * (norm.cdf(d1) - 1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def bs_gamma(S, K, T, r, sigma, q=0.0):
    d1, _ = d1_d2(S, K, T, r, q, sigma)
    return (
        np.exp(-q * T)
        * norm.pdf(d1)
        / (S * sigma * np.sqrt(T))
    )


def bs_vega(S, K, T, r, sigma, q=0.0):
    d1, _ = d1_d2(S, K, T, r, q, sigma)
    return S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)


def bs_theta(S, K, T, r, sigma, option_type="call", q=0.0):
    d1, d2 = d1_d2(S, K, T, r, q, sigma)

    term1 = -(
        S * norm.pdf(d1) * sigma * np.exp(-q * T)
    ) / (2 * np.sqrt(T))

    if option_type == "call":
        term2 = q * S * np.exp(-q * T) * norm.cdf(d1)
        term3 = -r * K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        term2 = -q * S * np.exp(-q * T) * norm.cdf(-d1)
        term3 = r * K * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return term1 + term2 + term3
