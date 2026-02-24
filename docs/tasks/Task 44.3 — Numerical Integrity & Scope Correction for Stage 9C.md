# Task 44.3 — Numerical Integrity & Scope Correction for Stage 9C
## Population-Level Longitudinal Geometry Audit  
**NeuroTransAnalytics-v4**

**Version:** v1  
**Date:** 2026-02-23  
**Target:** Task44_Population_Longitudinal_Geometry_Audit_Report.md  
**Status:** Mandatory Correction — Stage 9C Not Yet Closed  

---

# 1. Context

Following review of the generated:

`docs/stage9C/Task44_Population_Longitudinal_Geometry_Audit_Report.md`

several numerical and scope-related issues were identified that must be corrected before Stage 9C can be formally closed.

This document defines required corrections.

No new modeling is permitted.

---

# 2. Critical Numerical Integrity Issue

The report currently contains:

- Mean Mahalanobis (M_t): **nan**
- Skew: **nan**
- Mean Radial Excursion (Max M_t): **nan**

This is unacceptable for a geometric audit layer.

Stage 9C must be numerically complete and internally consistent.

---

# 3. Required Numerical Corrections

## 3.1 Identify Source of NaN

Possible causes:

- Missing values in `stage9b_frozen_longitudinal_coordinates.csv`
- Improper grouping or aggregation
- Division by zero
- Empty subject subsets
- Incorrect filtering logic

All NaN sources must be identified and corrected.

---

## 3.2 Recompute the Following Metrics

The following values must be recomputed and verified:

- Mean Mahalanobis (M_t)
- Skewness of M_t
- Mean Radial Excursion (max per subject)
- Any dependent statistics derived from these

No row should propagate NaN silently.

If missing data exists:

- Explicitly report count of excluded rows
- Provide reason for exclusion

Silent NaN propagation is prohibited.

---

# 4. Statistical Validation Requirements

After correction:

1. Confirm:
   - No NaN values remain in any summary metric.
2. Confirm:
   - Population sample size remains consistent.
3. Confirm:
   - Step-level counts match expected dataset size.
4. Provide:
   - Final valid timepoint count used in computations.

---

# 5. Scope Correction — Strategic Language Restriction

The current report contains forward-looking phrasing such as:

> "future risk modelling architectures"

Stage 9C is strictly descriptive.

Remove:

- Any references to future risk modeling
- Any architectural expansion language
- Any inference beyond geometric interpretation

Allowed:

- Pure geometric interpretation
- Statistical description
- Observed structural tendencies

Prohibited:

- Suggesting new risk models
- Suggesting model changes
- Inferring predictive implications

---

# 6. Clarified Interpretation Guidelines

The corrected report may state:

- Heavy-tailed step distribution
- Convergence dominance
- Lateralization axis prevalence
- Non-linear bounded trajectory behavior

It must NOT state:

- Predictive implications
- Pathological implications
- Risk architecture extensions

Stage 9C remains an audit layer only.

---

# 7. Deliverable

Regenerate:

`docs/stage9C/Task44_Population_Longitudinal_Geometry_Audit_Report.md`

With:

- No NaN values
- Corrected statistics
- Clean geometric interpretation
- No forward architectural projection

---

# 8. Governance Status

Stage 9C remains open.

Closure condition:

- Numerical integrity confirmed
- Interpretive scope restricted to geometric description

After successful correction, Stage 9C may be considered complete.

---

End of Task 44.3.