import numpy as np
import pandas as pd
import scipy.stats as stats
import sys
import os

sys.path.append(os.path.abspath("analysis"))
import robust_statistics as rs

# We expect the components dataset now
COMPONENTS_PATH = "docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
OUTPUT_DIR = "docs/audit_legacy/Stage L/L5_results"

# -----------------------------------------------------
# Utilities
# -----------------------------------------------------
def load_data():
    df = pd.read_csv(COMPONENTS_PATH)
    # Pivot components into a unified column structure for mapping
    df_v4 = df.dropna(subset=['delta_v4']).copy()
    df_v4['component'] = 'Delta V4 (Color)'
    df_v4['delta_val'] = df_v4['delta_v4']
    
    df_v5 = df.dropna(subset=['delta_v5_mt']).copy()
    df_v5['component'] = 'Delta V5/MT (Shift)'
    df_v5['delta_val'] = df_v5['delta_v5_mt']
    
    return pd.concat([df_v4, df_v5], ignore_index=True)

# -----------------------------------------------------
# BLOCK A: Protocol Order Effects
# -----------------------------------------------------
def analyze_order_effects(df: pd.DataFrame) -> dict:
    """A1, A2, A3: Test Order Confounding, Early/Late drift, Cross-Test Correlation"""
    results = {}
    
    # A1: Medians and MAD grouped by component
    a1_summary = df.groupby('component').agg(
        median_delta=('delta_val', rs.median_value),
        mad_delta=('delta_val', rs.mad_value),
        n_trials=('delta_val', 'count')
    ).reset_index()
    results['A1_summary'] = a1_summary

    # A2: Early/Late Series Decomposition
    def categorize_section(idx):
        if idx <= 12: return 'early'
        elif idx <= 24: return 'mid'
        else: return 'late'
        
    df_series = df.copy()
    df_series['section'] = df_series['stimulus_index'].apply(categorize_section)
    a2_drift = df_series.groupby(['component', 'section']).agg(
        median_delta=('delta_val', rs.median_value)
    ).reset_index()
    results['A2_drift'] = a2_drift

    # A3: Cross-Component Correlation (Subject Level)
    subj_medians = df.groupby(['subject_id', 'component'])['delta_val'].apply(rs.median_value).unstack().dropna()
    # Spearman rank correlation instead of Pearson on means
    a3_corr = subj_medians.corr(method='spearman')
    results['A3_cross_comp_corr'] = a3_corr
    
    return results

# -----------------------------------------------------
# BLOCK B: Temporal Dynamics
# -----------------------------------------------------
def analyze_temporal_dynamics(df: pd.DataFrame) -> dict:
    """B1: Optimal PSI, B2: PSI Predictability, B3: PSI Sensitivity Heterogeneity"""
    results = {}

    # B1: Optimal PSI (Using Median Binning Location)
    b1_fits = []
    for comp in df['component'].unique():
        sub = df[(df['component'] == comp) & (df['psi'].notna())].copy()
        if len(sub) > 10:
            # 5 bins to find median minimum
            sub['psi_bin'] = pd.qcut(sub['psi'], q=5, duplicates='drop')
            bin_medians = sub.groupby('psi_bin')['delta_val'].apply(rs.median_value)
            opt_bin = bin_medians.idxmin()
            b1_fits.append({'component': comp, 'optimal_psi_bin': str(opt_bin), 'min_median_delta': bin_medians.min()})
    results['B1_optimal_psi'] = pd.DataFrame(b1_fits)

    # B2: PSI Predictability (Markov bias checking sequential correlation by rank)
    b2_markov = []
    for comp in df['component'].unique():
        sub = df[df['component'] == comp].sort_values(['subject_id', 'stimulus_index']).copy()
        sub['psi_lag1'] = sub.groupby('subject_id')['psi'].shift(1)
        sub_valid = sub.dropna(subset=['delta_val', 'psi', 'psi_lag1'])
        if len(sub_valid) > 10:
            corr_curr, _ = stats.spearmanr(sub_valid['delta_val'], sub_valid['psi'])
            corr_prev, _ = stats.spearmanr(sub_valid['delta_val'], sub_valid['psi_lag1'])
            b2_markov.append({'component': comp, 'spearman_delta_psi_curr': corr_curr, 'spearman_delta_psi_prev': corr_prev})
    results['B2_predictability'] = pd.DataFrame(b2_markov)

    # B3: Subject level sensitivity (Rank correlation)
    b3_subj = []
    for subj, subj_df in df.groupby('subject_id'):
        if len(subj_df) > 5 and subj_df['psi'].nunique() > 1:
            rho, _ = stats.spearmanr(subj_df['psi'], subj_df['delta_val'])
            b3_subj.append({'subject_id': subj, 'psi_spearman_rho': rho})
    results['B3_subject_sensitivity'] = pd.DataFrame(b3_subj)

    return results

# -----------------------------------------------------
# BLOCK C: Spatial Structure
# -----------------------------------------------------
def analyze_spatial_structure(df: pd.DataFrame) -> dict:
    """C1: Lateralization Re-eval, C2: Spatial Attention Degradation"""
    results = {}
    
    c1_lat = df.groupby(['component', 'stim_pos']).agg(
        median_delta=('delta_val', rs.median_value),
        mad_delta=('delta_val', rs.mad_value)
    ).reset_index()
    results['C1_lateralization'] = c1_lat
    
    # C2: Interaction PSI * Field (Rank correlation per field)
    c2_degrad = []
    for field in ['left', 'center', 'right']:
        sub = df[df['stim_pos'] == field].dropna(subset=['delta_val', 'psi'])
        if len(sub) > 10:
            rho, _ = stats.spearmanr(sub['psi'], sub['delta_val'])
            c2_degrad.append({'stim_pos': field, 'degradation_spearman_rho': rho})
    results['C2_spatial_degradation'] = pd.DataFrame(c2_degrad)

    return results

# -----------------------------------------------------
# BLOCK D: Reaction Structure and Variability
# -----------------------------------------------------
def analyze_reaction_structure(df: pd.DataFrame) -> dict:
    """D1, D3, D4"""
    results = {}
    
    # D1: Non-Parametric Percentile Mapping instead of ExGaussian
    d1_params = []
    for comp in df['component'].unique():
        delta_vec = df[df['component'] == comp]['delta_val'].dropna()
        if len(delta_vec) > 10:
            d1_params.append({
                'component': comp, 
                'median': rs.median_value(delta_vec), 
                'mad': rs.mad_value(delta_vec),
                'p90': rs.percentile_range(delta_vec, 10, 90)[1]
            })
    results['D1_robust_percentiles'] = pd.DataFrame(d1_params)

    # D3: Variability Structure Mapping (MAD by component/field)
    d3_var = df.groupby(['component', 'stim_pos'])['delta_val'].apply(rs.mad_value).reset_index().rename(columns={'delta_val': 'delta_mad'})
    results['D3_mad_structure'] = d3_var
    
    # D4: Residuals (Overall Delta - PSI Median Bin predicated Delta)
    valid_mask = df['delta_val'].notna() & df['psi'].notna()
    sub_df = df[valid_mask].copy()
    if len(sub_df) > 10:
        sub_df['psi_bin'] = pd.qcut(sub_df['psi'], q=5, duplicates='drop')
        # Map each row to the median of its bin
        bin_medians = sub_df.groupby(['component', 'psi_bin'])['delta_val'].transform(rs.median_value)
        sub_df['residual_from_median'] = sub_df['delta_val'] - bin_medians
        res_summary = sub_df.groupby('component')['residual_from_median'].apply(rs.mad_value).reset_index().rename(columns={'residual_from_median': 'residual_mad'})
    else:
        res_summary = pd.DataFrame()
    results['D4_residual_mad_summary'] = res_summary
    
    return results

# -----------------------------------------------------
# BLOCK E: Sequential Dynamics
# -----------------------------------------------------
def analyze_sequential_dynamics(df: pd.DataFrame) -> dict:
    """E1: Micro-Oscillatory (Autocorr), E2: Post-Error Slowing"""
    results = {}
    
    # E1: Autocorrelation at lag 1 and 2 (Spearman on shifted values)
    e1_autocorr = []
    for comp in df['component'].unique():
        sub = df[df['component'] == comp].sort_values(['subject_id', 'stimulus_index']).copy()
        sub['lag1'] = sub.groupby('subject_id')['delta_val'].shift(1)
        sub['lag2'] = sub.groupby('subject_id')['delta_val'].shift(2)
        
        valid_1 = sub.dropna(subset=['delta_val', 'lag1'])
        valid_2 = sub.dropna(subset=['delta_val', 'lag2'])
        
        ac_1 = stats.spearmanr(valid_1['delta_val'], valid_1['lag1'])[0] if len(valid_1) > 10 else np.nan
        ac_2 = stats.spearmanr(valid_2['delta_val'], valid_2['lag2'])[0] if len(valid_2) > 10 else np.nan
        
        e1_autocorr.append({'component': comp, 'lag_1_spearman': ac_1, 'lag_2_spearman': ac_2})
    results['E1_autocorrelation'] = pd.DataFrame(e1_autocorr)
    
    # E2: Post-Error Slowing
    e2_pes = []
    for subj, subj_df in df.groupby('subject_id'):
        for comp, comp_df in subj_df.groupby('component'):
            comp_df = comp_df.sort_values('stimulus_index')
            if len(comp_df) < 2: continue
            
            indexes = comp_df['stimulus_index'].values
            deltas = comp_df['delta_val'].values
            
            baseline = rs.median_value(deltas)
            pes_deltas = []
            
            for i in range(1, len(indexes)):
                # If gap > 1, the previous trial was an error/omission
                if indexes[i] - indexes[i-1] > 1:
                    pes_deltas.append(deltas[i])
                    
            if pes_deltas:
                e2_pes.append({
                    'subject_id': subj, 'component': comp,
                    'baseline_median_delta': baseline, 'median_post_error_delta': rs.median_value(pes_deltas)
                })
    
    if e2_pes:
        pes_df = pd.DataFrame(e2_pes)
        pes_summary = pes_df.groupby('component').agg(
            baseline_median_delta=('baseline_median_delta', rs.median_value),
            post_error_median=('median_post_error_delta', rs.median_value)
        ).reset_index()
        pes_summary['PES_penalty_median_ms'] = pes_summary['post_error_median'] - pes_summary['baseline_median_delta']
    else:
        pes_summary = pd.DataFrame()
        
    results['E2_post_error_slowing'] = pes_summary
    return results

