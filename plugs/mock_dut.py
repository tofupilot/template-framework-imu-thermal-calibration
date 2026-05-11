import time
from pathlib import Path

import pandas as pd


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "imu_raw_data.csv"


class MockDut:
    """Simulated DUT that returns IMU log data from a CSV file."""

    def __init__(self):
        self._connected = False
        print("Mock DUT initialized")

    def __del__(self):
        if getattr(self, "_connected", False):
            print("Mock DUT disconnected")

    def connect(self) -> bool:
        print("Connecting to mock DUT...")
        time.sleep(0.2)
        self._connected = True
        return True

    def get_imu_data(self) -> dict:
        df = pd.read_csv(CSV_PATH, delimiter="\t")
        return {
            "acc_data": {
                "temperature": df["imu.temperature"].tolist(),
                "acc_x": df["imu.acc.x"].tolist(),
                "acc_y": df["imu.acc.y"].tolist(),
                "acc_z": (df["imu.acc.z"] - 9.80600).tolist(),
            },
            "gyro_data": {
                "temperature": df["imu.temperature"].tolist(),
                "gyro_x": df["imu.gyro.x"].tolist(),
                "gyro_y": df["imu.gyro.y"].tolist(),
                "gyro_z": df["imu.gyro.z"].tolist(),
            },
        }

    def save_accelerometer_calibration(self, coefficients: dict) -> None:
        print(f"Saved accelerometer calibration: {list(coefficients.keys())}")
        time.sleep(0.1)

    def save_gyroscope_calibration(self, coefficients: dict) -> None:
        print(f"Saved gyroscope calibration: {list(coefficients.keys())}")
        time.sleep(0.1)
