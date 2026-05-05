import pandas as pd
import numpy as np
import scipy.stats as stats
import sys
import os

sys.path.append(os.path.abspath("analysis"))
import robust_statistics as rs

COMPONENTS_PATH = "docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
OUTPUT_DIR = "docs/audit_legacy/Stage L/L4_results"

def load_data():
    return pd.read_csv(COMPONENTS_PATH)

def extract_target_component(df, target_col):
    return df.dropna(subset=[target_col]).copy()

def run_exgaussian(df):
    """Removed per L6 Standard. Replaced by Component Percentiles mapping (Median, MAD, IQR)."""
    results = []
    components = [('Delta V4 (Color)', 'delta_v4'), ('Delta V5/MT (Shift)', 'delta_v5_mt')]
    for comp_name, comp_col in components:
        comp_df = extract_target_component(df, comp_col)
        if len(comp_df) > 0:
            results.append({
                'component': comp_name,
                'median_ms': rs.median_value(comp_df[comp_col]),
                'mad_ms': rs.mad_value(comp_df[comp_col]),
                'iqr_ms': rs.iqr_value(comp_df[comp_col])
            })
    return pd.DataFrame(results)

def run_psi_sensitivity(df):
    """PSI Sensitivity mapped via median bins rather than linear regression on means."""
    results = []
    components = [('Delta V4 (Color)', 'delta_v4'), ('Delta V5/MT (Shift)', 'delta_v5_mt')]
    
    for comp_name, comp_col in components:
        comp_df = extract_target_component(df, comp_col)
        if len(comp_df) > 5:
            # Create PSI bins, exactly 3 quantiles (short, med, long)
            comp_df['psi_bin'] = pd.qcut(comp_df['psi'], q=3, labels=['short', 'medium', 'long'], duplicates='drop')
            grp = comp_df.groupby('psi_bin')[comp_col].median()
            
            val_short = grp.get('short', np.nan)
            val_med = grp.get('medium', np.nan)
            val_long = grp.get('long', np.nan)
            
            results.append({
                'component': comp_name,
                'median_short_psi_ms': val_short,
                'median_medium_psi_ms': val_med,
                'median_long_psi_ms': val_long,
                'psi_long_vs_short_ms': val_long - val_short if not pd.isna(val_long) and not pd.isna(val_short) else np.nan
            })
    return pd.DataFrame(results)

def run_lateralization(df):
    """Extract lateralization indices using Deltas via median."""
    results = []
    components = [('Delta V4 (Color)', 'delta_v4'), ('Delta V5/MT (Shift)', 'delta_v5_mt')]
    
    for comp_name, comp_col in components:
        comp_df = extract_target_component(df, comp_col)
        
        left_vals = comp_df[comp_df['stim_pos'] == 'left'][comp_col]
        center_vals = comp_df[comp_df['stim_pos'] == 'center'][comp_col]
        right_vals = comp_df[comp_df['stim_pos'] == 'right'][comp_col]
        
        left_delta = rs.median_value(left_vals) if len(left_vals) > 0 else np.nan
        center_delta = rs.median_value(center_vals) if len(center_vals) > 0 else np.nan
        right_delta = rs.median_value(right_vals) if len(right_vals) > 0 else np.nan
        
        results.append({
            'component': comp_name,
            'Delta_left_ms': left_delta,
            'Delta_center_ms': center_delta,
            'Delta_right_ms': right_delta,
            'lateralization_index_ms': right_delta - left_delta if not pd.isna(right_delta) and not pd.isna(left_delta) else np.nan
        })
    return pd.DataFrame(results)

def run_dynamics(df):
    """Extract intra-series dynamic sequence parameters on Deltas via rank correlation."""
    results = []
    components = [('Delta V4 (Color)', 'delta_v4'), ('Delta V5/MT (Shift)', 'delta_v5_mt')]
    
    for comp_name, comp_col in components:
        comp_df = extract_target_component(df, comp_col)
        seq_medians = comp_df.groupby('stimulus_index')[comp_col].median().sort_index()
        
        if len(seq_medians) > 2:
            x = np.arange(1, len(seq_medians)+1)
            corr, pval = stats.spearmanr(x, seq_medians.values)
            
            results.append({
                'component': comp_name,
                'trend_spearman_rho': corr,
                'trend_pval': pval,
                'series_start_delta_ms': seq_medians.iloc[0],
                'series_end_delta_ms': seq_medians.iloc[-1]
            })
    return pd.DataFrame(results)

if __name__ == "__main__":
    df = load_data()
    print("Data loaded from components dataset.")
