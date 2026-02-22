"""
scripts/run_task37_extended_dynamics.py

Executes Stage 8: Extended Trait-State Dynamics & Stress Audit.
Projects trial-level sequential rolling windows into the Stage 7 3D Latent Space.
Calculates ICC, Path Trajectories, Temporal Structure (Hurst), and Noise Tolerance.
"""

import sys
import os
import sqlite3
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor

# ============================================================================
# CONFIG / HARDCODED VARIABLES (FROM STAGE 7)
# ============================================================================
DATABASE_PATH = Path(__file__).parent.parent / "neuro_data.db"
LINEAR_CSV = Path(__file__).parent.parent / "data" / "exploratory" / "symmetric_regression" / "linear_regression_results.csv"
OUT_DIR = Path(__file__).parent.parent / "results" / "task37_extended_dynamics"

MODEL_MAP = {
    "delta_v4_left":  "median_dv1_left",
    "delta_v4_right": "median_dv1_right",
    "delta_v5_left":  "median_dv1_left",
    "delta_v5_right": "median_dv1_right",
}

CORE_RESIDUALS = [
    "delta_v4_left_residual", "delta_v4_right_residual",
    "delta_v5_left_residual", "delta_v5_right_residual",
]

# ============================================================================
# 1. DATA EXTRACTION & ROLLING TRAJECTORIES
# ============================================================================

def load_demographics_and_trials():
    """Load trials and merge sex/gender from the users table."""
    conn = sqlite3.connect(DATABASE_PATH)
    trials_query = "SELECT * FROM trials"
    trials_wide = pd.read_sql_query(trials_query, conn)
    
    users = pd.read_sql_query("SELECT subject_id, gender FROM users", conn)
    # Map gender 0 -> False, 1 -> True, or directly as string
    users['sex_str'] = users['gender'].map({0: 'Female', 1: 'Male'})
    
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()
    
    return trials_wide, users, metadata_simple, metadata_color, metadata_shift

def convert_to_trial_df(session_row, metadata_simple, metadata_color, metadata_shift, stim_indices):
    """Filters a subject's session into just the selected stimulus (chronological) indices."""
    trial_level_data = []
    sid = session_row['subject_id']
    
    for stim in stim_indices:
        # Tst1
        rt = session_row[f'tst1_{stim}']
        if pd.notna(rt) and rt > 0:
            m = metadata_simple[metadata_simple['stimulus_id'] == stim].iloc[0]
            trial_level_data.append({'subject_id': sid, 'test_type': 'Tst1', 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        
        # Tst2
        rt = session_row[f'tst2_{stim}']
        if pd.notna(rt) and rt > 0:
            m = metadata_color[metadata_color['stimulus_id'] == stim].iloc[0]
            trial_level_data.append({'subject_id': sid, 'test_type': 'Tst2', 'stimulus_location': m['position'], 'stimulus_color': 'red', 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
            
        # Tst3
        rt = session_row[f'tst3_{stim}']
        if pd.notna(rt) and rt > 0:
            m = metadata_shift[metadata_shift['stimulus_id'] == stim].iloc[0]
            trial_level_data.append({'subject_id': sid, 'test_type': 'Tst3', 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
            
    return pd.DataFrame(trial_level_data)

def generate_trajectories(window_size=12, step=3):
    """
    Extracts chronological states. 
    Returns: Baseline subject Space (DF) and Dictionary of Trajectories.
    """
    trials_wide, users, meta1, meta2, meta3 = load_demographics_and_trials()
    extractor = BaselineFeatureExtractor()
    linear_df = pd.read_csv(LINEAR_CSV, index_col=0)
    
    trajectories = {}
    baseline_features = []
    
    total_subjects = len(trials_wide)
    print(f"Extracting rolling trajectories for {total_subjects} sessions...")
    
    # 1. Global Precalculation for PCA Baseline
    for idx, row in trials_wide.iterrows():
        sid = row['subject_id']
        full_df = convert_to_trial_df(row, meta1, meta2, meta3, list(range(1, 37)))
        if len(full_df) == 0: continue
            
        try:
            feats = extractor.extract_subject_features(full_df)
            if pd.notna(feats.get('median_dv1_left')):
                feats['subject_id'] = sid
                baseline_features.append(feats)
                
            # Compute Rolling Windows
            traj_points = []
            for w_start in range(1, 37 - window_size + 1, step):
                w_indices = list(range(w_start, w_start + window_size))
                w_df = convert_to_trial_df(row, meta1, meta2, meta3, w_indices)
                w_feats = extractor.extract_subject_features(w_df)
                
                # Check validity
                if pd.notna(w_feats.get('delta_v4_left')) and pd.notna(w_feats.get('delta_v4_right')) and pd.notna(w_feats.get('delta_v5_left')) and pd.notna(w_feats.get('delta_v5_right')):
                    
                    resid_vec = []
                    valid = True
                    for outcome in CORE_RESIDUALS:
                        out_key = outcome.replace("_residual", "")
                        pred_key = MODEL_MAP[out_key]
                        
                        beta = linear_df.loc[out_key, 'beta']
                        intercept = linear_df.loc[out_key, 'intercept']
                        
                        if pd.isna(w_feats.get(out_key)) or pd.isna(w_feats.get(pred_key)):
                            valid = False
                            break
                        
                        r = w_feats[out_key] - (beta * w_feats[pred_key] + intercept)
                        resid_vec.append(r)
                        
                    if valid:
                        traj_points.append(resid_vec)
                        
            if len(traj_points) > 3: # min frames required for dynamics
                gender = users[users['subject_id'] == sid]['sex_str'].values[0]
                trajectories[sid] = {
                    "points_4d": np.array(traj_points),
                    "sex": gender
                }
                
        except Exception as e:
            continue
            
    # 2. Reconstruct Global Baseline PCA space
    base_df = pd.DataFrame(baseline_features).set_index('subject_id')
    resid_baseline = pd.DataFrame(index=base_df.index)
    
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in linear_df.index: continue
        beta = linear_df.loc[outcome, 'beta']
        intercept = linear_df.loc[outcome, 'intercept']
        resid_baseline[f"{outcome}_residual"] = base_df[outcome] - (beta * base_df[predictor] + intercept)
        
    core_base = resid_baseline[CORE_RESIDUALS].dropna()
    scaler = StandardScaler().fit(core_base.values)
    pca = PCA(n_components=3, random_state=42).fit(scaler.transform(core_base.values))
    
    # 3. Project Trajectories into 3D Space
    for sid in trajectories:
        p4d = trajectories[sid]["points_4d"]
        p3d = pca.transform(scaler.transform(p4d))
        trajectories[sid]["points_3d"] = p3d
        
    return trajectories, pca, scaler

# ============================================================================
# 2. DYNAMIC METRICS: Variance, Hurst, Geometry
# ============================================================================

def calc_hurst(ts):
    """Calculate Hurst exponent using variance of differences method."""
    lags = range(2, min(10, len(ts)//2))
    if len(lags) < 3: return 0.5
    
    tau = []
    lag_vars = []
    for lag in lags:
        diffs = ts[lag:] - ts[:-lag]
        lag_vars.append(np.var(diffs))
        tau.append(lag)
        
    poly = np.polyfit(np.log(tau), np.log(lag_vars), 1)
    hurst = poly[0] / 2.0
    return max(0.0, min(1.0, hurst))

def compute_block_metrics(trajectories):
    """Calculates all dynamics for the cohort."""
    all_points = []
    subject_centroids = []
    
    res = {
        'icc': [], 'path_lengths': [], 'steps': [], 'radial_drifts': [], 
        'hurst': [], 'subject_var': [], 'global_drift': [], 'dim_vars': []
    }
    
    for sid, data in trajectories.items():
        pts = data["points_3d"]
        n_pts = len(pts)
        
        all_points.extend(pts)
        centroid = np.mean(pts, axis=0)
        subject_centroids.append(centroid)
        
        # Block A: Within-Subject Variance
        res['subject_var'].append(np.var(pts, axis=0))
        res['dim_vars'].append(np.var(pts, axis=0))
        
        # Block B: Trajectory Geometry
        diffs = np.diff(pts, axis=0)
        steps = np.linalg.norm(diffs, axis=1)
        res['path_lengths'].append(np.sum(steps))
        res['steps'].append(np.mean(steps))
        
        # Radial drift (distance of end vs distance of start from centroid)
        d_start = euclidean(pts[0], centroid)
        d_end = euclidean(pts[-1], centroid)
        res['radial_drifts'].append(d_end - d_start)
        
        # Block C: Hurst Exponent
        res['hurst'].append([calc_hurst(pts[:, i]) for i in range(3)])
        
        # Block D: Global Attractor Drift
        global_center = np.zeros(3) # PCA centered
        drift = euclidean(pts[-1], global_center) - euclidean(pts[0], global_center)
        res['global_drift'].append(drift)
        
    # Aggregate Block A (ICC)
    var_within = np.mean(np.array(res['subject_var']), axis=0)
    var_between = np.var(np.array(subject_centroids), axis=0)
    
    icc = var_between / (var_between + var_within + 1e-10)
    
    return {
        "icc": icc,
        "var_between": var_between,
        "var_within": var_within,
        "path_length_median": np.median(res['path_lengths']),
        "step_mean": np.mean(res['steps']),
        "radial_drift_mean": np.mean(res['radial_drifts']),
        "global_drift_mean": np.mean(res['global_drift']),
        "hurst_median": np.median(np.array(res['hurst']), axis=0),
        "raw_hurst": np.array(res['hurst'])
    }

# ============================================================================
# 3. NOISE STRESS-TEST
# ============================================================================

def stress_test_noise(trajectories):
    """Injects gaussian noise to the 3D space and recalculates stability."""
    noise_levels = [0.01, 0.03, 0.05, 0.10] # 1%, 3%, 5%, 10%
    noise_results = []
    
    # Calculate baseline standard deviation per axis across all points
    all_pts = np.vstack([t['points_3d'] for t in trajectories.values()])
    global_sd = np.std(all_pts, axis=0)
    
    for level in noise_levels:
        perturbed_traj = {}
        for sid, t in trajectories.items():
            pts = t['points_3d'].copy()
            noise = np.random.normal(0, global_sd * level, pts.shape)
            perturbed_traj[sid] = {
                "points_3d": pts + noise,
                "sex": t['sex']
            }
            
        m = compute_block_metrics(perturbed_traj)
        noise_results.append({
            "noise": f"{level*100:.0f}%",
            "icc_mean": np.mean(m['icc']),
            "hurst_mean": np.mean(m['hurst_median'])
        })
        
    return noise_results

# ============================================================================
# 4. REPORT & VERDICT
# ============================================================================

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Executing Task 37: Trait-State Decomposition...")
    trajectories, pca, scaler = generate_trajectories(window_size=10, step=3)
    
    print("\nRunning Dynamic Computations...")
    base_metrics = compute_block_metrics(trajectories)
    
    # Sex Stratification
    males = {k: v for k, v in trajectories.items() if v['sex'] == 'Male'}
    females = {k: v for k, v in trajectories.items() if v['sex'] == 'Female'}
    
    male_m = compute_block_metrics(males)
    female_m = compute_block_metrics(females)
    
    print("\nRunning Noise Stress Test...")
    noise_m = stress_test_noise(trajectories)
    
    # Formal Verdict Resolution
    icc_mean = np.mean(base_metrics['icc'])
    h_mean = np.mean(base_metrics['hurst_median'])
    noise_icc_drop = base_metrics['icc'].mean() - noise_m[-1]['icc_mean']
    
    sex_diff = abs(male_m['path_length_median'] - female_m['path_length_median']) / base_metrics['path_length_median']
    
    if icc_mean > 0.80:
        if h_mean > 0.55:
            verdict = "TRAIT_DOMINANT_SPACE"
        else:
            verdict = "DYNAMICALLY_STRUCTURED_MANIFOLD"
    elif icc_mean < 0.50:
        verdict = "STATE_SIGNIFICANT_MODULATION"
    elif noise_icc_drop > 0.30:
        verdict = "NOISE_SENSITIVE_STRUCTURE"
    else:
        verdict = "DYNAMICALLY_STRUCTURED_MANIFOLD"
        
    sex_verdict = "SEX_INVARIANT_DYNAMICS" if sex_diff < 0.15 else "SEX_DIFFERENTIATED_DYNAMICS"
    
    print(f"\nVerdicts:\n> {verdict}\n> {sex_verdict}")
    
    # Report Generation
    report = f"""# Task 37: Extended Trait-State Dynamics Audit

## 1. Variance Decomposition (Block A)
| Metric | PC1 (Speed) | PC2 (Lateral) | PC3 (Tone) | Mean |
|---|---|---|---|---|
| Var Between | {base_metrics['var_between'][0]:.4f} | {base_metrics['var_between'][1]:.4f} | {base_metrics['var_between'][2]:.4f} | - |
| Var Within | {base_metrics['var_within'][0]:.4f} | {base_metrics['var_within'][1]:.4f} | {base_metrics['var_within'][2]:.4f} | - |
| **ICC (Trait %)** | **{base_metrics['icc'][0]:.3f}** | **{base_metrics['icc'][1]:.3f}** | **{base_metrics['icc'][2]:.3f}** | **{icc_mean:.3f}** |

## 2. Temporal Structure & Trajectories (Block B & C)
* **Median Path Length**: {base_metrics['path_length_median']:.3f}
* **Mean Step Size**: {base_metrics['step_mean']:.3f}
* **Mean Radial Drift**: {base_metrics['radial_drift_mean']:.4f} (drift from subject centroid)
* **Global Drift**: {base_metrics['global_drift_mean']:.4f} (drift vs absolute test center)
* **Hurst Exponents (PC1, 2, 3)**: {base_metrics['hurst_median'][0]:.3f}, {base_metrics['hurst_median'][1]:.3f}, {base_metrics['hurst_median'][2]:.3f} (Values ~0.50 imply random walk, >0.50 implies persistent trajectory, <0.50 implies mean-reversion)

## 3. Noise Injection Stress-Test (Block E)
*Measures topological stability limit before state trajectories degrade to noise.*
| Noise Added (SD) | ICC Mean | Hurst Mean |
|---|---|---|
| Baseline 0% | {icc_mean:.3f} | {h_mean:.3f} |
"""
    for nr in noise_m:
        report += f"| {nr['noise']} | {nr['icc_mean']:.3f} | {nr['hurst_mean']:.3f} |\n"
        
    report += f"""
## 4. Sex-Stratified Dynamic Analysis (Block F)
| Cohort | N | Median Path Length | ICC Mean | Hurst PC1 |
|---|---|---|---|---|
| Male | {len(males)} | {male_m['path_length_median']:.3f} | {np.mean(male_m['icc']):.3f} | {male_m['hurst_median'][0]:.3f} |
| Female | {len(females)} | {female_m['path_length_median']:.3f} | {np.mean(female_m['icc']):.3f} | {female_m['hurst_median'][0]:.3f} |

---
## FINAL ARCHITECTURAL CONCLUSIONS
**{verdict}**
**{sex_verdict}**
"""
    
    with open(OUT_DIR / "Task_37_Dynamics_Report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\nArtifacts generated in {OUT_DIR}")
    return 0
    

if __name__ == "__main__":
    exit(main())
