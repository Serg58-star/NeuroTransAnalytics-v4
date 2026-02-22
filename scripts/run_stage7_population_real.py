"""
scripts/run_stage7_population_real.py

Executes the Stage 7 Population Geometry Audit on REAL experimental data.
Extracts the validated 3D Trait Core (Speed Axis, Lateral Axis, Residual Tone)
from the PCA of delta-V4/V5 residuals, testing it against the population continuum.
"""

import sys
import os
import sqlite3
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor
from src.c3x_exploratory.population_geometry import PopulationGeometryAnalysis

plt.style.use('ggplot')

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
LINEAR_CSV = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression" / "linear_regression_results.csv"
OUT_DIR = PROJECT_ROOT / "results" / "stage7_population_geometry"

MODEL_MAP = {
    "delta_v4_left":  "median_dv1_left",
    "delta_v4_right": "median_dv1_right",
    "delta_v5_left":  "median_dv1_left",
    "delta_v5_right": "median_dv1_right",
}

CORE_RESIDUALS = [
    "delta_v4_left_residual",
    "delta_v4_right_residual",
    "delta_v5_left_residual",
    "delta_v5_right_residual",
]

# ============================================================================
# DATA EXTRACTION (From Stage 4/5)
# ============================================================================

def load_features(database_path: str) -> pd.DataFrame:
    print("[1/4] Loading trial data from neuro_data.db...")
    conn = sqlite3.connect(database_path)
    trials_query = """
    SELECT 
        t.trial_id, t.subject_id, t.test_date,
        t.tst1_1, t.tst1_2, t.tst1_3, t.tst1_4, t.tst1_5, t.tst1_6,
        t.tst1_7, t.tst1_8, t.tst1_9, t.tst1_10, t.tst1_11, t.tst1_12,
        t.tst1_13, t.tst1_14, t.tst1_15, t.tst1_16, t.tst1_17, t.tst1_18,
        t.tst1_19, t.tst1_20, t.tst1_21, t.tst1_22, t.tst1_23, t.tst1_24,
        t.tst1_25, t.tst1_26, t.tst1_27, t.tst1_28, t.tst1_29, t.tst1_30,
        t.tst1_31, t.tst1_32, t.tst1_33, t.tst1_34, t.tst1_35, t.tst1_36,
        t.tst2_1, t.tst2_2, t.tst2_3, t.tst2_4, t.tst2_5, t.tst2_6,
        t.tst2_7, t.tst2_8, t.tst2_9, t.tst2_10, t.tst2_11, t.tst2_12,
        t.tst2_13, t.tst2_14, t.tst2_15, t.tst2_16, t.tst2_17, t.tst2_18,
        t.tst2_19, t.tst2_20, t.tst2_21, t.tst2_22, t.tst2_23, t.tst2_24,
        t.tst2_25, t.tst2_26, t.tst2_27, t.tst2_28, t.tst2_29, t.tst2_30,
        t.tst2_31, t.tst2_32, t.tst2_33, t.tst2_34, t.tst2_35, t.tst2_36,
        t.tst3_1, t.tst3_2, t.tst3_3, t.tst3_4, t.tst3_5, t.tst3_6,
        t.tst3_7, t.tst3_8, t.tst3_9, t.tst3_10, t.tst3_11, t.tst3_12,
        t.tst3_13, t.tst3_14, t.tst3_15, t.tst3_16, t.tst3_17, t.tst3_18,
        t.tst3_19, t.tst3_20, t.tst3_21, t.tst3_22, t.tst3_23, t.tst3_24,
        t.tst3_25, t.tst3_26, t.tst3_27, t.tst3_28, t.tst3_29, t.tst3_30,
        t.tst3_31, t.tst3_32, t.tst3_33, t.tst3_34, t.tst3_35, t.tst3_36
    FROM trials t
    INNER JOIN users u ON t.subject_id = u.subject_id
    """
    trials_wide = pd.read_sql_query(trials_query, conn)
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    print("[2/4] Reshaping and extracting subject traits...")
    trial_level_data = []
    for _, session_row in trials_wide.iterrows():
        subject_id = session_row['subject_id']
        trial_id = session_row['trial_id']
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst1_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_simple[metadata_simple['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id, 'test_type': 'Tst1', 
                    'stimulus_id': stimulus_id, 'stimulus_location': meta['position'], 
                    'stimulus_color': meta['color'], 'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst2_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_color[metadata_color['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id, 'test_type': 'Tst2', 
                    'stimulus_id': stimulus_id, 'stimulus_location': meta['position'], 
                    'stimulus_color': 'red', 'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst3_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_shift[metadata_shift['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id, 'test_type': 'Tst3', 
                    'stimulus_id': stimulus_id, 'stimulus_location': meta['position'], 
                    'stimulus_color': meta['color'], 'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

    trials_df = pd.DataFrame(trial_level_data)
    extractor = BaselineFeatureExtractor()
    features_list = []
    for subject_id in trials_df['subject_id'].unique():
        subject_trials = trials_df[trials_df['subject_id'] == subject_id].copy()
        try:
            features = extractor.extract_subject_features(subject_trials)
            if isinstance(features, dict):
                features['subject_id'] = subject_id
                features_list.append(features)
        except Exception:
            continue

    features_df = pd.DataFrame(features_list).set_index('subject_id')
    return features_df

def reconstruct_residuals(features_df, linear_csv):
    print("[3/4] Reconstructing structural core residuals...")
    residuals_df = pd.DataFrame(index=features_df.index)
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in linear_csv.index:
            continue
        if outcome not in features_df.columns or predictor not in features_df.columns:
            continue
        beta = linear_csv.loc[outcome, 'beta']
        intercept = linear_csv.loc[outcome, 'intercept']
        data = features_df[[outcome, predictor]].dropna()
        y_pred = beta * data[predictor] + intercept
        residuals_df.loc[data.index, f"{outcome}_residual"] = data[outcome] - y_pred
    return residuals_df

def extract_3d_state_space(residuals_df):
    print("[4/4] Executing PCA to isolate the 3D axes (Speed, Lateral, Residual Tone)...")
    core_data = residuals_df[CORE_RESIDUALS].dropna()
    
    scaler = StandardScaler()
    X_std = scaler.fit_transform(core_data.values)
    
    pca = PCA(n_components=3, random_state=42)
    scores = pca.fit_transform(X_std)
    
    return scores, core_data.index

# ============================================================================
# EXECUTION
# ============================================================================

def plot_gap_statistic(k_range, gaps, title, filename):
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, gaps, marker='o', linestyle='-', color='indigo')
    plt.title(title)
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Gap Statistic")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

def plot_3d_scatter(X: np.ndarray, title: str, filename: str):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, s=20, c='royalblue')
    
    ax.set_title(title)
    ax.set_xlabel("PC1 (Speed Axis)")
    ax.set_ylabel("PC2 (Lateral Axis)")
    ax.set_zlabel("PC3 (Residual Tone)")
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def main():
    print("=" * 60)
    print("STAGE 7: POPULATION GEOMETRY AUDIT (REAL EXPERIMENTAL DATA)")
    print("=" * 60)

    if not DATABASE_PATH.exists():
        print(f"ERROR: Database not found: {DATABASE_PATH}")
        return 1
    if not LINEAR_CSV.exists():
        print(f"ERROR: Linear CSV not found: {LINEAR_CSV}")
        return 1
        
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    features_df = load_features(str(DATABASE_PATH))
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    
    X_3d, subject_ids = extract_3d_state_space(residuals_df)
    
    print(f"\nConstructed 3D Latent State Space (N={X_3d.shape[0]})")
    
    # Analyze Geometry using Stage 7 Logic
    print("-" * 60)
    print("Running Formal Geometry Analysis Procedure...")
    analysis = PopulationGeometryAnalysis()
    res = analysis.execute(X_3d)
    
    print(f"\n[Architectural Compliance]\n{analysis.non_interpretation_clause}\n")
    print(f"Hopkins Statistic: {res['density']['hopkins']:.3f} (expect < 0.85 for Continuum)")
    best_sil = max(res['clustering']['metrics']['kmeans']['silhouette'])
    print(f"Best KMeans Silhouette: {best_sil:.3f}")
    print(f"Gap Optimal k: {res['gap']['optimal_k']}")
    
    print(f"\n>>> FINAL VERDICT: {res['conclusion']}")
    
    # Plotting
    plot_3d_scatter(X_3d, "Real Data Population - 3D State Space", OUT_DIR / "real_data_3d.png")
    plot_gap_statistic(list(range(1, 9)), res['gap']['scores'], "Gap Statistic: Real Experimental Data", OUT_DIR / "gap_real_data.png")
    
    with open(OUT_DIR / "results_real_data.json", "w") as f:
        json.dump(res, f, indent=2)
        
    print("\n" + "=" * 60)
    print(f"Analysis complete. Artifacts saved to '{OUT_DIR}'")

    return 0

if __name__ == "__main__":
    exit(main())
