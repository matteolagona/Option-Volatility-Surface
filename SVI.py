import numpy as np
from dataclasses import dataclass


@dataclass
class SVIParams:
    a: float
    b: float
    rho: float
    m: float
    sigma: float


def svi_total_variance(
    k: np.ndarray,
    params: SVIParams
) -> np.ndarray:
    a, b, rho, m, sigma = (
        params.a,
        params.b,
        params.rho,
        params.m,
        params.sigma,
    )

    return a + b * (
        rho * (k - m) +
        np.sqrt((k - m) ** 2 + sigma ** 2)
    )


def svi_implied_vol(
    k: np.ndarray,
    T: float,
    params: SVIParams
) -> np.ndarray:
    w = svi_total_variance(k, params)

    if T <= 0:
        raise ValueError("Time to maturity must be positive")

    return np.sqrt(np.maximum(w, 0.0) / T)


def svi_parameter_constraints(params: SVIParams) -> bool:
    if params.b <= 0:
        return False
    if params.sigma <= 0:
        return False
    if not (-1.0 < params.rho < 1.0):
        return False

    return True


def svi_slice_loss(
    param_vector: np.ndarray,
    k: np.ndarray,
    w_market: np.ndarray,
    weights: np.ndarray | None = None
) -> float:
    params = SVIParams(*param_vector)

    if not svi_parameter_constraints(params):
        return 1e10

    w_model = svi_total_variance(k, params)

    if weights is None:
        return np.mean((w_model - w_market) ** 2)

    return np.average((w_model - w_market) ** 2, weights=weights)


def svi_initial_guess(
    k: np.ndarray,
    w_market: np.ndarray
) -> np.ndarray:
    a0 = np.min(w_market)
    b0 = 0.1
    rho0 = 0.0
    m0 = k[np.argmin(w_market)]
    sigma0 = 0.1

    return np.array([a0, b0, rho0, m0, sigma0])
