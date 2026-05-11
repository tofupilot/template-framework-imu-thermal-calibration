import numpy as np


def compute_residuals(data: np.ndarray, fit_model: np.ndarray) -> dict:
    residuals = np.asarray(data) - np.asarray(fit_model)
    return {
        "residuals": residuals,
        "mean_residual": float(np.mean(residuals)),
        "std_residual": float(np.std(residuals)),
        "p2p_residual": float(np.ptp(residuals)),
    }
