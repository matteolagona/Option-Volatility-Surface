import numpy as np
from dataclasses import dataclass
from typing import Callable, Dict, Optional

from scipy.optimize import least_squares

from src.SVI import svi_total_variance, SVIParams
from src.SABR import sabr_implied_vol


@dataclass
class CalibrationResult:
    params: Dict[str, float]
    success: bool
    message: str
    cost: float
    nfev: int


def svi_objective(
    theta: np.ndarray,
    log_moneyness: np.ndarray,
    total_variance_mkt: np.ndarray,
    weights: Optional[np.ndarray] = None
) -> np.ndarray:
    params = SVIParams(*theta)
    w_model = svi_total_variance(log_moneyness, params)
    residuals = w_model - total_variance_mkt

    if weights is not None:
        residuals *= weights

    return residuals


def calibrate_svi(
    log_moneyness: np.ndarray,
    implied_vol: np.ndarray,
    maturity: float,
    initial_guess: np.ndarray,
    bounds: tuple,
    weights: Optional[np.ndarray] = None
) -> CalibrationResult:
    total_variance_mkt = implied_vol ** 2 * maturity

    res = least_squares(
        svi_objective,
        x0=initial_guess,
        bounds=bounds,
        args=(log_moneyness, total_variance_mkt, weights)
    )

    param_names = ["a", "b", "rho", "m", "sigma"]
    params = dict(zip(param_names, res.x))

    return CalibrationResult(
        params=params,
        success=res.success,
        message=res.message,
        cost=res.cost,
        nfev=res.nfev
    )


def sabr_objective(
    theta: np.ndarray,
    strikes: np.ndarray,
    forward: float,
    maturity: float,
    implied_vol_mkt: np.ndarray,
    beta: float,
    weights: Optional[np.ndarray] = None
) -> np.ndarray:
    alpha, rho, nu = theta

    iv_model = np.array([
        sabr_implied_vol(
            F=forward,
            K=k,
            T=maturity,
            alpha=alpha,
            beta=beta,
            rho=rho,
            nu=nu
        )
        for k in strikes
    ])

    residuals = iv_model - implied_vol_mkt

    if weights is not None:
        residuals *= weights

    return residuals


def calibrate_sabr(
    strikes: np.ndarray,
    implied_vol: np.ndarray,
    forward: float,
    maturity: float,
    beta: float,
    initial_guess: np.ndarray,
    bounds: tuple,
    weights: Optional[np.ndarray] = None
) -> CalibrationResult:
    res = least_squares(
        sabr_objective,
        x0=initial_guess,
        bounds=bounds,
        args=(strikes, forward, maturity, implied_vol, beta, weights)
    )

    param_names = ["alpha", "rho", "nu"]
    params = dict(zip(param_names, res.x))

    return CalibrationResult(
        params=params,
        success=res.success,
        message=res.message,
        cost=res.cost,
        nfev=res.nfev
    )
