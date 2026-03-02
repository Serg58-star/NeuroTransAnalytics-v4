"""
Task 55B — Full Dynamic Validation of Candidate Kappa Values
Stage 9C: Architectural Correction (Stage 2/3)

Candidates from Task 55A v1.1 (T=10): kappa in {0.08, 0.09, 0.10}
Parameters: N=400, T=10, no bootstrap.

Six validation criteria:
  1. No absorbing states (P_ii <= 0.95)
  2. Spectral Gap >= 0.10
  3. Stationary Q2 <= 50%
  4. Mean System Entropy >= 0.50
  5. Saturation Slope in [-0.05, 0.02]
  6. Longitudinal Silhouette < 0.20

Selection rule: minimum kappa passing all 6.
"""

import numpy as np
from scipy.stats import linregress, entropy as sp_entropy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_longitudinal_population
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration

CANDIDATES = [0.08, 0.09, 0.10]
N_SUBJECTS = 400
TIMEPOINTS = 10

REPORT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../..',
    'docs', 'v5', 'Stage_9C_Task_55B_Full_Dynamic_Validation_Report.md'
))


def _compute_sev_dii(Z_long, inv_sigma):
    N, T, _ = Z_long.shape
    severity = np.zeros((N, T))
    dii = np.zeros((N, T))
    for i in range(N):
        for t in range(T):
            z = Z_long[i, t, :]
            severity[i, t] = np.sqrt(max(0.0, np.dot(np.dot(z, inv_sigma), z)))
            if t > 0:
                z_prev = Z_long[i, t - 1, :]
                dz = z - z_prev
                nm = np.linalg.norm(z_prev)
                dii[i, t] = np.linalg.norm(dz) / (nm if nm > 1e-6 else 1.0)
    return severity, dii


def _classify(severity, dii, S75, D75):
    N, T = severity.shape
    Q = np.zeros((N, T), dtype=int)
    for i in range(N):
        for t in range(1, T):
            s, d = severity[i, t], dii[i, t]
            if s <= S75 and d <= D75:
                Q[i, t] = 0
            elif s > S75 and d <= D75:
                Q[i, t] = 1
            elif s <= S75 and d > D75:
                Q[i, t] = 2
            else:
                Q[i, t] = 3
    return Q


def _transition_matrix(Q, T):
    trans = np.zeros((4, 4))
    for i in range(Q.shape[0]):
        for t in range(1, T - 1):
            trans[Q[i, t], Q[i, t + 1]] += 1
    rs = trans.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1.0
    return trans / rs


def _spectral(T_mat):
    evals = np.linalg.eigvals(T_mat.T)
    evals_sorted = sorted(np.abs(evals), reverse=True)
    gap = 1.0 - evals_sorted[1] if len(evals_sorted) > 1 else 0.0
    # stationary distribution via left eigenvector
    evals_r, evecs_r = np.linalg.eig(T_mat.T)
    idx = np.argmax(np.abs(evals_r))
    stat = evecs_r[:, idx].real
    stat = stat / stat.sum()
    return evals_sorted, gap, stat


def _mean_entropy(T_mat):
    ents = [sp_entropy(row) for row in T_mat]
    return float(np.mean(ents))


def _saturation_slope(severity, T):
    S_flat, dS_flat = [], []
    for i in range(severity.shape[0]):
        for t in range(1, T - 1):
            S_flat.append(severity[i, t])
            dS_flat.append(severity[i, t + 1] - severity[i, t])
    slope, *_ = linregress(S_flat, dS_flat)
    return float(slope)


def _silhouette(Z_long, T):
    delta_Z = np.vstack([Z_long[:, t, :] - Z_long[:, t - 1, :] for t in range(1, T)])
    best_silh = -1.0
    for k in range(2, 6):
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(delta_Z)
        s = silhouette_score(delta_Z, labels)
        if s > best_silh:
            best_silh = s
    return best_silh


def validate_kappa(kappa, inv_sigma, S75, D75):
    print(f"  Evaluating kappa={kappa:.2f}...")
    Z = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=kappa, inv_sigma_mcd=inv_sigma)
    sev, dii = _compute_sev_dii(Z, inv_sigma)
    Q = _classify(sev, dii, S75, D75)
    T_mat = _transition_matrix(Q, TIMEPOINTS)
    evals, gap, stat = _spectral(T_mat)
    mean_ent = _mean_entropy(T_mat)
    slope = _saturation_slope(sev, TIMEPOINTS)
    silh = _silhouette(Z, TIMEPOINTS)

    c1 = float(np.max(np.diag(T_mat))) <= 0.95
    c2 = gap >= 0.10
    c3 = stat[1] <= 0.50
    c4 = mean_ent >= 0.50
    c5 = -0.05 <= slope <= 0.02
    c6 = silh < 0.20

    passed = c1 and c2 and c3 and c4 and c5 and c6

    print(f"    Absorbing={not c1} | Gap={gap:.4f} | StatQ2={stat[1]*100:.1f}% | Entropy={mean_ent:.3f} | Slope={slope:.4f} | Silh={silh:.3f} | PASS={passed}")

    return {
        'kappa': kappa,
        'T_mat': T_mat,
        'evals': evals,
        'spectral_gap': gap,
        'stationary': stat,
        'mean_entropy': mean_ent,
        'slope': slope,
        'silhouette': silh,
        'c1_no_absorbing': c1,
        'c2_spectral_gap': c2,
        'c3_stationary_q2': c3,
        'c4_entropy': c4,
        'c5_slope': c5,
        'c6_silhouette': c6,
        'passed': passed
    }


def format_matrix(T_mat):
    lines = []
    qlabels = ["Q1(Stable)", "Q2(Radial)", "Q3(Ortho)", "Q4(Volatile)"]
    header = "| Origin | " + " | ".join(qlabels) + " |"
    sep    = "|---|" + "---|" * 4
    lines.append(header)
    lines.append(sep)
    for i, row in enumerate(T_mat):
        cells = " | ".join(f"{v:.3f}" for v in row)
        lines.append(f"| **{qlabels[i]}** | {cells} |")
    return "\n".join(lines)


def generate_report(results, selected_kappa):
    summary_rows = []
    for r in results:
        ok = lambda b: "✓" if b else "✗"
        summary_rows.append(
            f"| {r['kappa']:.2f} | {ok(r['c1_no_absorbing'])} | "
            f"{r['spectral_gap']:.3f} {ok(r['c2_spectral_gap'])} | "
            f"{r['stationary'][1]*100:.1f}% {ok(r['c3_stationary_q2'])} | "
            f"{r['mean_entropy']:.3f} {ok(r['c4_entropy'])} | "
            f"{r['slope']:.4f} {ok(r['c5_slope'])} | "
            f"{r['silhouette']:.3f} {ok(r['c6_silhouette'])} | "
            f"{'**PASS**' if r['passed'] else 'FAIL'} |"
        )

    matrix_sections = []
    for r in results:
        matrix_sections.append(f"### κ = {r['kappa']:.2f}\n\n{format_matrix(r['T_mat'])}")

    report = f"""# Stage 9C Task 55B — Full Dynamic Validation Report

**Validation Date:** 2026-03-02
**N=400, T=10 | No bootstrap**
**Selected κ:** {f'{selected_kappa:.2f}' if selected_kappa is not None else 'None — requires g(S) revision'}

## 1. Summary Table

| κ | No Absorb | Spec. Gap | Stat. Q2 | Entropy | Slope | Silhouette | Result |
|---|---|---|---|---|---|---|---|
{chr(10).join(summary_rows)}

## 2. Transition Matrices

{chr(10).join(matrix_sections)}

## 3. Eigenvalue Spectra

{chr(10).join(f'- **κ={r["kappa"]:.2f}:** {[round(float(e),4) for e in r["evals"][:4]]}' for r in results)}

## 4. 選択 Final Selected Kappa

{'**κ = ' + str(selected_kappa) + '** — minimum sufficient stabilization parameter identified.' if selected_kappa else 'No candidate passed. Proceed to g(S) function revision.'}
"""
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport written: {REPORT_PATH}")


if __name__ == "__main__":
    np.random.seed(42)

    print("Calibrating universal Phase 1 covariance (N=1000)...")
    cal = Task51SeverityCalibration(n_subjects=1000)
    cal.block_1_robust_centroid()
    inv_sigma = cal.inv_sigma_mcd

    # Pre-compute global thresholds at kappa=0
    print("Pre-computing global quadrant thresholds (kappa=0)...")
    Z_ref = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=0.0, inv_sigma_mcd=inv_sigma)
    sev_ref, dii_ref = _compute_sev_dii(Z_ref, inv_sigma)
    S75 = np.percentile(sev_ref[:, 1:].flatten(), 75)
    D75 = np.percentile(dii_ref[:, 1:].flatten(), 75)
    print(f"  S_75th={S75:.4f}, DII_75th={D75:.4f}")

    results = []
    selected_kappa = None

    for kappa in CANDIDATES:
        r = validate_kappa(kappa, inv_sigma, S75, D75)
        results.append(r)
        if r['passed'] and selected_kappa is None:
            selected_kappa = kappa
            print(f"  >>> Selected kappa = {kappa:.2f} <<<")

    generate_report(results, selected_kappa)
    print(f"\nFinal selected kappa: {selected_kappa}")
