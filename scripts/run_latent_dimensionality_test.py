"""
Task 27.3E — Latent Dimensionality Test (No Clustering)

PCA on residual space to determine latent dimensionality.
No clustering, no UMAP, no t-SNE, no visualization, no interpretation.

Two analyses:
  1. Core: 4 residual features
  2. Extended: 4 residuals + Asym_abs + Asym_rel + PSI_tau

Output: Task_27_3E_Latent_Dimensionality_Report.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"

LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3E_Latent_Dimensionality_Report.md"


# ============================================================================
# MODEL MAP (same as 27.3D)
# ============================================================================

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

EXTENDED_FEATURES = CORE_RESIDUALS + ["asym_dv1_abs", "asym_dv1_rel", "psi_tau"]


# ============================================================================
# DATA LOADING (reuse from 27.3D)
# ============================================================================

def load_features(database_path: str) -> pd.DataFrame:
    """Load features from neuro_data.db via BaselineFeatureExtractor."""
    import sqlite3

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
    print(f"  → Loaded {len(trials_wide)} sessions from {trials_wide['subject_id'].nunique()} subjects")

    print("[2/4] Loading stimulus metadata...")
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    print("[3/4] Reshaping to trial-level format...")
    trial_level_data = []

    for _, session_row in trials_wide.iterrows():
        subject_id = session_row['subject_id']
        trial_id = session_row['trial_id']

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst1_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_simple[metadata_simple['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst1', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst2_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_color[metadata_color['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst2', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': 'red',
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst3_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_shift[metadata_shift['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst3', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

    trials_df = pd.DataFrame(trial_level_data)
    print(f"  → Reshaped to {len(trials_df)} trial-level observations")

    print("[4/4] Extracting features per subject...")
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

    features_df = pd.DataFrame(features_list)
    if 'subject_id' in features_df.columns:
        features_df = features_df.set_index('subject_id')
    print(f"  → Extracted features for {len(features_df)} subjects")

    return features_df


def reconstruct_residuals(features_df: pd.DataFrame,
                          linear_csv: pd.DataFrame) -> pd.DataFrame:
    """Reconstruct residuals using stored β/intercept."""
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
        residuals = data[outcome] - y_pred
        residuals_df.loc[residuals.index, f"{outcome}_residual"] = residuals

    return residuals_df


# ============================================================================
# PCA ANALYSIS
# ============================================================================

def run_pca_analysis(data: np.ndarray, feature_names: list) -> dict:
    """
    PCA via eigendecomposition of covariance matrix.
    Returns eigenvalues, variance explained, participation ratio,
    effective rank, condition number.
    """
    # Z-score standardization
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)

    # Covariance matrix
    cov_matrix = np.cov(data_std, rowvar=False)

    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # Sort descending
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Variance explained
    total_var = np.sum(eigenvalues)
    variance_explained = eigenvalues / total_var
    cumulative_variance = np.cumsum(variance_explained)

    # Participation Ratio: (Σλ)² / Σλ²
    participation_ratio = (np.sum(eigenvalues) ** 2) / np.sum(eigenvalues ** 2)

    # Effective Rank: exp(-Σ pᵢ log pᵢ) where pᵢ = λᵢ/Σλ
    p = eigenvalues / total_var
    p_safe = p[p > 0]  # avoid log(0)
    effective_rank = np.exp(-np.sum(p_safe * np.log(p_safe)))

    # Condition number: λ_max / λ_min
    lambda_min = eigenvalues[-1]
    condition_number = eigenvalues[0] / lambda_min if lambda_min > 0 else np.inf

    # Components with eigenvalue > 1
    n_components_gt1 = int(np.sum(eigenvalues > 1.0))

    return {
        'n_samples': data.shape[0],
        'n_features': data.shape[1],
        'feature_names': feature_names,
        'eigenvalues': eigenvalues,
        'variance_explained': variance_explained,
        'cumulative_variance': cumulative_variance,
        'participation_ratio': participation_ratio,
        'effective_rank': effective_rank,
        'condition_number': condition_number,
        'n_components_gt1': n_components_gt1,
        'cov_matrix': cov_matrix,
    }


# ============================================================================
# REPORT GENERATION
# ============================================================================

def fmt(v, precision=6):
    if isinstance(v, (float, np.floating)):
        if np.isnan(v) or np.isinf(v):
            return str(v)
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{precision}f}"
    return str(v)


def generate_report(core: dict, extended: dict) -> str:
    lines = []
    lines.append("# Task 27.3E — Latent Dimensionality Report")
    lines.append("")

    for label, result in [("Core (4 residuals)", core),
                          ("Extended (4 residuals + 3 latent)", extended)]:
        lines.append(f"---")
        lines.append("")
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"n = {result['n_samples']}, p = {result['n_features']}")
        lines.append("")

        # 1. Eigenvalues table
        lines.append("### 1. Eigenvalues")
        lines.append("")
        lines.append("| PC | Eigenvalue | % Variance | Cumulative % |")
        lines.append("|---|---|---|---|")
        for i in range(result['n_features']):
            lines.append(
                f"| PC{i+1} "
                f"| {fmt(result['eigenvalues'][i])} "
                f"| {fmt(result['variance_explained'][i] * 100, 2)} "
                f"| {fmt(result['cumulative_variance'][i] * 100, 2)} |"
            )
        lines.append("")

        # 2. Components with eigenvalue > 1
        lines.append("### 2. Kaiser criterion (eigenvalue > 1)")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Components with λ > 1 | {result['n_components_gt1']} |")
        lines.append("")

        # 3. Participation Ratio
        lines.append("### 3. Participation Ratio")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Participation Ratio | {fmt(result['participation_ratio'])} |")
        lines.append("")

        # 4. Effective Rank
        lines.append("### 4. Effective Rank")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Effective Rank | {fmt(result['effective_rank'])} |")
        lines.append("")

        # 5. Condition Number
        lines.append("### 5. Condition Number")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Condition Number | {fmt(result['condition_number'])} |")
        lines.append("")

        # 6. Formal criteria check
        lines.append("### 6. Formal Criteria")
        lines.append("")
        pc1_pct = result['variance_explained'][0] * 100
        pc12_pct = result['cumulative_variance'][1] * 100 if result['n_features'] >= 2 else pc1_pct
        lines.append(f"| Criterion | Threshold | Value | Met |")
        lines.append(f"|---|---|---|---|")
        lines.append(f"| PC1 ≥ 65% | 65% | {fmt(pc1_pct, 2)}% | {pc1_pct >= 65} |")
        lines.append(f"| PC1 ≥ 80% | 80% | {fmt(pc1_pct, 2)}% | {pc1_pct >= 80} |")
        lines.append(f"| PC1+PC2 ≥ 80% | 80% | {fmt(pc12_pct, 2)}% | {pc12_pct >= 80} |")
        lines.append(f"| Components λ>1 ≥ 3 | 3 | {result['n_components_gt1']} | {result['n_components_gt1'] >= 3} |")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3E — Latent Dimensionality Test")
    print("=" * 60)
    print()

    if not DATABASE_PATH.exists():
        print(f"ERROR: Database not found: {DATABASE_PATH}")
        return 1
    if not LINEAR_CSV.exists():
        print(f"ERROR: Linear CSV not found: {LINEAR_CSV}")
        return 1

    # Load features + reconstruct residuals
    features_df = load_features(str(DATABASE_PATH))
    print()

    print("[5/7] Loading stored β/intercept...")
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    print()

    print("[6/7] Reconstructing residuals...")
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    print(f"  → {len(residuals_df.dropna())} subjects with complete residuals")
    print()

    # Prepare data matrices
    print("[7/7] Running PCA...")

    # Core: 4 residuals only
    core_cols = [c for c in CORE_RESIDUALS if c in residuals_df.columns]
    core_data = residuals_df[core_cols].dropna()
    print(f"  Core analysis: {core_data.shape[0]} subjects × {core_data.shape[1]} features")
    core_result = run_pca_analysis(core_data.values, core_cols)

    # Extended: 4 residuals + latent vars
    ext_cols = []
    ext_df = residuals_df.copy()
    for col in EXTENDED_FEATURES:
        if col in residuals_df.columns:
            ext_cols.append(col)
        elif col in features_df.columns:
            ext_df[col] = features_df[col]
            ext_cols.append(col)

    ext_data = ext_df[ext_cols].dropna()
    print(f"  Extended analysis: {ext_data.shape[0]} subjects × {ext_data.shape[1]} features")
    ext_result = run_pca_analysis(ext_data.values, ext_cols)
    print()

    # Generate report
    report = generate_report(core_result, ext_result)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → Report saved to: {OUTPUT_REPORT}")
    print()

    # Print summary
    print("=" * 60)
    print("Core PCA Summary:")
    for i, (ev, ve) in enumerate(zip(core_result['eigenvalues'], core_result['variance_explained'])):
        print(f"  PC{i+1}: λ={ev:.4f}  ({ve*100:.1f}%)")
    print(f"  Participation Ratio: {core_result['participation_ratio']:.4f}")
    print(f"  Effective Rank: {core_result['effective_rank']:.4f}")
    print(f"  Condition Number: {core_result['condition_number']:.4f}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
