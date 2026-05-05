import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DB_PATH = Path('C:/NeuroTransAnalytics-v4/neuro_data.db')
RESULTS_DIR = Path('C:/NeuroTransAnalytics-v4/docs/audit_legacy/Stage L/L_results')

def calculate_mad(series):
    """Calculates Median Absolute Deviation (MAD)."""
    median = series.median()
    return np.median(np.abs(series - median))

def extract_trials(session_id, phase, test_type, df):
    """
    Extracts chronological trials for a specific test and applies
    robust outlier filtering (Median ± 3.5 * MAD) per condition.
    """
    test_data = df[(df['session_id'] == session_id) & (df['test_type'] == test_type)].copy()
    if test_data.empty:
        return None, None
        
    test_data = test_data.sort_values(by='start_pos')
    
    # 1. Warmup exclusion: Only 36 trials are considered valid in legacy logic
    # In neuro_data, Tst1 block has warmup=3 (we rely on SQL for basic structural validity)
    # The 'rt' is the reaction time we care about.
    # 2. Legacy limits (135 <= RT <= 2000)
    
    total_trials = len(test_data)
    premature_errors = len(test_data[test_data['rt'] < 135])
    late_errors = len(test_data[test_data['rt'] > 2000])
    
    valid_data = test_data[(test_data['rt'] >= 135) & (test_data['rt'] <= 2000)].copy()
    
    # Robust Statistics Logic
    if len(valid_data) > 0:
        median_rt = valid_data['rt'].median()
        mad_rt = calculate_mad(valid_data['rt'])
        
        # 3.5 MAD threshold
        valid_data['robust_deviation'] = np.abs(valid_data['rt'] - median_rt) / mad_rt
        
        # Filter unstable responses
        filtered_data = valid_data[valid_data['robust_deviation'] <= 3.5].copy()
        
        # Compute final stable distributions
        final_median = filtered_data['rt'].median()
        final_mad = calculate_mad(filtered_data['rt'])
        
        # Stability flag: Stable if we retaining more than 75% of events without crazy deviation
        stable_flag = len(filtered_data) >= 25 # (Requires at least 25 solid trials for stable test session)
        
    else:
        median_rt = np.nan
        mad_rt = np.nan
        final_median = np.nan
        final_mad = np.nan
        filtered_data = pd.DataFrame()
        stable_flag = False

    error_metrics = {
        'total_trials': total_trials,
        'premature_count': premature_errors,
        'late_count': late_errors,
        'mad_outliers': len(valid_data) - len(filtered_data)
    }

    distribution_pack = {
        'median_rt': final_median,
        'mad_rt': final_mad,
        'q25_rt': filtered_data['rt'].quantile(0.25) if len(filtered_data)>0 else np.nan,
        'q75_rt': filtered_data['rt'].quantile(0.75) if len(filtered_data)>0 else np.nan,
        'is_stable': stable_flag
    }

    return filtered_data, error_metrics, distribution_pack

def run_extraction_pipeline():
    """Reads SQL, filters out RTs, and generates components."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
def run_extraction_pipeline():
    """Reads SQL, filters out RTs, and generates components."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Load trials
    df_trials = pd.read_sql_query("SELECT * FROM trials", conn)
    
    # Load metadata
    df_meta_simple = pd.read_sql_query("SELECT stimulus_id, position as field, psi_ms as psi, color FROM metadata_simple", conn)
    df_meta_color = pd.read_sql_query("SELECT stimulus_id, position as field, psi_ms as psi, color FROM metadata_color_red", conn)
    df_meta_shift = pd.read_sql_query("SELECT stimulus_id, position as field, psi_ms as psi, color FROM metadata_shift", conn)
    
    conn.close()
    
    # Helper to generate exactly the 36 reaction time columns
    def get_rt_cols(prefix):
        return [f"{prefix}_{i}" for i in range(1, 37)]

    # Unpivot Tst1 (Simple)
    tst1_cols = get_rt_cols('tst1')
    df_tst1 = df_trials.melt(id_vars=['subject_id', 'trial_id'], value_vars=tst1_cols, var_name='col', value_name='rt')
    df_tst1['stimulus_index'] = df_tst1['col'].str.replace('tst1_', '').astype(int)
    df_tst1['test_type'] = 'simple'
    df_tst1 = df_tst1.merge(df_meta_simple, left_on='stimulus_index', right_on='stimulus_id', how='left')
    
    # Unpivot Tst2 (Color)
    tst2_cols = get_rt_cols('tst2')
    df_tst2 = df_trials.melt(id_vars=['subject_id', 'trial_id'], value_vars=tst2_cols, var_name='col', value_name='rt')
    df_tst2['stimulus_index'] = df_tst2['col'].str.replace('tst2_', '').astype(int)
    # The actual docs say Tst2 is Color! Let's align with the documentation `2_Research_Axes_and_Test_Conditions_v4`.
    df_tst2['test_type'] = 'color'
    df_tst2 = df_tst2.merge(df_meta_color, left_on='stimulus_index', right_on='stimulus_id', how='left')

    # Unpivot Tst3 (Motion/Shift)
    tst3_cols = get_rt_cols('tst3')
    df_tst3 = df_trials.melt(id_vars=['subject_id', 'trial_id'], value_vars=tst3_cols, var_name='col', value_name='rt')
    df_tst3['stimulus_index'] = df_tst3['col'].str.replace('tst3_', '').astype(int)
    df_tst3['test_type'] = 'shift'
    df_tst3 = df_tst3.merge(df_meta_shift, left_on='stimulus_index', right_on='stimulus_id', how='left')

    df_events = pd.concat([df_tst1, df_tst2, df_tst3], ignore_index=True)
    
    # Clean up empty non-reactions
    df_events = df_events.dropna(subset=['rt'])
    df_events = df_events[df_events['rt'] > 0]
    
    # Rename columns to match the extraction logic
    df_events.rename(columns={'trial_id': 'session_id', 'field': 'stim_pos'}, inplace=True)
    df_events['start_pos'] = df_events['stimulus_index']
    
    component_metrics = []
    
    # Ensure correct types
    df_events['rt'] = df_events['rt'].astype(float)
    
    # 2. Legacy limits (135 <= RT <= 2000)
    df_valid = df_events[(df_events['rt'] >= 135) & (df_events['rt'] <= 2000)].copy()
    
    # 3. Robust Statistics (Median ± 3.5 * MAD) per session & test_type
    def compute_mad(x):
        return np.median(np.abs(x - x.median()))
        
    grouped = df_valid.groupby(['session_id', 'test_type'])['rt']
    medians = grouped.transform('median')
    mads = grouped.transform(compute_mad)
    
    # Avoid zero-division in MAD
    mads = mads.replace(0, 1e-6)
    
    df_valid['robust_deviation'] = np.abs(df_valid['rt'] - medians) / mads
    df_filtered = df_valid[df_valid['robust_deviation'] <= 3.5].copy()
    
    # Calculate final components -> Delta V1 goes from Simple (Tst1) test
    # Get session-level Delta V1 (Median of stable Simple test RTs)
    v1_baselines = df_filtered[df_filtered['test_type'] == 'simple'].groupby('session_id')['rt'].median().reset_index()
    v1_baselines.rename(columns={'rt': 'delta_v1'}, inplace=True)
    
    df_components = df_filtered.merge(v1_baselines, on='session_id', how='inner')
    
    # Calculate components
    df_components['delta_v4'] = np.nan
    df_components['delta_v5_mt'] = np.nan
    
    # Delta V4 (Color subset)
    color_mask = df_components['test_type'] == 'color'
    df_components.loc[color_mask, 'delta_v4'] = df_components.loc[color_mask, 'rt'] - df_components.loc[color_mask, 'delta_v1']
    df_components.loc[color_mask & (df_components['delta_v4'] < 0), 'delta_v4'] = np.nan
    
    # Delta V5/MT (Shift subset)
    shift_mask = df_components['test_type'] == 'shift'
    df_components.loc[shift_mask, 'delta_v5_mt'] = df_components.loc[shift_mask, 'rt'] - df_components.loc[shift_mask, 'delta_v1']
    df_components.loc[shift_mask & (df_components['delta_v5_mt'] < 0), 'delta_v5_mt'] = np.nan

    # Save dataset
    df_components.to_csv(RESULTS_DIR / 'L_component_dataset.csv', index=False)
    
    print(f"Extraction successful. Generated {len(df_components)} component records.")
    return df_components

if __name__ == '__main__':
    run_extraction_pipeline()
