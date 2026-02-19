"""
Task 27.3I — First Visit Population Control

Repeats full analysis pipeline (regression, residuals, PCA, bootstrap,
split-half) on first-visit-only data. Generates first-visit report and
comparative analysis against full-population results.

Output:
    - Task_27_3I_First_Visit_Report.md
    - Task_27_3I_Comparative_Analysis.md
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
# PATHS & CONFIG
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"
LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3I_First_Visit_Report.md"
OUTPUT_COMPARATIVE = DATA_DIR / "Task_27_3I_Comparative_Analysis.md"

N_BOOTSTRAP = 1000
N_SPLITS = 500
RANDOM_SEED = 42

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
EXTENDED_FEATURES = CORE_RESIDUALS + ["asym_dv1_abs", "asym_dv1_rel", "psi_tau"]


# ============================================================================
# DATA LOADING — FIRST VISIT ONLY
# ============================================================================

def load_first_visit_features(database_path: str):
    """Load features using only the first visit per subject."""
    import sqlite3
    print("[1/5] Loading trial data from neuro_data.db...")
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
    n_total_sessions = len(trials_wide)
    n_total_subjects = trials_wide['subject_id'].nunique()
    print(f"  → Loaded {n_total_sessions} sessions from {n_total_subjects} subjects")

    # Filter to first visit per subject
    print("[2/5] Filtering to first visit per subject...")
    trials_wide['test_date'] = pd.to_datetime(trials_wide['test_date'])
    first_visits = trials_wide.sort_values('test_date').groupby('subject_id').first().reset_index()
    n_first_visit = len(first_visits)
    pct_reduction = (1 - n_first_visit / n_total_sessions) * 100
    print(f"  → First visits: {n_first_visit} (from {n_total_sessions} sessions, {pct_reduction:.1f}% reduction)")

    print("[3/5] Loading stimulus metadata...")
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    print("[4/5] Reshaping to trial-level format...")
    trial_level_data = []
    for _, sr in first_visits.iterrows():
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

    print("[5/5] Extracting features per subject...")
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

    sample_info = {
        'n_total_sessions': n_total_sessions,
        'n_total_subjects': n_total_subjects,
        'n_first_visit': n_first_visit,
        'pct_reduction': pct_reduction,
    }
    return features_df, sample_info


# ============================================================================
# REGRESSION
# ============================================================================

def run_linear_regressions(features_df: pd.DataFrame) -> pd.DataFrame:
    """Simple linear regression: outcome ~ predictor."""
    rows = []
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in features_df.columns or predictor not in features_df.columns:
            continue
        data = features_df[[outcome, predictor]].dropna()
        x, y = data[predictor].values, data[outcome].values
        slope, intercept, r, p, se = sp_stats.linregress(x, y)
        r_sq = r ** 2
        n = len(data)
        adj_r_sq = 1 - (1 - r_sq) * (n - 1) / (n - 2)
        y_pred = slope * x + intercept
        residuals = y - y_pred
        resid_var = np.var(residuals, ddof=1)
        orig_var = np.var(y, ddof=1)
        rows.append({
            'model': outcome,
            'n': n, 'r_squared': r_sq, 'adj_r_squared': adj_r_sq,
            'beta': slope, 'intercept': intercept, 'p_value': p,
            'residual_variance': resid_var, 'original_variance': orig_var,
            'residual_ratio': resid_var / orig_var if orig_var > 0 else np.nan,
        })
    return pd.DataFrame(rows).set_index('model')


def reconstruct_residuals(features_df, reg_results):
    residuals_df = pd.DataFrame(index=features_df.index)
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in reg_results.index:
            continue
        beta = reg_results.loc[outcome, 'beta']
        intercept = reg_results.loc[outcome, 'intercept']
        data = features_df[[outcome, predictor]].dropna()
        residuals_df.loc[data.index, f"{outcome}_residual"] = data[outcome] - (beta * data[predictor] + intercept)
    return residuals_df


# ============================================================================
# PCA
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
        'n': data.shape[0], 'p': data.shape[1],
        'eigenvalues': eigenvalues,
        'pc1_pct': var_exp[0] * 100,
        'pc2_pct': var_exp[1] * 100 if len(var_exp) > 1 else 0.0,
        'cumul_pct': cum_var[1] * 100 if len(cum_var) > 1 else cum_var[0] * 100,
        'n_lambda_gt1': int(np.sum(eigenvalues > 1.0)),
        'participation_ratio': (total ** 2) / np.sum(eigenvalues ** 2),
        'effective_rank': np.exp(-np.sum(p_safe * np.log(p_safe))),
    }


# ============================================================================
# BOOTSTRAP
# ============================================================================

def bootstrap_pca(data, n_iter, rng):
    n = data.shape[0]
    records = []
    for _ in range(n_iter):
        idx = rng.integers(0, n, size=n)
        try:
            m = pca_metrics(data[idx])
            records.append({
                'pc1_pct': m['pc1_pct'], 'pc2_pct': m['pc2_pct'],
                'cumul_pct': m['cumul_pct'], 'n_lambda_gt1': m['n_lambda_gt1'],
                'participation_ratio': m['participation_ratio'],
                'effective_rank': m['effective_rank'],
            })
        except Exception:
            continue
    return pd.DataFrame(records)


# ============================================================================
# SPLIT-HALF
# ============================================================================

def split_half_pca(data, n_iter, rng):
    n = data.shape[0]
    half = n // 2
    records = []
    for _ in range(n_iter):
        perm = rng.permutation(n)
        idx_a, idx_b = perm[:half], perm[half:half*2]
        try:
            ev_a, vec_a = _pca_full(data[idx_a])
            ev_b, vec_b = _pca_full(data[idx_b])
            ta, tb = np.sum(ev_a), np.sum(ev_b)
            va, vb = ev_a / ta * 100, ev_b / tb * 100
            records.append({
                'diff_pc1_pct': abs(va[0] - vb[0]),
                'diff_pc2_pct': abs(va[1] - vb[1]) if len(va) > 1 else 0.0,
                'cos_theta_pc1': abs(np.dot(vec_a[:, 0], vec_b[:, 0])),
                'cos_theta_pc2': abs(np.dot(vec_a[:, 1], vec_b[:, 1])) if vec_a.shape[1] > 1 else 0.0,
            })
        except Exception:
            continue
    return pd.DataFrame(records)


def _pca_full(data):
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)
    cov = np.cov(data_std, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]


# ============================================================================
# HELPERS
# ============================================================================

def fmt(v, p=4):
    if isinstance(v, (float, np.floating)):
        if np.isnan(v) or np.isinf(v):
            return str(v)
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{p}f}"
    return str(v)


def summarize(s):
    return {
        'mean': s.mean(), 'sd': s.std(),
        'ci_lo': np.percentile(s, 2.5), 'ci_hi': np.percentile(s, 97.5),
    }


def prepare_data_matrix(residuals_df, features_df, cols_list):
    df = residuals_df.copy()
    actual_cols = []
    for col in cols_list:
        if col in residuals_df.columns:
            actual_cols.append(col)
        elif col in features_df.columns:
            df[col] = features_df[col]
            actual_cols.append(col)
    return df[actual_cols].dropna().values, actual_cols


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_first_visit_report(sample_info, reg_results, pca_core, pca_ext,
                                 bs_core, bs_ext, sh_core, sh_ext) -> str:
    lines = []
    lines.append("# Task 27.3I — First Visit Report")
    lines.append("")

    # 1. Sample
    lines.append("## 1. Sample")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total sessions (original) | {sample_info['n_total_sessions']} |")
    lines.append(f"| Total subjects | {sample_info['n_total_subjects']} |")
    lines.append(f"| First-visit sessions | {sample_info['n_first_visit']} |")
    lines.append(f"| Reduction | {fmt(sample_info['pct_reduction'], 1)}% |")
    lines.append("")

    # 2. Regression
    lines.append("## 2. Regression")
    lines.append("")
    lines.append("| Model | n | R² | Adj R² | β | p-value | Residual Ratio |")
    lines.append("|---|---|---|---|---|---|---|")
    for model, row in reg_results.iterrows():
        lines.append(
            f"| {model} | {row['n']} | {fmt(row['r_squared'])} | {fmt(row['adj_r_squared'])} "
            f"| {fmt(row['beta'])} | {fmt(row['p_value'])} | {fmt(row['residual_ratio'])} |")
    lines.append("")

    # 3-4. PCA core + extended
    for label, pca in [("3. PCA Core", pca_core), ("4. PCA Extended", pca_ext)]:
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"n = {pca['n']}, p = {pca['p']}")
        lines.append("")
        lines.append("| PC | Eigenvalue | % Variance | Cumulative % |")
        lines.append("|---|---|---|---|")
        ev = pca['eigenvalues']
        total = np.sum(ev)
        for i, e in enumerate(ev):
            ve = e / total * 100
            cv = np.sum(ev[:i+1]) / total * 100
            lines.append(f"| PC{i+1} | {fmt(e)} | {fmt(ve, 2)} | {fmt(cv, 2)} |")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| λ>1 count | {pca['n_lambda_gt1']} |")
        lines.append(f"| Participation Ratio | {fmt(pca['participation_ratio'])} |")
        lines.append(f"| Effective Rank | {fmt(pca['effective_rank'])} |")
        lines.append("")

    # 5. Bootstrap
    for label, bs in [("5. Bootstrap Core", bs_core), ("6. Bootstrap Extended", bs_ext)]:
        lines.append(f"## {label}")
        lines.append("")
        metrics = ['pc1_pct', 'pc2_pct', 'n_lambda_gt1', 'participation_ratio', 'effective_rank']
        labels = ['PC1 %', 'PC2 %', 'λ>1 count', 'PR', 'ER']
        lines.append("| Metric | Mean | SD | 95% CI |")
        lines.append("|---|---|---|---|")
        for m, ml in zip(metrics, labels):
            s = summarize(bs[m])
            lines.append(f"| {ml} | {fmt(s['mean'])} | {fmt(s['sd'])} "
                         f"| [{fmt(s['ci_lo'])}, {fmt(s['ci_hi'])}] |")
        lines.append("")
        freq = bs['n_lambda_gt1'].value_counts().sort_index()
        lines.append(f"λ>1 modal: {freq.idxmax()} ({freq.max()/len(bs)*100:.1f}%)")
        lines.append("")

    # 7. Split-half
    for label, sh in [("7. Split-Half Core", sh_core), ("8. Split-Half Extended", sh_ext)]:
        lines.append(f"## {label}")
        lines.append("")
        metrics = ['diff_pc1_pct', 'diff_pc2_pct', 'cos_theta_pc1', 'cos_theta_pc2']
        labels = ['|ΔPC1| %', '|ΔPC2| %', '|cos(θ)| PC1', '|cos(θ)| PC2']
        lines.append("| Metric | Mean | SD | 95% CI |")
        lines.append("|---|---|---|---|")
        for m, ml in zip(metrics, labels):
            s = summarize(sh[m])
            lines.append(f"| {ml} | {fmt(s['mean'])} | {fmt(s['sd'])} "
                         f"| [{fmt(s['ci_lo'])}, {fmt(s['ci_hi'])}] |")
        lines.append("")

    return "\n".join(lines)


def generate_comparative_report(sample_info, reg_fv, pca_core_fv, pca_ext_fv,
                                 bs_core_fv, bs_ext_fv, sh_core_fv, sh_ext_fv,
                                 reg_orig, pca_core_orig, pca_ext_orig,
                                 bs_core_orig, bs_ext_orig,
                                 sh_core_orig, sh_ext_orig) -> str:
    lines = []
    lines.append("# Task 27.3I — Comparative Analysis")
    lines.append("")
    lines.append("Full population vs First-visit only")
    lines.append("")

    # Sample comparison
    lines.append("## Sample")
    lines.append("")
    lines.append(f"| | Full | First-visit |")
    lines.append(f"|---|---|---|")
    lines.append(f"| Sessions | {sample_info['n_total_sessions']} | {sample_info['n_first_visit']} |")
    lines.append(f"| Subjects | {sample_info['n_total_subjects']} | {sample_info['n_first_visit']} |")
    lines.append("")

    # Regression comparison
    lines.append("## Regression")
    lines.append("")
    lines.append("| Model | R²_full | R²_fv | ΔR² | Residual Ratio_full | Residual Ratio_fv | Direction |")
    lines.append("|---|---|---|---|---|---|---|")
    for model in reg_fv.index:
        if model not in reg_orig.index:
            continue
        r2_f = reg_orig.loc[model, 'r_squared']
        r2_fv = reg_fv.loc[model, 'r_squared']
        dr2 = r2_fv - r2_f
        rr_f = reg_orig.loc[model, 'residual_ratio']
        rr_fv = reg_fv.loc[model, 'residual_ratio']
        direction = "↑" if dr2 > 0 else "↓"
        lines.append(f"| {model} | {fmt(r2_f)} | {fmt(r2_fv)} | {fmt(dr2)} "
                     f"| {fmt(rr_f)} | {fmt(rr_fv)} | {direction} |")
    lines.append("")

    # PCA comparison
    for label, pca_fv, pca_orig in [("PCA Core", pca_core_fv, pca_core_orig),
                                     ("PCA Extended", pca_ext_fv, pca_ext_orig)]:
        lines.append(f"## {label}")
        lines.append("")
        metrics = [
            ('PC1 %', 'pc1_pct'), ('PC2 %', 'pc2_pct'),
            ('Cumulative %', 'cumul_pct'), ('λ>1', 'n_lambda_gt1'),
            ('PR', 'participation_ratio'), ('ER', 'effective_rank'),
        ]
        lines.append("| Metric | Full | First-visit | Δ | Δ% | Direction |")
        lines.append("|---|---|---|---|---|---|")
        for ml, mk in metrics:
            vf = pca_orig[mk]
            vfv = pca_fv[mk]
            d = vfv - vf
            dp = (d / vf * 100) if vf != 0 else 0.0
            direction = "↑" if d > 0 else ("↓" if d < 0 else "=")
            lines.append(f"| {ml} | {fmt(vf)} | {fmt(vfv)} | {fmt(d)} "
                         f"| {fmt(dp, 1)} | {direction} |")
        lines.append("")

    # Bootstrap comparison
    for label, bs_fv, bs_orig in [("Bootstrap Core", bs_core_fv, bs_core_orig),
                                    ("Bootstrap Extended", bs_ext_fv, bs_ext_orig)]:
        lines.append(f"## {label}")
        lines.append("")
        metrics = [('Mean PC1%', 'pc1_pct'), ('SD PC1%', 'pc1_pct')]
        s_fv = summarize(bs_fv['pc1_pct'])
        s_orig = summarize(bs_orig['pc1_pct'])
        freq_fv = bs_fv['n_lambda_gt1'].value_counts()
        freq_orig = bs_orig['n_lambda_gt1'].value_counts()
        modal_fv = freq_fv.idxmax()
        modal_orig = freq_orig.idxmax()
        modal_pct_fv = freq_fv.max() / len(bs_fv) * 100
        modal_pct_orig = freq_orig.max() / len(bs_orig) * 100

        lines.append("| Metric | Full | First-visit | Direction |")
        lines.append("|---|---|---|---|")
        d_mean = "↑" if s_fv['mean'] > s_orig['mean'] else "↓"
        d_sd = "↑" if s_fv['sd'] > s_orig['sd'] else "↓"
        lines.append(f"| Mean PC1% | {fmt(s_orig['mean'])} | {fmt(s_fv['mean'])} | {d_mean} |")
        lines.append(f"| SD PC1% | {fmt(s_orig['sd'])} | {fmt(s_fv['sd'])} | {d_sd} |")
        lines.append(f"| λ>1 modal | {modal_orig} ({fmt(modal_pct_orig,1)}%) "
                     f"| {modal_fv} ({fmt(modal_pct_fv,1)}%) "
                     f"| {'=' if modal_fv == modal_orig else '≠'} |")
        lines.append("")

    # Split-half comparison
    for label, sh_fv, sh_orig in [("Split-Half Core", sh_core_fv, sh_core_orig),
                                    ("Split-Half Extended", sh_ext_fv, sh_ext_orig)]:
        lines.append(f"## {label}")
        lines.append("")
        metrics = [('Mean |ΔPC1|', 'diff_pc1_pct'), ('cos(θ_PC1)', 'cos_theta_pc1'),
                   ('cos(θ_PC2)', 'cos_theta_pc2')]
        lines.append("| Metric | Full | First-visit | Direction |")
        lines.append("|---|---|---|---|")
        for ml, mk in metrics:
            sf = summarize(sh_orig[mk])
            sfv = summarize(sh_fv[mk])
            direction = "↑" if sfv['mean'] > sf['mean'] else "↓"
            lines.append(f"| {ml} | {fmt(sf['mean'])} | {fmt(sfv['mean'])} | {direction} |")
        lines.append("")

    # Summary: changes > 5%
    lines.append("## Changes > 5% (absolute)")
    lines.append("")
    changes = []
    for mk, ml in [('pc1_pct', 'PC1%'), ('pc2_pct', 'PC2%'), ('cumul_pct', 'Cumul%')]:
        d = abs(pca_core_fv[mk] - pca_core_orig[mk])
        if d > 5:
            changes.append(f"Core {ml}: Δ={d:.2f}%")
    for mk, ml in [('pc1_pct', 'PC1%'), ('pc2_pct', 'PC2%'), ('cumul_pct', 'Cumul%')]:
        d = abs(pca_ext_fv[mk] - pca_ext_orig[mk])
        if d > 5:
            changes.append(f"Extended {ml}: Δ={d:.2f}%")
    if changes:
        for c in changes:
            lines.append(f"- {c}")
    else:
        lines.append("None")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3I — First Visit Population Control")
    print("=" * 60)
    print()

    if not DATABASE_PATH.exists():
        print(f"ERROR: {DATABASE_PATH}"); return 1

    # --- FIRST VISIT DATA ---
    features_fv, sample_info = load_first_visit_features(str(DATABASE_PATH))
    print()

    # Regression (fresh β for first-visit)
    print("[6/12] Running regression on first-visit data...")
    reg_fv = run_linear_regressions(features_fv)
    for model, row in reg_fv.iterrows():
        print(f"  → {model}: R²={row['r_squared']:.6f}")
    print()

    # Residuals
    print("[7/12] Computing residuals...")
    residuals_fv = reconstruct_residuals(features_fv, reg_fv)
    print()

    # PCA
    print("[8/12] PCA...")
    core_data_fv, _ = prepare_data_matrix(residuals_fv, features_fv, CORE_RESIDUALS)
    ext_data_fv, _ = prepare_data_matrix(residuals_fv, features_fv, EXTENDED_FEATURES)
    pca_core_fv = pca_metrics(core_data_fv)
    pca_ext_fv = pca_metrics(ext_data_fv)
    print(f"  Core: PC1={pca_core_fv['pc1_pct']:.2f}%, n={pca_core_fv['n']}")
    print(f"  Ext:  PC1={pca_ext_fv['pc1_pct']:.2f}%, n={pca_ext_fv['n']}")
    print()

    rng = np.random.default_rng(RANDOM_SEED)

    # Bootstrap
    print(f"[9/12] Bootstrap ({N_BOOTSTRAP} iterations)...")
    bs_core_fv = bootstrap_pca(core_data_fv, N_BOOTSTRAP, rng)
    print(f"  Core: {len(bs_core_fv)} iterations")
    bs_ext_fv = bootstrap_pca(ext_data_fv, N_BOOTSTRAP, rng)
    print(f"  Ext:  {len(bs_ext_fv)} iterations")
    print()

    # Split-half
    print(f"[10/12] Split-half ({N_SPLITS} iterations)...")
    sh_core_fv = split_half_pca(core_data_fv, N_SPLITS, rng)
    print(f"  Core: {len(sh_core_fv)} iterations")
    sh_ext_fv = split_half_pca(ext_data_fv, N_SPLITS, rng)
    print(f"  Ext:  {len(sh_ext_fv)} iterations")
    print()

    # --- ORIGINAL DATA (reload for comparison) ---
    print("[11/12] Loading original full-population results for comparison...")
    reg_orig = pd.read_csv(LINEAR_CSV, index_col=0)

    # Reload full data for fair comparison (recompute from DB)
    import sqlite3 as _sq
    _conn = _sq.connect(str(DATABASE_PATH))
    _tw = pd.read_sql_query("""
        SELECT t.trial_id, t.subject_id, t.test_date,
        """ + ", ".join(f"t.tst{t}_{s}" for t in [1,2,3] for s in range(1,37)) + """
        FROM trials t INNER JOIN users u ON t.subject_id = u.subject_id
    """, _conn)
    _ms = pd.read_sql_query("SELECT * FROM metadata_simple", _conn)
    _mc = pd.read_sql_query("SELECT * FROM metadata_color_red", _conn)
    _msh = pd.read_sql_query("SELECT * FROM metadata_shift", _conn)
    _conn.close()
    _tld = []
    for _, _sr in _tw.iterrows():
        _sid, _tid = _sr['subject_id'], _sr['trial_id']
        for _stim in range(1, 37):
            rt = _sr[f'tst1_{_stim}']
            if pd.notna(rt) and rt > 0:
                _m = _ms[_ms['stimulus_id'] == _stim].iloc[0]
                _tld.append({'subject_id': _sid, 'session_id': _tid, 'test_type': 'Tst1',
                    'stimulus_id': _stim, 'stimulus_location': _m['position'],
                    'stimulus_color': _m['color'], 'psi': _m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for _stim in range(1, 37):
            rt = _sr[f'tst2_{_stim}']
            if pd.notna(rt) and rt > 0:
                _m = _mc[_mc['stimulus_id'] == _stim].iloc[0]
                _tld.append({'subject_id': _sid, 'session_id': _tid, 'test_type': 'Tst2',
                    'stimulus_id': _stim, 'stimulus_location': _m['position'],
                    'stimulus_color': 'red', 'psi': _m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for _stim in range(1, 37):
            rt = _sr[f'tst3_{_stim}']
            if pd.notna(rt) and rt > 0:
                _m = _msh[_msh['stimulus_id'] == _stim].iloc[0]
                _tld.append({'subject_id': _sid, 'session_id': _tid, 'test_type': 'Tst3',
                    'stimulus_id': _stim, 'stimulus_location': _m['position'],
                    'stimulus_color': _m['color'], 'psi': _m['psi_ms'], 'rt': rt, 'is_outlier': False})
    _tdf = pd.DataFrame(_tld)
    _ext = BaselineFeatureExtractor()
    _fl = []
    for _sid in _tdf['subject_id'].unique():
        try:
            _f = _ext.extract_subject_features(_tdf[_tdf['subject_id'] == _sid].copy())
            if isinstance(_f, dict): _f['subject_id'] = _sid; _fl.append(_f)
        except Exception: continue
    features_full = pd.DataFrame(_fl)
    if 'subject_id' in features_full.columns:
        features_full = features_full.set_index('subject_id')
    print(f"  → Full population: {len(features_full)} subjects")
    residuals_full = pd.DataFrame(index=features_full.index)
    for outcome, predictor in MODEL_MAP.items():
        if outcome not in reg_orig.index:
            continue
        beta = reg_orig.loc[outcome, 'beta']
        intercept = reg_orig.loc[outcome, 'intercept']
        data = features_full[[outcome, predictor]].dropna()
        residuals_full.loc[data.index, f"{outcome}_residual"] = data[outcome] - (beta * data[predictor] + intercept)

    core_data_full, _ = prepare_data_matrix(residuals_full, features_full, CORE_RESIDUALS)
    ext_data_full, _ = prepare_data_matrix(residuals_full, features_full, EXTENDED_FEATURES)
    pca_core_orig = pca_metrics(core_data_full)
    pca_ext_orig = pca_metrics(ext_data_full)

    rng2 = np.random.default_rng(RANDOM_SEED)
    bs_core_orig = bootstrap_pca(core_data_full, N_BOOTSTRAP, rng2)
    bs_ext_orig = bootstrap_pca(ext_data_full, N_BOOTSTRAP, rng2)
    rng3 = np.random.default_rng(RANDOM_SEED)
    sh_core_orig = split_half_pca(core_data_full, N_SPLITS, rng3)
    sh_ext_orig = split_half_pca(ext_data_full, N_SPLITS, rng3)
    print()

    # --- REPORTS ---
    print("[12/12] Generating reports...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    report = generate_first_visit_report(
        sample_info, reg_fv, pca_core_fv, pca_ext_fv,
        bs_core_fv, bs_ext_fv, sh_core_fv, sh_ext_fv)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → {OUTPUT_REPORT}")

    comparative = generate_comparative_report(
        sample_info, reg_fv, pca_core_fv, pca_ext_fv,
        bs_core_fv, bs_ext_fv, sh_core_fv, sh_ext_fv,
        reg_orig, pca_core_orig, pca_ext_orig,
        bs_core_orig, bs_ext_orig, sh_core_orig, sh_ext_orig)
    with open(OUTPUT_COMPARATIVE, "w", encoding="utf-8") as f:
        f.write(comparative)
    print(f"  → {OUTPUT_COMPARATIVE}")
    print()

    print("=" * 60)
    print(f"First-visit: PC1={pca_core_fv['pc1_pct']:.2f}% vs Full: PC1={pca_core_orig['pc1_pct']:.2f}%")
    print(f"ΔPC1 = {pca_core_fv['pc1_pct'] - pca_core_orig['pc1_pct']:.2f}%")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
