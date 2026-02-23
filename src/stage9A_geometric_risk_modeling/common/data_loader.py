"""
stage9A_geometric_risk_modeling.common.data_loader

Generates synthetic 3D latent data (ΔSpeed, ΔLateral, ΔTone) and Mahalanobis
Distance for Stage 9A Comparative Geometric Risk Modeling.
Conforms strictly to the `synthetic-data-first` constraint.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

def generate_base_data(n_samples: int, seed: int) -> pd.DataFrame:
    """Generates the base 3D coordinates and Mahalanobis distance (from centroid)."""
    rng = np.random.default_rng(seed)
    
    # Generate 3D standard normal distribution (Core Invariant: no clusters, continuous gradient)
    data = rng.normal(0, 1, size=(n_samples, 3))
    
    df = pd.DataFrame(data, columns=['ΔSpeed', 'ΔLateral', 'ΔTone'])
    
    # Calculate Mahalanobis distance from centroid (assuming unit variance and 0 covariance for synthetic)
    centroid = np.zeros((1, 3))
    df['Mahalanobis_Distance'] = cdist(df[['ΔSpeed', 'ΔLateral', 'ΔTone']].values, centroid, metric='euclidean').flatten()
    
    return df

def generate_radial_dominant_data(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Risk strongly tied to Mahalanobis Distance (Radial Risk Model dominates)."""
    df = generate_base_data(n_samples, seed)
    logits = -3.0 + 1.5 * df['Mahalanobis_Distance']
    probs = 1 / (1 + np.exp(-logits))
    rng = np.random.default_rng(seed + 1)
    df['Condition'] = rng.binomial(1, probs)
    return df

def generate_vector_sensitive_data(n_samples: int = 1000, seed: int = 43) -> pd.DataFrame:
    """Risk strongly tied to specific vector directions (Vector Risk Model dominates)."""
    df = generate_base_data(n_samples, seed)
    logits = -1.0 + 2.0 * df['ΔSpeed'] - 2.5 * df['ΔLateral'] + 0.5 * df['ΔTone']
    probs = 1 / (1 + np.exp(-logits))
    rng = np.random.default_rng(seed + 1)
    df['Condition'] = rng.binomial(1, probs)
    return df

def generate_topology_dependent_data(n_samples: int = 10000, seed: int = 44) -> pd.DataFrame:
    """Risk tied to specific non-linear topological hotspots in 3D (Bayesian Risk Mapping dominates)."""
    df = generate_base_data(n_samples, seed)
    
    speed = df['ΔSpeed']
    lateral = df['ΔLateral']
    logits = 1.0 * speed * lateral
    probs = 1.0 / (1.0 + np.exp(-logits))
    
    rng = np.random.default_rng(seed + 1)
    df['Condition'] = rng.binomial(1, probs)
    return df
