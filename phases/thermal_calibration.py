import numpy as np

from utils.calibrate_sensor import calibrate_sensor
from utils.compute_noise_density import compute_noise_density
from utils.compute_r2 import compute_r2
from utils.compute_residuals import compute_residuals
from utils.compute_temp_sensitivity import compute_temp_sensitivity


def thermal_calibration(dut, measurements, log):
    """Retrieve IMU data, validate it, compute polynomial thermal calibration, validate fit, save."""
    log.info("Fetching IMU log from DUT")
    data = dut.get_imu_data()

    sensor_units = {"acc": "m/s²", "gyro": "°/s"}
    axes = ("x", "y", "z")
    calibration_results = {}

    for sensor, data_key in (("acc", "acc_data"), ("gyro", "gyro_data")):
        sensor_data = data[data_key]
        temperature = np.asarray(sensor_data["temperature"], dtype=float)
        axes_data = {axis: np.asarray(sensor_data[f"{sensor}_{axis}"], dtype=float) for axis in axes}

        # --- Raw-data validation ---
        for axis, values in axes_data.items():
            noise = compute_noise_density(values)
            sens = compute_temp_sensitivity(values, temperature)

            setattr(measurements, f"{sensor}_noise_density_{axis}", noise)
            setattr(
                measurements,
                f"{sensor}_temp_sensitivity_ref_{axis}",
                sens["sensitivity_at_ref"],
            )

            log.info(
                f"{sensor}/{axis}: noise={noise:.5f} {sensor_units[sensor]}/√Hz, "
                f"sens@25°C={sens['sensitivity_at_ref']:.5f} {sensor_units[sensor]}/°C"
            )

        # --- Polynomial calibration ---
        fit = calibrate_sensor((temperature, *axes_data.values()))
        calibration_results[sensor] = {
            axis: fit["polynomial_coefficients"][f"{axis}_axis"].tolist() for axis in axes
        }

        # --- Multi-dimensional measurement: raw / fitted / residual vs temperature ---
        # Sort by temperature for a sensible chart axis.
        order = np.argsort(temperature)
        temp_sorted = temperature[order]

        for axis in axes:
            raw = axes_data[axis][order]
            fitted = fit["fitted_values"][f"{axis}_axis"][order]
            residuals_dict = compute_residuals(raw, fitted)
            residuals = residuals_dict["residuals"]

            md = getattr(measurements, f"{sensor}_calibration_{axis}")
            md.x_axis = temp_sorted.tolist()
            md.y_axis.raw = raw.tolist()
            md.y_axis.fitted = fitted.tolist()
            md.y_axis.residual = residuals.tolist()

            aggs = md.y_axis.residual.aggregations
            aggs.mean = residuals_dict["mean_residual"]
            aggs.std = residuals_dict["std_residual"]
            aggs.p2p = residuals_dict["p2p_residual"]

            setattr(measurements, f"{sensor}_r2_{axis}", compute_r2(raw, fitted))

            log.info(
                f"{sensor}/{axis}: residual mean={residuals_dict['mean_residual']:.4f}, "
                f"std={residuals_dict['std_residual']:.4f}, p2p={residuals_dict['p2p_residual']:.4f}"
            )

    # --- Persist calibration to DUT ---
    log.info("Saving calibration to DUT")
    dut.save_accelerometer_calibration(calibration_results["acc"])
    dut.save_gyroscope_calibration(calibration_results["gyro"])
