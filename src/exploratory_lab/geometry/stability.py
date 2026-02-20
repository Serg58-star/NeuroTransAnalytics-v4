"""
Stability Metrics for Dimensionality

Contains functions for Bootstrap and Split-Half stability testing of PCA latent dimensions.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr


# ============================================================================
# BOOTSTRAP METRICS
# ============================================================================

def pca_metrics(data: np.ndarray) -> dict:
    """Run PCA on z-scored data, return key metrics."""
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)
    cov = np.cov(data_std, rowvar=False)
    eigenvalues = np.sort(np.linalg.eigvalsh(cov))[::-1]

    total = np.sum(eigenvalues)
    var_exp = eigenvalues / total
    cum_var = np.cumsum(var_exp)

    p = eigenvalues / total
    p_safe = p[p > 0]
    pr = (total ** 2) / np.sum(eigenvalues ** 2)
    er = np.exp(-np.sum(p_safe * np.log(p_safe)))

    return {
        'pc1_pct': var_exp[0] * 100,
        'pc2_pct': var_exp[1] * 100 if len(var_exp) > 1 else 0.0,
        'cumul_pc12_pct': cum_var[1] * 100 if len(cum_var) > 1 else cum_var[0] * 100,
        'n_lambda_gt1': int(np.sum(eigenvalues > 1.0)),
        'participation_ratio': pr,
        'effective_rank': er,
    }

def run_bootstrap(data: np.ndarray, n_iter: int, rng: np.random.Generator) -> pd.DataFrame:
    """Run n_iter bootstrap iterations, return DataFrame of metrics."""
    n = data.shape[0]
    records = []
    for i in range(n_iter):
        idx = rng.integers(0, n, size=n)
        sample = data[idx]
        try:
            m = pca_metrics(sample)
            records.append(m)
        except Exception:
            continue
    return pd.DataFrame(records)


# ============================================================================
# SPLIT-HALF METRICS
# ============================================================================

def pca_on_half(data: np.ndarray):
    """Z-score + PCA, return eigenvalues (desc) and eigenvectors."""
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)
    cov = np.cov(data_std, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]

def run_split_half(data: np.ndarray, n_iter: int, rng: np.random.Generator) -> pd.DataFrame:
    """Run split-half iterations, returning stability differences."""
    n = data.shape[0]
    half = n // 2
    records = []

    for i in range(n_iter):
        perm = rng.permutation(n)
        idx_a, idx_b = perm[:half], perm[half:half * 2]

        try:
            ev_a, vec_a = pca_on_half(data[idx_a])
            ev_b, vec_b = pca_on_half(data[idx_b])
        except Exception:
            continue

        total_a = np.sum(ev_a)
        total_b = np.sum(ev_b)
        var_a = ev_a / total_a * 100
        var_b = ev_b / total_b * 100

        # 1. Variance explained differences
        diff_pc1 = abs(var_a[0] - var_b[0])
        diff_pc2 = abs(var_a[1] - var_b[1]) if len(var_a) > 1 else 0.0

        # 2. Eigenvalue correlation
        ev_corr, _ = pearsonr(ev_a, ev_b)

        # 3. Cosine similarity of PC directions (absolute value, sign arbitrary)
        cos_pc1 = abs(np.dot(vec_a[:, 0], vec_b[:, 0]))
        cos_pc2 = abs(np.dot(vec_a[:, 1], vec_b[:, 1])) if vec_a.shape[1] > 1 else 0.0

        records.append({
            'diff_pc1_pct': diff_pc1,
            'diff_pc2_pct': diff_pc2,
            'eigenvalue_corr': ev_corr,
            'cos_theta_pc1': cos_pc1,
            'cos_theta_pc2': cos_pc2,
        })

    return pd.DataFrame(records)
