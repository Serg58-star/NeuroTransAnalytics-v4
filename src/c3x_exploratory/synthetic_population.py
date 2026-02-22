"""
c3x_exploratory.synthetic_population

Generates synthetic 3D population data (Speed Axis, Lateral Axis, Residual Tone) 
for validating the Stage 7 population geometry exploratory analysis.
"""

import numpy as np

def generate_continuum_population(n_samples: int = 1000, seed: int = 42) -> np.ndarray:
    """
    Generates a 3D dataset representing a continuous, uniform population
    with NO discrete subtypes, filling the space evenly.
    """
    rng = np.random.default_rng(seed)
    
    # Uniform distribution over a 3D box provides Hopkins ~0.5
    mins = np.array([-3.0, -3.0, -3.0])
    maxs = np.array([3.0, 3.0, 3.0])
    
    return rng.uniform(mins, maxs, size=(n_samples, 3))

def generate_discrete_population(n_samples: int = 1000, seed: int = 42) -> np.ndarray:
    """
    Generates a 3D dataset containing 3 distinct discrete subtypes.
    """
    rng = np.random.default_rng(seed)
    
    # 3 Distinct types in the latent space
    cluster_means = [
        np.array([-3.0, -1.5, 1.0]),  # Cluster 1: slow, left, high residual
        np.array([3.0, -1.5, -1.0]),  # Cluster 2: fast, left, low residual
        np.array([0.0, 3.0, 0.0])     # Cluster 3: average speed, right, average residual
    ]
    
    # Tight clusters
    cov = np.array([
        [0.4, 0.0, 0.0],
        [0.0, 0.4, 0.0],
        [0.0, 0.0, 0.4]
    ])
    
    n_per_cluster = n_samples // len(cluster_means)
    
    clusters = []
    for mean in cluster_means:
        clusters.append(rng.multivariate_normal(mean, cov, size=n_per_cluster))
        
    data = np.vstack(clusters)
    rng.shuffle(data)
    
    return data
