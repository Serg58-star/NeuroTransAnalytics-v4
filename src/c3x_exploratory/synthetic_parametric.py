"""
c3x_exploratory.synthetic_parametric

This module provides reproducible synthetic generators for parametric distribution
modeling used in Task 35.1 (Stage 6 extension) of the 
Exploratory Architecture Framework v4.
"""

import numpy as np
import scipy.stats as stats

def generate_normal_rt(n_samples: int = 36, loc: float = 500.0, scale: float = 50.0, seed: int | None = None) -> np.ndarray:
    """Generates RTs from a Normal distribution."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc, scale, n_samples)

def generate_lognormal_rt(n_samples: int = 36, s: float = 0.2, scale: float = 500.0, seed: int | None = None) -> np.ndarray:
    """Generates RTs from a Lognormal distribution. s is the shape parameter (sigma of underlying normal)."""
    rng = np.random.default_rng(seed)
    return stats.lognorm.rvs(s=s, scale=scale, size=n_samples, random_state=rng.integers(0, 10000))

def generate_gamma_rt(n_samples: int = 36, a: float = 10.0, scale: float = 50.0, seed: int | None = None) -> np.ndarray:
    """Generates RTs from a Gamma distribution. a is the shape parameter."""
    rng = np.random.default_rng(seed)
    return stats.gamma.rvs(a=a, scale=scale, size=n_samples, random_state=rng.integers(0, 10000))

def generate_weibull_rt(n_samples: int = 36, c: float = 2.5, scale: float = 500.0, seed: int | None = None) -> np.ndarray:
    """Generates RTs from a Weibull Min distribution."""
    rng = np.random.default_rng(seed)
    return stats.weibull_min.rvs(c=c, scale=scale, size=n_samples, random_state=rng.integers(0, 10000))

def generate_exgaussian_rt(n_samples: int = 36, mu: float = 400.0, sigma: float = 30.0, tau: float = 100.0, seed: int | None = None) -> np.ndarray:
    """
    Generates RTs from an Exponentially Modified Gaussian (Ex-Gaussian) distribution.
    Combines a normal process (mu, sigma) with an exponential delay (tau).
    """
    rng = np.random.default_rng(seed)
    normal_part = rng.normal(mu, sigma, n_samples)
    exp_part = rng.exponential(tau, n_samples)
    return normal_part + exp_part
