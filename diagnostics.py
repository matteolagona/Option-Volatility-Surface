import numpy as np
import pandas as pd

def compute_errors(
    market_vol: np.ndarray,
    model_vol: np.ndarray
) -> pd.DataFrame:
    market_vol = np.asarray(market_vol)
    model_vol = np.asarray(model_vol)

    abs_error = model_vol - market_vol
    sq_error = abs_error ** 2

    with np.errstate(divide="ignore", invalid="ignore"):
        rel_error = abs_error / market_vol

    return pd.DataFrame({
        "market_vol": market_vol,
        "model_vol": model_vol,
        "abs_error": abs_error,
        "sq_error": sq_error,
        "rel_error": rel_error
    })

def compute_fit_metrics(errors: pd.DataFrame) -> dict:
    rmse = np.sqrt(errors["sq_error"].mean())
    mae = np.abs(errors["abs_error"]).mean()
    max_error = np.abs(errors["abs_error"]).max()

    return {
        "RMSE": rmse,
        "MAE": mae,
        "MaxError": max_error
    }

def attach_surface_coordinates(
    errors: pd.DataFrame,
    strikes: np.ndarray,
    forwards: np.ndarray,
    maturities: np.ndarray
) -> pd.DataFrame:
    log_moneyness = np.log(strikes / forwards)

    errors = errors.copy()
    errors["log_moneyness"] = log_moneyness
    errors["maturity"] = maturities

    return errors

def bucket_errors(
    errors: pd.DataFrame,
    by: str,
    n_buckets: int = 10
) -> pd.DataFrame:
    buckets = pd.qcut(errors[by], n_buckets, duplicates="drop")

    return (
        errors
        .groupby(buckets)["abs_error"]
        .agg(["mean", "std", "max"])
        .reset_index()
    )

