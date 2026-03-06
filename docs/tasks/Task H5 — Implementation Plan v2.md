# Task H5 — Implementation Plan v2

## Correlated Baseline Generator Redesign

**Version:** v2.0
**Date:** 2026-03-04
**Objective:** Implement a physiologically consistent Phase-1 baseline generator for v5 that produces a **1D-dominant correlated baseline architecture** while preserving compatibility with the existing v5 pipeline.

This version corrects the demographic modeling error present in Implementation Plan v1.

---

# 1. Governance Rule

> **Approval Gate Rule:**
> Implementation is **blocked** until the user explicitly replies:

```
Approved for implementation. Task H5.
```

No code changes may occur prior to this approval.

---

# 2. Architectural Target

The redesigned Phase-1 generator must produce:

| Property                | Requirement                |
| ----------------------- | -------------------------- |
| Baseline dimensionality | Effective Rank ≈ 1.1–1.5   |
| PC1 variance share      | ≥ 90%                      |
| Channel correlation     | Corr(L,C,R) ≥ 0.90         |
| Demographic influence   | affects variance, not mean |
| Phase-2 independence    | preserved                  |

---

# 3. Baseline Generative Model

## 3.1 Global Latent Speed Factor

Each subject receives a latent baseline processing factor:

[
G_i \sim LogNormal(\mu,\sigma_i)
]

Where:

* ( \mu ) controls typical reaction speed (~250 ms range)
* ( \sigma_i ) controls subject variability

Important rule:

> Demography affects **variance parameter σ**, not the mean.

---

# 4. Demographic Variance Model

## 4.1 Sex Variance Scaling

Empirical observation:

* Male baseline variance > Female variance

Implementation:

```
if Sex == Male:
    σ_i = σ_base * σ_male
else:
    σ_i = σ_base * σ_female
```

Target outcome:

```
Male/Female λ1 ratio ≈ 1.8–2.1
```

Sex must be generated probabilistically:

```
Sex_i ~ Bernoulli(p)
```

(Default p = 0.5 unless specified otherwise.)

---

## 4.2 Age Variance Modifier

Age affects **spread of baseline speeds**, not their mean.

Implementation:

```
Age_i ~ Uniform(20,80)
σ_i = σ_i * age_variance_modifier(Age_i)
```

Constraints:

* non-monotonic variance profile allowed
* Q2 cohort must exhibit **variance minimum**

Example conceptual form:

```
σ_age = σ_base * (1 + β * |Age - optimal_age|)
```

Parameters will be tuned during validation.

---

# 5. Spatial Channel Construction

Baseline spatial channels must be derived from the shared latent factor.

[
V1_L = G_i + \epsilon_L
]

[
V1_C = G_i + \epsilon_C
]

[
V1_R = G_i + \epsilon_R
]

Where:

[
\epsilon_k \sim N(0, \sigma_{local})
]

Requirement:

```
Corr(L,C) ≥ 0.90
Corr(L,R) ≥ 0.90
Corr(C,R) ≥ 0.90
```

This guarantees the required **1D-dominant baseline geometry**.

---

# 6. Code Modification Plan

### Modify

```
population_generator_v5.py
```

Replace the existing baseline generation block:

```
base_speed = np.random.normal(250,40)
```

with the correlated latent model:

```
G_i = LogNormal(μ, σ_i)
```

Then generate spatial channels via shared factor projection.

---

# 7. Validation Framework

Create a validation script:

```
scripts/stage_H5_generator_validation.py
```

This script automatically verifies all architectural constraints.

---

# 8. Validation Blocks

## Block 0 — Global Factor Verification

Confirm global baseline factor exists.

Check:

```
Corr(L,G) > 0.95
Corr(C,G) > 0.95
Corr(R,G) > 0.95
```

Output:

```
docs/redesign/H5_Block0_Global_Factor_Verification.md
```

---

## Block 1 — Spectral Geometry

Compute:

* Effective Rank
* PC1 variance
* channel correlations

Output:

```
docs/redesign/H5_Block1_Baseline_Spectral_Geometry.md
```

Pass criteria:

```
Rank ∈ [1.1,1.5]
PC1 ≥ 90%
```

---

## Block 2 — Sex Variance Scaling

Verify:

```
Male/Female λ1 ratio ∈ [1.8,2.1]
```

Output:

```
docs/redesign/H5_Block2_Sex_Baseline_Scaling.md
```

---

## Block 3 — Age Spectral Structure

Verify:

* Q2 variance minimum
* non-monotonic variance

Output:

```
docs/redesign/H5_Block3_Age_Baseline_Structure.md
```

---

## Block 4 — Baseline–Load Independence

Using the Stage_H4 decoupled load generator:

Verify:

```
Cov(Baseline, ΔLoad) ≈ 0
```

Output:

```
docs/redesign/H5_Block4_Baseline_Load_Independence.md
```

---

## Block 5 — v5 System Compatibility

Reassemble:

```
Baseline + Phase2 Load
```

Verify:

* Z-score computation
* κ = 0.08 stability
* no overflow or NaN

Output:

```
docs/redesign/H5_Block5_v5_System_Compatibility.md
```

---

# 9. Automated Execution

Validation command:

```
PYTHONPATH=. python scripts/stage_H5_generator_validation.py
```

The script must produce explicit PASS / FAIL markers.

---

# 10. Completion Criteria

Stage_H5 is complete only if:

* baseline geometry matches empirical structure
* demographic variance patterns reproduced
* Phase-2 independence preserved
* v5 downstream metrics remain stable

---

# 11. Expected Result

The corrected v5 architecture will contain:

1. **Correlated Neural Baseline Layer**
2. **Independent Functional Load Layer**
3. **Stable Z-space Severity System**
4. **κ-anchored diagnostic thresholds**

---

# End of Implementation Plan
