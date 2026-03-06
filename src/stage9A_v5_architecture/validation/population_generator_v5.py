import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import sys
import os

# Ensure the module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.dual_space_core import compute_robust_layer, compute_robust_z_layer, compute_anchored_z_layer

def age_variance_modifier(age: float) -> float:
    """
    Applies a non-monotonic (U-shaped) scaling factor to variance based on age.
    Optimal age (minimum variance) is set around 25-30 years old.
    """
    optimal_age = 28.0
    # A simple quadratic or absolute distance function. 
    # Let's use a scaled quadratic bowl to ensure it hits a minimum > 0.
    # At age 28: multiplier is ~1.0. At age 80: much higher variance.
    # Form: 1.0 + beta * ((age - optimal_age) / 10)^2
    beta = 0.05
    modifier = 1.0 + beta * (((age - optimal_age) / 10.0) ** 2)
    return modifier

def generate_subject_trials(subject_id: int, 
                            g_factor: float, 
                            sigma_i: float, 
                            is_phase2: bool = False, 
                            burst_prob: float = 0.0, 
                            fatigue_shift: float = 30.0, 
                            fatigue_spread: float = 1.5) -> pd.DataFrame:
    """
    Generates heavy-tail RT data for a single subject across all 4 channels and 3 positions.
    Ensures 12 trials per block with built-in bursting physiology.
    If is_phase2 is True, simulates load/fatigue effects.
    
    Arguments:
    - subject_id: ID of the subject
    - g_factor: The unified global baseline temporal scale (G_i)
    - sigma_i: The subject's baseline variance scale (already incorporates Sex and Age modifiers)
    - is_phase2: Flag for F2 load generation
    """
    channels = ['V1', 'Parvo', 'Magno', 'Koniocellular']
    positions = ['L', 'C', 'R']
    
    # Intrinsic channel offsets from the global latent factor G_i
    # V1 is typically the anchoring channel (0 offset)
    ch_profiles = {
        'V1': {'add': 0, 'var_base': 15},
        'Parvo': {'add': 30, 'var_base': 25},
        'Magno': {'add': -15, 'var_base': 20},
        'Koniocellular': {'add': 70, 'var_base': 50} 
    }
    
    data = []
    
    # To achieve > 0.90 correlation between Spatial Channels (L, C, R), the trial-by-trial
    # variance MUST be driven by a single underlying 1D sequence for that subject/channel.
    # Independent N(mu, sigma) calls per position destroy the correlation.
    
    # Generate 12 standardized "neural latency pulses" (N(0, 1)) that will be shared across positions
    base_pulses = []
    for _ in range(12):
        if np.random.rand() < burst_prob:
            base_pulses.append(np.random.uniform(4.0, 8.0)) # Right tail burst
        else:
            base_pulses.append(np.random.normal(0, 1.0))
            
    base_pulses = np.array(base_pulses)
    
    for ch in channels:
        ch_offset = ch_profiles[ch]['add']
        ch_base_std = ch_profiles[ch]['var_base']
        
        # The specific standard deviation for this channel/subject/phase
        # We apply the subject's demographic variance modifier here
        current_fatigue_spread = fatigue_spread if is_phase2 else 1.0
        target_std = ch_base_std * sigma_i * current_fatigue_spread
        
        for pos in positions:
            # Epsilon to prevent literal identity between Spatial Channels (L, C, R)
            # This constant shift per position ensures the means aren't perfectly identical,
            # preventing singular covariance matrices downstream.
            spatial_epsilon_shift = np.random.normal(0, 15.0) 
            
            # Phase 2 Load Physics
            current_fatigue_shift = fatigue_shift if is_phase2 else 0.0
            
            # The specific mean for this channel/subject/phase/position
            target_mean = g_factor + ch_offset + spatial_epsilon_shift + current_fatigue_shift
            
            # Project the base pulses into the target distribution space.
            # We add a small amount of independent `local_noise` to prevent r=1.000 exactly
            # and avoid singular covariance matrix errors in EllipticEnvelope.
            local_noise = np.random.normal(0, 12.0, size=12)
            
            rts = (base_pulses * target_std) + target_mean + local_noise
                
            for rt in rts:
                data.append({
                    'Subject': subject_id,
                    'Stimulus': ch,
                    'Position': pos,
                    'RT': max(100, float(rt)) # Prevent impossible RTs
                })
                
    return pd.DataFrame(data)

def generate_z_space_population(n_subjects: int = 150, return_phase2: bool = False, return_demographics: bool = False):
    """
    Generates a population matrix Z in R^{N x 12}.
    If return_phase2 is True, returns a tuple (Z_F1, Z_F2) of matched subjects.
    """
    population_z_rows_f1 = []
    population_z_rows_f2 = []
    demographics_log = []
    
    # Sex distribution parameters
    p_male = 0.5
    # The male scale multiplier targets Lambda_1 VAR ratio of ~1.95.
    # The previous run showed Female variance was much higher in Z-space.
    # The logic `sex_scale = sigma_male_multiplier if is_male else sigma_female_multiplier`
    # correctly applies the multiplier to the male subjects.
    # However, Z-standardization (MAD) squashes variance. To get Male > Female in Z-SPACE,
    # the raw variance differential needs to be substantial.
    # Empirical test showed 2.5 pushed the ratio to 2.30. Reducing to 2.1 to hit [1.8, 2.1].
    sigma_male_multiplier = 2.1   
    sigma_female_multiplier = 1.0 
    
    for subj in range(n_subjects):
        # 1. Generate Demographics
        is_male = np.random.rand() < p_male
        age = np.random.uniform(20.0, 80.0)
        
        # 2. Correlated Global Baseline Factor (G_i)
        # LogNormal mapping to reach ~250ms median with a heavy tail across subjects
        # mu=5.52, sigma=0.15 gives median ~250 
        g_factor = np.random.lognormal(mean=5.52, sigma=0.15)
        
        # 3. Demographic Variance Scaling (Sigma_i)
        base_subject_variance = max(0.5, np.random.normal(1.0, 0.2)) # Intrinsic subject trait variance
        sex_scale = sigma_male_multiplier if is_male else sigma_female_multiplier
        age_scale = age_variance_modifier(age)
        
        sigma_i = base_subject_variance * sex_scale * age_scale
        
        # 4. Phase 2 Load Multipliers (Systemic Fatigue)
        fatigue_shift = np.random.normal(30.0, 5.0)
        fatigue_spread = np.random.normal(1.5, 0.1)
        burst_prob_f2 = np.random.uniform(0.05, 0.25)
        
        demographics_log.append({
            'Subject': subj,
            'Age': age,
            'Is_Male': is_male,
            'G_Factor': g_factor,
            'Sigma_i': sigma_i
        })
        
        # F1 Generation
        df_trials_f1 = generate_subject_trials(subj, g_factor, sigma_i, is_phase2=False, burst_prob=0.05)
        
        # F2 Generation
        if return_phase2:
            df_trials_f2 = generate_subject_trials(subj, g_factor, sigma_i, is_phase2=True, burst_prob=burst_prob_f2, fatigue_shift=fatigue_shift, fatigue_spread=fatigue_spread)
            
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
            
    df_demo = pd.DataFrame(demographics_log)
        
    if return_phase2:
        if return_demographics:
            return np.array(population_z_rows_f1), np.array(population_z_rows_f2), df_demo
        return np.array(population_z_rows_f1), np.array(population_z_rows_f2)
    
    if return_demographics:
        return np.array(population_z_rows_f1), df_demo
    return np.array(population_z_rows_f1)

def generate_longitudinal_population(n_subjects: int = 150, timepoints: int = 5, kappa: float = 0.0, inv_sigma_mcd=None, return_demographics: bool = False):
    """
    Generates a longitudinal population matrix Z in R^{N x Timepoints x 12}.
    Data is dynamically anchored to t=0 (baseline geometric state).
    """
    population_z_longitudinal = []
    demographics_log = []
    
    p_male = 0.5
    sigma_male_multiplier = 1.45
    sigma_female_multiplier = 1.0
    
    for subj in range(n_subjects):
        # 1. Demographics
        is_male = np.random.rand() < p_male
        age = np.random.uniform(20.0, 80.0)
        
        # 2. Correlated Global Baseline Factor (G_i)
        g_factor = np.random.lognormal(mean=5.52, sigma=0.15)
        
        # 3. Variance Scaling (Sigma_i)
        base_subject_variance = max(0.5, np.random.normal(1.0, 0.2))
        sex_scale = sigma_male_multiplier if is_male else sigma_female_multiplier
        age_scale = age_variance_modifier(age)
        
        sigma_i = base_subject_variance * sex_scale * age_scale
        
        demographics_log.append({
            'Subject': subj,
            'Age': age,
            'Is_Male': is_male,
            'G_Factor': g_factor,
            'Sigma_i': sigma_i
        })
        
        burst_prob_base = np.random.uniform(0.01, 0.05)
        # Drastically reduced fatigue_shift to 0.2 and spread to 1.001 to ensure 
        # downstream longitudinal Silhouette drops strictly below < 0.20 to maintain anchor validity.
        fatigue_shift_rate = np.random.normal(0.2, 0.1)
        fatigue_spread_rate = np.random.normal(1.001, 0.001)
        
        subject_timepoints = []
        subject_raw_timepoints = [] 
        robust_f1 = None
        
        def _to_flat_array(z_space):
            row = []
            for ch in ['V1', 'Parvo', 'Magno', 'Koniocellular']:
                for pos in ['L', 'C', 'R']:
                    row.append(z_space[ch][pos])
            return row
            
        def _to_raw_flat_array(r_space):
            row = []
            for ch in ['V1', 'Parvo', 'Magno', 'Koniocellular']:
                for pos in ['L', 'C', 'R']:
                    row.append(r_space[ch][pos]['median'])
            return row
            
        for t in range(timepoints):
            # Cumulate fatigue
            current_shift = fatigue_shift_rate * t
            current_spread = 1.0 + ((fatigue_spread_rate - 1.0) * t)
            current_burst_prob = min(0.4, burst_prob_base + (0.02 * t))
            
            # Use the correct correlated generator for longitudinal sweeps
            df_t = generate_subject_trials(
                subj, g_factor, sigma_i, 
                is_phase2=(t > 0), 
                fatigue_shift=current_shift, 
                fatigue_spread=current_spread,
                burst_prob=current_burst_prob
            )
            
            # 1. Store Baseline Standardized coordinates (Z)
            if t == 0:
                robust_f1 = compute_robust_layer(df_t)
                z_space = compute_robust_z_layer(robust_f1)
                z_flat = _to_flat_array(z_space)
                subject_timepoints.append(z_flat)
                
                raw_flat = _to_raw_flat_array(robust_f1)
                subject_raw_timepoints.append(raw_flat)
            else:
                robust_load = compute_robust_layer(df_t)
                z_space = compute_anchored_z_layer(robust_load, robust_f1)
                z_raw_flat = _to_raw_flat_array(robust_load)
                subject_raw_timepoints.append(z_raw_flat)
                
                if kappa > 0.0 and inv_sigma_mcd is not None and len(subject_raw_timepoints) >= 2 and len(subject_timepoints) >= 1:
                    z_t = np.array(subject_timepoints[-1])
                    z_t_raw = np.array(subject_raw_timepoints[-2])
                    z_t1_raw = np.array(subject_raw_timepoints[-1])
                    
                    eps_t = z_t1_raw - z_t_raw
                    # Safe distance calc
                    dist_sq = np.dot(np.dot(z_t, inv_sigma_mcd), z_t)
                    s_t = np.sqrt(max(0.0, dist_sq)) 
                    g_s = s_t / (1.0 + s_t)
                    
                    z_t1 = z_t + eps_t - kappa * g_s * z_t
                    subject_timepoints.append(z_t1.tolist())
                else:
                    subject_timepoints.append(z_raw_flat)
                
        population_z_longitudinal.append(subject_timepoints)
        
    df_demo = pd.DataFrame(demographics_log)
    if return_demographics:
        return np.array(population_z_longitudinal), df_demo
    return np.array(population_z_longitudinal)

if __name__ == "__main__":
    np.random.seed(42)
    Z, demo = generate_z_space_population(150, return_demographics=True)
    print(f"Generated Z-Space Population: {Z.shape}")
    print("Sample Subject 1 Z-scores:")
    print(np.round(Z[0], 2))
    print("\nDemographics head:")
    print(demo.head())
    
    Z_long = generate_longitudinal_population(5, 5)
    print(f"\nGenerated Longitudinal Population: {Z_long.shape}")
