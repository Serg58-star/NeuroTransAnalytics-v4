"""
Task 55C — Geometric Preservation Check
Stage 9C: Architectural Verification (Stage 3/3)

Fixed parameter: kappa = 0.08 (selected by Task 55B)
Parameters: N=500, T=10, Bootstrap=500

Validates 8 geometric invariants of the stabilized v5 generator:
  1. Participation Ratio >= 4
  2. Effective Rank >= 4
  3. PC1 Variance in [10%, 25%]
  4. Bootstrap SD PC1 <= 2%
  5. Silhouette Static (t=0) < 0.20
  6. Silhouette Longitudinal (delta-Z field) < 0.20
  7. Condition Number <= baseline * 1.20
  8. No dominant axis: PC1 < 40%

Final status: LOCKED (all pass) or REJECTED (return to Task 55A).
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_longitudinal_population
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration

KAPPA_LOCKED = 0.08
N_SUBJECTS = 500
TIMEPOINTS = 10
BOOTSTRAP = 500

REPORT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../..',
    'docs', 'v5', 'Stage_9C_Task_55C_Geometric_Preservation_Report.md'
))


def _pca_metrics(Z_t0):
    """Compute PR, Effective Rank, PC1 variance from the Phase-1 (t=0) snapshot."""
    pca = PCA()
    pca.fit(Z_t0)
    ev = pca.explained_variance_ratio_

    # Participation Ratio: (sum ev)^2 / sum(ev^2) — a smoothed dimensionality estimate
    pr = (ev.sum() ** 2) / (ev ** 2).sum()

    # Effective Rank: entropy-based
    ev_nonzero = ev[ev > 1e-12]
    eff_rank = float(np.exp(-np.sum(ev_nonzero * np.log(ev_nonzero))))

    pc1_pct = float(ev[0]) * 100.0
    return pr, eff_rank, pc1_pct, pca


def _bootstrap_pc1_sd(Z_t0, n_boot=500, seed=42):
    rng = np.random.default_rng(seed)
    N = Z_t0.shape[0]
    boot_pc1 = []
    for _ in range(n_boot):
        idx = rng.integers(0, N, size=N)
        pca_b = PCA(n_components=1)
        pca_b.fit(Z_t0[idx])
        boot_pc1.append(float(pca_b.explained_variance_ratio_[0]) * 100.0)
    return float(np.std(boot_pc1))


def _silhouette_static(Z_t0):
    best = -1.0
    for k in range(2, 6):
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(Z_t0)
        s = silhouette_score(Z_t0, labels)
        best = max(best, s)
    return best


def _silhouette_longitudinal(Z_long, T):
    delta_Z = np.vstack([Z_long[:, t, :] - Z_long[:, t - 1, :] for t in range(1, T)])
    best = -1.0
    for k in range(2, 6):
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(delta_Z)
        s = silhouette_score(delta_Z, labels)
        best = max(best, s)
    return best


def _cond_number(Z_t0):
    cov = np.cov(Z_t0, rowvar=False)
    return np.linalg.cond(cov)


def evaluate(kappa, inv_sigma, label):
    print(f"\n  [{label}] Generating population (N={N_SUBJECTS}, T={TIMEPOINTS}, kappa={kappa})...")
    Z_long = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=kappa, inv_sigma_mcd=inv_sigma)
    Z_t0 = Z_long[:, 0, :]

    print(f"  [{label}] PCA metrics...")
    pr, eff_rank, pc1_pct, _ = _pca_metrics(Z_t0)

    print(f"  [{label}] Bootstrap PC1 SD (k={BOOTSTRAP})...")
    boot_sd = _bootstrap_pc1_sd(Z_t0, n_boot=BOOTSTRAP)

    print(f"  [{label}] Silhouette static...")
    silh_static = _silhouette_static(Z_t0)

    print(f"  [{label}] Silhouette longitudinal...")
    silh_long = _silhouette_longitudinal(Z_long, TIMEPOINTS)

    print(f"  [{label}] Condition number...")
    cond = _cond_number(Z_t0)

    print(f"  [{label}] PR={pr:.2f} | Eff.Rank={eff_rank:.2f} | PC1={pc1_pct:.1f}% | BootSD={boot_sd:.3f}% | SilhS={silh_static:.3f} | SilhL={silh_long:.3f} | Cond={cond:.1f}")

    return {
        'kappa': kappa,
        'pr': pr,
        'eff_rank': eff_rank,
        'pc1_pct': pc1_pct,
        'boot_sd': boot_sd,
        'silh_static': silh_static,
        'silh_long': silh_long,
        'cond': cond
    }


def check_invariants(m_stable, m_base):
    c1 = m_stable['pr'] >= 4.0
    c2 = m_stable['eff_rank'] >= 4.0
    c3 = 10.0 <= m_stable['pc1_pct'] <= 25.0
    c4 = m_stable['boot_sd'] <= 2.0
    c5 = m_stable['silh_static'] < 0.20
    c6 = m_stable['silh_long'] < 0.20
    c7 = m_stable['cond'] <= m_base['cond'] * 1.20
    c8 = m_stable['pc1_pct'] < 40.0

    return {
        'c1_pr': c1, 'c2_eff_rank': c2, 'c3_pc1_range': c3,
        'c4_boot_sd': c4, 'c5_silh_static': c5, 'c6_silh_long': c6,
        'c7_cond': c7, 'c8_no_dominant': c8,
        'all_passed': all([c1, c2, c3, c4, c5, c6, c7, c8])
    }


def generate_report(m_base, m_stable, checks):
    ok = lambda b: "✓" if b else "✗"
    status = "LOCKED" if checks['all_passed'] else "REJECTED"

    report = f"""# Stage 9C Task 55C — Geometric Preservation Report

**Validation Date:** 2026-03-02
**Locked κ:** {KAPPA_LOCKED} | **N={N_SUBJECTS}, T={TIMEPOINTS}, Bootstrap={BOOTSTRAP}**
**Final Status:** **{status}**

## 1. Geometric Invariant Verification Table

| # | Invariant | Baseline (κ=0) | Stabilized (κ=0.08) | Target | Pass |
|---|---|---|---|---|---|
| 1 | Participation Ratio | {m_base['pr']:.2f} | {m_stable['pr']:.2f} | ≥ 4 | {ok(checks['c1_pr'])} |
| 2 | Effective Rank | {m_base['eff_rank']:.2f} | {m_stable['eff_rank']:.2f} | ≥ 4 | {ok(checks['c2_eff_rank'])} |
| 3 | PC1 Variance | {m_base['pc1_pct']:.1f}% | {m_stable['pc1_pct']:.1f}% | ∈ [10%, 25%] | {ok(checks['c3_pc1_range'])} |
| 4 | Bootstrap SD PC1 | {m_base['boot_sd']:.3f}% | {m_stable['boot_sd']:.3f}% | ≤ 2% | {ok(checks['c4_boot_sd'])} |
| 5 | Silhouette Static | {m_base['silh_static']:.3f} | {m_stable['silh_static']:.3f} | < 0.20 | {ok(checks['c5_silh_static'])} |
| 6 | Silhouette Longitudinal | {m_base['silh_long']:.3f} | {m_stable['silh_long']:.3f} | < 0.20 | {ok(checks['c6_silh_long'])} |
| 7 | Condition Number | {m_base['cond']:.1f} | {m_stable['cond']:.1f} | ≤ {m_base['cond']*1.20:.1f} | {ok(checks['c7_cond'])} |
| 8 | No Dominant Axis | {m_base['pc1_pct']:.1f}% | {m_stable['pc1_pct']:.1f}% | < 40% | {ok(checks['c8_no_dominant'])} |

## 2. Conclusion

{"The Mean-Reverting Elastic Drift (κ=0.08) **preserves all geometric invariants** of the v5 architecture. The stabilized generator is formally **LOCKED**. Stage 9C development may continue with the Risk Layer." if checks['all_passed'] else "One or more geometric invariants have been violated. κ=0.08 is **REJECTED**. Return to Task 55A for revised g(S) form or κ range."}
"""
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport written: {REPORT_PATH}")
    print(f"Final Status: {status}")


if __name__ == "__main__":
    np.random.seed(42)

    print("Calibrating universal Phase 1 covariance (N=1000)...")
    cal = Task51SeverityCalibration(n_subjects=1000)
    cal.block_1_robust_centroid()
    inv_sigma = cal.inv_sigma_mcd

    print("\n--- Baseline (kappa=0) ---")
    m_base = evaluate(kappa=0.0, inv_sigma=inv_sigma, label="Baseline")

    print("\n--- Stabilized (kappa=0.08) ---")
    m_stable = evaluate(kappa=KAPPA_LOCKED, inv_sigma=inv_sigma, label="Stabilized")

    print("\n--- Checking invariants ---")
    checks = check_invariants(m_stable, m_base)

    for k, v in checks.items():
        if k != 'all_passed':
            print(f"  {k}: {'PASS' if v else 'FAIL'}")

    generate_report(m_base, m_stable, checks)
