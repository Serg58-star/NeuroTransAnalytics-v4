"""
c3x_exploratory.synthetic_variability

This module provides reproducible synthetic generators for distribution geometry
(skewness, kurtosis, tail indices, and variance) used in Stage 6 of the 
Exploratory Architecture Framework v4.
"""

import numpy as np
import scipy.stats as stats

def generate_skewed_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, skew_alpha: float = 5.0, seed: int | None = None) -> np.ndarray:
    """
    Generates an RT sequence with controlled skewness using a skew-normal distribution.
    
    Args:
        n_samples: Length of the sequence (default 36 for v4).
        mean: Target Base Reaction Time.
        std: Target Standard deviation.
        skew_alpha: Skew parameter (positive = right skewed, negative = left skewed).
        seed: Random seed for reproducibility.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    # Generate standard skew normal
    raw_data = stats.skewnorm.rvs(a=skew_alpha, size=n_samples, random_state=rng.integers(0, 10000))
    
    # Standardize and shift
    raw_mean = np.mean(raw_data)
    raw_std = np.std(raw_data)
    
    if raw_std > 0:
        scaled_data = (raw_data - raw_mean) / raw_std * std
    else:
        scaled_data = raw_data - raw_mean
        
    return scaled_data + mean


def generate_heavy_tail_rt(n_samples: int = 36, mean: float = 500.0, std: float = 50.0, df: float = 3.0, seed: int | None = None) -> np.ndarray:
    """
    Generates an RT sequence with heavy tails (elevated kurtosis) using a Student's t-distribution.
    
    Args:
        n_samples: Length of the sequence.
        mean: Target Base Reaction Time.
        std: Target Standard deviation.
        df: Degrees of freedom (lower = heavier tails, e.g., 3.0).
        seed: Random seed.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    
    # Generate from t-distribution
    raw_data = stats.t.rvs(df=df, size=n_samples, random_state=rng.integers(0, 10000))
    
    # Standardize and shift
    raw_mean = np.mean(raw_data)
    raw_std = np.std(raw_data)
    
    if raw_std > 0:
        scaled_data = (raw_data - raw_mean) / raw_std * std
    else:
        scaled_data = raw_data - raw_mean
        
    return scaled_data + mean


def generate_high_variance_rt(n_samples: int = 36, mean: float = 500.0, target_mad: float = 80.0, seed: int | None = None) -> np.ndarray:
    """
    Generates a symmetric RT sequence with a specific Median Absolute Deviation (MAD),
    independent of the mean (speed).
    
    Args:
        n_samples: Length of the sequence.
        mean: Target Median Reaction Time.
        target_mad: The desired Median Absolute Deviation.
        seed: Random seed.
        
    Returns:
        np.ndarray: One-dimensional array of samples.
    """
    rng = np.random.default_rng(seed)
    
    # Generate standard normal
    raw_data = rng.normal(0, 1, n_samples)
    
    # Calculate current median and MAD
    current_median = np.median(raw_data)
    current_mad = np.median(np.abs(raw_data - current_median))
    
    # Scale to target MAD
    if current_mad > 0:
        scaled_data = (raw_data - current_median) / current_mad * target_mad
    else:
        scaled_data = raw_data - current_median
        
    return scaled_data + mean
