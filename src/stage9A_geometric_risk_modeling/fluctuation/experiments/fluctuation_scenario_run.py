"""
stage9A_geometric_risk_modeling.fluctuation.experiments.fluctuation_scenario_run

Validates the longitudinal vector fluctuation models against purely synthetic 
cohorts expressing orthogonal regimes: physiological, drift, and instability.
"""

import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from stage9A_geometric_risk_modeling.fluctuation.common.synthetic_time_series import generate_synthetic_cohort
from stage9A_geometric_risk_modeling.fluctuation.fluctuation_model import compute_fluctuations, compute_longitudinal_descriptors

def test_regime(name: str, regime_type: str):
    print(f"\n======================================")
    print(f"Testing Regime: {name.upper()} ({regime_type})")
    print(f"======================================")
    
    # Generate Synthetic longitudinal dataset (N=30 subjects, T=50 timesteps)
    df = generate_synthetic_cohort(n_subjects=30, n_timesteps=50, seed=42, regime=regime_type)
    
    # Assume C3-Core centroid is explicitly located at the origin for this controlled synthetic test
    mu = np.array([0.0, 0.0, 0.0])
    
    # Assume unit variance no-covariance for the base latent physiological space
    cov = np.eye(3)
    
    # 1. Compute local, instantaneous fluctuation vectors per-step
    df_fluct = compute_fluctuations(df, mu, cov)
    
    # 2. Extract aggregated macro-descriptors longitudinally
    summary = compute_longitudinal_descriptors(df_fluct)
    
    # 3. Analyze summary bounds
    print("\n[Cohort Summary Aggregates]")
    print(f"Mean Radial Drift (E[r_t]): {summary['E_rt'].mean():.4f}  (Expected: ~0 for physio, >0 for drift)")
    print(f"Radial Variance (Var(r_t)): {summary['Var_rt'].mean():.4f}")
    print(f"Tangential Variance (Var(t_t)): {summary['Var_taut'].mean():.4f}")
    print(f"Drift Ratio: {summary['Drift_Ratio'].mean():.4f}")
    print(f"Return Tendency (Autocorr lag-1): {summary['Return_Tendency'].mean():.4f} (Expected: <0 for physio mean-reversion)")
    
    print("\n[Vector Partial Monitoring (Mean Z-Variances)]")
    print(f"Speed: {summary['Var_dz_Speed'].mean():.4f}")
    print(f"Lateral: {summary['Var_dz_Lateral'].mean():.4f}")
    print(f"Tone: {summary['Var_dz_Tone'].mean():.4f}")

if __name__ == "__main__":
    test_regime("Healthy Base", "physiological")
    test_regime("Pathological Escape", "progressive_drift")
    test_regime("System Breakdown", "instability")
