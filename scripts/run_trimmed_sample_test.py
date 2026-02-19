"""
Task 27.3H — Robustness To Trimmed Sample Test

PCA on samples with top/bottom/random 10% subjects removed (by residual norm).
Compare with full sample to verify structure is not driven by outliers.

Output: Task_27_3H_Trimmed_Sample_Stability_Report.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor


# ============================================================================
# PATHS & CONFIG
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"
LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3H_Trimmed_Sample_Stability_Report.md"

TRIM_PCT = 0.10
RANDOM_SEED = 42

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
# DATA LOADING (same pipeline as 27.3D–G)
# ============================================================================

def load_features(database_path: str) -> pd.DataFrame:
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
    for _, sr in trials_wide.iterrows():
        sid, tid = sr['subject_id'], sr['trial_id']
        for stim in range(1, 37):
            rt = sr[f'tst1_{stim}']
            if pd.notna(rt) and rt > 0:
                m = metadata_simple[metadata_simple['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_type': 'Tst1',
                    'stimulus_id': stim, 'stimulus_location': m['position'],
                    'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst2_{stim}']
            if pd.notna(rt) and rt > 0:
                m = metadata_color[metadata_color['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_type': 'Tst2',
                    'stimulus_id': stim, 'stimulus_location': m['position'],
                    'stimulus_color': 'red', 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst3_{stim}']
            if pd.notna(rt) and rt > 0:
                m = metadata_shift[metadata_shift['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_type': 'Tst3',
                    'stimulus_id': stim, 'stimulus_location': m['position'],
                    'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})

    trials_df = pd.DataFrame(trial_level_data)
    print(f"  → Reshaped to {len(trials_df)} trial-level observations")
    print("[4/4] Extracting features per subject...")
    extractor = BaselineFeatureExtractor()
    features_list = []
    for subject_id in trials_df['subject_id'].unique():
        try:
            features = extractor.extract_subject_features(
                trials_df[trials_df['subject_id'] == subject_id].copy())
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


def reconstruct_residuals(features_df, linear_csv):
    residuals_df = pd.DataFrame(index=features_df.index)
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in linear_csv.index or outcome not in features_df.columns:
            continue
        beta = linear_csv.loc[outcome, 'beta']
        intercept = linear_csv.loc[outcome, 'intercept']
        data = features_df[[outcome, predictor]].dropna()
        residuals_df.loc[data.index, f"{outcome}_residual"] = data[outcome] - (beta * data[predictor] + intercept)
    return residuals_df


# ============================================================================
# PCA + TRIMMING
# ============================================================================

def pca_metrics(data: np.ndarray) -> dict:
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)
    cov = np.cov(data_std, rowvar=False)
    eigenvalues = np.sort(np.linalg.eigvalsh(cov))[::-1]
    total = np.sum(eigenvalues)
    var_exp = eigenvalues / total
    cum_var = np.cumsum(var_exp)
    p = eigenvalues / total
    p_safe = p[p > 0]
    return {
        'n': data.shape[0],
        'pc1_pct': var_exp[0] * 100,
        'pc2_pct': var_exp[1] * 100 if len(var_exp) > 1 else 0.0,
        'cumul_pct': cum_var[1] * 100 if len(cum_var) > 1 else cum_var[0] * 100,
        'n_lambda_gt1': int(np.sum(eigenvalues > 1.0)),
        'participation_ratio': (total ** 2) / np.sum(eigenvalues ** 2),
        'effective_rank': np.exp(-np.sum(p_safe * np.log(p_safe))),
    }


def compute_residual_norms(data: np.ndarray) -> np.ndarray:
    """Euclidean norm of each subject's residual vector."""
    return np.sqrt(np.sum(data ** 2, axis=1))


def trim_data(data: np.ndarray, norms: np.ndarray, mode: str,
              trim_pct: float, rng: np.random.Generator) -> np.ndarray:
    n = data.shape[0]
    n_trim = int(n * trim_pct)
    sorted_idx = np.argsort(norms)

    if mode == 'top':
        keep = sorted_idx[:-n_trim]
    elif mode == 'bottom':
        keep = sorted_idx[n_trim:]
    elif mode == 'random':
        remove = rng.choice(n, size=n_trim, replace=False)
        keep = np.setdiff1d(np.arange(n), remove)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return data[keep]


# ============================================================================
# REPORT
# ============================================================================

def fmt(v, p=4):
    if isinstance(v, (float, np.floating)):
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{p}f}"
    return str(v)


def generate_report(results: dict) -> str:
    lines = []
    lines.append("# Task 27.3H — Trimmed Sample Stability Report")
    lines.append("")
    lines.append(f"Trim percentage: {TRIM_PCT*100:.0f}%, seed: {RANDOM_SEED}")
    lines.append("")

    for space_label, space_results in results.items():
        lines.append("---")
        lines.append("")
        lines.append(f"## {space_label}")
        lines.append("")

        # 1. Full table
        lines.append("### 1. PCA Metrics by Sample")
        lines.append("")
        lines.append("| Sample | n | PC1 % | PC2 % | Cumul % | λ>1 | PR | ER |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for sample_label, m in space_results.items():
            lines.append(
                f"| {sample_label} "
                f"| {m['n']} "
                f"| {fmt(m['pc1_pct'])} "
                f"| {fmt(m['pc2_pct'])} "
                f"| {fmt(m['cumul_pct'])} "
                f"| {m['n_lambda_gt1']} "
                f"| {fmt(m['participation_ratio'])} "
                f"| {fmt(m['effective_rank'])} |"
            )
        lines.append("")

        # 2. Differences from full
        full = space_results['Full sample']
        lines.append("### 2. Differences from Full Sample")
        lines.append("")
        lines.append("| Sample | ΔPC1 | ΔPC2 | ΔPR | Δλ>1 |")
        lines.append("|---|---|---|---|---|")
        for sample_label, m in space_results.items():
            if sample_label == 'Full sample':
                continue
            d_pc1 = m['pc1_pct'] - full['pc1_pct']
            d_pc2 = m['pc2_pct'] - full['pc2_pct']
            d_pr = m['participation_ratio'] - full['participation_ratio']
            d_lam = m['n_lambda_gt1'] - full['n_lambda_gt1']
            lines.append(
                f"| {sample_label} "
                f"| {fmt(d_pc1, 2)} "
                f"| {fmt(d_pc2, 2)} "
                f"| {fmt(d_pr)} "
                f"| {d_lam} |"
            )
        lines.append("")

        # 3. Robustness criteria
        lines.append("### 3. Robustness Criteria")
        lines.append("")
        lines.append("| Sample | |ΔPC1|<5% | |ΔPC2|<5% | |ΔPR|<0.5 | Δλ>1=0 |")
        lines.append("|---|---|---|---|---|")
        for sample_label, m in space_results.items():
            if sample_label == 'Full sample':
                continue
            d_pc1 = abs(m['pc1_pct'] - full['pc1_pct'])
            d_pc2 = abs(m['pc2_pct'] - full['pc2_pct'])
            d_pr = abs(m['participation_ratio'] - full['participation_ratio'])
            d_lam = m['n_lambda_gt1'] - full['n_lambda_gt1']
            lines.append(
                f"| {sample_label} "
                f"| {d_pc1 < 5.0} "
                f"| {d_pc2 < 5.0} "
                f"| {d_pr < 0.5} "
                f"| {d_lam == 0} |"
            )
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3H — Robustness To Trimmed Sample Test")
    print(f"Trim: {TRIM_PCT*100:.0f}%, Seed: {RANDOM_SEED}")
    print("=" * 60)
    print()

    if not DATABASE_PATH.exists():
        print(f"ERROR: {DATABASE_PATH}"); return 1
    if not LINEAR_CSV.exists():
        print(f"ERROR: {LINEAR_CSV}"); return 1

    features_df = load_features(str(DATABASE_PATH))
    print()

    print("[5/7] Loading stored β/intercept...")
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    print()

    print("[6/7] Reconstructing residuals...")
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    print()

    rng = np.random.default_rng(RANDOM_SEED)
    results = {}

    for space_label, cols_list in [("Core (4 residuals)", CORE_RESIDUALS),
                                    ("Extended (7 features)", EXTENDED_FEATURES)]:
        # Build data matrix
        df = residuals_df.copy()
        actual_cols = []
        for col in cols_list:
            if col in residuals_df.columns:
                actual_cols.append(col)
            elif col in features_df.columns:
                df[col] = features_df[col]
                actual_cols.append(col)
        data = df[actual_cols].dropna().values
        norms = compute_residual_norms(data[:, :4])  # norms on core residuals only

        print(f"[7/7] {space_label} ({data.shape[0]} × {data.shape[1]})...")

        space_results = {}
        space_results['Full sample'] = pca_metrics(data)

        for mode, label in [('top', f'Remove top {TRIM_PCT*100:.0f}%'),
                            ('bottom', f'Remove bottom {TRIM_PCT*100:.0f}%'),
                            ('random', f'Remove random {TRIM_PCT*100:.0f}%')]:
            trimmed = trim_data(data, norms, mode, TRIM_PCT, rng)
            space_results[label] = pca_metrics(trimmed)
            print(f"  → {label}: n={trimmed.shape[0]}")

        results[space_label] = space_results

    print()

    report = generate_report(results)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → Report saved to: {OUTPUT_REPORT}")
    print()

    # Summary
    print("=" * 60)
    for space, sr in results.items():
        full = sr['Full sample']
        print(f"{space}: Full PC1={full['pc1_pct']:.2f}%")
        for label, m in sr.items():
            if label == 'Full sample':
                continue
            d = abs(m['pc1_pct'] - full['pc1_pct'])
            print(f"  {label}: ΔPC1={d:.2f}%")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
