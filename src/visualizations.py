import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_vol_smile(
    strikes: np.ndarray,
    market_vol: np.ndarray,
    model_vol: np.ndarray,
    maturity: float,
    forward: float,
    model_name: str = "Model"
):
    log_moneyness = np.log(strikes / forward)

    plt.figure(figsize=(8, 5))
    plt.plot(log_moneyness, market_vol, "o", label="Market")
    plt.plot(log_moneyness, model_vol, "-", label=model_name)
    plt.xlabel("Log-moneyness")
    plt.ylabel("Implied Volatility")
    plt.title(f"Volatility Smile (T = {maturity:.2f})")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_atm_term_structure(
    maturities: np.ndarray,
    market_atm_vol: np.ndarray,
    model_atm_vol: np.ndarray,
    model_name: str = "Model"
):

    plt.figure(figsize=(8, 5))
    plt.plot(maturities, market_atm_vol, "o-", label="Market")
    plt.plot(maturities, model_atm_vol, "s--", label=model_name)
    plt.xlabel("Maturity")
    plt.ylabel("ATM Implied Volatility")
    plt.title("ATM Volatility Term Structure")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_errors_vs_moneyness(
    errors: pd.DataFrame,
    maturity: float = None
):
    data = errors.copy()

    if maturity is not None:
        data = data[data["maturity"] == maturity]

    plt.figure(figsize=(8, 5))
    plt.scatter(
        data["log_moneyness"],
        data["abs_error"],
        alpha=0.7
    )
    plt.xlabel("Log-moneyness")
    plt.ylabel("Absolute Error")
    plt.title("Calibration Errors vs Moneyness")
    plt.grid(True)
    plt.show()

def plot_errors_vs_maturity(errors: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    plt.scatter(
        errors["maturity"],
        errors["abs_error"],
        alpha=0.7
    )
    plt.xlabel("Maturity")
    plt.ylabel("Absolute Error")
    plt.title("Calibration Errors vs Maturity")
    plt.grid(True)
    plt.show()

def plot_error_distribution(errors: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    plt.hist(
        errors["abs_error"],
        bins=30,
        edgecolor="black"
    )
    plt.xlabel("Absolute Error")
    plt.ylabel("Frequency")
    plt.title("Distribution of Calibration Errors")
    plt.grid(True)
    plt.show()
