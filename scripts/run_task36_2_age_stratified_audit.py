"""
scripts/run_task36_2_age_stratified_audit.py

Executes the Task 36.2 Age-Stratified Population Geometry Audit.
Extracts age demographics and loops over Quartile & Decadal strata to check if the `CONTINUUM`
classification breaks down into discrete `k>1` clusters within specific age corridors.
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
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from run_stage7_population_real import load_features, reconstruct_residuals, DATABASE_PATH, LINEAR_CSV, CORE_RESIDUALS
from run_task36_1_hopkins_audit import calculate_hopkins

# Output Directory
OUT_DIR = Path(__file__).parent.parent / "results" / "task36_2_age_stratified_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATA EXTRACTION & STRATIFICATION
# ============================================================================

def load_demographics(database_path: str, features_df: pd.DataFrame) -> pd.DataFrame:
    """Merges demographic data from the users table and computes age."""
    conn = sqlite3.connect(database_path)
    users_df = pd.read_sql_query("SELECT subject_id, birth_date, first_test_date FROM users", conn)
    conn.close()
    
    # Calculate Age
    users_df['birth_date'] = pd.to_datetime(users_df['birth_date'], errors='coerce')
    users_df['first_test_date'] = pd.to_datetime(users_df['first_test_date'], errors='coerce')
    users_df['age'] = (users_df['first_test_date'] - users_df['birth_date']).dt.days / 365.25
    
    merged_df = features_df.merge(users_df[['subject_id', 'age']], on='subject_id', how='inner')
    merged_df.dropna(subset=['age'], inplace=True)
    merged_df.set_index('subject_id', inplace=True)
    return merged_df

def create_quartile_strata(df: pd.DataFrame):
    """Categorizes the population into exact Quartiles based on age."""
    df['age_quartile'] = pd.qcut(df['age'], q=4, labels=['Q1 (Youngest)', 'Q2', 'Q3', 'Q4 (Oldest)'])
    strata = {}
    for group in df['age_quartile'].cat.categories:
        strata[f"Quartile_{group}"] = df[df['age_quartile'] == group].index
    return strata

def create_decadal_strata(df: pd.DataFrame):
    """
    Categorizes the population into Decades: <30, 30-39, 40-49, 50-59, 60+.
    Groups with N < 100 are merged forward or backward.
    """
    bins = [0, 29.99, 39.99, 49.99, 59.99, 120]
    labels = ['<30', '30-39', '40-49', '50-59', '60+']
    df['age_decade'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    
    # Check sizes and merge if necessary
    counts = df['age_decade'].value_counts()
    
    # We will do a static map for safety to ensure groups >= 100 on N=1482 dataset
    # If a bin is too small, we merge it dynamically
    valid_groups = {}
    current_label = ""
    current_indices = []
    
    for label in labels:
        subset = df[df['age_decade'] == label].index.tolist()
        if not current_label:
            current_label = label
            current_indices.extend(subset)
        else:
            if len(current_indices) < 100:
                current_label = f"{current_label}_{label}"
                current_indices.extend(subset)
            elif len(subset) < 100:
                current_label = f"{current_label}_{label}"
                current_indices.extend(subset)
            else:
                valid_groups[current_label] = current_indices
                current_label = label
                current_indices = list(subset)
                
    if current_indices:
        if len(current_indices) < 100 and valid_groups:
            last_key = list(valid_groups.keys())[-1]
            valid_groups[f"{last_key}_{current_label}"] = valid_groups.pop(last_key) + current_indices
        else:
            valid_groups[current_label] = current_indices
            
    strata = {}
    for k, v in valid_groups.items():
        strata[f"Decade_{k}"] = pd.Index(v)
    return strata

# ============================================================================
# AUDIT METRICS PER COHORT
# ============================================================================

def _gap_statistic_fast(X: np.ndarray, k_range: list, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, d = X.shape
    mins = X.min(axis=0)
    maxs = X.max(axis=0)
    
    gaps = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=seed, n_init=10).fit(X)
        disp_orig = max(km.inertia_, 1e-10)
            
        ref_disps = []
        for _ in range(5): # reduced reference bootstrap for speed on cohorts
            U = rng.uniform(mins, maxs, (n, d))
            km_ref = KMeans(n_clusters=k, random_state=seed, n_init=10).fit(U)
            ref_disps.append(max(km_ref.inertia_, 1e-10))
            
        gap = np.mean(np.log(ref_disps)) - np.log(disp_orig)
        gaps.append(gap)
        
    return np.array(gaps)

def evaluate_cohort_geometry(X_3d: np.ndarray, cohort_name: str) -> dict:
    """Runs the abbreviated geometric audit on an isolated cohort."""
    n_samples = X_3d.shape[0]
    
    # 1. Density
    hopkins = calculate_hopkins(X_3d)
    
    # 2. Clustering
    best_sil = -1
    k_range = list(range(2, 7))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for k in k_range:
            labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X_3d)
            if len(np.unique(labels)) > 1:
                sil = silhouette_score(X_3d, labels)
                if sil > best_sil:
                    best_sil = sil
                    
    gap_k_range = list(range(1, 7))
    gap_scores = _gap_statistic_fast(X_3d, gap_k_range)
    optimal_k = int(gap_k_range[np.argmax(gap_scores)])
    
    # 3. Eigen-Geometry (Anisotropy)
    cov = np.cov(X_3d, rowvar=False)
    eigvals, _ = np.linalg.eigh(cov)
    eigvals = np.sort(eigvals)[::-1]
    anisotropy = float(eigvals[0] / (eigvals[-1] + 1e-10))
    participation_ratio = float((np.sum(eigvals)**2) / np.sum(eigvals**2))
    
    return {
        "Cohort": cohort_name,
        "N": n_samples,
        "Hopkins": float(hopkins),
        "Peak_Silhouette": float(best_sil),
        "Gap_Optimal_k": optimal_k,
        "Anisotropy": anisotropy,
        "Participation_Ratio": participation_ratio
    }

# ============================================================================
# REGRESSION AND VERDICT
# ============================================================================

def run_age_regression(df: pd.DataFrame, residuals_df: pd.DataFrame):
    """
    Evaluates correlation between Age and local structural density metrics by 
    running a rolling local geometry probe on N=50 clusters sorted by age.
    """
    df = df.sort_values(by='age').dropna(subset=['age'])
    
    # Create rolling age windows of size 100
    window_size = 100
    step = 50
    n = len(df)
    
    if n < window_size:
        return {"slope": 0.0, "p_value": 1.0, "r_squared": 0.0, "trend": "INSUFFICIENT_N"}
        
    windows = []
    for i in range(0, n - window_size + 1, step):
        chunk_indices = df.index[i:i+window_size]
        mean_age = df.loc[chunk_indices, 'age'].mean()
        
        core_data = residuals_df.loc[chunk_indices, CORE_RESIDUALS].dropna()
        if len(core_data) < 20: continue
            
        scaler = StandardScaler()
        X_std = scaler.fit_transform(core_data.values)
        pca = PCA(n_components=3, random_state=42)
        X_3d = pca.fit_transform(X_std)
        
        h_score = calculate_hopkins(X_3d, num_samples=min(20, len(X_3d)//2))
        windows.append({"mean_age": mean_age, "hopkins": h_score})
        
    res_df = pd.DataFrame(windows)
    
    X = sm.add_constant(res_df['mean_age'])
    y = res_df['hopkins']
    model = sm.OLS(y, X).fit()
    
    return {
        "slope": float(model.params['mean_age']),
        "p_value": float(model.pvalues['mean_age']),
        "r_squared": float(model.rsquared),
        "windows_analyzed": len(res_df)
    }

def format_report_tables(cohort_results: list, regression_res: dict, verdict: str) -> str:
    lines = [
        "# Task 36.2: Age-Stratified Population Geometry Audit Report",
        "",
        "## 1. Geometric Continuity per Cohort",
        "| Cohort | N | Hopkins (H) | Silhouette Peak | Optimal k (Gap) | Anisotropy (\u03bb1/\u03bb3) | PR |",
        "|---|---|---|---|---|---|---|"
    ]
    for r in cohort_results:
        lines.append(f"| {r['Cohort']} | {r['N']} | {r['Hopkins']:.3f} | {r['Peak_Silhouette']:.3f} | {r['Gap_Optimal_k']} | {r['Anisotropy']:.2f} | {r['Participation_Ratio']:.2f} |")
        
    lines.extend([
        "",
        "## 2. Age vs Density Regression (Rolling Windows N=100)",
        f"- \u03b2 (Slope) : {regression_res['slope']:.6f}",
        f"- R\u00b2        : {regression_res['r_squared']:.4f}",
        f"- p-value  : {regression_res['p_value']:.4e}",
        "",
        "---",
        "## FINAL VALUATION CONCLUSION",
        f"**{verdict}**",
        ""
    ])
    
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("TASK 36.2: AGE-STRATIFIED POPULATION GEOMETRY AUDIT")
    print("=" * 60)

    features_df = load_features(str(DATABASE_PATH))
    features_df = load_demographics(str(DATABASE_PATH), features_df)
    
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    
    # 1. Stratify Populations
    print("\nExtracting demography stratifications...")
    strata_map = {}
    strata_map.update(create_quartile_strata(features_df))
    strata_map.update(create_decadal_strata(features_df))
    
    cohort_results = []
    max_k = 1
    
    # 2. Iterate and Evaluate Geometries
    print("\nRunning structural analysis per aging cohort...")
    for cohort_name, indices in strata_map.items():
        # Extrapolate cohort trait-core
        core_data = residuals_df.loc[indices, CORE_RESIDUALS].dropna()
        if len(core_data) < 20:
            print(f"Skipping {cohort_name}: insufficient valid N ({len(core_data)})")
            continue
            
        scaler = StandardScaler()
        X_std = scaler.fit_transform(core_data.values)
        pca = PCA(n_components=3, random_state=42)
        X_3d = pca.fit_transform(X_std)
        
        # Audit Cohort
        res_dict = evaluate_cohort_geometry(X_3d, cohort_name)
        cohort_results.append(res_dict)
        print(f"[{cohort_name}] N={res_dict['N']} | H={res_dict['Hopkins']:.3f} | k={res_dict['Gap_Optimal_k']} | Sil={res_dict['Peak_Silhouette']:.3f}")
        
        if res_dict['Gap_Optimal_k'] > max_k and res_dict['Peak_Silhouette'] > 0.35:
            max_k = res_dict['Gap_Optimal_k']
            
    # 3. Run Age Regression (Rolling)
    print("\nRunning rolling H(Density) ~ Age regression...")
    reg_res = run_age_regression(features_df, residuals_df)
    
    # 4. Synthesize Verdict
    if max_k > 1:
        verdict = "AGE_SPECIFIC_CLUSTERING"
    elif reg_res['p_value'] < 0.05 and abs(reg_res['r_squared']) > 0.10:
        verdict = "AGE_DEPENDENT_DENSITY_GRADIENT"
    else:
        verdict = "AGE_INVARIANT_CONTINUUM"
        
    print(f"\n>>> FINAL VERDICT: {verdict}")
    
    # Export File Reports
    report_md = format_report_tables(cohort_results, reg_res, verdict)
    with open(OUT_DIR / "Task_36_2_Age_Stratified_Report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
        
    dump_data = {
        "cohorts": cohort_results,
        "regression": reg_res,
        "verdict": verdict
    }
    with open(OUT_DIR / "audit_results.json", "w", encoding="utf-8") as f:
        json.dump(dump_data, f, indent=4)
        
    print(f"Artifacts saved to {OUT_DIR}")
    return 0

if __name__ == "__main__":
    exit(main())
