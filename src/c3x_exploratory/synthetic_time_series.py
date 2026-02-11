"""
c3x_exploratory.synthetic_time_series

This module provides reproducible synthetic time-series generators for
developing and validating exploratory procedures (C3.x).
"""

import numpy as np


def generate_piecewise_series(
    n_samples: int,
    change_points: list[int],
    means: list[float],
    std: float,
    seed: int
) -> np.ndarray:
    """
    Generates a reproducible piecewise constant time-series with Gaussian noise.
    
    Args:
        n_samples: Total number of data points.
        change_points: List of indices where the mean shifts.
        means: List of mean values for each segment (len = len(change_points) + 1).
        std: Standard deviation of additive Gaussian noise.
        seed: Random seed for reproducibility.
        
    Returns:
        np.ndarray: One-dimensional array of time-series samples.
    """
    if len(means) != len(change_points) + 1:
        raise ValueError("Number of means must be len(change_points) + 1.")
    
    # Validation: change_points must be non-negative, within bounds, and strictly increasing
    for i, cp in enumerate(change_points):
        if cp < 0 or cp >= n_samples:
            raise ValueError(f"Change point {cp} is out of bounds [0, {n_samples}).")
        if i > 0 and cp <= change_points[i-1]:
            raise ValueError("Change points must be strictly increasing.")

    rng = np.random.default_rng(seed)
    series = np.zeros(n_samples)
    
    # Define segment boundaries
    boundaries = [0] + sorted(change_points) + [n_samples]
    
    for i in range(len(boundaries) - 1):
        start, end = boundaries[i], boundaries[i+1]
        series[start:end] = means[i]
        
    # Add noise
    noise = rng.normal(0, std, n_samples)
    return series + noise
