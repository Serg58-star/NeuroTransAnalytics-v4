import sys
import os
import sqlite3
import pandas as pd
import numpy as np
import math
from scipy.stats import spearmanr, entropy
from collections import Counter
from sklearn.cluster import KMeans

# Constants
DB_PATH = "C:/NeuroTransAnalytics-v4/data/neuro_data.db"
L_DATASET_PATH = "C:/NeuroTransAnalytics-v4/docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
OUT_DIR = "C:/NeuroTransAnalytics-v4/docs/audit_legacy/Stage G/G_results_ecology"

def load_data():
    print("Loading empirical data...")
    conn = sqlite3.connect(DB_PATH)
    
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(DB_PATH)))
    from data.test_metadata_old import TestMetadataManager
    
    tm = TestMetadataManager()
    
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
        })
    df_shift_meta = pd.DataFrame(records_shift)
    df_shift = df_sessions.assign(key=1).merge(df_shift_meta.assign(key=1), on='key').drop('key', axis=1)
    
    df_meta = pd.concat([df_color, df_shift], ignore_index=True)
    conn.close()
    
    cols_to_drop = ['test_type', 'color', 'psi', 'stim_pos', 'start_pos', 'stimulus_id', 'col']
    df_comp_clean = df_components.drop(columns=[c for c in cols_to_drop if c in df_components.columns])
    
    df = pd.merge(df_meta, df_comp_clean, on=['subject_id', 'session_id', 'stimulus_index'], how='inner')
    
    print(f"Loaded {len(df)} joined trials.")
    return df

def run_task_a(df):
    """Task A: Real Distribution of Context Triples"""
    print("\n--- Task A: Real Distribution of Context Triples ---")
    import re
    all_triples = []
    for mask in df['mask_triples'].dropna():
        all_triples.extend(re.findall(r'[СЖК]{3}', mask))
        
    if not all_triples:
        print("No valid triples found.")
        return None
        
    freqs = pd.Series(all_triples).value_counts(normalize=True) * 100
    print("Top 5 dominant triples (%):")
    print(freqs.head(5))
    print("\nBottom 5 rare triples (%):")
    print(freqs.tail(5))
    print(f"\nTotal unique triples used: {len(freqs)} out of 27.")
    return freqs

def run_task_b(df):
    """Task B: Channel Load of Context Triples"""
    print("\n--- Task B: Channel Load of Context Triples ---")
    def count_g(x): return x.count('Ж') if isinstance(x, str) else np.nan
    def count_b(x): return x.count('С') if isinstance(x, str) else np.nan
    def count_r(x): return x.count('К') if isinstance(x, str) else np.nan
    
    df['P_load'] = df['mask_triples'].apply(count_g)
    df['K_load'] = df['mask_triples'].apply(count_b)
    df['R_load'] = df['mask_triples'].apply(count_r)
    
    sub = df.dropna(subset=['P_load', 'K_load', 'R_load'])
    print(f"Mean P load: {sub['P_load'].mean():.2f}, Variance: {sub['P_load'].var():.2f}")
    print(f"Mean K load: {sub['K_load'].mean():.2f}, Variance: {sub['K_load'].var():.2f}")
    print(f"Mean R load: {sub['R_load'].mean():.2f}, Variance: {sub['R_load'].var():.2f}")
    
    # Change over index
    corr_p, _ = spearmanr(sub['stimulus_index'], sub['P_load'])
    corr_k, _ = spearmanr(sub['stimulus_index'], sub['K_load'])
    print(f"Spearman(index, P_load): {corr_p:.3f}")
    print(f"Spearman(index, K_load): {corr_k:.3f}")
    return

def run_task_c(df):
    """Task C: Dynamics of Triple Sequence"""
    print("\n--- Task C: Dynamics of Triple Sequence ---")
    def dom(x):
        if not isinstance(x, str): return np.nan
        p, k = x.count('Ж'), x.count('С')
        if p > k: return 'GreenDom'
        elif k > p: return 'BlueDom'
        else: return 'Neutral'
    df['dom'] = df['mask_triples'].apply(dom)
    
    sub = df.dropna(subset=['dom']).sort_values(['subject_id', 'session_id', 'stimulus_index'])
    sub['next_dom'] = sub.groupby(['subject_id', 'session_id'])['dom'].shift(-1)
    
    trans = pd.crosstab(sub['dom'], sub['next_dom'], normalize='index')
    print("Transition Matrix (Dom -> NextDom):")
    print(trans)
    return

def run_task_d(df):
    """Task D: Sensory Environment Before Target Signal"""
    print("\n--- Task D: Sensory Env Before Target Signal (N=3,5,7 windows) ---")
    sub = df.dropna(subset=['mask_triples']).sort_values(['subject_id', 'session_id', 'stimulus_index']).copy()
    
    sub['prev_P_3'] = sub.groupby(['subject_id', 'session_id'])['P_load'].transform(lambda x: x.shift(1).rolling(3, min_periods=1).sum())
    sub['prev_K_3'] = sub.groupby(['subject_id', 'session_id'])['K_load'].transform(lambda x: x.shift(1).rolling(3, min_periods=1).sum())
    
    sub['prev_P_5'] = sub.groupby(['subject_id', 'session_id'])['P_load'].transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
    sub['prev_K_5'] = sub.groupby(['subject_id', 'session_id'])['K_load'].transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
    
    sub['prev_P_7'] = sub.groupby(['subject_id', 'session_id'])['P_load'].transform(lambda x: x.shift(1).rolling(7, min_periods=1).sum())
    sub['prev_K_7'] = sub.groupby(['subject_id', 'session_id'])['K_load'].transform(lambda x: x.shift(1).rolling(7, min_periods=1).sum())
    
    df['prev_P_3'], df['prev_K_3'] = sub['prev_P_3'], sub['prev_K_3']
    df['prev_P_7'], df['prev_K_7'] = sub['prev_P_7'], sub['prev_K_7']
    
    print("Median accumulated loads before signal (N=3):")
    print(f"P (Green) accumulated: {sub['prev_P_3'].median():.2f}")
    print(f"K (Blue) accumulated: {sub['prev_K_3'].median():.2f}")
    
    print("\nMedian accumulated loads before signal (N=7):")
    print(f"P (Green) accumulated: {sub['prev_P_7'].median():.2f}")
    print(f"K (Blue) accumulated: {sub['prev_K_7'].median():.2f}")
    return

def run_task_e(df):
    """Task E: Relationship Between PSI and Context Environment"""
    print("\n--- Task E: PSI vs Context Environment ---")
    sub = df.dropna(subset=['psi', 'P_load', 'K_load', 'R_load'])
    sub['total_load'] = sub['P_load'] + sub['K_load'] + sub['R_load']
    
    corr, p = spearmanr(sub['psi'], sub['total_load'])
    print(f"Spearman(PSI, Total Load Length): {corr:.3f}, p={p:.3e}")
    
    corr_p, p_p = spearmanr(sub['psi'], sub['P_load'])
    print(f"Spearman(PSI, P_load): {corr_p:.3f}, p={p_p:.3e}")
    return

def run_task_f(df):
    """Task F: Complexity of Context Triples"""
    print("\n--- Task F: Complexity of Context Triples ---")
    import re
    import math
    def calc_mean_entropy(mask):
        if not isinstance(mask, str): return np.nan
        triples = re.findall(r'[СЖК]{3}', mask)
        if not triples: return np.nan
        ents = []
        for t in triples:
            c1, c2, c3 = t.count('Ж'), t.count('С'), t.count('К')
            ent = 0
            for c in (c1, c2, c3):
                if c > 0:
                    p = c / 3.0
                    ent -= p * math.log2(p)
            ents.append(ent)
        return sum(ents) / len(ents)
    
    df['complexity'] = df['mask_triples'].apply(calc_mean_entropy)
    
    print(f"Mean Triple Complexity (Entropy): {df['complexity'].mean():.3f}")
    print(f"Variance: {df['complexity'].var():.3f}")
    
    dist = pd.cut(df['complexity'].dropna(), bins=[-0.1, 0.1, 1.0, 1.6], labels=['Low (AAA)', 'Mid (AAB)', 'High (ABC)']).value_counts(normalize=True) * 100
    print("Complexity Distribution (%):")
    print(dist)
    return

def run_task_g(df):
    """Task G: Slow Dynamics of Stimulus Environment"""
    print("\n--- Task G: Slow Dynamics of Stimulus Environment ---")
    sub = df.sort_values(['subject_id', 'session_id', 'stimulus_index']).copy()
    sub['slow_P'] = sub.groupby(['subject_id', 'session_id'])['P_load'].transform(lambda x: x.rolling(12, min_periods=3).mean())
    sub['slow_compl'] = sub.groupby(['subject_id', 'session_id'])['complexity'].transform(lambda x: x.rolling(12, min_periods=3).mean())
    
    corr_p, _ = spearmanr(sub['stimulus_index'], sub['slow_P'], nan_policy='omit')
    corr_c, _ = spearmanr(sub['stimulus_index'], sub['slow_compl'], nan_policy='omit')
    print(f"Spearman(index, slow_P load): {corr_p:.3f}")
    print(f"Spearman(index, slow_complexity): {corr_c:.3f}")
    return

def run_task_h(df):
    """Task H: Signal Appearance Context"""
    print("\n--- Task H: Signal Appearance Context ---")
    sub = df.dropna(subset=['test_type', 'prev_P_3', 'prev_K_3'])
    
    p_red = sub[sub['test_type'] == 'color_red']['prev_P_3'].median()
    k_red = sub[sub['test_type'] == 'color_red']['prev_K_3'].median()
    
    p_shift = sub[sub['test_type'] == 'shift']['prev_P_3'].median()
    k_shift = sub[sub['test_type'] == 'shift']['prev_K_3'].median()
    
    print(f"Red target preceded by median loads: P={p_red:.2f}, K={k_red:.2f}")
    print(f"Shift preceded by median loads: P={p_shift:.2f}, K={k_shift:.2f}")
    return

def run_task_i(df):
    """Task I: Perceptual Contrast Relative to Background"""
    print("\n--- Task I: Perceptual Contrast ---")
    bg = np.array([43, 149, 255])
    col_map = {'Ж': np.array([10, 222, 16]), 'С': np.array([6, 0, 254]), 'К': np.array([254, 0, 0])}
    
    def rgb_dist(c1, c2):
        return np.linalg.norm(c1 - c2)
        
    def triple_contrast(mask):
        if not isinstance(mask, str): return np.nan
        total_dist = 0
        for char in mask:
            if char in col_map:
                total_dist += rgb_dist(bg, col_map[char])
        return total_dist / max(1, len(mask)) # average contrast per element
        
    df['contrast'] = df['mask_triples'].apply(triple_contrast)
    print(f"Mean Perceptual Contrast: {df['contrast'].mean():.2f}")
    
    corr_rt, p_rt = spearmanr(df['contrast'], df['rt'], nan_policy='omit')
    print(f"Spearman(Contrast, RT): {corr_rt:.3f}, p={p_rt:.3e}")
    return

def run_task_j(df):
    """Task J: Stimulus Environment Map"""
    print("\n--- Task J: Stimulus Environment Map Clustering ---")
    sub = df.dropna(subset=['P_load', 'K_load', 'complexity', 'contrast', 'psi']).copy()
    
    if len(sub) == 0:
         print("No data for clustering")
         return
         
    features = sub[['P_load', 'K_load', 'complexity', 'contrast', 'psi']]
    
    # Normalize
    f_norm = (features - features.mean()) / features.std()
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    sub['cluster'] = kmeans.fit_predict(f_norm)
    
    print("Cluster Centers (Standardized):")
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=features.columns)
    print(centers)
    
    sizes = sub['cluster'].value_counts(normalize=True) * 100
    print("\nCluster Sizes (%):")
    print(sizes)
    return

def run_all_tasks():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()
    
    with open(os.path.join(OUT_DIR, "stage_G_ecology_logs.txt"), 'w', encoding='utf-8') as f:
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
        
        sys.stdout = Logger(os.path.join(OUT_DIR, "stage_G_ecology_logs.txt"))
        
        run_task_a(df)
        run_task_b(df)
        run_task_c(df)
        run_task_d(df)
        run_task_e(df)
        run_task_f(df)
        run_task_g(df)
        run_task_h(df)
        run_task_i(df)
        run_task_j(df)
        
        sys.stdout = sys.stdout.terminal
        print("\nAnalysis complete. Logs saved to G_results_ecology.")
        
        df.to_csv(os.path.join(OUT_DIR, "G_ecology_compiled_data.csv"), index=False)

if __name__ == "__main__":
    run_all_tasks()
