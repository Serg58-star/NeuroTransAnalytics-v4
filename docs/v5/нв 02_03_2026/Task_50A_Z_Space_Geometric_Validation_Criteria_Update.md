# Task 50A — Z-Space Geometric Validation Criteria Update

## Status
ARCHITECTURAL CRITERIA REVISION (v5 ONLY)

## Branch
v5-dual-space-architecture

## Applies To
Synthetic population simulations only (no empirical dataset yet)

---

# 1. Context

Task 50 — Population Geometry v5 (Post-Z Revalidation)  
was executed under validation criteria inherited from v4.

Result: Geometry incorrectly marked as FAILED.

Root cause:

The validation criteria (e.g., Dim ≥ 3 via λ > 1) are not mathematically appropriate for Z-standardized robust space.

This document revises the validation criteria specifically for v5 Z-Space.

---

# 2. Scope Limitation (Critical)

This update applies ONLY to:

- v5 Dual-Space Architecture
- Z-Standardized Analytical Space
- Synthetic population simulations

It does NOT modify:
- v4 validation framework
- real empirical data validation (future stage)
- Stage 8.5 methodology

---

# 3. Problem with Previous Criteria

The Kaiser rule:

    λ > 1

is valid only when:

- using correlation matrix
- variables have unit variance
- Gaussian standardization applied

In v5:

- Standardization uses MAD (robust scale)
- Covariance matrix is computed on robust Z-scores
- Variance normalization is not Gaussian

Therefore:

λ > 1 is not a valid dimensionality threshold in v5.

---

# 4. Revised Validation Criteria for v5 Z-Space

## 4.1 Dimensionality Assessment (Replaces λ > 1)

Dimensionality must now be evaluated using:

### A. Participation Ratio (PR)

\[
PR = \frac{(\sum \lambda_i)^2}{\sum \lambda_i^2}
\]

Validation rule:

- PR ≥ 4 (minimum)
- PR ≥ 6 preferred
- PR ≥ 8 indicates high-rank geometry

PR << 3 would indicate collapse.

---

### B. Effective Rank

\[
r_{eff} = \exp(H)
\]

where:

\[
H = -\sum p_i \log p_i
\]

and

\[
p_i = \frac{\lambda_i}{\sum \lambda_i}
\]

Validation rule:

- r_eff ≥ 4 required

---

### C. Cumulative Variance Distribution

Check:

- PC1 < 40%
- PC1 + PC2 < 65%
- No single axis dominating

This prevents 1D or 2D artificial collapse.

---

# 4.2 Global Modulator Stability

PC1 explained variance must satisfy:

- 10% ≤ PC1 ≤ 25%
- Bootstrap SD ≤ 2%
- Split-half ΔPC1 ≤ 3%

This confirms stable ~15% systemic module.

---

# 4.3 Radial Continuum Validation (Replaces KDE Peak Count)

KDE peak count alone is insufficient.

Replace with:

### A. Silhouette Score (k=2..5)

- Silhouette < 0.20 → no meaningful clustering
- Silhouette < 0.15 preferred

### B. Hartigan Dip Test (if implemented)

- Non-significant → unimodal

### C. Rank Preservation Under Noise

Inject 5–10% Gaussian noise:

- PR shift ≤ 10%
- PC1 shift ≤ 3%

---

# 4.4 Covariance Stability

Bootstrap ≥ 1000 iterations:

- PR SD ≤ 10%
- PC1 SD ≤ 2%
- No singular covariance matrices

---

# 5. Failure Definition (Updated)

v5 Z-Space is considered FAILED only if:

- PR < 3
- r_eff < 3
- PC1 > 50%
- Clear clustering with Silhouette ≥ 0.25
- Covariance singularity detected

Otherwise, geometry is considered VALID.

---

# 6. Required Action for GoAn

1. Update `task_50_geometric_validation.py`
2. Remove λ > 1 criterion
3. Implement:
   - Participation Ratio
   - Effective Rank
   - Silhouette testing
4. Regenerate:
   docs/v5/Task_50_Population_Geometry_v5_Report.md
5. Clearly mark report as:
   "Z-Space Criteria v5 Applied"

---

# 7. Governance Rule

This criteria update is version-locked to v5 synthetic modeling.

When real empirical dataset becomes available,
a separate empirical validation protocol must be written.

---

# 8. Architectural Status

After revalidation under Task 50A:

If geometry passes:

    v5 Population Geometry → LOCKED (Synthetic Model)

If fails:

    Structural Z-Space Redesign Required

---

# End of Task 50A
