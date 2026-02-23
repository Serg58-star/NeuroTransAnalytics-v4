"""
stage9A_geometric_risk_modeling.fluctuation.fluctuation_model

Implements the formal vector fluctuation computations on longitudinal latent data.
Evaluates Radial ($r_t$) and Tangential ($\\tau_t$) deviations via Mahalanobis norms,
without introducing secondary clustering or redefining the C3-core geometry.
"""

import numpy as np
import pandas as pd

def compute_mahalanobis_norm_sq(v: np.ndarray, inv_cov: np.ndarray) -> np.ndarray:
    """ Computes squared Mahalanobis norm: ||v||^2_Sigma = v^T Sigma^-1 v.
        Handles batched (N, 3) arrays efficiently.
    """
    # v is (N, 3), inv_cov is (3, 3)
    # v @ inv_cov is (N, 3)
    # sum((v @ inv_cov) * v, axis=1) yields (N,)
    return np.sum((v @ inv_cov) * v, axis=1)

def compute_fluctuations(df: pd.DataFrame, mu: np.ndarray, cov: np.ndarray) -> pd.DataFrame:
    """
    Computes step-wise geometric fluctuations for longitudinal data.
    
    Args:
        df: DataFrame containing ['Subject_ID', 'TimeStep', 'ΔSpeed', 'ΔLateral', 'ΔTone']
            Must be sorted by ['Subject_ID', 'TimeStep'] prior to input.
        mu: (3,) centroid vector of the C3-Core distribution.
        cov: (3,3) expected physiological covariance matrix of the core.
        
    Returns:
        DataFrame appended with microdynamic step indicators.
    """
    assert 'Subject_ID' in df.columns
    assert 'TimeStep' in df.columns
    
    # Internal copy to avoid mutating original source uncontrollably
    out = df.copy()
    
    inv_cov = np.linalg.inv(cov)
    coords = ['ΔSpeed', 'ΔLateral', 'ΔTone']
    
    # Ensure sorted by subject and time
    out = out.sort_values(['Subject_ID', 'TimeStep']).reset_index(drop=True)
    
    # Compute standard vector differences against the core
    # x_t
    x_t = out[coords].values
    
    # Mask to identify where Subject_ID shifts (i.e., t=0 baseline states where step-wise delta is NaN)
    subject_shifted = out['Subject_ID'] != out['Subject_ID'].shift(1)
    
    # x_{t-1}
    x_t_minus_1 = out[coords].shift(1).values
    
    # Delta step vector: \delta_t = x_t - x_{t-1}
    delta_t = x_t - x_t_minus_1
    
    # Position relative to core: x_{t-1} - \mu
    rel_pos_t_minus_1 = x_t_minus_1 - mu
    
    # 1. Squared Mahalanobis distance from core at t-1: ||x_{t-1} - \mu||^2_\Sigma
    dist_sq_t_minus_1 = compute_mahalanobis_norm_sq(rel_pos_t_minus_1, inv_cov)
    dist_t_minus_1 = np.sqrt(np.maximum(dist_sq_t_minus_1, 1e-12)) # protect against literal zero pre-division
    
    # 2. Radial unit vector u_t
    # Defined mathematically as (x_{t-1} - \mu) / ||x_{t-1} - \mu||_\Sigma
    # For broadcasting, reshape dist_t_minus_1 to (N, 1)
    u_t = rel_pos_t_minus_1 / dist_t_minus_1[:, np.newaxis]
    
    # 3. Radial Component: r_t = u_t^T \Sigma^{-1} \delta_t
    # Vectorized: sum((u_t @ inv_cov) * delta_t, axis=1)
    r_t = np.sum((u_t @ inv_cov) * delta_t, axis=1)
    
    # 4. Total step variance: ||\delta_t||^2_\Sigma
    delta_sq_norm = compute_mahalanobis_norm_sq(delta_t, inv_cov)
    
    # 5. Tangential Component: \tau_t = sqrt( ||\delta_t||^2_\Sigma - r_t^2 )
    # Due to floating point math, sometimes r_t^2 can be infinitesimally larger than delta_sq_norm. Clip to 0.
    tau_t_sq = np.maximum(delta_sq_norm - (r_t ** 2), 0.0)
    tau_t = np.sqrt(tau_t_sq)
    
    # ---------------------------------------------------------
    # Numerical Stabilization at singularity (subject exactly on \mu)
    # ---------------------------------------------------------
    epsilon = 1e-6
    singularity_mask = dist_t_minus_1 < epsilon
    
    # If at singularity, entire movement constitutes radial drift AWAY from core.
    r_t[singularity_mask] = np.sqrt(delta_sq_norm[singularity_mask])
    tau_t[singularity_mask] = 0.0
    
    # ---------------------------------------------------------
    # Vector-Level Partial Monitoring
    # ---------------------------------------------------------
    # \Delta z_S = \Delta S_t / \sigma_S
    # We can extract standard deviations from the diagonal of the covariance matrix
    sigma_vec = np.sqrt(np.diag(cov))
    delta_z = delta_t / sigma_vec
    
    # Apply invalidations at subject boundaries
    r_t[subject_shifted] = np.nan
    tau_t[subject_shifted] = np.nan
    delta_z[subject_shifted] = np.nan
    
    out['Radial_Velocity_rt'] = r_t
    out['Tangential_Velocity_taut'] = tau_t
    out['DeltaZ_Speed'] = delta_z[:, 0]
    out['DeltaZ_Lateral'] = delta_z[:, 1]
    out['DeltaZ_Tone'] = delta_z[:, 2]
    
    return out

def compute_longitudinal_descriptors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapses the step-wise microdynamics into the requested 5 subject-level descriptors.
    Args:
        df: DataFrame produced by `compute_fluctuations`
    Returns:
        Summary DataFrame per subject.
    """
    # Filter out baseline steps (where metrics are NaN)
    valid_steps = df.dropna(subset=['Radial_Velocity_rt'])
    
    summary = []
    
    for subject_id, group in valid_steps.groupby('Subject_ID'):
        r_tarr = group['Radial_Velocity_rt'].values
        tau_tarr = group['Tangential_Velocity_taut'].values
        
        # 1. Mean radial drift
        E_rt = np.mean(r_tarr)
        
        # 2. Radial variance
        Var_rt = np.var(r_tarr, ddof=1) if len(r_tarr) > 1 else 0.0
        
        # 3. Tangential variance
        Var_taut = np.var(tau_tarr, ddof=1) if len(tau_tarr) > 1 else 0.0
        
        # 4. Drift ratio: E[r_t] / sqrt(Var(r_t))
        std_rt = np.std(r_tarr, ddof=1) if len(r_tarr) > 1 else 0.0
        drift_ratio = (E_rt / std_rt) if std_rt > 1e-9 else 0.0
        
        # 5. Return tendency: Corr(r_t, r_{t+1}) (lag-1 autocorrelation)
        return_tendency = 0.0
        if len(r_tarr) > 2:
            r_t0 = r_tarr[:-1]
            r_t1 = r_tarr[1:]
            
            # If completely static vector, correlation is undefined. Guard against it.
            if np.std(r_t0) > 1e-9 and np.std(r_t1) > 1e-9:
                return_tendency = np.corrcoef(r_t0, r_t1)[0, 1]
            
        summary.append({
            'Subject_ID': subject_id,
            'E_rt': E_rt,
            'Var_rt': Var_rt,
            'Var_taut': Var_taut,
            'Drift_Ratio': drift_ratio,
            'Return_Tendency': return_tendency,
            
            # Optional vector monitoring
            'Var_dz_Speed': np.var(group['DeltaZ_Speed'], ddof=1),
            'Var_dz_Lateral': np.var(group['DeltaZ_Lateral'], ddof=1),
            'Var_dz_Tone': np.var(group['DeltaZ_Tone'], ddof=1)
        })
        
    return pd.DataFrame(summary)
