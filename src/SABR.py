import numpy as np


def _check_sabr_parameters(alpha, beta, rho, nu):
    if alpha <= 0.0:
        raise ValueError("alpha must be strictly positive")
    if not (0.0 <= beta <= 1.0):
        raise ValueError("beta must be in [0, 1]")
    if not (-1.0 < rho < 1.0):
        raise ValueError("rho must be in (-1, 1)")
    if nu <= 0.0:
        raise ValueError("nu must be strictly positive")


def hagan_log_normal_vol(F, K, T, alpha, beta, rho, nu, eps=1e-07):

    _check_sabr_parameters(alpha, beta, rho, nu)

    F = np.asarray(F, dtype=float)
    K = np.asarray(K, dtype=float)

    is_atm = np.abs(F - K) < eps

    FK_beta = (F * K) ** ((1.0 - beta) / 2.0)
    log_FK = np.log(F / K)

    z = (nu / alpha) * FK_beta * log_FK
    chi_z = np.log(
        (np.sqrt(1.0 - 2.0 * rho * z + z**2) + z - rho) / (1.0 - rho)
    )

    z_over_chi = np.where(
        np.abs(z) < eps,
        1.0,
        z / chi_z
    )

    denom = FK_beta * (
        1.0
        + ((1.0 - beta)**2 / 24.0) * log_FK**2
        + ((1.0 - beta)**4 / 1920.0) * log_FK**4
    )

    time_corr = (
        1.0
        + (
            ((1.0 - beta)**2 / 24.0) * (alpha**2 / (FK_beta**2))
            + (rho * beta * nu * alpha) / (4.0 * FK_beta)
            + ((2.0 - 3.0 * rho**2) * nu**2 / 24.0)
        ) * T
    )

    sigma = (alpha / denom) * z_over_chi * time_corr

    if np.any(is_atm):
        sigma_atm = (
            (alpha / (F[is_atm] ** (1.0 - beta)))
            * (
                1.0
                + (
                    ((1.0 - beta)**2 / 24.0) * (alpha**2 / (F[is_atm] ** (2.0 - 2.0 * beta)))
                    + (rho * beta * nu * alpha) / (4.0 * F[is_atm] ** (1.0 - beta))
                    + ((2.0 - 3.0 * rho**2) * nu**2 / 24.0)
                ) * T
            )
        )
        sigma = np.where(is_atm, sigma_atm, sigma)

    return sigma


def sabr_implied_vol(F, K, T, alpha, beta, rho, nu):
    return hagan_log_normal_vol(F, K, T, alpha, beta, rho, nu)
