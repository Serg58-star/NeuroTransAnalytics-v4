"""
src/stage9C_population_longitudinal_geometry_audit/trajectory_metrics.py

Descriptor computation module for Stage 9C Population Geometry Audit.
Strictly restricted to frozen 3D latent components from Stage 9B.
No recalculation or mapping permitted.
"""

import numpy as np
import pandas as pd


def compute_radial_distribution(df_long: pd.DataFrame) -> dict:
    """
    Computes population-level radial distribution metrics (M_t, r_t, Delta_M).
    Pure descriptive statistics based ONLY on frozen inputs.
    """
    if 'Delta_M' not in df_long.columns:
        df_long['Delta_M'] = np.sqrt(df_long['Radial_Velocity_rt']**2 + df_long['Tangential_Velocity_taut']**2)
        
    df = df_long.dropna(subset=['Radial_Velocity_rt', 'Delta_M'])
    
    metrics = {
        'M_t_mean': df['Mahalanobis_Distance'].mean() if 'Mahalanobis_Distance' in df.columns else np.nan,
        'M_t_median': df['Mahalanobis_Distance'].median() if 'Mahalanobis_Distance' in df.columns else np.nan,
        'M_t_skew': df['Mahalanobis_Distance'].skew() if 'Mahalanobis_Distance' in df.columns else np.nan,
        
        'delta_M_mean': df['Delta_M'].mean(),
        'delta_M_median': df['Delta_M'].median(),
        'delta_M_p95': df['Delta_M'].quantile(0.95),
        'delta_M_skew': df['Delta_M'].skew(),
        'delta_M_kurtosis': df['Delta_M'].kurt(),
        
        'r_t_mean': df['Radial_Velocity_rt'].mean(),
        'r_t_std': df['Radial_Velocity_rt'].std(),
        'r_t_skew': df['Radial_Velocity_rt'].skew()
    }
    
    return metrics

def compute_trajectory_lengths(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Computes trajectory length metrics per subject from frozen vectors.
    """
    results = []
    for sid, group in df_long.groupby('Subject_ID'):
        group = group.sort_values('TimeStep').dropna(subset=['Delta_M'])
        if len(group) == 0:
            continue
            
        total_path_length = group['Delta_M'].sum()
        mean_step_length = group['Delta_M'].mean()
        
        max_excursion = group['Mahalanobis_Distance'].max() if 'Mahalanobis_Distance' in group.columns else np.nan
        
        net_d_speed = group['DeltaZ_Speed'].sum()
        net_d_lateral = group['DeltaZ_Lateral'].sum()
        net_d_tone = group['DeltaZ_Tone'].sum()
        cum_displacement = np.sqrt(net_d_speed**2 + net_d_lateral**2 + net_d_tone**2)
        
        results.append({
            'Subject_ID': sid,
            'total_path_length': total_path_length,
            'mean_step_length': mean_step_length,
            'max_radial_excursion': max_excursion,
            'cumulative_displacement': cum_displacement,
            'n_steps': len(group)
        })
        
    return pd.DataFrame(results)

def compute_axis_dominance(df_long: pd.DataFrame) -> dict:
    """
    Identifies the dominant geometric axis per step across the population.
    """
    df = df_long.dropna(subset=['DeltaZ_Speed', 'DeltaZ_Lateral', 'DeltaZ_Tone'])
    
    abs_speed = df['DeltaZ_Speed'].abs()
    abs_lateral = df['DeltaZ_Lateral'].abs()
    abs_tone = df['DeltaZ_Tone'].abs()
    
    axes = pd.DataFrame({'Speed': abs_speed, 'Lateral': abs_lateral, 'Tone': abs_tone})
    dominant = axes.idxmax(axis=1)
    
    counts = dominant.value_counts()
    props = (counts / len(df)) * 100
    
    return {
        'total_steps': len(df),
        'Speed_count': counts.get('Speed', 0),
        'Lateral_count': counts.get('Lateral', 0),
        'Tone_count': counts.get('Tone', 0),
        'Speed_prop': props.get('Speed', 0.0),
        'Lateral_prop': props.get('Lateral', 0.0),
        'Tone_prop': props.get('Tone', 0.0)
    }

def compute_convergence_divergence(df_long: pd.DataFrame) -> dict:
    """
    Evaluates net displacements and convergence behaviors derived from frozen r_t fields.
    """
    df = df_long.dropna(subset=['Radial_Velocity_rt'])
    
    total_steps = len(df)
    convergent_steps = (df['Radial_Velocity_rt'] < 0).sum()
    divergent_steps = (df['Radial_Velocity_rt'] > 0).sum()
    
    prop_convergent = (convergent_steps / total_steps) * 100 if total_steps > 0 else 0
    prop_divergent = (divergent_steps / total_steps) * 100 if total_steps > 0 else 0
    
    net_r_t = df.groupby('Subject_ID')['Radial_Velocity_rt'].sum()
    drifting_subjects = (net_r_t > 0).sum()
    returning_subjects = (net_r_t < 0).sum()
    total_subs = len(net_r_t)
    
    return {
        'prop_convergent_steps': prop_convergent,
        'prop_divergent_steps': prop_divergent,
        'drifting_subjects_prop': (drifting_subjects / total_subs) * 100 if total_subs > 0 else 0,
        'returning_subjects_prop': (returning_subjects / total_subs) * 100 if total_subs > 0 else 0
    }

def compute_geometric_shape(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Computes curvature index and angular dispersion for trajectories.
    """
    results = []
    for sid, group in df_long.groupby('Subject_ID'):
        group = group.sort_values('TimeStep').dropna(subset=['Delta_M', 'Tangential_Velocity_taut', 'Radial_Velocity_rt'])
        if len(group) == 0:
            continue
            
        total_path_length = group['Delta_M'].sum()
        
        net_d_speed = group['DeltaZ_Speed'].sum()
        net_d_lateral = group['DeltaZ_Lateral'].sum()
        net_d_tone = group['DeltaZ_Tone'].sum()
        net_displacement = np.sqrt(net_d_speed**2 + net_d_lateral**2 + net_d_tone**2)
        
        curvature_index = total_path_length / net_displacement if net_displacement > 0 else np.nan
        
        total_v2 = group['Radial_Velocity_rt']**2 + group['Tangential_Velocity_taut']**2
        mean_tau_ratio = (group['Tangential_Velocity_taut']**2 / total_v2).mean() if total_v2.sum() > 0 else np.nan
        
        results.append({
            'Subject_ID': sid,
            'curvature_index': curvature_index,
            'mean_tau_ratio': mean_tau_ratio
        })
        
    return pd.DataFrame(results)
