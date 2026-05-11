import numpy as np


def compute_noise_density(data: np.ndarray, sampling_rate: int = 100) -> float:
    initial_samples = data[:50]
    detrended_data = initial_samples - np.mean(initial_samples)
    noise_std = np.std(detrended_data)
    return float(noise_std / np.sqrt(sampling_rate))
