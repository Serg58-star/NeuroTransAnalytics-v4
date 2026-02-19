"""
Task 27.3J — Longitudinal Trajectory Analysis (REG 8, 122)

Projects each visit of subjects 8 and 122 into the existing PCA core space.
Computes PC scores, within/between variance ratios, autocorrelations,
and formal trajectory classification.

Output: Task_27_3J_Longitudinal_Report.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from sklearn.preprocessing import StandardScaler

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor


# ============================================================================
# CONFIG
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"
LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3J_Longitudinal_Report.md"

TARGET_SUBJECTS = [8, 122]

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
# DATA LOADING — ALL SESSIONS (per-session features)
# ============================================================================

def load_all_session_features(database_path: str):
    """Load features per session (not per subject). Returns df with session_id index."""
    import sqlite3
    print("[1/4] Loading trial data...")
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
    print(f"  → {len(trials_wide)} sessions, {trials_wide['subject_id'].nunique()} subjects")

    print("[2/4] Loading metadata...")
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    print("[3/4] Reshaping to trial-level...")
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
    print(f"  → {len(trials_df)} trial-level observations")

    # Extract features PER SESSION (not per subject aggregated)
    print("[4/4] Extracting features per session...")
    extractor = BaselineFeatureExtractor()
    session_features = []
    session_meta = []  # track session→subject mapping and date

    for _, sr in trials_wide.iterrows():
        sid, tid, test_date = sr['subject_id'], sr['trial_id'], sr['test_date']
        session_trials = trials_df[trials_df['session_id'] == tid].copy()
        if len(session_trials) == 0:
            continue
        try:
            features = extractor.extract_subject_features(session_trials)
            if isinstance(features, dict):
                features['session_id'] = tid
                features['subject_id'] = sid
                features['test_date'] = test_date
                session_features.append(features)
        except Exception:
            continue

    sf_df = pd.DataFrame(session_features)
    print(f"  → Extracted features for {len(sf_df)} sessions")
    return sf_df, trials_wide


# ============================================================================
# PCA BASIS (from full population, Task 27.3E)
# ============================================================================

def compute_population_pca_basis(features_df, linear_csv):
    """Compute PCA basis from all subjects (first-visit or all sessions aggregated per subject)."""
    # Aggregate by subject (mean per subject across sessions)
    subject_features = features_df.groupby('subject_id').first()  # use first session per subject

    # Reconstruct residuals
    residuals = pd.DataFrame(index=subject_features.index)
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in linear_csv.index or outcome not in subject_features.columns:
            continue
        beta = linear_csv.loc[outcome, 'beta']
        intercept = linear_csv.loc[outcome, 'intercept']
        data = subject_features[[outcome, predictor]].dropna()
        residuals.loc[data.index, f"{outcome}_residual"] = data[outcome] - (beta * data[predictor] + intercept)

    core_cols = [c for c in CORE_RESIDUALS if c in residuals.columns]
    pop_data = residuals[core_cols].dropna()

    # Z-score standardization
    scaler = StandardScaler()
    pop_std = scaler.fit_transform(pop_data.values)

    # PCA via eigendecomposition
    cov = np.cov(pop_std, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Population variance for between-subject comparison
    pop_pc_scores = pop_std @ eigenvectors
    var_pop_pc1 = np.var(pop_pc_scores[:, 0])
    var_pop_pc2 = np.var(pop_pc_scores[:, 1])

    return scaler, eigenvectors, eigenvalues, var_pop_pc1, var_pop_pc2, pop_data.index, core_cols


# ============================================================================
# PROJECT SESSIONS INTO PCA SPACE
# ============================================================================

def project_sessions(session_features, linear_csv, scaler, eigenvectors, core_cols):
    """Reconstruct residuals for each session and project into PCA space."""
    records = []
    for _, row in session_features.iterrows():
        # Reconstruct residuals for this session
        resid = {}
        skip = False
        for outcome, predictor in MODEL_MAP.items():
            if outcome not in linear_csv.index:
                skip = True; break
            if pd.isna(row.get(outcome)) or pd.isna(row.get(predictor)):
                skip = True; break
            beta = linear_csv.loc[outcome, 'beta']
            intercept = linear_csv.loc[outcome, 'intercept']
            resid[f"{outcome}_residual"] = row[outcome] - (beta * row[predictor] + intercept)
        if skip:
            continue

        resid_vec = np.array([resid[c] for c in core_cols]).reshape(1, -1)
        resid_std = scaler.transform(resid_vec)
        pc_scores = resid_std @ eigenvectors

        records.append({
            'session_id': row['session_id'],
            'subject_id': row['subject_id'],
            'test_date': row['test_date'],
            'pc1': pc_scores[0, 0],
            'pc2': pc_scores[0, 1],
            'residual_norm': np.sqrt(np.sum(resid_vec ** 2)),
            'delta_v4_hemispheric': resid[f"delta_v4_left_residual"] - resid[f"delta_v4_right_residual"],
            'delta_v5_hemispheric': resid[f"delta_v5_left_residual"] - resid[f"delta_v5_right_residual"],
        })

    return pd.DataFrame(records)


# ============================================================================
# WITHIN-SUBJECT ANALYSIS
# ============================================================================

def analyze_subject_trajectory(subj_df):
    """Compute within-subject variability metrics."""
    subj_df = subj_df.sort_values('test_date').reset_index(drop=True)
    pc1 = subj_df['pc1'].values
    pc2 = subj_df['pc2'].values
    n = len(pc1)

    mean_pc1, sd_pc1 = np.mean(pc1), np.std(pc1, ddof=1)
    mean_pc2, sd_pc2 = np.mean(pc2), np.std(pc2, ddof=1)
    var_pc1 = np.var(pc1, ddof=1)
    var_pc2 = np.var(pc2, ddof=1)
    total_var = var_pc1 + var_pc2

    # Consecutive distances
    dists = np.sqrt(np.diff(pc1) ** 2 + np.diff(pc2) ** 2)
    mean_dist = np.mean(dists) if len(dists) > 0 else 0.0
    max_dist = np.max(dists) if len(dists) > 0 else 0.0

    # Autocorrelation (lag-1)
    if n > 2:
        acf_pc1 = np.corrcoef(pc1[:-1], pc1[1:])[0, 1]
        acf_pc2 = np.corrcoef(pc2[:-1], pc2[1:])[0, 1]
    else:
        acf_pc1 = acf_pc2 = np.nan

    # Correlation with chronological order
    order = np.arange(n)
    if n > 2:
        corr_pc1_order, p_pc1_order = sp_stats.pearsonr(order, pc1)
        corr_pc2_order, p_pc2_order = sp_stats.pearsonr(order, pc2)
    else:
        corr_pc1_order = corr_pc2_order = np.nan
        p_pc1_order = p_pc2_order = np.nan

    # Variance ratio
    var_ratio = var_pc1 / var_pc2 if var_pc2 > 0 else np.inf

    return {
        'n_visits': n,
        'mean_pc1': mean_pc1, 'sd_pc1': sd_pc1, 'var_pc1': var_pc1,
        'mean_pc2': mean_pc2, 'sd_pc2': sd_pc2, 'var_pc2': var_pc2,
        'total_var': total_var,
        'var_ratio_pc1_pc2': var_ratio,
        'mean_consec_dist': mean_dist,
        'max_consec_dist': max_dist,
        'mean_resid_norm': subj_df['residual_norm'].mean(),
        'sd_resid_norm': subj_df['residual_norm'].std(),
        'acf_pc1': acf_pc1, 'acf_pc2': acf_pc2,
        'corr_pc1_order': corr_pc1_order, 'p_pc1_order': p_pc1_order,
        'corr_pc2_order': corr_pc2_order, 'p_pc2_order': p_pc2_order,
        'mean_dv4_hemi': subj_df['delta_v4_hemispheric'].mean(),
        'sd_dv4_hemi': subj_df['delta_v4_hemispheric'].std(),
        'mean_dv5_hemi': subj_df['delta_v5_hemispheric'].mean(),
        'sd_dv5_hemi': subj_df['delta_v5_hemispheric'].std(),
    }


def classify_trajectory(stats, var_pop_pc1, var_pop_pc2):
    """Formal classification: Stable / Axial drift / Chaotic."""
    within_total = stats['total_var']
    between_total = var_pop_pc1 + var_pop_pc2

    ratio_pc1 = stats['var_pc1'] / var_pop_pc1 if var_pop_pc1 > 0 else np.inf
    ratio_pc2 = stats['var_pc2'] / var_pop_pc2 if var_pop_pc2 > 0 else np.inf
    ratio_total = within_total / between_total if between_total > 0 else np.inf

    # Classification
    if ratio_total < 0.1 and stats['sd_pc1'] < 1.0 and stats['sd_pc2'] < 1.0:
        classification = "Stable"
    elif stats['var_ratio_pc1_pc2'] > 3 or stats['var_ratio_pc1_pc2'] < 1/3:
        classification = "Axial drift"
    elif abs(stats['acf_pc1']) < 0.3 and abs(stats['acf_pc2']) < 0.3:
        classification = "Chaotic"
    else:
        classification = "Mixed/Unclassified"

    return classification, ratio_pc1, ratio_pc2, ratio_total


# ============================================================================
# REPORT
# ============================================================================

def fmt(v, p=4):
    if isinstance(v, (float, np.floating)):
        if np.isnan(v) or np.isinf(v):
            return str(v)
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{p}f}"
    return str(v)


def generate_report(subject_results, var_pop_pc1, var_pop_pc2, n_pop):
    lines = []
    lines.append("# Task 27.3J — Longitudinal Trajectory Report")
    lines.append("")
    lines.append(f"Population PCA basis: n = {n_pop}")
    lines.append(f"Var_pop(PC1) = {fmt(var_pop_pc1)}")
    lines.append(f"Var_pop(PC2) = {fmt(var_pop_pc2)}")
    lines.append("")

    for sid, (stats, classification, r_pc1, r_pc2, r_total) in subject_results.items():
        lines.append("---")
        lines.append("")
        lines.append(f"## Subject {sid}")
        lines.append("")

        # 1. Visit count
        lines.append(f"### 1. Visits: {stats['n_visits']}")
        lines.append("")

        # 2. Mean coordinates
        lines.append("### 2. Mean Coordinates")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| Mean(PC1) | {fmt(stats['mean_pc1'])} |")
        lines.append(f"| Mean(PC2) | {fmt(stats['mean_pc2'])} |")
        lines.append(f"| Mean(Residual Norm) | {fmt(stats['mean_resid_norm'])} |")
        lines.append(f"| Mean(ΔV4 hemispheric) | {fmt(stats['mean_dv4_hemi'])} |")
        lines.append(f"| Mean(ΔV5 hemispheric) | {fmt(stats['mean_dv5_hemi'])} |")
        lines.append("")

        # 3. SD and variances
        lines.append("### 3. Variability")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| SD(PC1) | {fmt(stats['sd_pc1'])} |")
        lines.append(f"| SD(PC2) | {fmt(stats['sd_pc2'])} |")
        lines.append(f"| Var(PC1) | {fmt(stats['var_pc1'])} |")
        lines.append(f"| Var(PC2) | {fmt(stats['var_pc2'])} |")
        lines.append(f"| Total Var | {fmt(stats['total_var'])} |")
        lines.append(f"| Var ratio PC1/PC2 | {fmt(stats['var_ratio_pc1_pc2'])} |")
        lines.append(f"| Mean consecutive dist | {fmt(stats['mean_consec_dist'])} |")
        lines.append(f"| Max consecutive dist | {fmt(stats['max_consec_dist'])} |")
        lines.append(f"| SD(Residual Norm) | {fmt(stats['sd_resid_norm'])} |")
        lines.append(f"| SD(ΔV4 hemispheric) | {fmt(stats['sd_dv4_hemi'])} |")
        lines.append(f"| SD(ΔV5 hemispheric) | {fmt(stats['sd_dv5_hemi'])} |")
        lines.append("")

        # 4. Within/Between ratios
        lines.append("### 4. Within/Between Ratios")
        lines.append("")
        lines.append("| Metric | Within | Between | Ratio |")
        lines.append("|---|---|---|---|")
        lines.append(f"| PC1 | {fmt(stats['var_pc1'])} | {fmt(var_pop_pc1)} | {fmt(r_pc1)} |")
        lines.append(f"| PC2 | {fmt(stats['var_pc2'])} | {fmt(var_pop_pc2)} | {fmt(r_pc2)} |")
        lines.append(f"| Total | {fmt(stats['total_var'])} | {fmt(var_pop_pc1 + var_pop_pc2)} | {fmt(r_total)} |")
        lines.append("")

        # 5. Autocorrelation
        lines.append("### 5. Temporal Structure")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| Autocorr PC1 (lag-1) | {fmt(stats['acf_pc1'])} |")
        lines.append(f"| Autocorr PC2 (lag-1) | {fmt(stats['acf_pc2'])} |")
        lines.append(f"| Corr(PC1, order) | {fmt(stats['corr_pc1_order'])} (p={fmt(stats['p_pc1_order'])}) |")
        lines.append(f"| Corr(PC2, order) | {fmt(stats['corr_pc2_order'])} (p={fmt(stats['p_pc2_order'])}) |")
        lines.append("")

        # 6. Classification
        lines.append("### 6. Formal Classification")
        lines.append("")
        lines.append(f"**{classification}**")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3J — Longitudinal Trajectory Analysis")
    print(f"Subjects: {TARGET_SUBJECTS}")
    print("=" * 60)
    print()

    if not DATABASE_PATH.exists():
        print(f"ERROR: {DATABASE_PATH}"); return 1

    # Load all sessions
    sf_df, trials_wide = load_all_session_features(str(DATABASE_PATH))
    print()

    # Check target subjects exist
    for sid in TARGET_SUBJECTS:
        n = len(sf_df[sf_df['subject_id'] == sid])
        print(f"  Subject {sid}: {n} sessions")
    print()

    # Load stored regression coefficients (population-level β)
    print("[5/8] Loading population β...")
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    print()

    # Compute PCA basis from population
    print("[6/8] Computing population PCA basis...")
    scaler, eigenvectors, eigenvalues, var_pop_pc1, var_pop_pc2, pop_idx, core_cols = \
        compute_population_pca_basis(sf_df, linear_csv)
    n_pop = len(pop_idx)
    print(f"  → Population: {n_pop} subjects")
    print(f"  → Var_pop(PC1)={var_pop_pc1:.4f}, Var_pop(PC2)={var_pop_pc2:.4f}")
    print()

    # Project target subjects' sessions into PCA space
    print("[7/8] Projecting sessions...")
    subject_results = {}
    for sid in TARGET_SUBJECTS:
        subj_sessions = sf_df[sf_df['subject_id'] == sid].copy()
        projected = project_sessions(subj_sessions, linear_csv, scaler, eigenvectors, core_cols)
        print(f"  Subject {sid}: {len(projected)} projected sessions")

        stats = analyze_subject_trajectory(projected)
        classification, r_pc1, r_pc2, r_total = classify_trajectory(
            stats, var_pop_pc1, var_pop_pc2)
        subject_results[sid] = (stats, classification, r_pc1, r_pc2, r_total)
        print(f"    → Classification: {classification}")
        print(f"    → W/B ratio: {r_total:.4f}")
    print()

    # Report
    print("[8/8] Generating report...")
    report = generate_report(subject_results, var_pop_pc1, var_pop_pc2, n_pop)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → {OUTPUT_REPORT}")
    print()

    print("=" * 60)
    for sid, (stats, cls, r1, r2, rt) in subject_results.items():
        print(f"Subject {sid}: {cls}, W/B={rt:.4f}, "
              f"Mean(PC1)={stats['mean_pc1']:.2f}, SD={stats['sd_pc1']:.2f}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
