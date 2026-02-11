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
