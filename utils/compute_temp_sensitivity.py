import numpy as np


def compute_temp_sensitivity(
    data: np.ndarray, temperatures: np.ndarray, temp_ref: float = 25
) -> dict:
    d_temp = np.diff(temperatures)
    valid_idx = np.abs(d_temp) > 1e-5
    d_data = np.diff(data)
    sensitivities = d_data[valid_idx] / d_temp[valid_idx]
    if sensitivities.size == 0:
        return {"max_sensitivity": 0.0, "sensitivity_at_ref": 0.0}
    ref_idx = int(np.argmin(np.abs(temperatures - temp_ref)))
    ref_range = slice(max(ref_idx - 10, 0), min(ref_idx + 10, len(sensitivities)))
    sensitivity_ref = float(np.mean(sensitivities[ref_range])) if sensitivities[ref_range].size else 0.0
    return {
        "max_sensitivity": float(np.max(np.abs(sensitivities))),
        "sensitivity_at_ref": abs(sensitivity_ref),
    }
