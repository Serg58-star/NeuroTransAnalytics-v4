"""
c3x_exploratory.synthetic_generators

This module provides reproducible synthetic distribution generators for
developing and validating exploratory procedures (C3.x).
"""

import numpy as np


def generate_mixture_distribution(
    n_samples: int,
    modes: int,
    separation: float,
    seed: int
) -> np.ndarray:
    """
    Generates a reproducible mixture of Gaussian distributions.
    
    Args:
        n_samples: Total number of data points to generate.
        modes: Number of Gaussian modes (1, 2, or 3).
        separation: Relative distance between modes in standard deviation units.
        seed: Random seed for reproducibility.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    
    if modes == 1:
        # Unimodal: Normal(0, 1)
        return rng.standard_normal(n_samples)
    
    elif modes == 2:
        # Bimodal: Mix of Normal(-separation/2, 1) and Normal(separation/2, 1)
        samples_per_mode = n_samples // 2
        mod1 = rng.standard_normal(samples_per_mode) - (separation / 2)
        mod2 = rng.standard_normal(n_samples - samples_per_mode) + (separation / 2)
        return np.concatenate([mod1, mod2])
    
    elif modes == 3:
        # Trimodal: Mix of Normal(-separation, 1), Normal(0, 1), Normal(separation, 1)
        samples_per_mode = n_samples // 3
        mod1 = rng.standard_normal(samples_per_mode) - separation
        mod2 = rng.standard_normal(samples_per_mode)
        mod3 = rng.standard_normal(n_samples - 2 * samples_per_mode) + separation
        return np.concatenate([mod1, mod2, mod3])
    
    else:
        raise ValueError(f"Unsupported number of modes: {modes}. Expected 1, 2, or 3.")
def generate_time_series_with_shifts(
    n_samples: int,
    shifts: int,
    magnitude: float,
    seed: int
) -> np.ndarray:
    """
    Generates a reproducible time-series with mean shifts.
    
    Args:
        n_samples: Total number of data points.
        shifts: Number of mean shifts to introduce.
        magnitude: Absolute magnitude of the mean shifts.
        seed: Random seed.
    """
    rng = np.random.default_rng(seed)
    data = rng.standard_normal(n_samples)
    
    if shifts > 0:
        # Divide into segments
        segment_len = n_samples // (shifts + 1)
        for i in range(1, shifts + 1):
            # Apply shift to all subsequent points
            data[i * segment_len:] += magnitude * (1 if i % 2 == 1 else -1)
            
    return data
