"""
Task 55A — Lightweight Kappa Screening
Stage 9C: Architectural Correction (Stage 1/3)

Objective:
Rapidly screen kappa candidates that eliminate the Q2 attractor,
using only 2 lightweight criteria:
  1. Return_Prob_Q2 >= 10%
  2. Saturation_Slope in [-0.05, 0.02]

Constraints (strictly per spec):
  - N = 200 subjects
  - T = 5 timepoints
  - No bootstrap
  - No eigendecomposition / spectral analysis
  - No Silhouette computation
  - No re-instantiation of heavy classes inside the inner loop
"""

import numpy as np
from scipy.stats import linregress
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.stage9A_v5_architecture.validation.population_generator_v5 import generate_longitudinal_population
from src.stage9A_v5_architecture.validation.task_51_severity_calibration import Task51SeverityCalibration

REPORT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../..',
    'docs', 'v5', 'Stage_9C_Task_55A_Lightweight_Screening_Report.md'
))

N_SUBJECTS = 200
TIMEPOINTS = 10  # v1.1: extended to 10 timepoints
S_75th_global = None
DII_75th_global = None


def _compute_severity_and_dii(Z_long, inv_sigma):
    N, T, D = Z_long.shape
    severity = np.zeros((N, T))
    dii = np.zeros((N, T))

    for i in range(N):
        for t in range(T):
            z = Z_long[i, t, :]
            dist_sq = np.dot(np.dot(z, inv_sigma), z)
            severity[i, t] = np.sqrt(max(0.0, dist_sq))

            if t > 0:
                z_prev = Z_long[i, t - 1, :]
                dz = z - z_prev
                norm_prev = np.linalg.norm(z_prev)
                dii[i, t] = np.linalg.norm(dz) / (norm_prev if norm_prev > 1e-6 else 1.0)

    return severity, dii


def _classify_quadrants(severity, dii, S_75, DII_75):
    N, T = severity.shape
    Q = np.zeros((N, T), dtype=int)
    for i in range(N):
        for t in range(1, T):
            s = severity[i, t]
            d = dii[i, t]
            if s <= S_75 and d <= DII_75:
                Q[i, t] = 0   # Stable Core
            elif s > S_75 and d <= DII_75:
                Q[i, t] = 1   # Radial Escalation (Q2)
            elif s <= S_75 and d > DII_75:
                Q[i, t] = 2   # Orthogonal Instability
            else:
                Q[i, t] = 3   # Volatile Regime
    return Q


def _return_prob_q2(Q, T):
    entries = 0
    exits = 0
    N = Q.shape[0]
    for i in range(N):
        in_q2 = False
        for t in range(1, T):
            if Q[i, t] == 1:
                if not in_q2:
                    in_q2 = True
                    entries += 1
            else:
                if in_q2:
                    exits += 1
                    in_q2 = False
    return (exits / entries) if entries > 0 else 0.0


def _saturation_slope(severity, T):
    S_flat = []
    dS_flat = []
    N = severity.shape[0]
    for i in range(N):
        for t in range(1, T - 1):
            S_flat.append(severity[i, t])
            dS_flat.append(severity[i, t + 1] - severity[i, t])
    if len(S_flat) < 2:
        return 0.0
    slope, *_ = linregress(S_flat, dS_flat)
    return slope


def screen_kappa(kappas, inv_sigma):
    global S_75th_global, DII_75th_global

    # Pre-compute global thresholds using kappa=0 baseline
    print("  Pre-computing global thresholds (kappa=0)...")
    Z0 = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=0.0, inv_sigma_mcd=inv_sigma)
    sev0, dii0 = _compute_severity_and_dii(Z0, inv_sigma)
    S_75th_global = np.percentile(sev0[:, 1:].flatten(), 75)
    DII_75th_global = np.percentile(dii0[:, 1:].flatten(), 75)
    print(f"  Thresholds: S_75th={S_75th_global:.4f}, DII_75th={DII_75th_global:.4f}")

    candidates = []
    results = []

    for kappa in kappas:
        Z = generate_longitudinal_population(N_SUBJECTS, TIMEPOINTS, kappa=kappa, inv_sigma_mcd=inv_sigma)
        sev, dii = _compute_severity_and_dii(Z, inv_sigma)
        Q = _classify_quadrants(sev, dii, S_75th_global, DII_75th_global)

        rp = _return_prob_q2(Q, TIMEPOINTS)
        slope = _saturation_slope(sev, TIMEPOINTS)

        passed = (rp >= 0.10) and (-0.05 <= slope <= 0.02)

        results.append({
            'kappa': kappa,
            'Return_Prob_Q2': rp,
            'Saturation_Slope': slope,
            'Passed': passed
        })

        marker = "  *** CANDIDATE ***" if passed else ""
        print(f"  kappa={kappa:.2f} | RetProb={rp*100:.1f}% | Slope={slope:.4f} | Pass={passed}{marker}")

        if passed:
            candidates.append(kappa)
            if len(candidates) >= 3:
                print("  >>> Found 3 candidates. Stopping early. <<<")
                break

    return results, candidates


def generate_report(results, candidates):
    rows = []
    for r in results:
        marker = "✓ CANDIDATE" if r['Passed'] else ""
        rows.append(
            f"| {r['kappa']:.2f} | {r['Return_Prob_Q2']*100:.1f}% | {r['Saturation_Slope']:.4f} | {marker} |"
        )

    table = "\n".join(rows)

    candidate_str = ", ".join([f"{k:.2f}" for k in candidates]) if candidates else "None found in range"

    report = f"""# Stage 9C Task 55A — Lightweight Kappa Screening Report

**Validation Date:** 2026-03-02
**Screening Criteria:** Return_Prob_Q2 >= 10% AND Saturation_Slope ∈ [-0.05, 0.02]
**Candidates Found:** {len(candidates)} → [{candidate_str}]

## Screening Table

| κ | Return_Prob_Q2 | Saturation_Slope | Status |
|---|---|---|---|
{table}

## Selected Candidates
{candidate_str}

## Next Step
Proceed to Task 55B (Full Validation) using the identified candidate κ values above.
Run spectral analysis, Silhouette constraint, and Transition Matrix verification
only for the confirmed candidates.
"""
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport written to: {REPORT_PATH}")


if __name__ == "__main__":
    np.random.seed(42)

    print("Calibrating universal Phase 1 covariance (N=1000)...")
    cal = Task51SeverityCalibration(n_subjects=1000)
    cal.block_1_robust_centroid()
    inv_sigma = cal.inv_sigma_mcd

    kappas_primary = np.round(np.arange(0.01, 0.11, 0.01), 4)

    print(f"\nScreening kappa in {kappas_primary.tolist()} ...")
    results, candidates = screen_kappa(kappas_primary, inv_sigma)

    if not candidates:
        print("\nNo candidates in [0.01, 0.10]. Extending to 0.15...")
        kappas_extended = np.round(np.arange(0.11, 0.16, 0.01), 4)
        r2, c2 = screen_kappa(kappas_extended, inv_sigma)
        results += r2
        candidates += c2

    generate_report(results, candidates)
    print(f"\nFinal candidates: {candidates}")
