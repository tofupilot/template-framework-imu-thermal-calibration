from typing import Dict, List, Tuple

import numpy as np


def calibrate_sensor(
    data: Tuple[List[float], List[float], List[float], List[float]],
    polynomial_order: int = 3,
) -> Dict[str, Dict[str, np.ndarray]]:
    temp, *sensor_data = (np.asarray(arr, dtype=float) for arr in data)

    poly_coeffs: Dict[str, np.ndarray] = {}
    fitted_values: Dict[str, np.ndarray] = {}
    axis_list = ("x", "y", "z")

    for i, axis_data in enumerate(sensor_data):
        axis_name = f"{axis_list[i]}_axis"
        coeffs = np.polyfit(temp, axis_data, polynomial_order)
        poly_coeffs[axis_name] = coeffs
        fitted_values[axis_name] = np.polyval(coeffs, temp)

    return {
        "polynomial_coefficients": poly_coeffs,
        "fitted_values": fitted_values,
    }
