# Task 51A — Z-Space Severity Centering Correction

## Status
ARCHITECTURAL CORRECTION (Mandatory Before Revalidation)

## Branch
v5-dual-space-architecture

## Parent Task
Task 51 — Severity Calibration v5 (Robust Z-Space)

---

# 1. Context

Task 51 reported a FAILED status due to extreme relative drift
of the MCD centroid under Heavy-Tail Stress testing.

Root Cause:

The drift metric was computed as a **relative percentage shift**
of a centroid vector whose L2-norm is approximately zero
in Z-standardized space.

Because:

\[
\|\mu_{base}\| \approx 0
\]

any finite perturbation produces an arbitrarily large relative percentage.

This is a mathematical artifact, not a geometric instability.

---

# 2. Architectural Clarification

In Z-Space:

- All channel-field coordinates are centered by construction.
- The theoretical population centroid is:

\[
E[Z] = 0
\]

Therefore:

The centroid location is not an informative stability metric.

Severity in Z-Space should be covariance-driven, not mean-driven.

---

# 3. Architectural Correction

## 3.1 Center Fixation Rule

In Z-Space:

\[
\mu_{Severity} := 0
\]

The Severity metric shall not subtract a fitted centroid.

The distance metric becomes:

\[
D_M(Z) = \sqrt{Z^T \Sigma_{robust}^{-1} Z}
\]

No explicit subtraction of \(\mu_{MCD}\).

---

## 3.2 Covariance Estimation

Robust covariance (MCD or equivalent) remains mandatory:

\[
\Sigma_{robust}
\]

The covariance matrix must be:

- Positive Semi-Definite
- Stable under Bootstrap
- Stable under Heavy-Tail injection

---

# 4. Revised Drift Stability Metric

Relative drift percentage is deprecated.

Replace with absolute L2 displacement:

\[
\Delta_{abs} = \|\mu_{stress} - \mu_{base}\|_2
\]

Validation rule:

\[
\Delta_{abs} \le 1.0
\]

(1 Z-unit tolerance)

This measures geometric displacement in standardized units,
not unstable percentage ratios.

---

# 5. Heavy-Tail Stress Validation (Revised)

Under 20% tail injection and 30% burst simulation:

Verify:

1. Covariance matrix condition number remains bounded.
2. Severity percentile boundaries shift ≤ 5%.
3. Bootstrap SD ≤ 5%.
4. Silhouette remains < 0.20.

No centroid-relative percentage metrics allowed.

---

# 6. Revised Severity Definition (v5 Final Form)

\[
Severity(Z) =
\sqrt{
Z^T \Sigma_{robust}^{-1} Z
}
\]

This definition is:

- Mean-invariant
- Scale-invariant
- Robust to heavy tails
- Geometrically stable in Z-Space

---

# 7. Required Implementation Changes

GoAn must:

1. Remove centroid subtraction from Severity calculation.
2. Deprecate relative drift percentage metric.
3. Implement absolute drift check.
4. Re-run Task 51 stress suite under revised criteria.
5. Regenerate:

docs/v5/Task_51_Severity_Calibration_v5_Report.md


marked:

"Task 51A Criteria Applied"

---

# 8. Failure Definition (Updated)

Task 51A fails only if:

- Covariance becomes unstable (singular / exploding condition number)
- Severity zones shift > 5% under stress
- Clustering emerges (Silhouette ≥ 0.25)

Centroid percentage drift is no longer a valid failure condition.

---

# 9. Architectural Impact

This correction:

- Preserves Z-Space invariance
- Eliminates artificial sensitivity
- Finalizes Severity definition for v5 synthetic modeling

---

# 10. Expected Outcome

After Task 51A:

v5 Severity Model → LOCKED (Synthetic)

Then eligible for:

Task 52 — Phase 2 Dynamics Modeling  
Stage 9B — Functional Monitoring Framework v5
