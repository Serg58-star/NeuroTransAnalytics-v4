"""
stage9A_geometric_risk_modeling.common.noise_injection

Implements Gaussian noise injection to test model robustness for Task 39.
"""

import numpy as np
import pandas as pd
from .evaluation_metrics import compute_metrics
from sklearn.model_selection import train_test_split

def _inject_noise(df: pd.DataFrame, noise_level: float, seed: int) -> pd.DataFrame:
    """Injects Gaussian noise (SD = noise_level) to the 3D vectors."""
    df_noisy = df.copy()
    rng = np.random.default_rng(seed)
    
    noise = rng.normal(0, noise_level, size=(len(df), 3))
    
    df_noisy['ΔSpeed'] += noise[:, 0]
    df_noisy['ΔLateral'] += noise[:, 1]
    df_noisy['ΔTone'] += noise[:, 2]
    
    # Note: We purposely DO NOT recompute Mahalanobis to simulate noise at the input level
    # while the radial model naively relies on the provided (now implicitly noisy via coords) distance. 
    # Actually, to make it fair, we should recompute the distance based on the noisy coords.
    from scipy.spatial.distance import cdist
    centroid = np.zeros((1, 3))
    df_noisy['Mahalanobis_Distance'] = cdist(df_noisy[['ΔSpeed', 'ΔLateral', 'ΔTone']].values, centroid, metric='euclidean').flatten()
    
    return df_noisy
    
def evaluate_noise_robustness(model_class, df: pd.DataFrame, noise_level: float, seed: int = 42) -> dict:
    """
    Evaluates metric degradation when trained on clean data and tested on noisy data.
    """
    # Split to train and clean test
    df_train, df_test_clean = train_test_split(df, test_size=0.3, random_state=seed, stratify=df['Condition'])
    
    model = model_class()
    model.fit(df_train)
    
    # Ensure baseline is recorded
    preds_clean = model.predict_proba(df_test_clean)
    metrics_clean = compute_metrics(df_test_clean['Condition'].values, preds_clean)
    
    df_test_noisy = _inject_noise(df_test_clean, noise_level, seed + 1)
    preds_noisy = model.predict_proba(df_test_noisy)
    metrics_noisy = compute_metrics(df_test_noisy['Condition'].values, preds_noisy)
    
    return {
        'clean_auc': metrics_clean['roc_auc'],
        'clean_loss': metrics_clean['log_loss'],
        'noisy_auc': metrics_noisy['roc_auc'],
        'noisy_loss': metrics_noisy['log_loss'],
        'delta_auc': metrics_noisy['roc_auc'] - metrics_clean['roc_auc'],
        'delta_loss': metrics_noisy['log_loss'] - metrics_clean['log_loss']
    }
