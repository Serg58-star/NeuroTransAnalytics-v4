"""
Task 27.3F — Bootstrap Stability of Latent Dimensionality

1000-iteration bootstrap to verify PCA dimensionality stability.
Resamples subjects with replacement, runs PCA per iteration,
collects PC1%, PC2%, cumulative%, λ>1 count, participation ratio, effective rank.

Output: Task_27_3F_Bootstrap_Stability_Report.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor
from exploratory_lab.geometry.stability import pca_metrics, run_bootstrap


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"

LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3F_Bootstrap_Stability_Report.md"

N_BOOTSTRAP = 1000
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
# DATA LOADING (same as 27.3D/E)
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


def reconstruct_residuals(features_df, linear_csv):
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


# ============================================================================
# BOOTSTRAP PCA (Imported from stability module)
# ============================================================================



# ============================================================================
# REPORT
# ============================================================================

def fmt(v, p=4):
    if isinstance(v, (float, np.floating)):
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{p}f}"
    return str(v)


def summarize(series: pd.Series) -> dict:
    return {
        'mean': series.mean(),
        'sd': series.std(),
        'ci_lo': np.percentile(series, 2.5),
        'ci_hi': np.percentile(series, 97.5),
        'min': series.min(),
        'max': series.max(),
    }


def generate_report(core_bs: pd.DataFrame, ext_bs: pd.DataFrame,
                    core_n: int, ext_n: int) -> str:
    lines = []
    lines.append("# Task 27.3F — Bootstrap Stability Report")
    lines.append("")
    lines.append(f"Bootstrap iterations: {N_BOOTSTRAP}, seed: {RANDOM_SEED}")
    lines.append("")

    for label, bs, n_subj in [("Core (4 residuals)", core_bs, core_n),
                               ("Extended (7 features)", ext_bs, ext_n)]:
        lines.append("---")
        lines.append("")
        lines.append(f"## {label}")
        lines.append(f"n = {n_subj}")
        lines.append("")

        # 1. Summary table
        metrics = ['pc1_pct', 'pc2_pct', 'cumul_pc12_pct',
                   'n_lambda_gt1', 'participation_ratio', 'effective_rank']
        metric_labels = ['PC1 %', 'PC2 %', 'PC1+PC2 cumul %',
                         'λ>1 count', 'Participation Ratio', 'Effective Rank']

        lines.append("### 1. Bootstrap Summary")
        lines.append("")
        lines.append("| Metric | Mean | SD | 95% CI | Min | Max |")
        lines.append("|---|---|---|---|---|---|")
        for m, ml in zip(metrics, metric_labels):
            s = summarize(bs[m])
            lines.append(
                f"| {ml} "
                f"| {fmt(s['mean'])} "
                f"| {fmt(s['sd'])} "
                f"| [{fmt(s['ci_lo'])}, {fmt(s['ci_hi'])}] "
                f"| {fmt(s['min'])} "
                f"| {fmt(s['max'])} |"
            )
        lines.append("")

        # 2. λ>1 count frequency
        lines.append("### 2. λ>1 count frequency")
        lines.append("")
        freq = bs['n_lambda_gt1'].value_counts().sort_index()
        lines.append("| λ>1 count | Frequency | % |")
        lines.append("|---|---|---|")
        for val, cnt in freq.items():
            pct = cnt / len(bs) * 100
            lines.append(f"| {val} | {cnt} | {fmt(pct, 1)} |")
        lines.append("")

        # Modal value stability check
        modal_val = freq.idxmax()
        modal_pct = freq.max() / len(bs) * 100
        lines.append(f"Modal value: {modal_val} ({fmt(modal_pct, 1)}% of iterations)")
        lines.append("")

        # 3-5. Ranges for PC1%, PR, ER already in summary table

        # 6. Stability criteria
        s_pc1 = summarize(bs['pc1_pct'])
        s_pr = summarize(bs['participation_ratio'])
        s_er = summarize(bs['effective_rank'])

        lines.append("### 3. Stability Criteria")
        lines.append("")
        lines.append("| Criterion | Threshold | Value | Met |")
        lines.append("|---|---|---|---|")
        lines.append(f"| SD(PC1%) < 5% | 5.0 | {fmt(s_pc1['sd'])} | {s_pc1['sd'] < 5.0} |")
        lines.append(f"| λ>1 stable ≥90% | 90% | {fmt(modal_pct, 1)}% | {modal_pct >= 90.0} |")
        lines.append(f"| PR SD < 0.3 | 0.3 | {fmt(s_pr['sd'])} | {s_pr['sd'] < 0.3} |")
        lines.append(f"| ER SD < 0.5 | 0.5 | {fmt(s_er['sd'])} | {s_er['sd'] < 0.5} |")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3F — Bootstrap Stability of Latent Dimensionality")
    print(f"Iterations: {N_BOOTSTRAP}, Seed: {RANDOM_SEED}")
    print("=" * 60)
    print()

    if not DATABASE_PATH.exists():
        print(f"ERROR: Database not found: {DATABASE_PATH}")
        return 1
    if not LINEAR_CSV.exists():
        print(f"ERROR: Linear CSV not found: {LINEAR_CSV}")
        return 1

    features_df = load_features(str(DATABASE_PATH))
    print()

    print("[5/8] Loading stored β/intercept...")
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    print()

    print("[6/8] Reconstructing residuals...")
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    print()

    rng = np.random.default_rng(RANDOM_SEED)

    # Core: 4 residuals
    core_cols = [c for c in CORE_RESIDUALS if c in residuals_df.columns]
    core_data = residuals_df[core_cols].dropna().values
    print(f"[7/8] Bootstrap Core PCA ({core_data.shape[0]} × {core_data.shape[1]})...")
    core_bs = run_bootstrap(core_data, N_BOOTSTRAP, rng)
    print(f"  → {len(core_bs)} successful iterations")

    # Extended: 7 features
    ext_df = residuals_df.copy()
    ext_cols = []
    for col in EXTENDED_FEATURES:
        if col in residuals_df.columns:
            ext_cols.append(col)
        elif col in features_df.columns:
            ext_df[col] = features_df[col]
            ext_cols.append(col)
    ext_data = ext_df[ext_cols].dropna().values
    print(f"[8/8] Bootstrap Extended PCA ({ext_data.shape[0]} × {ext_data.shape[1]})...")
    ext_bs = run_bootstrap(ext_data, N_BOOTSTRAP, rng)
    print(f"  → {len(ext_bs)} successful iterations")
    print()

    # Report
    report = generate_report(core_bs, ext_bs, core_data.shape[0], ext_data.shape[0])
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → Report saved to: {OUTPUT_REPORT}")
    print()

    # Summary
    print("=" * 60)
    s = summarize(core_bs['pc1_pct'])
    print(f"Core PC1%: {s['mean']:.2f} ± {s['sd']:.2f}  "
          f"[{s['ci_lo']:.2f}, {s['ci_hi']:.2f}]")
    s = summarize(core_bs['participation_ratio'])
    print(f"Core PR:   {s['mean']:.4f} ± {s['sd']:.4f}")
    s = summarize(core_bs['effective_rank'])
    print(f"Core ER:   {s['mean']:.4f} ± {s['sd']:.4f}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
