"""
stage9A_geometric_risk_modeling.fluctuation.common.synthetic_time_series

Generates mock longitudinal trajectories in the C3-Core latent space.
Strictly adheres to `synthetic-data-first` for Stage 9B model development.
"""

import numpy as np
import pandas as pd

def generate_synthetic_cohort(
    n_subjects: int = 100, 
    n_timesteps: int = 10, 
    seed: int = 42,
    regime: str = 'physiological'
) -> pd.DataFrame:
    """
    Generates a synthetic longitudinal cohort.
    
    Args:
        n_subjects: Number of distinct subjects to generate.
        n_timesteps: Number of longitudinal observations per subject.
        seed: Random seed for reproducibility.
        regime: Type of longitudinal behavior to simulate.
            - 'physiological': mean-reverting oscillation around core, no drift.
            - 'progressive_drift': steady velocity vector away from core.
            - 'instability': exponentially increasing tangential/radial variance.
            
    Returns:
        pd.DataFrame containing ['Subject_ID', 'TimeStep', 'ΔSpeed', 'ΔLateral', 'ΔTone']
        representing the full longitudinal cohort.
    """
    rng = np.random.default_rng(seed)
    
    records = []
    
    for subj in range(n_subjects):
        # Starting point for each subject (baseline initialization from standard normal core)
        current_pos = rng.normal(0, 1, size=3)
        
        if regime == 'progressive_drift':
            # Assign a random fixed drift vector for this subject
            drift_vector = rng.normal(0, 0.5, size=3)
            # Normalize to ensure it escapes steadily
            drift_vector = drift_vector / np.linalg.norm(drift_vector) * 0.4 
        elif regime == 'instability':
            volatility = 0.5
            
        for t in range(n_timesteps):
            records.append({
                'Subject_ID': f'SUBJ_{subj:04d}',
                'TimeStep': t,
                'ΔSpeed': current_pos[0],
                'ΔLateral': current_pos[1],
                'ΔTone': current_pos[2]
            })
            
            # Compute next step based on regime
            if regime == 'physiological':
                # Mean reverting (Ornstein-Uhlenbeck style)
                # Pulls back slightly toward original starting pos + noise
                pull = -0.2 * current_pos 
                noise = rng.normal(0, 0.2, size=3)
                current_pos = current_pos + pull + noise
                
            elif regime == 'progressive_drift':
                noise = rng.normal(0, 0.1, size=3)
                current_pos = current_pos + drift_vector + noise
                
            elif regime == 'instability':
                # Exploding variance
                noise = rng.normal(0, volatility, size=3)
                current_pos = current_pos + noise
                volatility *= 1.15 # Variance escalates geometrically

    return pd.DataFrame(records)
