import numpy as np
import pandas as pd
from typing import Dict, List
import sys
import os

# Ensure the module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.dual_space_core import compute_robust_layer, compute_robust_z_layer, compute_anchored_z_layer

def generate_subject_trials(subject_id: int, base_speed: float, variance_multiplier: float, is_phase2: bool = False, burst_prob: float = 0.0, fatigue_shift: float = 30.0, fatigue_spread: float = 1.5) -> pd.DataFrame:
    """
    Generates heavy-tail RT data for a single subject across all 4 channels and 3 positions.
    Ensures 12 trials per block with built-in bursting physiology.
    If is_phase2 is True, simulates load/fatigue effects.
    """
    channels = ['V1', 'Parvo', 'Magno', 'Koniocellular']
    positions = ['L', 'C', 'R']
    
    # Intrinsic channel speeds and physiological variance
    ch_profiles = {
        'V1': {'add': 0, 'var': 15},
        'Parvo': {'add': 30, 'var': 25},
        'Magno': {'add': -15, 'var': 20},
        'Koniocellular': {'add': 70, 'var': 50} # High variance channel
    }
    
    data = []
    
    for ch in channels:
        for pos in positions:
            # Base RT for this channel
            ch_base = base_speed + ch_profiles[ch]['add']
            
            # Phase 2 Load Physics (Fatigue increases base speed and drastically increases variance)
            current_variance_mult = variance_multiplier
            if is_phase2:
                # Systemic cognitive fatigue applies the subject's shift + small local noise
                ch_base += fatigue_shift + np.random.normal(0, 5.0) 
                # Fatigue spreads the variance systemically
                current_variance_mult *= fatigue_spread 
                
            # Normal variance for this subject on this channel
            std_dev = ch_profiles[ch]['var'] * current_variance_mult
            
            # Generate 12 trials
            rts = []
            for _ in range(12):
                if np.random.rand() < burst_prob:
                    rts.append(np.random.uniform(ch_base + std_dev*4, ch_base + std_dev*8))
                else:
                    rts.append(np.random.normal(ch_base, std_dev))
            
            for rt in rts:
                data.append({
                    'Subject': subject_id,
                    'Stimulus': ch,
                    'Position': pos,
                    'RT': max(100, rt) # Prevent impossible RTs
                })
                
    return pd.DataFrame(data)

def generate_z_space_population(n_subjects: int = 150, return_phase2: bool = False):
    """
    Generates a population matrix Z in R^{N x 12}.
    If return_phase2 is True, returns a tuple (Z_F1, Z_F2) of matched subjects.
    """
    population_z_rows_f1 = []
    population_z_rows_f2 = []
    
    for subj in range(n_subjects):
        # Determine subjective load severity across a continuum to prevent discrete clustering
        base_speed = np.random.normal(250, 40)
        variance_multiplier = max(0.5, np.random.normal(1.0, 0.3))
        
        # Systemic load multipliers computed ONCE per subject to form a single continuous isotropic cluster
        fatigue_shift = np.random.normal(30.0, 5.0)
        fatigue_spread = np.random.normal(1.5, 0.1)
        
        # Keep burst probability strictly under 50% breakdown point to prevent median coordinate snapping
        burst_prob_f2 = np.random.uniform(0.05, 0.25)
        
        # F1 Gen
        df_trials_f1 = generate_subject_trials(subj, base_speed, variance_multiplier, is_phase2=False, burst_prob=0.05)
        
        # F2 Gen
        if return_phase2:
            df_trials_f2 = generate_subject_trials(subj, base_speed, variance_multiplier, is_phase2=True, burst_prob=burst_prob_f2, fatigue_shift=fatigue_shift, fatigue_spread=fatigue_spread)
            
        def _to_flat_array(z_space):
            row = []
            for ch in ['V1', 'Parvo', 'Magno', 'Koniocellular']:
                for pos in ['L', 'C', 'R']:
                    row.append(z_space[ch][pos])
            return row
            
        # Process F1 normally (Static Mode)
        robust_f1 = compute_robust_layer(df_trials_f1)
        z_space_f1 = compute_robust_z_layer(robust_f1)
        population_z_rows_f1.append(_to_flat_array(z_space_f1))
        
        # Process F2 using Anchored Projection (Dynamic Mode)
        if return_phase2:
            robust_f2 = compute_robust_layer(df_trials_f2)
            z_space_f2 = compute_anchored_z_layer(robust_f2, robust_f1)
            population_z_rows_f2.append(_to_flat_array(z_space_f2))
        
    if return_phase2:
        return np.array(population_z_rows_f1), np.array(population_z_rows_f2)
    return np.array(population_z_rows_f1)

if __name__ == "__main__":
    np.random.seed(42)
    Z = generate_z_space_population(150)
    print(f"Generated Z-Space Population: {Z.shape}")
    print("Sample Subject 1 Z-scores:")
    print(np.round(Z[0], 2))
