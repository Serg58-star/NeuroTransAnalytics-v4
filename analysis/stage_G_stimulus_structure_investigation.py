import sys
import os
import sqlite3
import pandas as pd
import numpy as np
import math
from scipy.stats import chi2_contingency
from scipy.stats import spearmanr

# Constants
DB_PATH = "C:/NeuroTransAnalytics-v4/data/neuro_data.db"
L_DATASET_PATH = "C:/NeuroTransAnalytics-v4/docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
OUT_DIR = "C:/NeuroTransAnalytics-v4/docs/audit_legacy/Stage G/G_results"

def load_data():
    print("Loading empirical data...")
    conn = sqlite3.connect(DB_PATH)
    
    # We must load metadata from the original Python script as they aren't fully materialized in this db
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(DB_PATH)))
    from data.test_metadata_old import TestMetadataManager
    
    tm = TestMetadataManager()
    
    # Load Stage L Component Dataset for RT and Deltas FIRST to get subjects/sessions
    try:
         df_components = pd.read_csv(L_DATASET_PATH)
         df_sessions = df_components[['subject_id', 'session_id']].drop_duplicates()
    except FileNotFoundError:
         print(f"CRITICAL: Component dataset not found at {L_DATASET_PATH}")
         df_components = pd.DataFrame(columns=['subject_id', 'session_id', 'stimulus_index', 'rt', 'delta_v4', 'delta_v5_mt'])
         df_sessions = pd.DataFrame(columns=['subject_id', 'session_id'])
    
    # 1. Process color_red metadata
    records_color = []
    for s in tm.get_test_metadata('color_red').stimuli:
        records_color.append({
            'test_type': 'color_red',
            'stimulus_index': s.stimulus_number,
            'position': s.position,
            'color': s.color,
            'psi': s.prestimulus_interval,
            'mask_triples': s.circle_sequence,
            'test_triple': None # we dont have test_triple for stage g technically, but preserving signature
        })
    df_color_meta = pd.DataFrame(records_color)
    df_color = df_sessions.assign(key=1).merge(df_color_meta.assign(key=1), on='key').drop('key', axis=1)
    
    # 2. Process shift metadata
    records_shift = []
    for s in tm.get_test_metadata('shift').stimuli:
        records_shift.append({
            'test_type': 'shift',
            'stimulus_index': s.stimulus_number,
            'position': s.position,
            'color': s.color,
            'psi': s.prestimulus_interval,
            'mask_triples': s.circle_sequence,
            'test_triple': None
        })
    df_shift_meta = pd.DataFrame(records_shift)
    df_shift = df_sessions.assign(key=1).merge(df_shift_meta.assign(key=1), on='key').drop('key', axis=1)
    
    df_meta = pd.concat([df_color, df_shift], ignore_index=True)
    conn.close()
    
    # Merge on subject, session, index
    # First drop redundant columns from df_components to avoid suffixing
    cols_to_drop = ['test_type', 'color', 'psi', 'stim_pos', 'start_pos', 'stimulus_id', 'col']
    df_comp_clean = df_components.drop(columns=[c for c in cols_to_drop if c in df_components.columns])
    
    df = pd.merge(df_meta, df_comp_clean, on=['subject_id', 'session_id', 'stimulus_index'], how='inner')
    
    # Rename position for consistency in later code if necessary (though meta provides 'position' already)
    # test_metadata uses 'left', 'right', 'center'. L dataset used 'stim_pos'
    print(f"Loaded {len(df)} joined trials. Columns: {list(df.columns)}")
    return df

def run_task_1(df):
    """T1: Positional Color Distribution"""
    print("\n--- Task 1: Positional Color Distribution ---")
    
    # Drop rows without color or position
    sub = df.dropna(subset=['color', 'position'])
    
    crosstab_perc = pd.crosstab(sub['position'], sub['color'], normalize='index')
    print("Probability Table P(color | position):")
    print(crosstab_perc)
    
    contingency = pd.crosstab(sub['position'], sub['color'])
    chi2, p, dof, expected = chi2_contingency(contingency)
    print(f"Chi-square statistic: {chi2:.2f}, p-value: {p:.4e}")
    
    res = "biased" if p < 0.05 else "uniform"
    print(f"Conclusion: {res}")
    
    return crosstab_perc, chi2, p, res

def run_task_2(df):
    """T2: Context Triple Sequence Structure"""
    print("\n--- Task 2: Triple Sequence Structure ---")
    
    def dominant_color(mask):
        if not isinstance(mask, str): return np.nan
        j_count = mask.count('Ж')
        s_count = mask.count('С')
        if j_count > s_count: return 1  # Green dominant
        elif s_count > j_count: return -1 # Blue dominant
        else: return 0
        
    df['dominant'] = df['mask_triples'].apply(dominant_color)
    sub = df.dropna(subset=['dominant']).copy()
    
    autocorr = {}
    for lag in range(1, 11):
        corr = sub['dominant'].autocorr(lag=lag)
        autocorr[f'lag_{lag}'] = corr
        
    print("Autocorrelations (lags 1-10):")
    for k, v in autocorr.items():
        print(f"{k}: {v:.3f}")
        
    res = "slow context dynamics" if any(abs(v) > 0.1 and not pd.isna(v) for v in autocorr.values()) else "random sequence"
    print(f"Conclusion: {res}")
    
    return autocorr, res

def run_task_3(df):
    """T3: ContextTriple vs PSI"""
    print("\n--- Task 3: ContextTriple vs PSI ---")
    
    sub = df.dropna(subset=['psi', 'dominant']).copy()
    if len(sub) == 0:
        print("No valid data.")
        return None, None, "no data"
        
    sub['psi_bin'] = pd.qcut(sub['psi'], q=5, duplicates='drop')
    
    contingency = pd.crosstab(sub['psi_bin'], sub['dominant'])
    chi2, p, dof, expected = chi2_contingency(contingency)
    
    print(f"Chi-square statistic (Dominant Color vs PSI Bin): {chi2:.2f}, p-value: {p:.4e}")
    
    res = "structured relationship" if p < 0.05 else "independent"
    print(f"Conclusion: {res}")
    return chi2, p, res

def run_task_4(df):
    """T4: Color Balance Trajectory"""
    print("\n--- Task 4: Color Balance Trajectory ---")
    
    dfs = df.dropna(subset=['dominant', 'stimulus_index']).sort_values(by=['subject_id', 'stimulus_index']).copy()
    if len(dfs) == 0:
        print("No valid data.")
        return None, None, "no data"
        
    # Moving averages
    dfs['dominant_smooth_3'] = dfs.groupby('subject_id')['dominant'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    dfs['dominant_smooth_7'] = dfs.groupby('subject_id')['dominant'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    
    corr, p = spearmanr(dfs['stimulus_index'], dfs['dominant'])
    print(f"Spearman correlation (index vs dominant): {corr:.3f}, p-value: {p:.4e}")
    
    res = "P/K channel balance drift" if p < 0.05 else "stable"
    print(f"Conclusion: {res}")
    return corr, p, res

def run_task_5(df):
    """T5: Channel Balance Map"""
    print("\n--- Task 5: Channel Balance Map ---")
    
    def count_colors(mask, char):
        if not isinstance(mask, str): return np.nan
        return mask.count(char)
        
    df['P_green'] = df['mask_triples'].apply(lambda x: count_colors(x, 'Ж'))
    df['K_blue'] = df['mask_triples'].apply(lambda x: count_colors(x, 'С'))
    df['R_red'] = df['mask_triples'].apply(lambda x: count_colors(x, 'К'))
    
    sub = df.dropna(subset=['delta_v4', 'dominant']).copy()
    if len(sub) > 0:
        median_p = sub[sub['dominant'] == 1]['delta_v4'].median()
        median_k = sub[sub['dominant'] == -1]['delta_v4'].median()
        print(f"Median delta_v4 (Green Dominant): {median_p:.2f}")
        print(f"Median delta_v4 (Blue Dominant): {median_k:.2f}")
        
        corr, p = spearmanr(sub['P_green'], sub['delta_v4'])
        print(f"Spearman correlation (Num Green vs Delta V4): {corr:.3f}, p-value: {p:.4e}")
    
    return

def run_task_6(df):
    """T6: Position-weighted Channel Model"""
    print("\n--- Task 6: Position-weighted Channel Model ---")
    
    sub = df.dropna(subset=['delta_v4', 'position']).copy()
    if len(sub) == 0:
        print("No valid Delta V4 data.")
        return
        
    med_center = sub[sub['position'] == 'center']['delta_v4'].median()
    med_left = sub[sub['position'] == 'left']['delta_v4'].median()
    med_right = sub[sub['position'] == 'right']['delta_v4'].median()
    
    print(f"Median delta_v4: Left={med_left:.2f}, Center={med_center:.2f}, Right={med_right:.2f}")
    
    if (med_center < med_left) and (med_center < med_right):
        print("Central position shows stronger perceptual extraction (lower RT).")
    else:
        print("No central advantage found.")
        
    return med_left, med_center, med_right

def run_task_7(df):
    """T7: Context Complexity Index"""
    print("\n--- Task 7: Context Complexity Index ---")
    
    def triple_entropy(s):
        if not isinstance(s, str): return np.nan
        counts = {'Ж': s.count('Ж'), 'С': s.count('С'), 'К': s.count('К')}
        total = sum(counts.values())
        if total == 0: return np.nan
        ent = 0
        for v in counts.values():
            if v > 0:
                p = v / total
                ent -= p * math.log2(p)
        return ent
        
    df['context_entropy'] = df['mask_triples'].apply(triple_entropy)
    
    sub = df.dropna(subset=['context_entropy', 'delta_v4']).copy()
    if len(sub) > 0:
        corr, p = spearmanr(sub['context_entropy'], sub['delta_v4'])
        print(f"Spearman correlation (Context Entropy vs Delta V4): {corr:.3f}, p-value: {p:.4e}")
    return

def run_task_8(df):
    """T8: PSI-Context Interaction"""
    print("\n--- Task 8: PSI-Context Interaction ---")
    
    sub = df.dropna(subset=['psi', 'delta_v4', 'dominant']).copy()
    if len(sub) == 0:
        print("No data.")
        return
        
    df_g = sub[sub['dominant'] == 1].copy()
    df_b = sub[sub['dominant'] == -1].copy()
    
    if len(df_g) > 0 and len(df_b) > 0:
        corr_g, _ = spearmanr(df_g['psi'], df_g['delta_v4'])
        corr_b, _ = spearmanr(df_b['psi'], df_b['delta_v4'])
        print(f"PSI vs DeltaV4 correlation (Green Dominant): {corr_g:.3f}")
        print(f"PSI vs DeltaV4 correlation (Blue Dominant): {corr_b:.3f}")
    return

def run_task_9(df):
    """T9: Stimulus Index Drift"""
    print("\n--- Task 9: Stimulus Index Drift ---")
    
    def get_block(idx):
        if pd.isna(idx): return np.nan
        if idx <= 12: return 'early'
        elif idx <= 24: return 'mid'
        else: return 'late'
        
    df['block'] = df['stimulus_index'].apply(get_block)
    sub = df.dropna(subset=['block']).copy()
    
    if len(sub) > 0:
        block_dist = pd.crosstab(sub['block'], sub['color'], normalize='index')
        print("Color distribution across blocks:")
        print(block_dist)
        
        if 'dominant' in sub.columns:
            dom_sub = sub.dropna(subset=['dominant'])
            dom_dist = pd.crosstab(dom_sub['block'], dom_sub['dominant'], normalize='index')
            print("\nDominant context across blocks:")
            print(dom_dist)
            
            res = "protocol drift" if abs(dom_dist.iloc[0,0] - dom_dist.iloc[-1,0]) > 0.05 else "stable distribution"
            print(f"Conclusion: {res}")
    return

def run_task_10(df):
    """T10: Perceptual Contrast Index"""
    print("\n--- Task 10: Perceptual Contrast ---")
    
    # Delta E mock computation proxy (weighting Red higher contrast vs Azure BG)
    def approx_contrast(s):
        if not isinstance(s, str): return np.nan
        return s.count('К') * 1.5 + s.count('Ж') * 1.2 + s.count('С') * 1.0 # arbitrary luminance map
        
    df['perceptual_contrast'] = df['mask_triples'].apply(approx_contrast)
    sub = df.dropna(subset=['perceptual_contrast', 'delta_v4']).copy()
    
    if len(sub) > 0:
        corr, p = spearmanr(sub['perceptual_contrast'], sub['delta_v4'])
        print(f"Spearman correlation (Contrast vs Delta V4): {corr:.3f}, p-value: {p:.4e}")
    return

def run_all_tasks():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()
    
    with open(os.path.join(OUT_DIR, "stage_G_structural_logs.txt"), 'w', encoding='utf-8') as f:
        import sys
        
        class Logger:
            def __init__(self, filename):
                self.terminal = sys.stdout
                self.log = open(filename, "w", encoding='utf-8')

            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)

            def flush(self):
                self.terminal.flush()
                self.log.flush()
                
        sys.stdout = Logger(os.path.join(OUT_DIR, "stage_G_structural_logs.txt"))
        
        run_task_1(df)
        run_task_2(df)
        run_task_3(df)
        run_task_4(df)
        run_task_5(df)
        run_task_6(df)
        run_task_7(df)
        run_task_8(df)
        run_task_9(df)
        run_task_10(df)
        
        sys.stdout = sys.stdout.terminal
        print("\nAnalysis complete. Logs saved to G_results.")
        
        # Save output data specifically for the final report
        df.to_csv(os.path.join(OUT_DIR, "G_investigation_compiled_data.csv"), index=False)

if __name__ == "__main__":
    run_all_tasks()
