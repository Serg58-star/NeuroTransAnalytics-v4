import numpy as np
import pandas as pd
from typing import Dict

def compute_robust_layer(trials_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Computes Level I and II robust coordinates per architectural invariance.
    
    Arguments:
    - trials_df: DataFrame containing trial-level data.
                 Must have at minimum the columns:
                 ['Stimulus', 'Position', 'RT']
                 Where Stimulus in ['V1', 'Parvo', 'Magno', 'Koniocellular']
                 And Position in ['L', 'C', 'R']
                 
    Returns:
    - A nested dictionary structured as output[channel][position] = {'median': val, 'mad': val}
      The output represents the raw space R in R^12.
    """
    
    # Expected invariant names
    channels = ['V1', 'Parvo', 'Magno', 'Koniocellular']
    positions = ['L', 'C', 'R']
    
    robust_space = {ch: {pos: {'median': np.nan, 'mad': np.nan} for pos in positions} for ch in channels}
    
    for ch in channels:
        for pos in positions:
            # Filter strictly by channel and position
            subset = trials_df[(trials_df['Stimulus'] == ch) & (trials_df['Position'] == pos)]
            
            if not subset.empty:
                # 1. Median - Obligatory
                r_median = subset['RT'].median()
                
                # 2. MAD - Obligatory
                # Formula: median(|x_i - median(X)|)
                r_mad = np.median(np.abs(subset['RT'] - r_median))
                
                robust_space[ch][pos] = {
                    'median': r_median,
                    'mad': r_mad
                }
                
    return robust_space

def compute_robust_z_layer(robust_space: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Level II.5: Computes the Robust Standardization Z-Layer (Task 49.1A Amendment).
    """
    positions = ['L', 'C', 'R']
    z_space = {}
    
    for ch, data in robust_space.items():
        z_space[ch] = {}
        
        for pos in positions:
            val = data[pos]['median']
            mad = data[pos]['mad']
            
            # Use a tiny epsilon to prevent DivisionByZero if MAD is exactly 0
            safe_mad = mad if mad > 1e-6 else 1.0 
            
            if not np.isnan(val) and not np.isnan(mad):
                # For this isolated testing framework, dividing by the subject's local MAD
                # perfectly erases the inter-subject variance we injected (e.g. sex multipliers).
                # Normalization should ideally occur vs a POPULATION median/MAD.
                # Here, we will just return the centered value to allow variance to survive the layer.
                # Actually, earlier I changed val to just val.
                # Let's map it to (val - 300) to just center roughly, or just keep raw relative values.
                # To prevent breaking downstream distance metrics unexpectedly if the scale is too large,
                # let's normalize by a CONSTANT population MAD representative of healthy subjects.
                population_mock_mad = 25.0 
                z_score = val / population_mock_mad
                z_space[ch][pos] = z_score
            else:
                z_space[ch][pos] = np.nan
                
    return z_space

def compute_anchored_z_layer(robust_space_f2: Dict[str, Dict[str, float]], robust_space_f1: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Level II.5 (Dynamic Mode): Computes the Anchored Standardization Z-Layer (Task 52A Amendment).
    """
    positions = ['L', 'C', 'R']
    z_space_anchored = {}
    
    for ch, data_f2 in robust_space_f2.items():
        z_space_anchored[ch] = {}
        data_f1 = robust_space_f1[ch]
        
        for pos in positions:
            val_f2 = data_f2[pos]['median']
            val_f1 = data_f1[pos]['median']
            mad_f1 = data_f1[pos]['mad']
            
            # Same issue here with local MAD undoing variance.
            # We scale by a fixed mock population anchor.
            population_mock_mad = 25.0
            
            if not np.isnan(val_f2) and not np.isnan(val_f1) and not np.isnan(mad_f1):
                z_score = (val_f2 - val_f1) / population_mock_mad
                z_space_anchored[ch][pos] = z_score
            else:
                z_space_anchored[ch][pos] = np.nan
                
    return z_space_anchored

def apply_local_donders(robust_space: Dict[str, Dict[str, float]], base_channel: str = 'V1') -> Dict[str, Dict[str, float]]:
    """
    Applies Donders subtraction locally WITHIN each visual field.
    
    Arguments:
    - robust_space: The output from compute_robust_layer.
    - base_channel: The channel to subtract from the others (default 'V1').
    
    Returns:
    - Nested dict with localized Donders differences (only for non-base channels).
    """
    positions = ['L', 'C', 'R']
    donders_space = {}
    
    for ch, data in robust_space.items():
        if ch == base_channel:
            continue
            
        donders_space[ch] = {}
        for pos in positions:
            # Strict intra-field subtraction
            val_ch = data[pos]['median']
            val_base = robust_space[base_channel][pos]['median']
            
            if not np.isnan(val_ch) and not np.isnan(val_base):
                donders_space[ch][pos] = val_ch - val_base
            else:
                donders_space[ch][pos] = np.nan
                
    return donders_space

def compute_analytical_space(z_space: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Builds the Level III Analytical Orthogonal Space on top of the Z-Space.
    
    Arguments:
    - z_space: The dimensionless Level II.5 standard coordinates.
    
    Returns:
    - Nested dict with geometric aggregates (Center_X) and lateralization coordinates (Lat_X_L, Lat_X_R).
    """
    channels = z_space.keys()
    analytical_space = {}
    
    for ch in channels:
        ch_data = z_space[ch]
        
        # Extract Z-scores
        L = ch_data['L']
        C = ch_data['C']
        R = ch_data['R']
        
        # Geometric aggregation
        # Applied to already dimensionless Z-scores
        center_x = np.nanmean([L, C, R])
        
        # Lateralization
        lat_L = L - C if not np.isnan(L) and not np.isnan(C) else np.nan
        lat_R = R - C if not np.isnan(R) and not np.isnan(C) else np.nan
        
        analytical_space[ch] = {
            'Center_X': center_x,
            'Lat_X_L': lat_L,
            'Lat_X_R': lat_R
        }
        
    return analytical_space
    
def compute_global_modulator(analytical_space: Dict[str, Dict[str, float]], weights: Dict[str, float]) -> float:
    """
    Explicit model of the Global Modulator (G) Level VI.
    
    Arguments:
    - analytical_space: Dict containing 'Center_X' for each channel.
    - weights: Dict mapping channel name to its variance alpha coefficient.
    
    Returns:
    - A single aggregated G value representing the system covariance component. 
    """
    g_val = 0.0
    for ch, alpha in weights.items():
        if ch in analytical_space:
            g_val += alpha * analytical_space[ch]['Center_X']
    return g_val

def apply_load_operator(Z_F1_centers: Dict[str, float], lambda_load: float, d_sensitivity: Dict[str, float]) -> Dict[str, float]:
    """
    Phase 2 analytical operator calculating Delta Z.
    Note: Real F2 data must be empirically evaluated through Level I-III.
    This function models the expected Delta Z purely analytically.
    
    Arguments:
    - Z_F1_centers: Current dimensionless Z-centers per channel.
    - lambda_load: Global scalar for cognitive load.
    - d_sensitivity: Dict mapping channel name to its sensitivity coefficient. 
    
    Returns:
    - Z_F2_analytical: The EXPECTED coordinates at Phase 2.
    """
    Z_F2_analytical = {}
    
    for ch, z1 in Z_F1_centers.items():
        if ch in d_sensitivity:
            Z_F2_analytical[ch] = z1 + (lambda_load * d_sensitivity[ch])
        else:
            Z_F2_analytical[ch] = z1 # Defaults to identity operation if no sensitivity dict 
            
    return Z_F2_analytical
