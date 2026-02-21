"""
c3x_exploratory.synthetic_microdynamics

This module provides reproducible synthetic generators for trial-level dynamics
(microdynamics) used in Stage 5 of the Exploratory Architecture Framework v4.
"""

import numpy as np


def generate_stationary_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, seed: int | None = None) -> np.ndarray:
    """
    Generates a stationary sequence of RTs with Gaussian noise.
    
    Args:
        n_samples: Length of the sequence (default 36 for v4).
        mean: Base Reaction Time.
        std: Standard deviation of the noise.
        seed: Random seed for reproducibility.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(mean, std, n_samples)


def generate_trending_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, trend_effect: float = -100.0, seed: int | None = None) -> np.ndarray:
    """
    Generates an RT sequence with a linear trend.
    
    Args:
        n_samples: Length of the sequence.
        mean: Base Reaction Time at the start.
        std: Standard deviation of the noise.
        trend_effect: Total change from the first to the last trial (negative = acceleration).
        seed: Random seed.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    base_rt = rng.normal(mean, std, n_samples)
    trend_line = np.linspace(0, trend_effect, n_samples)
    return base_rt + trend_line


def generate_autocorrelated_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, phi: float = 0.6, seed: int | None = None) -> np.ndarray:
    """
    Generates an autoregressive AR(1) sequence of RTs simulating short-term dependencies.
    
    Args:
        n_samples: Length of the sequence.
        mean: Base Reaction Time.
        std: Standard deviation of the sequence.
        phi: The autocorrelation coefficient (0.0 to 1.0).
        seed: Random seed.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    
    noise = rng.normal(0, std, n_samples)
    series = np.zeros(n_samples)
    series[0] = noise[0]
    
    for t in range(1, n_samples):
        series[t] = phi * series[t-1] + noise[t]
        
    # Standardize and shift to requested mean and std
    series_std = np.std(series)
    if series_std > 0:
        series = (series - np.mean(series)) / series_std * std
    else:
        series = series - np.mean(series)
        
    return series + mean


def generate_bursty_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, burst_type: str = 'fast', burst_length: int = 4, burst_magnitude: float = 150.0, burst_start_idx: int = 15, seed: int | None = None) -> np.ndarray:
    """
    Generates an RT sequence with a sudden 'burst' (speed up or slow down)
    that lasts for a specified number of trials.
    
    Args:
        n_samples: Length of the sequence.
        mean: Base Reaction Time.
        std: Standard deviation of the noise.
        burst_type: 'fast' (decreased RT) or 'slow' (increased RT).
        burst_length: Number of consecutive trials in the burst.
        burst_magnitude: The absolute magnitude of RT change during the burst.
        burst_start_idx: The starting trial index for the burst.
        seed: Random seed.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    series = rng.normal(mean, std, n_samples)
    
    effect = -burst_magnitude if burst_type == 'fast' else burst_magnitude
    
    end_idx = min(burst_start_idx + burst_length, n_samples)
    series[burst_start_idx:end_idx] += effect
    
    return series
