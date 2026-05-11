import numpy as np


def compute_r2(data: np.ndarray, fit_model: np.ndarray) -> float:
    data = np.asarray(data, dtype=float)
    fit_model = np.asarray(fit_model, dtype=float)
    residuals = data - fit_model
    total_variation = float(np.sum((data - np.mean(data)) ** 2))
    if total_variation == 0.0:
        return 1.0
    residual_variation = float(np.sum(residuals ** 2))
    return 1.0 - residual_variation / total_variation
