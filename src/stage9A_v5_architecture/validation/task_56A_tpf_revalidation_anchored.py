"""
Task 56A — Anchored Transition Probability Field Revalidation
Stage 9C: Methodical Correction

Rebuilds the Transition Probability Field with the stabilized generator
(kappa = 0.08) at N=500, T=10, no bootstrap.
Uses FIXED S75 and DII75 thresholds calculated from the baseline generator (kappa=0).

Criteria:
  1. No absorbing states (P_ii <= 0.95), rows sum to 1
  2. Spectral Stability (|lambda_max| == 1, Gap >= 0.15)
  3. Stationary Q <= 50% for all quadrants
  4. Mean Entropy >= 0.60, Min H_i >= 0.10
  5. Longitudinal Silhouette < 0.20
"""

import numpy as np
from scipy.stats import entropy as sp_entropy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_longitudinal_population
from src.stage9A_v5_architecture.validation.task_53_transition_probability_field import Task53TransitionProbabilityField

KAPPA_LOCKED = 0.08
N_SUBJECTS = 500
TIMEPOINTS = 10

REPORT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../..',
    'docs', 'v5', 'Stage_9C_Task_56A_TPF_Revalidation_Anchored_Report.md'
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


def run_anchored_revalidation():
    print("Calibrating robust covariance (N=1000)...")
    cal = Task51SeverityCalibration(n_subjects=1000)
    cal.block_1_robust_centroid()
    inv_sigma = cal.inv_sigma_mcd

    print("\nPre-computing global quadrant thresholds (kappa=0)...")
    Z_ref = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=0.0, inv_sigma_mcd=inv_sigma)
    sev_ref, dii_ref = _compute_sev_dii(Z_ref, inv_sigma)
    S75 = np.percentile(sev_ref[:, 1:].flatten(), 75)
    D75 = np.percentile(dii_ref[:, 1:].flatten(), 75)
    print(f"  Anchored Thresholds: S_75th={S75:.4f}, DII_75th={D75:.4f}")

    print(f"\nBuilding TPF at N={N_SUBJECTS}, T={TIMEPOINTS} with kappa={KAPPA_LOCKED} (Anchored)...")
    tpf = Task53TransitionProbabilityField(
        n_subjects=N_SUBJECTS,
        timepoints=TIMEPOINTS,
        kappa=KAPPA_LOCKED,
        inv_sigma_mcd=inv_sigma
    )

    tpf.block_1_discrete_transition_matrix(fixed_S75=S75, fixed_DII75=D75)
    t_mat = tpf.T_matrix

    tpf.block_3_transition_entropy()
    ent = {
        'mean_system_entropy': tpf.metrics['Mean_Entropy'],
        'quadrant_entropies': tpf.entropies
    }

    # Spectral & Stationary
    evals, evecs = np.linalg.eig(t_mat.T)
    idx_sorted = np.argsort(np.abs(evals))[::-1]
    evals_sorted = evals[idx_sorted]
    evecs_sorted = evecs[:, idx_sorted]

    lambda_max_mag = np.abs(evals_sorted[0])
    gap = 1.0 - np.abs(evals_sorted[1]) if len(evals_sorted) > 1 else 0.0
    
    stat = evecs_sorted[:, 0].real
    stat = stat / stat.sum()

    spectral = {
        'lambda_max': lambda_max_mag,
        'spectral_gap': gap,
        'eigenvalues': np.abs(evals_sorted)
    }
    station = stat

    # Generate population manually for Silhouette (Task53 doesn't expose it directly)
    Z_long = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=KAPPA_LOCKED, inv_sigma_mcd=inv_sigma)
    delta_Z = np.vstack([Z_long[:, t, :] - Z_long[:, t - 1, :] for t in range(1, TIMEPOINTS)])
    
    silh = -1.0
    for k in range(2, 6):
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(delta_Z)
        s = silhouette_score(delta_Z, labels)
        silh = max(silh, s)

    return t_mat, spectral, station, ent, silh, S75, D75


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


def check_criteria(t_mat, spectral, station, ent, silh):
    # 1. Absorbing states
    max_pii = np.max(np.diag(t_mat))
    c1_absorb = max_pii <= 0.95
    c1_rowsum = np.allclose(np.sum(t_mat, axis=1), 1.0)
    
    # 2. Spectral
    gap = spectral['spectral_gap']
    c2_max = np.isclose(spectral['lambda_max'], 1.0, atol=1e-5)
    c2_gap = gap >= 0.15

    # 3. Stationary
    max_stat = np.max(station)
    c3_stat = max_stat <= 0.50

    # 4. Entropy
    mean_h = ent['mean_system_entropy']
    min_h = np.min(ent['quadrant_entropies'])
    c4_mean = mean_h >= 0.60
    c4_min = min_h >= 0.10

    # 5. Silhouette
    c5_silh = silh < 0.20

    checks = {
        'max_pii': max_pii,
        'c1_absorb': c1_absorb,
        'c1_rowsum': c1_rowsum,
        'gap': gap,
        'c2_max': c2_max,
        'c2_gap': c2_gap,
        'max_stat': max_stat,
        'c3_stat': c3_stat,
        'mean_h': mean_h,
        'min_h': min_h,
        'c4_mean': c4_mean,
        'c4_min': c4_min,
        'silh': silh,
        'c5_silh': c5_silh,
        'all_passed': all([
            c1_absorb, c1_rowsum, c2_max, c2_gap,
            c3_stat, c4_mean, c4_min, c5_silh
        ])
    }
    return checks


def generate_report(t_mat, spectral, station, ent, silh, checks, S75, D75):
    ok = lambda b: "✓" if b else "✗"
    status = "LOCKED" if checks['all_passed'] else "REJECTED"

    report = f"""# Stage 9C Task 56A — Anchored TPF Revalidation Report

**Validation Date:** 2026-03-02
**Locked κ:** {KAPPA_LOCKED} | **N={N_SUBJECTS}, T={TIMEPOINTS}**
**Anchored Thresholds:** S_75th = {S75:.4f}, DII_75th = {D75:.4f} (from baseline κ=0)
**Final Status:** **{status}**

## 1. Validation Criteria Table

| # | Criterion | Target | Measured | Pass |
|---|---|---|---|---|
| 1.1 | Max Absorbing State ($P_{{ii}}$) | $\le 0.95$ | {checks['max_pii']:.3f} | {ok(checks['c1_absorb'])} |
| 1.2 | Transition Matrix Row Sum | $= 1.0$ | Yes | {ok(checks['c1_rowsum'])} |
| 2.1 | Max Eigenvalue ($\|\lambda_{{max}}\|$) | $= 1.0$ | {spectral['lambda_max']:.5f} | {ok(checks['c2_max'])} |
| 2.2 | Spectral Gap | $\ge 0.15$ | {checks['gap']:.4f} | {ok(checks['c2_gap'])} |
| 3 | Max Stationary Mass | $\le 50\%$ | {(checks['max_stat']*100):.1f}% | {ok(checks['c3_stat'])} |
| 4.1 | Mean System Entropy | $\ge 0.60$ | {checks['mean_h']:.3f} | {ok(checks['c4_mean'])} |
| 4.2 | Min Quadrant Entropy | $\ge 0.10$ | {checks['min_h']:.3f} | {ok(checks['c4_min'])} |
| 5 | Longitudinal Silhouette | $< 0.20$ | {checks['silh']:.3f} | {ok(checks['c5_silh'])} |

## 2. Revalidated Transition Probability Field

{format_matrix(t_mat)}

## 3. Spectral & Stationary State

**Eigenvalues:** `{[round(float(e), 4) for e in spectral['eigenvalues']]}`
**Stationary Distribution:**
- Q1 (Stable): {(station[0]*100):.1f}%
- Q2 (Radial): {(station[1]*100):.1f}%
- Q3 (Ortho): {(station[2]*100):.1f}%
- Q4 (Volatile): {(station[3]*100):.1f}%

## 4. Entropy by Quadrant

- Q1: {ent['quadrant_entropies'][0]:.3f}
- Q2: {ent['quadrant_entropies'][1]:.3f}
- Q3: {ent['quadrant_entropies'][2]:.3f}
- Q4: {ent['quadrant_entropies'][3]:.3f}

## 5. Conclusion

{"Anchoring the thresholds successfully mitigated the Q2 distribution ballooning artifact. The Transition Probability Field is completely validated and ergonomically stable. TPF logic is **LOCKED**." if checks['all_passed'] else "Even with anchored thresholds, one or more TPF criteria failed. Further dynamic correction required."}
"""
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport written: {REPORT_PATH}")
    print(f"Final Status: {status}")


if __name__ == "__main__":
    np.random.seed(42)
    t_mat, spectral, station, ent, silh, S75, D75 = run_anchored_revalidation()
    checks = check_criteria(t_mat, spectral, station, ent, silh)
    
    print("\n--- Criteria Check ---")
    for k, v in checks.items():
        if k.startswith('c'):
            print(f"  {k}: {'PASS' if v else 'FAIL'}")

    generate_report(t_mat, spectral, station, ent, silh, checks, S75, D75)
